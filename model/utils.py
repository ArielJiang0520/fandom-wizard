import nltk
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from bs4 import BeautifulSoup
import requests

LEM = WordNetLemmatizer()
STOPWORDS = set(stopwords.words('english'))

PATTERN = r'''(?x)          # set flag to allow verbose regexps
        (?:[a-z]\.)+        # abbreviations, e.g. U.S.A.
      | \w+(?:-\w+)*        # words with optional internal hyphens
    '''

def scrape_link(url) -> str:
    headers = {'user-agent': 'bot (sj784@cornell.edu)'}
    
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text)
    
    output = ''
    if soup.find_all('div', class_="userstuff module", role='article'):
        for chapter in soup.find_all('div', class_="userstuff module", role='article'):
            output += chapter.get_text()+'\n'
    
    elif soup.find('div', class_='userstuff'):
        output += soup.find('div', class_='userstuff').get_text()
    
    else:
        print(f'can not find text for {url}')
        raise
        
    return output

def tokenize_corpus(corpus):
    output = []
    for doc in corpus:
        sentences = sent_tokenize(doc) 
        for sent in sentences:
            output.append(nltk.regexp_tokenize(sent.lower(), PATTERN))
    return output

# def convert_phrases(tokenized_sent, phrase_model=PHRASE_MODEL):
#     output = []
#     for sent in tokenized_sent:
#         if sent == []:
#             output.append([])
#         else:
#             tokens, _ = zip(*phrase_model.analyze_sentence(sent))
#             output.append(list(tokens))
#     return output

# def convert_unk(tokenized_sent, vocab=MODEL_VOCAB):
#     output = []
#     for sent in tokenized_sent:
#         tokens = [tok if tok in vocab else '<UNK>' for tok in sent]
#         output.append(tokens)
#     return output

# def tokenize_input(text):
#     tokenized_sent = convert_phrases(tokenize_corpus([text]))
#     tokenized_sent = convert_unk(tokenized_sent)
#     return list(chain.from_iterable(tokenized_sent))

# def embed_input(tokenized_query):
#     vec = np.zeros(shape=(len(tokenized_query), EMBED_SIZE))
#     for j, term in enumerate(tokenized_query):
#         vec[j] = EMBED_TABLE[term]
        
#     return np.mean(vec, axis=0).reshape(1, -1)

# def advance_tokenize(text):
#     tokenized_sent = sent_tokenize(text)
#     output = []
#     for sent in tokenized_sent:
#         sent = re.findall(r'[A-Za-z]+', sent)
#         sent = [word for word, tag in nltk.pos_tag(sent) \
#                   if (tag in ['NN', 'NNS'])]
#         sent = [LEM.lemmatize(token.lower()) for token in sent if token.lower() not in STOPWORDS]
#         output.append(tokenize_input(' '.join(sent)))
        
#     return list(chain.from_iterable(output))
