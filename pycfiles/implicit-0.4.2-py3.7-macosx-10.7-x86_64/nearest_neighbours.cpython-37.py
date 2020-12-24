# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/implicit/nearest_neighbours.py
# Compiled at: 2019-10-24 03:58:04
# Size of source mod 2**32: 6802 bytes
import itertools, numpy
from numpy import bincount, log, log1p, sqrt
from scipy.sparse import coo_matrix, csr_matrix
from ._nearest_neighbours import NearestNeighboursScorer, all_pairs_knn
from .recommender_base import RecommenderBase
from .utils import nonzeros

class ItemItemRecommender(RecommenderBase):
    __doc__ = ' Base class for Item-Item Nearest Neighbour recommender models\n    here.\n\n    Parameters\n    ----------\n    K : int, optional\n        The number of neighbours to include when calculating the item-item\n        similarity matrix\n    num_threads : int, optional\n        The number of threads to use for fitting the model. Specifying 0\n        means to default to the number of cores on the machine.\n    '

    def __init__(self, K=20, num_threads=0):
        self.similarity = None
        self.K = K
        self.num_threads = num_threads
        self.scorer = None

    def fit(self, weighted, show_progress=True):
        """ Computes and stores the similarity matrix """
        self.similarity = all_pairs_knn(weighted, (self.K), show_progress=show_progress,
          num_threads=(self.num_threads)).tocsr()
        self.scorer = NearestNeighboursScorer(self.similarity)

    def recommend(self, userid, user_items, N=10, filter_already_liked_items=True, filter_items=None, recalculate_user=False):
        """ returns the best N recommendations for a user given its id"""
        if userid >= user_items.shape[0]:
            raise ValueError('userid is out of bounds of the user_items matrix')
        else:
            items = N
            if filter_items:
                items += len(filter_items)
            indices, data = self.scorer.recommend(userid, (user_items.indptr), (user_items.indices), (user_items.data),
              K=items, remove_own_likes=filter_already_liked_items)
            best = sorted((zip(indices, data)), key=(lambda x: -x[1]))
            return filter_items or best
        liked = set(filter_items)
        return list(itertools.islice((rec for rec in best if rec[0] not in liked), N))

    def rank_items(self, userid, user_items, selected_items, recalculate_user=False):
        """ Rank given items for a user and returns sorted item list """
        if max(selected_items) >= user_items.shape[1] or min(selected_items) < 0:
            raise IndexError('Some of selected itemids are not in the model')
        liked_vector = user_items[userid]
        recommendations = liked_vector.dot(self.similarity)
        best = sorted((zip(recommendations.indices, recommendations.data)), key=(lambda x: -x[1]))
        ret = [rec for rec in best if rec[0] in selected_items]
        for itemid in selected_items:
            if itemid not in recommendations.indices:
                ret.append((itemid, -1.0))

        return ret

    def similar_users(self, userid, N=10):
        raise NotImplementedError('Not implemented Yet')

    def similar_items(self, itemid, N=10):
        """ Returns a list of the most similar other items """
        if itemid >= self.similarity.shape[0]:
            return []
        return sorted((list(nonzeros(self.similarity, itemid))), key=(lambda x: -x[1]))[:N]

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['scorer']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        if self.similarity is not None:
            self.scorer = NearestNeighboursScorer(self.similarity)
        else:
            self.scorer = None

    def save(self, filename):
        m = self.similarity
        numpy.savez(filename, data=(m.data), indptr=(m.indptr), indices=(m.indices), shape=(m.shape), K=(self.K))

    @classmethod
    def load(cls, filename):
        if not filename.endswith('.npz'):
            filename = filename + '.npz'
        m = numpy.load(filename)
        similarity = csr_matrix((m['data'], m['indices'], m['indptr']), shape=(m['shape']))
        ret = cls()
        ret.similarity = similarity
        ret.scorer = NearestNeighboursScorer(similarity)
        ret.K = m['K']
        return ret


class CosineRecommender(ItemItemRecommender):
    __doc__ = ' An Item-Item Recommender on Cosine distances between items '

    def fit(self, counts, show_progress=True):
        ItemItemRecommender.fit(self, normalize(counts), show_progress)


class TFIDFRecommender(ItemItemRecommender):
    __doc__ = ' An Item-Item Recommender on TF-IDF distances between items '

    def fit(self, counts, show_progress=True):
        weighted = normalize(tfidf_weight(counts))
        ItemItemRecommender.fit(self, weighted, show_progress)


class BM25Recommender(ItemItemRecommender):
    __doc__ = ' An Item-Item Recommender on BM25 distance between items '

    def __init__(self, K=20, K1=1.2, B=0.75, num_threads=0):
        super(BM25Recommender, self).__init__(K, num_threads)
        self.K1 = K1
        self.B = B

    def fit(self, counts, show_progress=True):
        weighted = bm25_weight(counts, self.K1, self.B)
        ItemItemRecommender.fit(self, weighted, show_progress)


def tfidf_weight(X):
    """ Weights a Sparse Matrix by TF-IDF Weighted """
    X = coo_matrix(X)
    N = float(X.shape[0])
    idf = log(N) - log1p(bincount(X.col))
    X.data = sqrt(X.data) * idf[X.col]
    return X


def normalize(X):
    """ equivalent to scipy.preprocessing.normalize on sparse matrices
    , but lets avoid another depedency just for a small utility function """
    X = coo_matrix(X)
    X.data = X.data / sqrt(bincount(X.row, X.data ** 2))[X.row]
    return X


def bm25_weight(X, K1=100, B=0.8):
    """ Weighs each row of a sparse matrix X  by BM25 weighting """
    X = coo_matrix(X)
    N = float(X.shape[0])
    idf = log(N) - log1p(bincount(X.col))
    row_sums = numpy.ravel(X.sum(axis=1))
    average_length = row_sums.mean()
    length_norm = 1.0 - B + B * row_sums / average_length
    X.data = X.data * (K1 + 1.0) / (K1 * length_norm[X.row] + X.data) * idf[X.col]
    return X