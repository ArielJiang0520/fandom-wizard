import os
import numpy as np
import time
import torch
import pickle

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer

import nltk
nltk.download('punkt', quiet=True)
from nltk.tokenize import sent_tokenize

from transformers import AutoTokenizer, AutoModel

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


## global

from database.db import db
from database.matrix import read_embed_matrix, read_word2vec_table
from database.models import MatrixTable, Word2vecTable

E, T, C, S = read_embed_matrix(db, MatrixTable, hard_refresh=False) # Turn this to true if you just pulled it
W2V = read_word2vec_table(db, Word2vecTable)

DB_SIZE = E.shape[0]

logging.info(f'All matrices and tables loaded. Database size is {DB_SIZE} at the time of first loading')

BERT_TOKENIZER = AutoTokenizer.from_pretrained("sentence-transformers/paraphrase-MiniLM-L6-v2")
BERT_MODEL = AutoModel.from_pretrained("sentence-transformers/paraphrase-MiniLM-L6-v2")

tiny_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tiny')
CLFS = [
    pickle.load(open(os.path.join(tiny_path, 'sexual.clf'), 'rb')),
    pickle.load(open(os.path.join(tiny_path, 'romance.clf'), 'rb')),
    pickle.load(open(os.path.join(tiny_path, 'tone.clf'), 'rb'))
]

logging.info(f'All ML model loaded')

Fandom_df, Char_df = pickle.load(open(os.path.join(tiny_path, 'fandom_df.p'), 'rb')),\
                pickle.load(open(os.path.join(tiny_path, 'character_df.p'), 'rb'))

def _make_F(fandom_df):
    genres = list(zip(fandom_df['genres'].tolist(), fandom_df['media_type'].tolist()))
    genres = [g1 + [g2] if g1 != '' else [] for g1, g2 in genres]

    count = np.log2(np.array(fandom_df['count'].values)).reshape(-1, 1)
    votes = np.log2(np.array([int(v) if v else 1e-6 for v in fandom_df['votes'].values])).reshape(-1, 1)

    year = np.array([int(y) if y != '' else 2000 for y in fandom_df['start_year'].values]).reshape(-1, 1)

    mlb = MultiLabelBinarizer()
    G = mlb.fit_transform(genres)

    return np.concatenate([G, count * 0.4, year * 0.3, votes * 0.3], axis=1)

F = _make_F(Fandom_df)

logging.info(f'Char & Fandom df loaded. F matrix made.')


### public methods

def index_KNN(poi):
    alpha, beta, gamma, delta = 1, 0.25, 0.25, 0.5

    es = cosine_similarity(E, E[poi].reshape(1, -1)).flatten()
    cs = cosine_similarity(C, C[poi].reshape(1, -1)).flatten()
    ts = cosine_similarity(T, T[poi].reshape(1, -1)).flatten()
    ss = cosine_similarity(S, S[poi].reshape(1, -1)).flatten()

    final = alpha * es + beta * cs + gamma * ts + delta * ss

    return np.argsort(-final)[1:51].tolist()

def input_KNN(input):
    alpha, beta = 1, 0.33

    embedded_input = _embed_doc_bert(input, BERT_MODEL, BERT_TOKENIZER)
    clf_logits = _models_logit(embedded_input, CLFS)

    es = cosine_similarity(E, embedded_input.reshape(1, -1)).flatten()
    ss = cosine_similarity(S, clf_logits.reshape(1, -1)).flatten()

    final = alpha * es + beta * ss

    return np.argsort(-final)[:50].tolist()

def fandom_KNN(fandom):
    return Fandom_df.loc[Fandom_df['ao3_parsed_name'] == fandom]['ao3_name'].values.tolist()

def query_KNN(queries):
    alpha, beta = 1, 1

    chars, rls, tags = queries
    
    if chars != '' or rls != '':
        chars = chars.split(',') if chars != '' else []
        # logging.info(f'Parsed chars: {chars}')
        rls = [tuple(cp.split('/')) for cp in rls.split(',')] if chars != '' else []
        # logging.info(f'Parsed rls: {rls}')
        char_and_cp_embed = _embed_char_and_cp(chars, rls, W2V)
        cs = cosine_similarity(C, char_and_cp_embed.reshape(1,-1)).flatten()
    else:
        cs = 0.0
    
    if tags != '':
        tags_embed = _embed_doc_bert(tags, BERT_MODEL, BERT_TOKENIZER)
        ts = cosine_similarity(T, tags_embed.reshape(1,-1)).flatten()
    else:
        ts = 0.0

    final = alpha * cs + beta * ts

    return np.argsort(-final)[:50].tolist()
    

### private methods

def _embed_doc_bert(doc, model, tokenizer):
    vec = _bert(sent_tokenize(doc), model, tokenizer).detach().numpy()
    return np.mean(vec, axis=0)

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

def _models_logit(input_, models):
    input_ = input_.reshape(1, -1)
    vec = []
    for model in models:
        vec.append(model.predict_proba(input_))
    
    return np.concatenate(vec, axis=1).reshape(-1,)[[1,3,5]]

def _find_word(word, table):
    if word in table:
        return table[word]
    else:
        for i in range(len(word)-1, 0, -1):
            if word[:i] in table:
                return table[word[:i]]
        return table['unknown']

def _embed_char(char, table):
    char = char.split(' ')
    output = []
    for c in char:
        output.append(_find_word(c, table))
    return np.mean(output, axis=0)

def _embed_char_and_cp(char_list, cp_list, table):
    char_vec = []
    weight = 1
    for char in char_list:
        char_vec.append(_embed_char(char, table) * weight)
        weight *= 0.8
    
    char_vec = np.sum(char_vec, axis=0) if char_list else np.zeros(300)

    cp_vec = []
    weight = 1
    for a, b in cp_list:
        cp_vec.append(_embed_char(a, table) * _embed_char(b, table) * weight)
        weight *= 0.8
    cp_vec = np.sum(cp_vec, axis=0) if cp_list else np.zeros(300)

    return char_vec * 0.33 + cp_vec

if __name__ == '__main__':
    sample_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sample.txt')
    text = open(sample_path, 'r+', encoding='utf-8').read()

    start = time.time()
    q = _embed_doc_bert(text, BERT_MODEL, BERT_TOKENIZER) # 2.8s
    print(time.time() - start)
