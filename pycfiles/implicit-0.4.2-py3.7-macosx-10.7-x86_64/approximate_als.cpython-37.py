# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/implicit/approximate_als.py
# Compiled at: 2019-10-24 03:58:04
# Size of source mod 2**32: 17627 bytes
""" Models that use various Approximate Nearest Neighbours libraries in order to quickly
generate recommendations and lists of similar items.

See http://www.benfrederickson.com/approximate-nearest-neighbours-for-recommender-systems/
"""
import itertools, logging, numpy, implicit.cuda
from implicit.als import AlternatingLeastSquares
log = logging.getLogger('implicit')

def augment_inner_product_matrix(factors):
    """ This function transforms a factor matrix such that an angular nearest neighbours search
    will return top related items of the inner product.

    This involves transforming each row by adding one extra dimension as suggested in the paper:
    "Speeding Up the Xbox Recommender System Using a Euclidean Transformation for Inner-Product
    Spaces" https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/XboxInnerProduct.pdf

    Basically this involves transforming each feature vector so that they have the same norm, which
    means the cosine of this transformed vector is proportional to the dot product (if the other
    vector in the cosine has a 0 in the extra dimension). """
    norms = numpy.linalg.norm(factors, axis=1)
    max_norm = norms.max()
    extra_dimension = numpy.sqrt(max_norm ** 2 - norms ** 2)
    return (max_norm, numpy.append(factors, (extra_dimension.reshape(norms.shape[0], 1)), axis=1))


class NMSLibAlternatingLeastSquares(AlternatingLeastSquares):
    __doc__ = " Speeds up the base :class:`~implicit.als.AlternatingLeastSquares` model by using\n    `NMSLib <https://github.com/searchivarius/nmslib>`_ to create approximate nearest neighbours\n    indices of the latent factors.\n\n    Parameters\n    ----------\n    method : str, optional\n        The NMSLib method to use\n    index_params: dict, optional\n        Optional params to send to the createIndex call in NMSLib\n    query_params: dict, optional\n        Optional query time params for the NMSLib 'setQueryTimeParams' call\n    approximate_similar_items : bool, optional\n        whether or not to build an NMSLIB index for computing similar_items\n    approximate_recommend : bool, optional\n        whether or not to build an NMSLIB index for the recommend call\n\n    Attributes\n    ----------\n    similar_items_index : nmslib.FloatIndex\n        NMSLib index for looking up similar items in the cosine space formed by the latent\n        item_factors\n\n    recommend_index : nmslib.FloatIndex\n        NMSLib index for looking up similar items in the inner product space formed by the latent\n        item_factors\n    "

    def __init__(self, approximate_similar_items=True, approximate_recommend=True, method='hnsw', index_params=None, query_params=None, *args, **kwargs):
        if index_params is None:
            index_params = {'M':16, 
             'post':0,  'efConstruction':400}
        if query_params is None:
            query_params = {'ef': 90}
        self.similar_items_index = None
        self.recommend_index = None
        self.approximate_similar_items = approximate_similar_items
        self.approximate_recommend = approximate_recommend
        self.method = method
        self.index_params = index_params
        self.query_params = query_params
        (super(NMSLibAlternatingLeastSquares, self).__init__)(*args, **kwargs)

    def fit(self, Ciu, show_progress=True):
        logging.getLogger('nmslib').setLevel(logging.WARNING)
        import nmslib
        super(NMSLibAlternatingLeastSquares, self).fit(Ciu, show_progress=show_progress)
        if self.approximate_similar_items:
            log.debug('Building nmslib similar items index')
            self.similar_items_index = nmslib.init(method=(self.method),
              space='cosinesimil')
            norms = numpy.linalg.norm((self.item_factors), axis=1)
            ids = numpy.arange(self.item_factors.shape[0])
            item_factors = numpy.delete((self.item_factors), (ids[(norms == 0)]), axis=0)
            ids = ids[(norms != 0)]
            self.similar_items_index.addDataPointBatch(item_factors, ids=ids)
            self.similar_items_index.createIndex((self.index_params), print_progress=show_progress)
            self.similar_items_index.setQueryTimeParams(self.query_params)
        if self.approximate_recommend:
            log.debug('Building nmslib recommendation index')
            self.max_norm, extra = augment_inner_product_matrix(self.item_factors)
            self.recommend_index = nmslib.init(method='hnsw',
              space='cosinesimil')
            self.recommend_index.addDataPointBatch(extra)
            self.recommend_index.createIndex((self.index_params), print_progress=show_progress)
            self.recommend_index.setQueryTimeParams(self.query_params)

    def similar_items(self, itemid, N=10):
        if not self.approximate_similar_items:
            return super(NMSLibAlternatingLeastSquares, self).similar_items(itemid, N)
        neighbours, distances = self.similar_items_index.knnQuery(self.item_factors[itemid], N)
        return zip(neighbours, 1.0 - distances)

    def recommend(self, userid, user_items, N=10, filter_items=None, recalculate_user=False):
        if not self.approximate_recommend:
            return super(NMSLibAlternatingLeastSquares, self).recommend(userid, user_items, N=N, filter_items=filter_items,
              recalculate_user=recalculate_user)
        user = self._user_factor(userid, user_items, recalculate_user)
        liked = set(user_items[userid].indices)
        if filter_items:
            liked.update(filter_items)
        count = N + len(liked)
        query = numpy.append(user, 0)
        ids, dist = self.recommend_index.knnQuery(query, count)
        scaling = self.max_norm * numpy.linalg.norm(query)
        dist = scaling * (1.0 - dist)
        return list(itertools.islice((rec for rec in zip(ids, dist) if rec[0] not in liked), N))


