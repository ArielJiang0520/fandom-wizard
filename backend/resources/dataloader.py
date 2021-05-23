import numpy as np
from sys import getsizeof
import os

def read_chunks(file_path, fn_prefix, chunk_size, chunks):
    res = []
    for i in range(chunks):
        fn = os.path.join(file_path, f'{fn_prefix}{i*chunk_size}-{i*chunk_size+chunk_size-1}.p.npy')
        # print('Loading', fn)
        res.append(np.load(fn))
        
    return res

def load_matrix(matrix_path):
    E = np.concatenate(read_chunks(matrix_path, 'BERT-corpus97878_chunk', 10000, 10), axis=0)
    print(f'Matrix E successfully loaded. Shape: {E.shape} Size in Memory: {getsizeof(E) * 1e-6:.2f} MB')
    return E