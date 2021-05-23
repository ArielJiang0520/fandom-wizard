import numpy as np
import sys
import os

curr_path = os.path.dirname(os.path.realpath(__file__))

def read_embed_matrix(db, table):
    cache_path = os.path.join(curr_path, 'cache')

    if os.path.exists(os.path.join(cache_path, 'E.npy')):
        print('detect cached matrix. using cached matrix instead...')
        E = np.load(os.path.join(cache_path, 'E.npy'))
        return E

    results = db.session.query(table).order_by(table.index.asc())
    print('embed fetched from db. parsing embed... (this can take up to 20sec)')
    E = np.array(
        [np.array([res.index] + [float(e) for e in res.embed.lstrip('[').rstrip(']').split(',')], 
            dtype=np.float32) for res in results], 
    )
    print(f'embed parsed. shape: {E.shape}. system memory usage: {sys.getsizeof(E) * 1e-6:.2f}')

    np.save(os.path.join(cache_path, 'E.npy'), E)
    print('embed matrix cached to local')

    return E