class AnnoyAlternatingLeastSquares(AlternatingLeastSquares):
    __doc__ = 'A version of the :class:`~implicit.als.AlternatingLeastSquares` model that uses an\n    `Annoy <https://github.com/spotify/annoy>`_ index to calculate similar items and\n    recommend items.\n\n    Parameters\n    ----------\n    n_trees : int, optional\n        The number of trees to use when building the Annoy index. More trees gives higher precision\n        when querying.\n    search_k : int, optional\n        Provides a way to search more trees at runtime, giving the ability to have more accurate\n        results at the cost of taking more time.\n    approximate_similar_items : bool, optional\n        whether or not to build an Annoy index for computing similar_items\n    approximate_recommend : bool, optional\n        whether or not to build an Annoy index for the recommend call\n\n    Attributes\n    ----------\n    similar_items_index : annoy.AnnoyIndex\n        Annoy index for looking up similar items in the cosine space formed by the latent\n        item_factors\n\n    recommend_index : annoy.AnnoyIndex\n        Annoy index for looking up similar items in the inner product space formed by the latent\n        item_factors\n    '

    def __init__(self, approximate_similar_items=True, approximate_recommend=True, n_trees=50, search_k=-1, *args, **kwargs):
        (super(AnnoyAlternatingLeastSquares, self).__init__)(*args, **kwargs)
        self.similar_items_index = None
        self.recommend_index = None
        self.approximate_similar_items = approximate_similar_items
        self.approximate_recommend = approximate_recommend
        self.n_trees = n_trees
        self.search_k = search_k

    def fit(self, Ciu, show_progress=True):
        import annoy
        super(AnnoyAlternatingLeastSquares, self).fit(Ciu, show_progress=show_progress)
        if self.approximate_similar_items:
            log.debug('Building annoy similar items index')
            self.similar_items_index = annoy.AnnoyIndex(self.item_factors.shape[1], 'angular')
            for i, row in enumerate(self.item_factors):
                self.similar_items_index.add_item(i, row)

            self.similar_items_index.build(self.n_trees)
        if self.approximate_recommend:
            log.debug('Building annoy recommendation index')
            self.max_norm, extra = augment_inner_product_matrix(self.item_factors)
            self.recommend_index = annoy.AnnoyIndex(extra.shape[1], 'angular')
            for i, row in enumerate(extra):
                self.recommend_index.add_item(i, row)

            self.recommend_index.build(self.n_trees)

    def similar_items(self, itemid, N=10):
        if not self.approximate_similar_items:
            return super(AnnoyAlternatingLeastSquares, self).similar_items(itemid, N)
        neighbours, dist = self.similar_items_index.get_nns_by_item(itemid, N, search_k=(self.search_k),
          include_distances=True)
        return zip(neighbours, 1 - numpy.array(dist) ** 2 / 2)

    def recommend(self, userid, user_items, N=10, filter_items=None, recalculate_user=False):
        if not self.approximate_recommend:
            return super(AnnoyAlternatingLeastSquares, self).recommend(userid, user_items, N=N, filter_items=filter_items,
              recalculate_user=recalculate_user)
        user = self._user_factor(userid, user_items, recalculate_user)
        liked = set(user_items[userid].indices)
        if filter_items:
            liked.update(filter_items)
        count = N + len(liked)
        query = numpy.append(user, 0)
        ids, dist = self.recommend_index.get_nns_by_vector(query, count, include_distances=True, search_k=(self.search_k))
        scaling = self.max_norm * numpy.linalg.norm(query)
        dist = scaling * (1 - numpy.array(dist) ** 2 / 2)
        return list(itertools.islice((rec for rec in zip(ids, dist) if rec[0] not in liked), N))


