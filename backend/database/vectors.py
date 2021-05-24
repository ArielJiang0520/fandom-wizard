import numpy as np
import sys
import os

curr_path = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(os.path.join(curr_path, 'cache')):
    try:
        os.mkdir(os.path.join(curr_path, 'cache'))
    except PermissionError:
        print('No cache folder found and no permission to make cache folder')


def read_embed_matrix(db, table, hard_refresh=False):
    if hard_refresh:
        print('Forced re-parsing embed from db')

    cache_path = os.path.join(curr_path, 'cache')

    if os.path.exists(os.path.join(cache_path, f'E.npy')) and not hard_refresh:
        print('detect cached matrix. using cached matrix...')
        try:
            E = np.load(os.path.join(cache_path, 'E.npy'))
            T = np.load(os.path.join(cache_path, 'T.npy'))
            C = np.load(os.path.join(cache_path, 'C.npy'))

            return E, T, C

        except FileNotFoundError:
            print('Missing a cache file. Making new ones instead.')
    else:
        print('Hard refresh or no cache files found. Making new matrix...')

    results = db.session.query(table).order_by(table.index.asc())

    print('embed fetched from db. parsing...')

    E = np.array(
        [np.array([float(e) for e in res.embed.lstrip('[').rstrip(']').split(',')], 
            dtype=np.float32) for res in results], 
    )

    print(f'E shape: {E.shape}. system memory usage: {sys.getsizeof(E) * 1e-6:.2f}')
    np.save(os.path.join(cache_path, 'E.npy'), E)

    T = np.array(
        [np.array([float(e) for e in res.tags.lstrip('[').rstrip(']').split(',')], 
            dtype=np.float32) for res in results], 
    )

    print(f'T shape: {T.shape}. system memory usage: {sys.getsizeof(T) * 1e-6:.2f}')
    np.save(os.path.join(cache_path, 'T.npy'), T)

    C = np.array(
        [np.array([float(e) for e in res.characters.lstrip('[').rstrip(']').split(',')], 
            dtype=np.float32) for res in results], 
    )

    print(f'C shape: {C.shape}. system memory usage: {sys.getsizeof(C) * 1e-6:.2f}')
    np.save(os.path.join(cache_path, 'C.npy'), C)

    print('all matrix cached to local')

    return E, T, C