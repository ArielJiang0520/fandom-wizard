import pickle
from sys import getsizeof

data_path = 'data/ao3_ver1_full.p'
df = pickle.load(open(data_path, 'rb'))

mask = df['text'].str.len() > 1000
df = df.loc[mask]

matadata = list(zip(df['id'].tolist(), df['title'].tolist()))

tag_sets = df['tags'].tolist()

fandoms = df['fandoms'].tolist()
ratings = list(zip(df['rating'].tolist(), df['warning'].tolist()))
ratings = df['rating'].tolist()

pairing = df['pairing'].tolist()

corpus = df['text'].tolist()

print(f'Data from "{data_path}" loaded. Document Size: {len(df)}. System Memory: {getsizeof(df) * 1e-6 :.2f}mb')

def print_fanfic(doc_id, print_corpus=False, corpus_len=2000):
    print(
f'''
[{doc_id}]{matadata[doc_id]} {ratings[doc_id]}
{fandoms[doc_id]}
https://archiveofourown.org/works/{matadata[doc_id][0]}
{tag_sets[doc_id]}
'''
)
    if print_corpus:
        print(corpus[doc_id][:corpus_len])