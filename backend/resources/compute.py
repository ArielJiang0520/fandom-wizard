import os
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import time
import torch

import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/paraphrase-MiniLM-L6-v2")
bert_model = AutoModel.from_pretrained("sentence-transformers/paraphrase-MiniLM-L6-v2")
bert_dim = bert_model.config.hidden_size

### public methods

def index_KNN(matrix, index, k):
    return np.argsort(-cosine_similarity(matrix, matrix[index].reshape(1, -1)).flatten())[:k].tolist()

def input_KNN(matrix, input, k):
    embedded_input = embed_doc_bert(input, bert_model, tokenizer)
    return np.argsort(-cosine_similarity(matrix, embedded_input.reshape(1, -1)).flatten())[:k].tolist()
    
### private methods

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    return sum_embeddings / sum_mask

def bert(sents, model, tokenizer, max_len=128):
    encoded_input = tokenizer(
        sents, padding=True, truncation=True, 
        max_length=max_len, return_tensors='pt'
    )

    model.eval()
    with torch.no_grad():
        model_output = model.forward(**encoded_input)
    return mean_pooling(model_output, encoded_input['attention_mask'])

def embed_doc_bert(doc, model, tokenizer):
    vec = bert(sent_tokenize(doc), model, tokenizer).detach().numpy()
    return np.mean(vec, axis=0)


if __name__ == '__main__':
    sample_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sample.txt')
    text = open(sample_path, 'r+', encoding='utf-8').read()

    start = time.time()
    q = embed_doc_bert(text, bert_model, tokenizer) # 2.8s
    print(time.time() - start)
