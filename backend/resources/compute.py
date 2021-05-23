from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def KNN(matrix, id, k):
    return np.argsort(-cosine_similarity(matrix, matrix[id].reshape(1, -1)).flatten())[:k].tolist()