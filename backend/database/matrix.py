import numpy as np
import pickle
import sys
import os

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

curr_path = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(os.path.join(curr_path, 'cache')):
    try:
        os.mkdir(os.path.join(curr_path, 'cache'))
    except PermissionError:
        print('Fatal Error: No cache folder found and no permission to make cache folder')
        raise PermissionError

def read_embed_matrix(db, table, hard_refresh=False):
    if hard_refresh:
        logging.info('Forced re-parsing embed from db')

    cache_path = os.path.join(curr_path, 'cache')

    if os.path.exists(os.path.join(cache_path, f'E.npy')) and not hard_refresh:
        logging.info('Detect cached matrix. using cached matrix...')
        try:
            E = np.load(os.path.join(cache_path, 'E.npy'))
            T = np.load(os.path.join(cache_path, 'T.npy'))
            C = np.load(os.path.join(cache_path, 'C.npy'))
            S = np.load(os.path.join(cache_path, 'S.npy'))

            return E, T, C, S

        except FileNotFoundError:
            logging.warning('Missing a cache file. Making new ones instead.')
    else:
        logging.info('Hard refresh or no cache files found. Making new matrix...')

    results = db.session.query(table).order_by(table.index.asc())

    logging.info('embed fetched from db. parsing...')

    E = np.array(
        [np.array([float(e) for e in res.embed.lstrip('[').rstrip(']').split(',')], 
            dtype=np.float32) for res in results], 
    )

    logging.info(f'E shape: {E.shape}. system memory usage: {sys.getsizeof(E) * 1e-6:.2f}')
    np.save(os.path.join(cache_path, 'E.npy'), E)

    T = np.array(
        [np.array([float(e) for e in res.tags.lstrip('[').rstrip(']').split(',')], 
            dtype=np.float32) for res in results], 
    )

    logging.info(f'T shape: {T.shape}. system memory usage: {sys.getsizeof(T) * 1e-6:.2f}')
    np.save(os.path.join(cache_path, 'T.npy'), T)

    C = np.array(
        [np.array([float(e) for e in res.characters.lstrip('[').rstrip(']').split(',')], 
            dtype=np.float32) for res in results], 
    )

    logging.info(f'C shape: {C.shape}. system memory usage: {sys.getsizeof(C) * 1e-6:.2f}')
    np.save(os.path.join(cache_path, 'C.npy'), C)

    S = np.array(
        [np.array([float(e) for e in res.sentiment.lstrip('[').rstrip(']').split(',')], 
            dtype=np.float32) for res in results], 
    )

    logging.info(f'S shape: {S.shape}. system memory usage: {sys.getsizeof(S) * 1e-6:.2f}')
    np.save(os.path.join(cache_path, 'S.npy'), S)

    assert E.shape[0] == T.shape[0] == C.shape[0] == S.shape[0], 'Fatal Error: matrices dimensions do not match'

    logging.info('All matrix cached to local')

    return E, T, C, S


def read_word2vec_table(db, table):
    cache_path = os.path.join(curr_path, 'cache')

    if os.path.exists(os.path.join(cache_path, f'word2vec_table.p')):
        logging.info('Detect cached word2vec table. using cached table...')
        return pickle.load(open(os.path.join(cache_path, 'word2vec_table.p'), 'rb'))
    else:
        logging.info('No cache files found. Making new table...')
    
    entries = db.session.query(table)

    table = {}
    for row in entries:
        table[row.key] = np.array([float(e) for e in row.vector.lstrip('[').rstrip(']').split(',')], dtype=np.float32)
    
    assert table['the'].shape == (300,), f'{table["the"].shape}'

    pickle.dump(table, open(os.path.join(cache_path, 'word2vec_table.p'), 'wb'))
    
    logging.info(f'Table made with size {len(table)}')
    logging.info('Word2vec table cached to local')

    return table