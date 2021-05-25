import os
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import time
import torch
import pickle

import nltk
nltk.download('punkt', quiet=True)
from nltk.tokenize import sent_tokenize

from transformers import AutoTokenizer, AutoModel

BERT_TOKENIZER = AutoTokenizer.from_pretrained("sentence-transformers/paraphrase-MiniLM-L6-v2")
BERT_MODEL = AutoModel.from_pretrained("sentence-transformers/paraphrase-MiniLM-L6-v2")

tiny_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tiny')
CLFS = [
    pickle.load(open(os.path.join(tiny_path, 'sexual.clf'), 'rb')),
    pickle.load(open(os.path.join(tiny_path, 'romance.clf'), 'rb')),
    pickle.load(open(os.path.join(tiny_path, 'tone.clf'), 'rb'))
]

### public methods

def index_KNN(matrices, poi, k):
    alpha, beta, gamma, delta = 1, 0.25, 0.5, 0.5

    E, T, C, S = matrices

    es = cosine_similarity(E, E[poi].reshape(1, -1)).flatten()
    cs = cosine_similarity(C, C[poi].reshape(1, -1)).flatten()
    ts = cosine_similarity(T, T[poi].reshape(1, -1)).flatten()
    ss = cosine_similarity(S, S[poi].reshape(1, -1)).flatten()

    final = alpha * es + beta * cs + gamma * ts + delta * ss

    return np.argsort(-final)[1:k+1].tolist()

def input_KNN(matrices, input, k):
    E, S = matrices
    embedded_input = _embed_doc_bert(input, BERT_MODEL, BERT_TOKENIZER)
    clf_logits = _models_logit(embedded_input, CLFS)

    es = cosine_similarity(E, embedded_input.reshape(1, -1)).flatten()
    ss = cosine_similarity(S, clf_logits.reshape(1, -1)).flatten()

    final = es + ss * 0.25

    return np.argsort(-final).flatten()[:k].tolist()
    
### private methods

def _mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    return sum_embeddings / sum_mask

def _bert(sents, model, tokenizer, max_len=128):
    encoded_input = tokenizer(
        sents, padding=True, truncation=True, 
        max_length=max_len, return_tensors='pt'
    )

    model.eval()
    with torch.no_grad():
        model_output = model.forward(**encoded_input)
    return _mean_pooling(model_output, encoded_input['attention_mask'])

def _embed_doc_bert(doc, model, tokenizer):
    vec = _bert(sent_tokenize(doc), model, tokenizer).detach().numpy()
    return np.mean(vec, axis=0)

def _models_logit(input_, models):
    input_ = input_.reshape(1, -1)
    vec = []
    for model in models:
        vec.append(model.predict_proba(input_))
    
    return np.concatenate(vec, axis=1).reshape(-1,)[[1,3,5]]

if __name__ == '__main__':
    sample_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sample.txt')
    text = open(sample_path, 'r+', encoding='utf-8').read()

    start = time.time()
    q = _embed_doc_bert(text, BERT_MODEL, BERT_TOKENIZER) # 2.8s
    print(time.time() - start)
