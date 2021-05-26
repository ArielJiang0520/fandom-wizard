import pickle
from sys import getsizeof

df = pickle.load(open('data/meta.df', 'rb'))

matadata = list(zip(df['id'].tolist(), df['title'].tolist()))

tag_sets = df['tags'].tolist()

fandoms = df['fandoms'].tolist()
ratings = df['rating'].tolist()

pairings = df['pairing'].tolist()
cps = df['relationships'].tolist()
characters = df['characters'].tolist()

summary = df['summary'].tolist()

def print_fanfic(doc_id, print_summary=False):
    print(
f'''
[{doc_id}]{matadata[doc_id]} {ratings[doc_id]}
{fandoms[doc_id]} {pairing[doc_id]} {cp[doc_id]}
https://archiveofourown.org/works/{matadata[doc_id][0]}
{tag_sets[doc_id]}
'''
)
    if print_summary:
        print(summary[doc_id])