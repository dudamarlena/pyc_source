# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/LSSC/functions/embeddings.py
# Compiled at: 2020-04-25 01:44:25
# Size of source mod 2**32: 4062 bytes
import os
os.environ['OMP_NUM_THREADS'] = '10'
os.environ['OPENBLAS_NUM_THREADS'] = '10'
os.environ['MKL_NUM_THREADS'] = '10'
os.environ['VECLIB_MAXIMUM_THREADS'] = '10'
os.environ['NUMEXPR_NUM_THREADS'] = '10'
import scipy.sparse as sparse
import hnswlib as hnsw, numpy as np
from dask import delayed

@delayed
def calc_affinity_matrix(*, pixel_list: np.matrix, metric: str, knn: int, accuracy: int, connections: int, normalize_w_k: int, num_threads: int, spatial_box_num: int, temporal_box_num: int):
    """
    Calculates an pairwise affinity matrix for the image stack
    Parameters
    ----------
    pixel_list: a 2d np array of pixels with dim 0 being a list of pixels and dim 1 being pixel values over time
    metric: can be "l2" squared l2, "ip" Inner product, "cosine" Cosine similarity
    knn: number of nearest neighbors to search for
    accuracy: time of construction vs acuracy tradeoff
    connections: max number of outgoing connections
    num_threads: number of threads to use
    normalize_w_k: kth clostest neighbor for autotune

    Returns
    -------
    affinity matrix
    """
    dim = pixel_list.shape[1]
    num_elements = pixel_list.shape[0]
    print('Spatial Box {}, Time Step {}: Started Processing'.format(spatial_box_num, temporal_box_num))
    p = hnsw.Index(space=metric, dim=dim)
    p.init_index(max_elements=num_elements, ef_construction=accuracy, M=connections)
    p.add_items(pixel_list, num_threads=num_threads)
    indices, distances = p.knn_query(pixel_list, k=knn, num_threads=num_threads)
    reformat_indicies_x = np.repeat(np.arange(0, num_elements, 1), knn)
    reformat_indicies_y = np.reshape(indices, -1)
    reformat_distances = np.reshape(distances, -1)
    scale_factor_indices = np.repeat(distances[:, normalize_w_k], knn)
    scale_factor_2_per_distances = scale_factor_indices[reformat_indicies_x] * scale_factor_indices[reformat_indicies_y]
    reformat_distances_scaled = np.exp(-reformat_distances / scale_factor_2_per_distances)
    return sparse.csr_matrix(sparse.coo_matrix((
     reformat_distances_scaled,
     (
      reformat_indicies_x, reformat_indicies_y)),
      shape=(
     num_elements, num_elements)))


def calc_D_inv(K):
    """Calculates a scaling diagonal matrix D to rescale eigen vectors

    Parameters
    ----------
    K the sparse matrix K for the pairwise affinity

    Returns
    -------
    a sparse matrix with type csr, and D's diagonal values
    """
    dim = K.shape[0]
    D_diag = 1 / K.sum(axis=1)
    D_sparse = sparse.dia_matrix((np.reshape(D_diag, [1, -1]), [0]), (
     dim, dim))
    return (
     sparse.csr_matrix(D_sparse), D_diag)


def calc_laplacian(P_sparse, dim):
    I_sparse = sparse.identity(dim, format='csr')
    laplacian_sparse = I_sparse - P_sparse
    return laplacian_sparse


def calc_D_sqrt(D_diag):
    dim = D_diag.shape[0]
    D_sqrt = sparse.csr_matrix(sparse.dia_matrix((np.reshape(np.power(D_diag, 0.5), [1, -1]), [0]), (
     dim, dim)))
    return D_sqrt


def calc_D_neg_sqrt(D_diag):
    dim = D_diag.shape[0]
    D_neg_sqrt = sparse.csr_matrix(sparse.dia_matrix((
     np.reshape(np.power(D_diag, -0.5), [1, -1]), [0]), (
     dim, dim)))
    return D_neg_sqrt


def embed_eigen_norm(eigen_vectors):
    pixel_embedings = np.sum((np.power(eigen_vectors, 2)), axis=1)
    return pixel_embedings