class FaissAlternatingLeastSquares(AlternatingLeastSquares):
    __doc__ = ' Speeds up the base :class:`~implicit.als.AlternatingLeastSquares` model by using\n    `Faiss <https://github.com/facebookresearch/faiss>`_ to create approximate nearest neighbours\n    indices of the latent factors.\n\n\n    Parameters\n    ----------\n    nlist : int, optional\n        The number of cells to use when building the Faiss index.\n    nprobe : int, optional\n        The number of cells to visit to perform a search.\n    use_gpu : bool, optional\n        Whether or not to enable run Faiss on the GPU. Requires faiss to have been\n        built with GPU support.\n    approximate_similar_items : bool, optional\n        whether or not to build an Faiss index for computing similar_items\n    approximate_recommend : bool, optional\n        whether or not to build an Faiss index for the recommend call\n\n    Attributes\n    ----------\n    similar_items_index : faiss.IndexIVFFlat\n        Faiss index for looking up similar items in the cosine space formed by the latent\n        item_factors\n\n    recommend_index : faiss.IndexIVFFlat\n        Faiss index for looking up similar items in the inner product space formed by the latent\n        item_factors\n    '

    def __init__(self, approximate_similar_items=True, approximate_recommend=True, nlist=400, nprobe=20, use_gpu=implicit.cuda.HAS_CUDA, *args, **kwargs):
        self.similar_items_index = None
        self.recommend_index = None
        self.approximate_similar_items = approximate_similar_items
        self.approximate_recommend = approximate_recommend
        self.nlist = nlist
        self.nprobe = nprobe
        (super(FaissAlternatingLeastSquares, self).__init__)(args, use_gpu=use_gpu, **kwargs)

    def fit(self, Ciu, show_progress=True):
        import faiss
        super(FaissAlternatingLeastSquares, self).fit(Ciu, show_progress=show_progress)
        self.quantizer = faiss.IndexFlat(self.factors)
        if self.use_gpu:
            self.gpu_resources = faiss.StandardGpuResources()
        item_factors = self.item_factors.astype('float32')
        if self.approximate_recommend:
            log.debug('Building faiss recommendation index')
            if self.use_gpu:
                index = faiss.GpuIndexIVFFlat(self.gpu_resources, self.factors, self.nlist, faiss.METRIC_INNER_PRODUCT)
            else:
                index = faiss.IndexIVFFlat(self.quantizer, self.factors, self.nlist, faiss.METRIC_INNER_PRODUCT)
            index.train(item_factors)
            index.add(item_factors)
            index.nprobe = self.nprobe
            self.recommend_index = index
        if self.approximate_similar_items:
            log.debug('Building faiss similar items index')
            norms = numpy.linalg.norm(item_factors, axis=1)
            norms[norms == 0] = 1e-10
            normalized = (item_factors.T / norms).T.astype('float32')
            if self.use_gpu:
                index = faiss.GpuIndexIVFFlat(self.gpu_resources, self.factors, self.nlist, faiss.METRIC_INNER_PRODUCT)
            else:
                index = faiss.IndexIVFFlat(self.quantizer, self.factors, self.nlist, faiss.METRIC_INNER_PRODUCT)
            index.train(normalized)
            index.add(normalized)
            index.nprobe = self.nprobe
            self.similar_items_index = index

    def similar_items--- This code section failed: ---

 L. 366         0  LOAD_FAST                'self'
                2  LOAD_ATTR                approximate_similar_items
                4  POP_JUMP_IF_FALSE    20  'to 20'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                use_gpu
               10  POP_JUMP_IF_FALSE    38  'to 38'
               12  LOAD_FAST                'N'
               14  LOAD_CONST               1024
               16  COMPARE_OP               >=
               18  POP_JUMP_IF_FALSE    38  'to 38'
             20_0  COME_FROM             4  '4'

 L. 367        20  LOAD_GLOBAL              super
               22  LOAD_GLOBAL              FaissAlternatingLeastSquares
               24  LOAD_FAST                'self'
               26  CALL_FUNCTION_2       2  '2 positional arguments'
               28  LOAD_METHOD              similar_items
               30  LOAD_FAST                'itemid'
               32  LOAD_FAST                'N'
               34  CALL_METHOD_2         2  '2 positional arguments'
               36  RETURN_VALUE     
             38_0  COME_FROM            18  '18'
             38_1  COME_FROM            10  '10'

 L. 369        38  LOAD_FAST                'self'
               40  LOAD_ATTR                item_factors
               42  LOAD_FAST                'itemid'
               44  BINARY_SUBSCR    
               46  STORE_FAST               'factors'

 L. 370        48  LOAD_FAST                'factors'
               50  LOAD_GLOBAL              numpy
               52  LOAD_ATTR                linalg
               54  LOAD_METHOD              norm
               56  LOAD_FAST                'factors'
               58  CALL_METHOD_1         1  '1 positional argument'
               60  INPLACE_TRUE_DIVIDE
               62  STORE_FAST               'factors'

 L. 371        64  LOAD_FAST                'self'
               66  LOAD_ATTR                similar_items_index
               68  LOAD_METHOD              search
               70  LOAD_FAST                'factors'
               72  LOAD_METHOD              reshape
               74  LOAD_CONST               1
               76  LOAD_CONST               -1
               78  CALL_METHOD_2         2  '2 positional arguments'
               80  LOAD_METHOD              astype
               82  LOAD_STR                 'float32'
               84  CALL_METHOD_1         1  '1 positional argument'

 L. 372        86  LOAD_FAST                'N'
               88  CALL_METHOD_2         2  '2 positional arguments'
               90  UNPACK_SEQUENCE_2     2 
               92  UNPACK_SEQUENCE_1     1 
               94  STORE_FAST               'dist'
               96  UNPACK_SEQUENCE_1     1 
               98  STORE_FAST               'ids'

 L. 373       100  LOAD_GLOBAL              zip
              102  LOAD_FAST                'ids'
              104  LOAD_FAST                'dist'
              106  CALL_FUNCTION_2       2  '2 positional arguments'
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 108

    def recommend(self, userid, user_items, N=10, filter_items=None, recalculate_user=False):
        if not self.approximate_recommend:
            return super(FaissAlternatingLeastSquares, self).recommend(userid, user_items, N=N, filter_items=filter_items,
              recalculate_user=recalculate_user)
        else:
            user = self._user_factor(userid, user_items, recalculate_user)
            liked = set(user_items[userid].indices)
            if filter_items:
                liked.update(filter_items)
            count = N + len(liked)
            if self.use_gpu and count >= 1024:
                return super(FaissAlternatingLeastSquares, self).recommend(userid, user_items, N=N, filter_items=filter_items,
                  recalculate_user=recalculate_user)
        query = user.reshape(1, -1).astype('float32')
        (dist,), (ids,) = self.recommend_index.search(query, count)
        return list(itertools.islice((rec for rec in zip(ids, dist) if rec[0] not in liked), N))