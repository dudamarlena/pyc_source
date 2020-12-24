# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/github/spyking-circus/build/lib/circus/shared/algorithms.py
# Compiled at: 2020-04-14 07:20:51
# Size of source mod 2**32: 53932 bytes
import os, logging, sys, scipy.optimize, numpy, scipy.spatial.distance, scipy.stats, shutil, h5py, scipy.linalg, scipy.sparse
from circus.shared.files import load_data, write_datasets, get_overlaps, load_data_memshared, get_stas
from circus.shared.utils import get_tqdm_progressbar, get_shared_memory_flag, dip, dip_threshold, batch_folding_test_with_MPA, bhatta_dist, nd_bhatta_dist, test_if_support, test_if_purity
from circus.shared.messages import print_and_log
from circus.shared.probes import get_nodes_and_edges
from circus.shared.mpi import all_gather_array, comm, gather_array
import scipy.linalg, scipy.sparse
import statsmodels.api as sm
logger = logging.getLogger(__name__)

class DistanceMatrix(object):

    def __init__(self, size, distances=None):
        self.size = size
        self.didx = lambda i, j: i * self.size + j - i * (i + 1) // 2 - i - 1
        self.distances = distances

    def initialize(self, data, ydata=None):
        if ydata is None:
            self.distances = scipy.spatial.distance.pdist(data, 'euclidean').astype(numpy.float32)
        else:
            self.distances = scipy.spatial.distance.cdist(data, ydata, 'euclidean').astype(numpy.float32)

    def get_value(self, i, j):
        if i < j:
            value = self.distances[self.didx(i, j)]
        else:
            if i > j:
                value = self.distances[self.didx(j, i)]
            else:
                if i == j:
                    value = 0.0
                else:
                    raise RuntimeError()
        return value

    def get_row(self, i, with_diag=True):
        start = self.distances[self.didx(numpy.arange(0, i), i)]
        end = self.distances[self.didx(i, numpy.arange(i + 1, self.size))]
        if with_diag:
            result = numpy.concatenate((start, numpy.array([0], dtype=(numpy.float32)), end))
        else:
            result = numpy.concatenate((start, end))
        return result

    def get_col(self, i, with_diag=True):
        return self.get_row(i, with_diag=with_diag)

    def to_dense(self):
        return scipy.spatial.distance.squareform(self.distances)

    def get_rows(self, indices, with_diag=True):
        if with_diag:
            result = numpy.zeros((len(indices), self.size), dtype=(numpy.float32))
        else:
            result = numpy.zeros((len(indices), self.size - 1), dtype=(numpy.float32))
        for count, i in enumerate(indices):
            result[count] = self.get_row(i, with_diag=with_diag)

        return result

    def get_cols(self, indices, with_diag=True):
        if with_diag:
            result = numpy.zeros((self.size, len(indices)), dtype=(numpy.float32))
        else:
            result = numpy.zeros((self.size - 1, len(indices)), dtype=(numpy.float32))
        for count, i in enumerate(indices):
            result[:, count] = self.get_col(i, with_diag=with_diag)

        return result

    def get_deltas_and_neighbors(self, rho):
        """Find the distance to and the index of the nearest point with a higher density.

        Argument:
            rho
        Returns:
            nearest_higher_rho_distances
                For each point, distance to the nearest point with a higher density (i.e. delta).
            nearest_higher_rho_indices
                For each point, index of the nearest point with a higher density (i.e. neighbor).
        """
        indices = numpy.argsort(-rho)
        nearest_higher_rho_indices = numpy.zeros((self.size), dtype=(numpy.int))
        nearest_higher_rho_distances = numpy.zeros((self.size), dtype=(numpy.float32))
        for k, index in enumerate(indices):
            higher_rho_indices = indices[0:k + 1]
            higher_rho_distances = self.get_row(index)[higher_rho_indices]
            higher_rho_distances[higher_rho_distances == 0.0] = float('inf')
            nearest_index = numpy.argmin(higher_rho_distances)
            nearest_higher_rho_indices[index] = higher_rho_indices[nearest_index]
            nearest_higher_rho_distances[index] = higher_rho_distances[nearest_index]

        if len(indices) > 1:
            nearest_higher_rho_distances[indices[0]] = numpy.max(nearest_higher_rho_distances[indices[1:]])
            nearest_higher_rho_distances[numpy.isinf(nearest_higher_rho_distances)] = 0
        return (nearest_higher_rho_distances, nearest_higher_rho_indices)

    @property
    def max(self):
        return numpy.max(self.distances)

    def __del__(self):
        del self.distances


def fit_rho_delta(xdata, ydata, alpha=3):
    if xdata.min() == xdata.max():
        return numpy.zeros(0, dtype=(numpy.int32))
    try:
        x = sm.add_constant(xdata)
        model = sm.RLM(ydata, x)
        results = model.fit()
        difference = ydata - results.fittedvalues
        factor = numpy.median(numpy.abs(difference - numpy.median(difference)))
        z_score = difference - alpha * factor * (1 + results.fittedvalues)
        centers = numpy.where(z_score >= 0)[0]
    except Exception:
        centers = numpy.zeros(0, dtype=(numpy.int32))

    return centers


def compute_rho(data, update=None, mratio=0.01):
    nb_points = len(data)
    nb_selec = max(5, int(mratio * nb_points))
    rho = numpy.zeros(nb_points, dtype=(numpy.float32))
    dist_sorted = {}
    if update is None:
        dist = DistanceMatrix(nb_points)
        dist.initialize(data)
        for i in range(nb_points):
            data = dist.get_row(i, with_diag=False)
            if len(data) > nb_selec:
                dist_sorted[i] = data[numpy.argpartition(data, nb_selec)[:nb_selec]]
            else:
                dist_sorted[i] = data
            rho[i] = numpy.mean(dist_sorted[i])

        answer = (
         rho, dist, dist_sorted)
    else:
        for i in range(nb_points):
            dist = scipy.spatial.distance.cdist(data[i].reshape(1, len(data[i])), update[0]).flatten()
            dist = numpy.concatenate((update[1][i], dist))
            if len(dist) > nb_selec:
                dist_sorted[i] = dist[numpy.argpartition(dist, nb_selec)[:nb_selec]]
            else:
                dist_sorted[i] = dist
            rho[i] = numpy.mean(dist_sorted[i])

        answer = (
         rho, dist_sorted)
    return answer


def clustering_by_density(rho, dist, n_min, alpha=3, halo_rejection=3):
    nb_points = len(rho)
    distances = DistanceMatrix(nb_points, distances=dist)
    deltas, neighbors = distances.get_deltas_and_neighbors(rho)
    nb_clusters, labels, centers = find_centroids_and_clusters(distances, rho, deltas, neighbors, alpha)
    halolabels = halo_assign(labels, rho, n_min, halo_rejection) - 1
    centers = numpy.where(centers - 1 >= 0)[0]
    del distances
    return (
     halolabels, rho, deltas, centers)


def find_centroids_and_clusters(dist, rho, delta, neighbors, alpha=3, method='nearest_denser_point'):
    """Find centroids and clusters.

    Arguments:
        dist
            Matrix of distances between pairs of points.
        rho
            For each point, density in its neighborhood.
        delta
            For each point, distance of the nearest point with higher density.
        neighbors
            For each point, index of the nearest point with higher density.
        alpha
        method
    """
    nb_points = len(rho)
    centroids = numpy.zeros(nb_points, dtype=(numpy.int))
    centroid_indices = fit_rho_delta(rho, delta, alpha)
    nb_clusters = len(centroid_indices)
    cluster_nbs = numpy.arange(1, nb_clusters + 1)
    centroids[centroid_indices] = cluster_nbs
    if method == 'nearest_centroid':
        if nb_clusters <= 1:
            labels = numpy.ones(nb_points, dtype=(numpy.int))
        else:
            distances_to_centroids = dist.get_rows(centroid_indices)
            labels = numpy.argmin(distances_to_centroids, axis=0) + 1
    elif method == 'nearest_denser_point':
        if nb_clusters <= 1:
            labels = numpy.ones(nb_points, dtype=(numpy.int))
        else:
            labels = numpy.copy(centroids)
            indices = numpy.argsort(-rho)
            for index in indices:
                if labels[index] == 0:
                    labels[index] = labels[neighbors[index]]

    else:
        raise ValueError('unexpected value %s' % method)
    return (nb_clusters, labels, centroids)


def halo_assign(labels, rhos, n_min, halo_rejection=3):
    """Unassign outliers."""
    halolabels = labels.copy()
    for label_nb in numpy.unique(labels):
        indices = numpy.where(labels == label_nb)[0]
        median_rho = numpy.median(rhos[indices])
        mad_rho = numpy.median(numpy.abs(rhos[indices] - median_rho))
        selected_indices = indices[(rhos[indices] < median_rho - halo_rejection * mad_rho)]
        if len(indices) - len(selected_indices) > n_min:
            halolabels[selected_indices] = 0

    return halolabels


def merging(groups, merging_method, merging_param, data):

    def perform_merging--- This code section failed: ---

 L. 269         0  LOAD_GLOBAL              numpy
                2  LOAD_METHOD              where
                4  LOAD_FAST                'groups_'
                6  LOAD_CONST               -1
                8  COMPARE_OP               >
               10  CALL_METHOD_1         1  '1 positional argument'
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  STORE_FAST               'mask_'

 L. 270        18  LOAD_GLOBAL              numpy
               20  LOAD_METHOD              unique
               22  LOAD_FAST                'groups_'
               24  LOAD_FAST                'mask_'
               26  BINARY_SUBSCR    
               28  CALL_METHOD_1         1  '1 positional argument'
               30  STORE_FAST               'clusters_'

 L. 271        32  LOAD_GLOBAL              numpy
               34  LOAD_ATTR                inf
               36  STORE_FAST               'dmin_'

 L. 272        38  LOAD_CONST               None
               40  LOAD_CONST               None
               42  BUILD_LIST_2          2 
               44  STORE_FAST               'to_merge'

 L. 274     46_48  SETUP_LOOP          740  'to 740'
               50  LOAD_GLOBAL              range
               52  LOAD_GLOBAL              len
               54  LOAD_FAST                'clusters_'
               56  CALL_FUNCTION_1       1  '1 positional argument'
               58  CALL_FUNCTION_1       1  '1 positional argument'
               60  GET_ITER         
            62_64  FOR_ITER            738  'to 738'
               66  STORE_FAST               'ic1'

 L. 275        68  LOAD_GLOBAL              numpy
               70  LOAD_METHOD              where
               72  LOAD_FAST                'groups_'
               74  LOAD_FAST                'clusters_'
               76  LOAD_FAST                'ic1'
               78  BINARY_SUBSCR    
               80  COMPARE_OP               ==
               82  CALL_METHOD_1         1  '1 positional argument'
               84  LOAD_CONST               0
               86  BINARY_SUBSCR    
               88  STORE_FAST               'idx1'

 L. 276        90  LOAD_GLOBAL              numpy
               92  LOAD_ATTR                take
               94  LOAD_FAST                'data_'
               96  LOAD_FAST                'idx1'
               98  LOAD_CONST               0
              100  LOAD_CONST               ('axis',)
              102  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              104  STORE_FAST               'sd1'

 L. 278       106  LOAD_FAST                'merging_method_'
              108  LOAD_CONST               ('distance', 'dip', 'folding', 'bhatta')
              110  COMPARE_OP               in
              112  POP_JUMP_IF_FALSE   128  'to 128'

 L. 279       114  LOAD_GLOBAL              numpy
              116  LOAD_METHOD              median
              118  LOAD_FAST                'sd1'
              120  LOAD_CONST               0
              122  CALL_METHOD_2         2  '2 positional arguments'
              124  STORE_FAST               'm1'
              126  JUMP_FORWARD        132  'to 132'
            128_0  COME_FROM           112  '112'

 L. 281       128  LOAD_CONST               None
              130  STORE_FAST               'm1'
            132_0  COME_FROM           126  '126'

 L. 283   132_134  SETUP_LOOP          736  'to 736'
              136  LOAD_GLOBAL              range
              138  LOAD_FAST                'ic1'
              140  LOAD_CONST               1
              142  BINARY_ADD       
              144  LOAD_GLOBAL              len
              146  LOAD_FAST                'clusters_'
              148  CALL_FUNCTION_1       1  '1 positional argument'
              150  CALL_FUNCTION_2       2  '2 positional arguments'
              152  GET_ITER         
            154_0  COME_FROM           718  '718'
          154_156  FOR_ITER            734  'to 734'
              158  STORE_FAST               'ic2'

 L. 284       160  LOAD_GLOBAL              numpy
              162  LOAD_METHOD              where
              164  LOAD_FAST                'groups_'
              166  LOAD_FAST                'clusters_'
              168  LOAD_FAST                'ic2'
              170  BINARY_SUBSCR    
              172  COMPARE_OP               ==
              174  CALL_METHOD_1         1  '1 positional argument'
              176  LOAD_CONST               0
              178  BINARY_SUBSCR    
              180  STORE_FAST               'idx2'

 L. 285       182  LOAD_GLOBAL              numpy
              184  LOAD_ATTR                take
              186  LOAD_FAST                'data_'
              188  LOAD_FAST                'idx2'
              190  LOAD_CONST               0
              192  LOAD_CONST               ('axis',)
              194  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              196  STORE_FAST               'sd2'

 L. 287       198  LOAD_FAST                'merging_method_'
              200  LOAD_CONST               ('distance', 'dip', 'folding', 'bhatta')
              202  COMPARE_OP               in
              204  POP_JUMP_IF_FALSE   252  'to 252'

 L. 288       206  LOAD_GLOBAL              numpy
              208  LOAD_METHOD              median
              210  LOAD_FAST                'sd2'
              212  LOAD_CONST               0
              214  CALL_METHOD_2         2  '2 positional arguments'
              216  STORE_FAST               'm2'

 L. 289       218  LOAD_FAST                'm1'
              220  LOAD_FAST                'm2'
              222  BINARY_SUBTRACT  
              224  STORE_FAST               'v_n'

 L. 290       226  LOAD_GLOBAL              numpy
              228  LOAD_METHOD              dot
              230  LOAD_FAST                'sd1'
              232  LOAD_FAST                'v_n'
              234  CALL_METHOD_2         2  '2 positional arguments'
              236  STORE_FAST               'pr_1'

 L. 291       238  LOAD_GLOBAL              numpy
              240  LOAD_METHOD              dot
              242  LOAD_FAST                'sd2'
              244  LOAD_FAST                'v_n'
              246  CALL_METHOD_2         2  '2 positional arguments'
              248  STORE_FAST               'pr_2'
              250  JUMP_FORWARD        260  'to 260'
            252_0  COME_FROM           204  '204'

 L. 293       252  LOAD_CONST               None
              254  STORE_FAST               'pr_1'

 L. 294       256  LOAD_CONST               None
              258  STORE_FAST               'pr_2'
            260_0  COME_FROM           250  '250'

 L. 296       260  LOAD_FAST                'merging_method_'
              262  LOAD_STR                 'folding'
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   324  'to 324'

 L. 297       270  LOAD_GLOBAL              numpy
              272  LOAD_METHOD              concatenate
              274  LOAD_FAST                'pr_1'
              276  LOAD_FAST                'pr_2'
              278  BUILD_LIST_2          2 
              280  CALL_METHOD_1         1  '1 positional argument'
              282  STORE_FAST               'sub_data'

 L. 298       284  LOAD_GLOBAL              batch_folding_test_with_MPA
              286  LOAD_FAST                'sub_data'
              288  LOAD_CONST               True
              290  CALL_FUNCTION_2       2  '2 positional arguments'
              292  UNPACK_SEQUENCE_4     4 
              294  STORE_FAST               'unimodal'
              296  STORE_FAST               'p_value'
              298  STORE_FAST               'phi'
              300  STORE_FAST               '_'

 L. 299       302  LOAD_FAST                'unimodal'
          304_306  POP_JUMP_IF_FALSE   314  'to 314'

 L. 300       308  LOAD_FAST                'p_value'
              310  STORE_FAST               'dist'
              312  JUMP_FORWARD        712  'to 712'
            314_0  COME_FROM           304  '304'

 L. 302       314  LOAD_GLOBAL              numpy
              316  LOAD_ATTR                inf
              318  STORE_FAST               'dist'
          320_322  JUMP_FORWARD        712  'to 712'
            324_0  COME_FROM           266  '266'

 L. 303       324  LOAD_FAST                'merging_method_'
              326  LOAD_STR                 'nd-folding'
              328  COMPARE_OP               ==
          330_332  POP_JUMP_IF_FALSE   404  'to 404'

 L. 304       334  LOAD_GLOBAL              numpy
              336  LOAD_METHOD              vstack
              338  LOAD_FAST                'sd1'
              340  LOAD_FAST                'sd2'
              342  BUILD_TUPLE_2         2 
              344  CALL_METHOD_1         1  '1 positional argument'
              346  LOAD_CONST               None
              348  LOAD_CONST               None
              350  BUILD_SLICE_2         2 
              352  LOAD_CONST               None
              354  LOAD_CONST               3
              356  BUILD_SLICE_2         2 
              358  BUILD_TUPLE_2         2 
              360  BINARY_SUBSCR    
              362  STORE_FAST               'sub_data'

 L. 305       364  LOAD_GLOBAL              batch_folding_test_with_MPA
              366  LOAD_FAST                'sub_data'
              368  LOAD_CONST               True
              370  CALL_FUNCTION_2       2  '2 positional arguments'
              372  UNPACK_SEQUENCE_4     4 
              374  STORE_FAST               'unimodal'
              376  STORE_FAST               'p_value'
              378  STORE_FAST               'phi'
              380  STORE_FAST               '_'

 L. 306       382  LOAD_FAST                'unimodal'
          384_386  POP_JUMP_IF_FALSE   394  'to 394'

 L. 307       388  LOAD_FAST                'p_value'
              390  STORE_FAST               'dist'
              392  JUMP_FORWARD        712  'to 712'
            394_0  COME_FROM           384  '384'

 L. 309       394  LOAD_GLOBAL              numpy
              396  LOAD_ATTR                inf
              398  STORE_FAST               'dist'
          400_402  JUMP_FORWARD        712  'to 712'
            404_0  COME_FROM           330  '330'

 L. 310       404  LOAD_FAST                'merging_method_'
              406  LOAD_STR                 'dip'
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   474  'to 474'

 L. 311       414  LOAD_GLOBAL              numpy
              416  LOAD_METHOD              concatenate
              418  LOAD_FAST                'pr_1'
              420  LOAD_FAST                'pr_2'
              422  BUILD_LIST_2          2 
              424  CALL_METHOD_1         1  '1 positional argument'
              426  STORE_FAST               'sub_data'

 L. 312       428  LOAD_GLOBAL              len
              430  LOAD_FAST                'sub_data'
              432  CALL_FUNCTION_1       1  '1 positional argument'
              434  LOAD_CONST               5
              436  COMPARE_OP               >
          438_440  POP_JUMP_IF_FALSE   466  'to 466'

 L. 313       442  LOAD_GLOBAL              dip
              444  LOAD_FAST                'sub_data'
              446  CALL_FUNCTION_1       1  '1 positional argument'
              448  LOAD_GLOBAL              dip_threshold
              450  LOAD_GLOBAL              len
              452  LOAD_FAST                'sub_data'
              454  CALL_FUNCTION_1       1  '1 positional argument'
              456  LOAD_FAST                'merging_param_'
              458  CALL_FUNCTION_2       2  '2 positional arguments'
              460  BINARY_TRUE_DIVIDE
              462  STORE_FAST               'dist'
              464  JUMP_FORWARD        472  'to 472'
            466_0  COME_FROM           438  '438'

 L. 315       466  LOAD_GLOBAL              numpy
              468  LOAD_ATTR                inf
              470  STORE_FAST               'dist'
            472_0  COME_FROM           464  '464'
              472  JUMP_FORWARD        712  'to 712'
            474_0  COME_FROM           410  '410'

 L. 316       474  LOAD_FAST                'merging_method_'
              476  LOAD_STR                 'distance'
              478  COMPARE_OP               ==
          480_482  POP_JUMP_IF_FALSE   584  'to 584'

 L. 317       484  LOAD_GLOBAL              numpy
              486  LOAD_METHOD              median
              488  LOAD_FAST                'pr_1'
              490  CALL_METHOD_1         1  '1 positional argument'
              492  STORE_FAST               'med1'

 L. 318       494  LOAD_GLOBAL              numpy
              496  LOAD_METHOD              median
              498  LOAD_FAST                'pr_2'
              500  CALL_METHOD_1         1  '1 positional argument'
              502  STORE_FAST               'med2'

 L. 319       504  LOAD_GLOBAL              numpy
              506  LOAD_METHOD              median
              508  LOAD_GLOBAL              numpy
              510  LOAD_METHOD              abs
              512  LOAD_FAST                'pr_1'
              514  LOAD_FAST                'med1'
              516  BINARY_SUBTRACT  
              518  CALL_METHOD_1         1  '1 positional argument'
              520  CALL_METHOD_1         1  '1 positional argument'
              522  LOAD_CONST               2
              524  BINARY_POWER     
              526  STORE_FAST               'mad1'

 L. 320       528  LOAD_GLOBAL              numpy
              530  LOAD_METHOD              median
              532  LOAD_GLOBAL              numpy
              534  LOAD_METHOD              abs
              536  LOAD_FAST                'pr_2'
              538  LOAD_FAST                'med2'
              540  BINARY_SUBTRACT  
              542  CALL_METHOD_1         1  '1 positional argument'
              544  CALL_METHOD_1         1  '1 positional argument'
              546  LOAD_CONST               2
              548  BINARY_POWER     
              550  STORE_FAST               'mad2'

 L. 321       552  LOAD_FAST                'mad1'
              554  LOAD_FAST                'mad2'
              556  BINARY_ADD       
              558  STORE_FAST               'norm'

 L. 322       560  LOAD_GLOBAL              numpy
              562  LOAD_METHOD              sqrt
              564  LOAD_FAST                'med1'
              566  LOAD_FAST                'med2'
              568  BINARY_SUBTRACT  
              570  LOAD_CONST               2
              572  BINARY_POWER     
              574  LOAD_FAST                'norm'
              576  BINARY_TRUE_DIVIDE
              578  CALL_METHOD_1         1  '1 positional argument'
              580  STORE_FAST               'dist'
              582  JUMP_FORWARD        712  'to 712'
            584_0  COME_FROM           480  '480'

 L. 323       584  LOAD_FAST                'merging_method_'
              586  LOAD_STR                 'bhatta'
              588  COMPARE_OP               ==
          590_592  POP_JUMP_IF_FALSE   640  'to 640'

 L. 324       594  SETUP_EXCEPT        610  'to 610'

 L. 325       596  LOAD_GLOBAL              bhatta_dist
              598  LOAD_FAST                'pr_1'
              600  LOAD_FAST                'pr_2'
              602  CALL_FUNCTION_2       2  '2 positional arguments'
              604  STORE_FAST               'dist'
              606  POP_BLOCK        
              608  JUMP_FORWARD        638  'to 638'
            610_0  COME_FROM_EXCEPT    594  '594'

 L. 326       610  DUP_TOP          
              612  LOAD_GLOBAL              Exception
              614  COMPARE_OP               exception-match
          616_618  POP_JUMP_IF_FALSE   636  'to 636'
              620  POP_TOP          
              622  POP_TOP          
              624  POP_TOP          

 L. 327       626  LOAD_GLOBAL              numpy
              628  LOAD_ATTR                inf
              630  STORE_FAST               'dist'
              632  POP_EXCEPT       
              634  JUMP_FORWARD        638  'to 638'
            636_0  COME_FROM           616  '616'
              636  END_FINALLY      
            638_0  COME_FROM           634  '634'
            638_1  COME_FROM           608  '608'
              638  JUMP_FORWARD        712  'to 712'
            640_0  COME_FROM           590  '590'

 L. 328       640  LOAD_FAST                'merging_method_'
              642  LOAD_STR                 'nd-bhatta'
              644  COMPARE_OP               ==
          646_648  POP_JUMP_IF_FALSE   700  'to 700'

 L. 329       650  SETUP_EXCEPT        670  'to 670'

 L. 330       652  LOAD_GLOBAL              nd_bhatta_dist
              654  LOAD_FAST                'sd1'
              656  LOAD_ATTR                T
              658  LOAD_FAST                'sd2'
              660  LOAD_ATTR                T
              662  CALL_FUNCTION_2       2  '2 positional arguments'
              664  STORE_FAST               'dist'
              666  POP_BLOCK        
              668  JUMP_FORWARD        698  'to 698'
            670_0  COME_FROM_EXCEPT    650  '650'

 L. 331       670  DUP_TOP          
              672  LOAD_GLOBAL              Exception
              674  COMPARE_OP               exception-match
          676_678  POP_JUMP_IF_FALSE   696  'to 696'
              680  POP_TOP          
              682  POP_TOP          
              684  POP_TOP          

 L. 332       686  LOAD_GLOBAL              numpy
              688  LOAD_ATTR                inf
              690  STORE_FAST               'dist'
              692  POP_EXCEPT       
              694  JUMP_FORWARD        698  'to 698'
            696_0  COME_FROM           676  '676'
              696  END_FINALLY      
            698_0  COME_FROM           694  '694'
            698_1  COME_FROM           668  '668'
              698  JUMP_FORWARD        712  'to 712'
            700_0  COME_FROM           646  '646'

 L. 334       700  LOAD_GLOBAL              ValueError
            702_0  COME_FROM           392  '392'
            702_1  COME_FROM           312  '312'
              702  LOAD_STR                 'unexpected value: %s'
              704  LOAD_DEREF               'merging_method'
              706  BINARY_MODULO    
              708  CALL_FUNCTION_1       1  '1 positional argument'
              710  RAISE_VARARGS_1       1  'exception instance'
            712_0  COME_FROM           698  '698'
            712_1  COME_FROM           638  '638'
            712_2  COME_FROM           582  '582'
            712_3  COME_FROM           472  '472'
            712_4  COME_FROM           400  '400'
            712_5  COME_FROM           320  '320'

 L. 336       712  LOAD_FAST                'dist'
              714  LOAD_FAST                'dmin_'
              716  COMPARE_OP               <
              718  POP_JUMP_IF_FALSE   154  'to 154'

 L. 337       720  LOAD_FAST                'dist'
              722  STORE_FAST               'dmin_'

 L. 338       724  LOAD_FAST                'ic1'
              726  LOAD_FAST                'ic2'
              728  BUILD_LIST_2          2 
              730  STORE_FAST               'to_merge'
              732  JUMP_BACK           154  'to 154'
              734  POP_BLOCK        
            736_0  COME_FROM_LOOP      132  '132'
              736  JUMP_BACK            62  'to 62'
              738  POP_BLOCK        
            740_0  COME_FROM_LOOP       46  '46'

 L. 340       740  LOAD_FAST                'merging_method_'
              742  LOAD_STR                 'dip'
              744  COMPARE_OP               ==
          746_748  POP_JUMP_IF_FALSE   756  'to 756'

 L. 341       750  LOAD_CONST               1
              752  STORE_FAST               'thr_'
              754  JUMP_FORWARD        804  'to 804'
            756_0  COME_FROM           746  '746'

 L. 342       756  LOAD_FAST                'merging_method_'
              758  LOAD_CONST               ('folding', 'nd-folding', 'bhatta', 'nd-bhatta')
              760  COMPARE_OP               in
          762_764  POP_JUMP_IF_FALSE   772  'to 772'

 L. 343       766  LOAD_FAST                'merging_param_'
              768  STORE_FAST               'thr_'
              770  JUMP_FORWARD        804  'to 804'
            772_0  COME_FROM           762  '762'

 L. 344       772  LOAD_FAST                'merging_method_'
              774  LOAD_STR                 'distance'
              776  COMPARE_OP               ==
          778_780  POP_JUMP_IF_FALSE   792  'to 792'

 L. 345       782  LOAD_FAST                'merging_param_'
              784  LOAD_CONST               0.674
              786  BINARY_TRUE_DIVIDE
              788  STORE_FAST               'thr_'
              790  JUMP_FORWARD        804  'to 804'
            792_0  COME_FROM           778  '778'

 L. 347       792  LOAD_GLOBAL              ValueError
              794  LOAD_STR                 'unexpected value: %s'
              796  LOAD_FAST                'merging_method_'
              798  BINARY_MODULO    
              800  CALL_FUNCTION_1       1  '1 positional argument'
              802  RAISE_VARARGS_1       1  'exception instance'
            804_0  COME_FROM           790  '790'
            804_1  COME_FROM           770  '770'
            804_2  COME_FROM           754  '754'

 L. 349       804  LOAD_FAST                'dmin_'
              806  LOAD_FAST                'thr_'
              808  COMPARE_OP               <
          810_812  POP_JUMP_IF_FALSE   886  'to 886'

 L. 350       814  LOAD_FAST                'to_merge'
              816  UNPACK_SEQUENCE_2     2 
              818  STORE_FAST               'ic1'
              820  STORE_FAST               'ic2'

 L. 351       822  LOAD_FAST                'clusters_'
              824  LOAD_FAST                'ic1'
              826  BINARY_SUBSCR    
              828  LOAD_FAST                'clusters_'
              830  LOAD_FAST                'ic2'
              832  BINARY_SUBSCR    
              834  ROT_TWO          
              836  STORE_FAST               'c1'
              838  STORE_FAST               'c2'

 L. 352       840  LOAD_GLOBAL              numpy
              842  LOAD_METHOD              where
              844  LOAD_FAST                'groups_'
              846  LOAD_FAST                'c2'
              848  COMPARE_OP               ==
              850  CALL_METHOD_1         1  '1 positional argument'
              852  LOAD_CONST               0
              854  BINARY_SUBSCR    
              856  STORE_FAST               'selection'

 L. 353       858  LOAD_FAST                'c1'
              860  LOAD_FAST                'groups_'
              862  LOAD_FAST                'selection'
              864  STORE_SUBSCR     

 L. 354       866  LOAD_FAST                'c1'
              868  LOAD_FAST                'c2'
              870  BUILD_TUPLE_2         2 
              872  STORE_FAST               'merge_'

 L. 355       874  LOAD_CONST               True
              876  LOAD_FAST                'groups_'
              878  LOAD_FAST                'merge_'
              880  LOAD_FAST                'dmin_'
              882  BUILD_TUPLE_4         4 
              884  RETURN_VALUE     
            886_0  COME_FROM           810  '810'

 L. 357       886  LOAD_CONST               False
              888  LOAD_FAST                'groups_'
              890  LOAD_CONST               None
              892  LOAD_CONST               None
              894  BUILD_TUPLE_4         4 
              896  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 702_0

    has_been_merged = True
    mask = numpy.where(groups > -1)[0]
    clusters = numpy.unique(groups[mask])
    merged = [len(clusters), 0]
    if merging_method == 'dip':
        thr = 1
    else:
        if merging_method in ('folding', 'nd-folding', 'bhatta', 'nd-bhatta'):
            thr = merging_param
        else:
            if merging_method == 'distance':
                thr = merging_param / 0.674
            else:
                raise ValueError('unexpected value: %s' % merging_method)
    merge_history = {'merge':[],  'distance':[],  'method':merging_method, 
     'threshold':thr}
    while has_been_merged:
        has_been_merged, groups, merge, dmin = perform_merging(groups, merging_method, merging_param, data)
        if has_been_merged:
            merged[1] += 1
            merge_history['merge'].append(merge)
            merge_history['distance'].append(dmin)

    return (
     groups, merged, merge_history)


def slice_templates(params, to_remove=None, to_merge=None, extension='', input_extension=''):
    """Slice templates in HDF5 file.

    Arguments:
        params
        to_remove: none | list (optional)
            An array of template indices to remove.
            The default value is None.
        to_merge: none | list | numpy.ndarray (optional)
            An array of pair of template indices to merge
            (i.e. shape = (nb_merges, 2)).
            The default value is None.
        extension: string (optional)
            The extension to use as output.
            The default value is ''.
        input_extension: string (optional)
            The extension to use as input.
            The default value is ''.
    """
    if to_remove is None:
        to_remove = []
    else:
        if to_merge is None:
            to_merge = []
        file_out_suff = params.get('data', 'file_out_suff')
        data_file = params.data_file
        n_e = params.getint('data', 'N_e')
        n_total = params.nb_channels
        hdf5_compress = params.getboolean('data', 'hdf5_compress')
        n_t = params.getint('detection', 'N_t')
        template_shift = params.getint('detection', 'template_shift')
        has_support = test_if_support(params, input_extension)
        has_purity = test_if_purity(params, input_extension)
        fine_amplitude = params.getboolean('clustering', 'fine_amplitude')
        if comm.rank == 0:
            print_and_log(['Node 0 is slicing templates'], 'debug', logger)
            old_templates = load_data(params, 'templates', extension=input_extension)
            old_limits = load_data(params, 'limits', extension=input_extension)
            if has_support:
                old_supports = load_data(params, 'supports', extension=input_extension)
            else:
                old_supports = None
            if has_purity:
                old_purity = load_data(params, 'purity', extension=input_extension)
            else:
                old_purity = None
            _, n_tm = old_templates.shape
            norm_templates = load_data(params, 'norm-templates', extension=input_extension)
            to_delete = list(to_remove)
            if len(to_merge) > 0:
                for count in range(len(to_merge)):
                    remove = to_merge[count][1]
                    to_delete += [remove]

            else:
                all_templates = set(numpy.arange(n_tm // 2))
                to_keep = numpy.array(list(all_templates.difference(to_delete)))
                positions = numpy.arange(len(to_keep))
                local_keep = to_keep[positions]
                templates = scipy.sparse.lil_matrix((n_e * n_t, 2 * len(to_keep)), dtype=(numpy.float32))
                hfilename = file_out_suff + '.templates{}.hdf5'.format('-new')
                hfile = h5py.File(hfilename, 'w', libver='earliest')
                norms = hfile.create_dataset('norms', shape=(2 * len(to_keep),), dtype=(numpy.float32), chunks=True)
                limits = hfile.create_dataset('limits', shape=(len(to_keep), 2), dtype=(numpy.float32), chunks=True)
                if has_support:
                    supports = hfile.create_dataset('supports', shape=(len(to_keep), n_e), dtype=(numpy.bool), chunks=True)
                else:
                    supports = None
                if has_purity:
                    purity = hfile.create_dataset('purity', shape=(len(to_keep),), dtype=(numpy.float32), chunks=True)
                else:
                    purity = None
            for count, keep in zip(positions, local_keep):
                templates[:, count] = old_templates[:, keep]
                templates[:, count + len(to_keep)] = old_templates[:, keep + n_tm // 2]
                norms[count] = norm_templates[keep]
                norms[count + len(to_keep)] = norm_templates[(keep + n_tm // 2)]
                if has_support:
                    supports[count] = old_supports[keep]
                if len(to_merge) == 0:
                    new_limits = old_limits[keep]
                    if has_purity:
                        new_purity = old_purity[keep]
                else:
                    subset = numpy.where(to_merge[:, 0] == keep)[0]
                if len(subset) > 0:
                    idx = numpy.unique(to_merge[subset].flatten())
                    ratios = norm_templates[idx] / norm_templates[keep]
                    new_limits = [
                     numpy.min(ratios * old_limits[idx][:, 0]),
                     numpy.max(ratios * old_limits[idx][:, 1])]
                    if has_purity:
                        new_purity = numpy.mean(old_purity[idx])
                    else:
                        new_limits = old_limits[keep]
                        if has_purity:
                            new_purity = old_purity[keep]
                        if not fine_amplitude:
                            limits[count] = new_limits
                        else:
                            limits[count] = [
                             0.5, 1.5]
                    if has_purity:
                        purity[count] = new_purity

            templates = templates.tocoo()
            if hdf5_compress:
                hfile.create_dataset('temp_x', data=(templates.row), compression='gzip')
                hfile.create_dataset('temp_y', data=(templates.col), compression='gzip')
                hfile.create_dataset('temp_data', data=(templates.data), compression='gzip')
            else:
                hfile.create_dataset('temp_x', data=(templates.row))
                hfile.create_dataset('temp_y', data=(templates.col))
                hfile.create_dataset('temp_data', data=(templates.data))
            hfile.create_dataset('temp_shape', data=numpy.array([n_e, n_t, 2 * len(to_keep)], dtype=(numpy.int32)))
            hfile.close()
            temporary_path = hfilename
            output_path = file_out_suff + '.templates{}.hdf5'.format(extension)
            if os.path.exists(output_path):
                os.remove(output_path)
            shutil.move(temporary_path, output_path)
        else:
            to_keep = numpy.array([])
    return to_keep


def slice_clusters(params, result, to_remove=None, to_merge=None, extension='', input_extension='', light=False, method='safe'):
    """Slice clusters in HDF5 templates.

    Arguments:
        params
        result
        to_remove: none | list (optional)
        to_merge: none | list | numpy.ndarray (optional)
        extension: string (optional)
            The default value is ''.
        input_extension: string (optional)
            The default value is ''.
        light: boolean (optional)
        method: string (optional)
    """
    if to_remove is None:
        to_remove = []
    if to_merge is None:
        to_merge = []
    file_out_suff = params.get('data', 'file_out_suff')
    data_file = params.data_file
    n_e = params.getint('data', 'N_e')
    n_total = params.nb_channels
    hdf5_compress = params.getboolean('data', 'hdf5_compress')
    n_t = params.getint('detection', 'N_t')
    template_shift = params.getint('detection', 'template_shift')
    debug = params.getboolean('clustering', 'debug')
    if comm.rank == 0:
        print_and_log(['Node 0 is slicing clusters'], 'debug', logger)
        old_templates = load_data(params, 'templates', extension=input_extension)
        _, n_tm = old_templates.shape
        to_delete = list(to_remove)
        if len(to_merge) > 0:
            for count in range(len(to_merge)):
                remove = to_merge[count][1]
                to_delete += [remove]

        else:
            all_templates = set(numpy.arange(n_tm // 2))
            to_keep = numpy.array(list(all_templates.difference(to_delete)))
            all_elements = [[] for _ in range(n_e)]
            for target in numpy.unique(to_delete):
                elec = result['electrodes'][target]
                nic = target - numpy.where(result['electrodes'] == elec)[0][0]
                mask = result[('clusters_' + str(elec))] > -1
                tmp = numpy.unique(result[('clusters_' + str(elec))][mask])
                all_elements[elec] += list(numpy.where(result[('clusters_' + str(elec))] == tmp[nic])[0])

            myfilename = file_out_suff + '.clusters{}.hdf5'.format(input_extension)
            myfile = h5py.File(myfilename, 'r', libver='earliest')
            for elec in range(n_e):
                if not light:
                    result['data_' + str(elec)] = numpy.delete((result[('data_' + str(elec))]), (all_elements[elec]), axis=0)
                    result['clusters_' + str(elec)] = numpy.delete(result[('clusters_' + str(elec))], all_elements[elec])
                    result['times_' + str(elec)] = numpy.delete(result[('times_' + str(elec))], all_elements[elec])
                    result['peaks_' + str(elec)] = numpy.delete(result[('peaks_' + str(elec))], all_elements[elec])
                    if debug:
                        result['rho_' + str(elec)] = numpy.delete(result[('rho_' + str(elec))], all_elements[elec])
                        result['delta_' + str(elec)] = numpy.delete(result[('delta_' + str(elec))], all_elements[elec])
                    else:
                        result['clusters_' + str(elec)] = numpy.delete(result[('clusters_' + str(elec))], all_elements[elec])
                        data = myfile.get('data_' + str(elec))[:]
                        result['data_' + str(elec)] = numpy.delete(data, (all_elements[elec]), axis=0)
                        data = myfile.get('times_' + str(elec))[:]
                        result['times_' + str(elec)] = numpy.delete(data, all_elements[elec])
                        data = myfile.get('peaks_' + str(elec))[:]
                        result['peaks_' + str(elec)] = numpy.delete(data, all_elements[elec])
                        data = myfile.get('noise_times_' + str(elec))[:]
                        result['noise_times_' + str(elec)] = data
                        if debug:
                            data = myfile.get('rho_' + str(elec))[:]
                            result['rho_' + str(elec)] = numpy.delete(data, all_elements[elec])
                            data = myfile.get('delta_' + str(elec))[:]
                            result['delta_' + str(elec)] = numpy.delete(data, all_elements[elec])

            myfile.close()
            if method == 'safe':
                result['electrodes'] = numpy.delete(result['electrodes'], numpy.unique(to_delete))
            else:
                if method == 'new':
                    result['electrodes'] = result['electrodes'][to_keep]
                else:
                    raise ValueError('Unexpected method value: {}'.format(method))
        cfilename = file_out_suff + '.clusters{}.hdf5'.format('-new')
        cfile = h5py.File(cfilename, 'w', libver='earliest')
        to_write = ['data_', 'clusters_', 'times_', 'peaks_', 'noise_times_']
        if debug:
            to_write += ['rho_', 'delta_']
        for ielec in range(n_e):
            write_datasets(cfile, to_write, result, ielec, compression=hdf5_compress)

        write_datasets(cfile, ['electrodes'], result)
        cfile.close()
        temporary_path = cfilename
        output_path = file_out_suff + '.clusters{}.hdf5'.format(extension)
        if os.path.exists(output_path):
            os.remove(output_path)
        shutil.move(temporary_path, output_path)


def slice_result(result, times):
    sub_results = []
    for t in times:
        sub_result = {'spiketimes':{},  'amplitudes':{}}
        for key in list(result['spiketimes'].keys()):
            spike_times = result['spiketimes'][key]
            spike_times = spike_times.ravel()
            amplitudes = result['amplitudes'][key]
            amplitudes = amplitudes.ravel()
            indices = numpy.where((spike_times >= t[0]) & (spike_times <= t[1]))[0]
            sub_result['spiketimes'][key] = spike_times[indices] - t[0]
            sub_result['amplitudes'][key] = amplitudes[indices]

        sub_results += [sub_result]

    return sub_results


def merging_cc(params, nb_cpu, nb_gpu, use_gpu):

    def remove(result_, distances_, cc_merge_):
        do_merge = True
        to_merge_ = numpy.zeros((0, 2), dtype=(numpy.int32))
        g_idx = list(range(len(distances_)))
        while do_merge:
            dmax = distances_.max()
            idx_ = numpy.where(distances_ == dmax)
            one_merge = [idx_[0][0], idx_[1][0]]
            do_merge = dmax >= cc_merge_
            if do_merge:
                elec_ic1 = result_['electrodes'][one_merge[0]]
                elec_ic2 = result_['electrodes'][one_merge[1]]
                nic1 = one_merge[0] - numpy.where(result_['electrodes'] == elec_ic1)[0][0]
                nic2 = one_merge[1] - numpy.where(result_['electrodes'] == elec_ic2)[0][0]
                mask1 = result_[('clusters_' + str(elec_ic1))] > -1
                mask2 = result_[('clusters_' + str(elec_ic2))] > -1
                tmp1 = numpy.unique(result_[('clusters_' + str(elec_ic1))][mask1])
                tmp2 = numpy.unique(result_[('clusters_' + str(elec_ic2))][mask2])
                elements1 = numpy.where(result_[('clusters_' + str(elec_ic1))] == tmp1[nic1])[0]
                elements2 = numpy.where(result_[('clusters_' + str(elec_ic2))] == tmp2[nic2])[0]
                if len(elements1) > len(elements2):
                    to_remove = one_merge[1]
                    to_keep = one_merge[0]
                    elec = elec_ic2
                    elements = elements2
                else:
                    to_remove = one_merge[0]
                    to_keep = one_merge[1]
                    elec = elec_ic1
                    elements = elements1
                result_['data_' + str(elec)] = numpy.delete((result_[('data_' + str(elec))]), elements, axis=0)
                result_['clusters_' + str(elec)] = numpy.delete(result_[('clusters_' + str(elec))], elements)
                result_['times_' + str(elec)] = numpy.delete(result_[('times_' + str(elec))], elements)
                result_['peaks_' + str(elec)] = numpy.delete(result_[('peaks_' + str(elec))], elements)
                result_['electrodes'] = numpy.delete(result_['electrodes'], to_remove)
                distances_ = numpy.delete(distances_, to_remove, axis=0)
                distances_ = numpy.delete(distances_, to_remove, axis=1)
                to_merge_ = numpy.vstack((to_merge_, numpy.array([g_idx[to_keep], g_idx[to_remove]])))
                g_idx.pop(to_remove)

        return (
         to_merge_, result_)

    data_file = params.data_file
    n_e = params.getint('data', 'N_e')
    n_total = params.nb_channels
    n_t = params.getint('detection', 'N_t')
    template_shift = params.getint('detection', 'template_shift')
    blosc_compress = params.getboolean('data', 'blosc_compress')
    n_tm = load_data(params, 'nb_templates')
    nb_temp = int(n_tm // 2)
    to_merge = []
    cc_merge = params.getfloat('clustering', 'cc_merge')
    norm = n_e * n_t
    decimation = params.getboolean('clustering', 'decimation')
    adapted_cc = params.getboolean('clustering', 'adapted_cc')
    adapted_thr = params.getint('clustering', 'adapted_thr')
    if cc_merge < 1:
        result = []
        overlap = get_overlaps(params,
          extension='-merging', erase=True, normalize=True, maxoverlap=False, verbose=False, half=True, use_gpu=use_gpu,
          nb_cpu=nb_cpu,
          nb_gpu=nb_gpu,
          decimation=decimation)
        overlap.close()
        filename = params.get('data', 'file_out_suff') + '.overlap-merging.hdf5'
        SHARED_MEMORY = get_shared_memory_flag(params)
        if not SHARED_MEMORY:
            over_x, over_y, over_data, over_shape = load_data(params,
              'overlaps-raw', extension='-merging')
        else:
            over_x, over_y, over_data, over_shape, mpi_memory = load_data_memshared(params,
              'overlaps-raw', extension='-merging', use_gpu=use_gpu, nb_cpu=nb_cpu, nb_gpu=nb_gpu)
        to_explore = numpy.arange(nb_temp)[comm.rank::comm.size]
        distances = numpy.zeros((len(to_explore), nb_temp), dtype=(numpy.float32))
        res = []
        for i in to_explore:
            res += [i * nb_temp + i + 1, (i + 1) * nb_temp]

        bounds = numpy.searchsorted(over_x, res, 'left')
        for count, i in enumerate(to_explore):
            xmin, xmax = bounds[2 * count:2 * (count + 1)]
            local_x = over_x[xmin:xmax] - (i * nb_temp + i + 1)
            local_y = over_y[xmin:xmax]
            local_data = over_data[xmin:xmax]
            data = scipy.sparse.csr_matrix((local_data, (local_x, local_y)), shape=(nb_temp - (i + 1), over_shape[1]), dtype=(numpy.float32))
            distances[count, i + 1:] = data.max(1).toarray().flatten()
            del local_x
            del local_y
            del local_data
            del data

        distances /= norm
        distances = gather_array(distances, comm, 0, 1, 'float32', compress=blosc_compress)
        if comm.rank == 0:
            indices = []
            for idx in range(comm.size):
                indices += list(numpy.arange(idx, nb_temp, comm.size))

            indices = numpy.argsort(indices)
            distances = distances[indices, :]
            distances = numpy.maximum(distances, distances.T)
        comm.Barrier()
        if comm.rank == 0:
            if adapted_cc:
                common_supports = load_data(params, 'common-supports')
                exponents = numpy.exp(-common_supports / adapted_thr)
                distances = distances ** exponents
            result = load_data(params, 'clusters')
            to_merge, result = remove(result, distances, cc_merge)
        to_merge = numpy.array(to_merge)
        to_merge = comm.bcast(to_merge, root=0)
        if len(to_merge) > 0:
            slice_templates(params, to_merge=to_merge)
            slice_clusters(params, result)
        comm.Barrier()
        del result
        del over_x
        del over_y
        del over_data
        if comm.rank == 0:
            os.remove(filename)
        if SHARED_MEMORY:
            for memory in mpi_memory:
                memory.Free()

    return [
     nb_temp, len(to_merge)]


def compute_error(good_values, bad_values, bounds):
    fn = numpy.sum((good_values < bounds[0]) | (good_values > bounds[1]))
    fp = numpy.sum((bounds[0] <= bad_values) & (bad_values <= bounds[1]))
    tp = numpy.sum((bounds[0] <= good_values) & (good_values <= bounds[1]))
    tn = numpy.sum((bad_values < bounds[0]) | (bad_values > bounds[1]))
    denom = (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)
    if denom > 0:
        mcc = 1 - (tp * tn - fp * fn) / numpy.sqrt(denom)
    else:
        mcc = 1
    return mcc


def score(x, good_values, bad_values):
    return compute_error(good_values, bad_values, x) + 0.01 * (2 - (x[1] - x[0])) ** 2


def refine_amplitudes(params, nb_cpu, nb_gpu, use_gpu, normalization=True, debug_plots=''):
    data_file = params.data_file
    template_shift = params.getint('detection', 'template_shift')
    norm_templates = load_data(params, 'norm-templates')
    best_elec = load_data(params, 'electrodes')
    limits = load_data(params, 'limits')
    fine_amplitude = params.getboolean('clustering', 'fine_amplitude')
    N_e = params.getint('data', 'N_e')
    N_t = params.getint('detection', 'N_t')
    n_total = params.nb_channels
    clusters = load_data(params, 'clusters-nodata')
    file_out_suff = params.get('data', 'file_out_suff')
    plot_path = os.path.join(params.get('data', 'file_out_suff'), 'plots')
    nodes, edges = get_nodes_and_edges(params)
    inv_nodes = numpy.zeros(n_total, dtype=(numpy.int32))
    inv_nodes[nodes] = numpy.arange(len(nodes))
    max_snippets = 250
    sparse_snippets = False
    max_noise_snippets = min(max_snippets, 10000 // N_e)
    SHARED_MEMORY = get_shared_memory_flag(params)
    if SHARED_MEMORY:
        templates, mpi_memory = load_data_memshared(params, 'templates', normalize=False)
    else:
        templates = load_data(params, 'templates')
    supports = load_data(params, 'supports')
    x, n_tm = templates.shape
    nb_temp = int(n_tm // 2)
    norm_templates = load_data(params, 'norm-templates')[:nb_temp]
    norm_templates *= numpy.sqrt(N_e * N_t)
    norm_2 = norm_templates ** 2
    indices = {}
    for i in range(N_e):
        labels = numpy.unique(clusters[('clusters_%d' % i)])
        labels = labels[(labels > -1)]
        indices[i] = list(labels)

    all_sizes = {}
    all_temp = numpy.arange(comm.rank, nb_temp, comm.size)
    all_elec = numpy.arange(comm.rank, N_e, comm.size)
    if comm.rank == 0:
        to_explore = get_tqdm_progressbar(params, all_temp)
    else:
        to_explore = all_temp
    clusters_info = {}
    all_snippets = {}
    for i in to_explore:
        ref_elec = best_elec[i]
        shank_nodes, _ = get_nodes_and_edges(params, shank_with=(nodes[ref_elec]))
        sindices = inv_nodes[shank_nodes]
        times = clusters[('times_%d' % ref_elec)]
        labels = clusters[('clusters_%d' % ref_elec)]
        peaks = clusters[('peaks_%d' % ref_elec)]
        position = numpy.where(best_elec[:i] == ref_elec)[0]
        tgt_label = indices[ref_elec][len(position)]
        idx = numpy.where(labels == tgt_label)[0]
        clusters_info[i] = {'electrode_nb':ref_elec, 
         'local_cluster_nb':tgt_label}
        if peaks[idx][0] == 0:
            p = 'pos'
        else:
            if peaks[idx][0] == 1:
                p = 'neg'
            else:
                raise ValueError('unexpected value {}'.format(peaks[idx][0]))
        idx_i = numpy.random.permutation(idx)[:max_snippets]
        times_i = times[idx_i]
        labels_i = labels[idx_i]
        snippets = get_stas(params, times_i, labels_i, ref_elec, neighs=sindices, nodes=nodes, pos=p)
        if sparse_snippets:
            snippets[:, ~supports[i], :] = 0
        nb_snippets, nb_electrodes, nb_times_steps = snippets.shape
        snippets = snippets.reshape(nb_snippets, nb_electrodes * nb_times_steps)
        if sparse_snippets:
            snippets = scipy.sparse.csr_matrix(snippets)
        for j in range(nb_temp):
            template = templates[:, j].toarray().ravel()
            data = snippets.dot(template).astype(numpy.float32)
            all_snippets[(j, i)] = data

        all_sizes[i] = snippets.shape[0]

    noise_amplitudes = {}
    for i in range(nb_temp):
        noise_amplitudes[i] = [
         numpy.zeros(0, dtype=(numpy.float32))]

    if comm.rank == 0:
        to_explore = get_tqdm_progressbar(params, all_elec)
    else:
        to_explore = all_elec
    for elec in to_explore:
        times = clusters[('noise_times_' + str(elec))]
        shank_nodes, _ = get_nodes_and_edges(params, shank_with=(nodes[elec]))
        sindices = inv_nodes[shank_nodes]
        idx = len(times)
        idx_i = numpy.random.permutation(idx)[:max_noise_snippets]
        times_i = times[idx_i]
        labels_i = numpy.zeros(idx)
        snippets = get_stas(params, times_i, labels_i, elec, neighs=sindices, nodes=nodes, auto_align=False)
        nb_snippets, nb_electrodes, nb_times_steps = snippets.shape
        snippets = snippets.reshape(nb_snippets, nb_electrodes * nb_times_steps)
        if sparse_snippets:
            snippets = scipy.sparse.csr_matrix(snippets)
        for j in range(nb_temp):
            template = templates[:, j].toarray().ravel()
            data = snippets.dot(template).astype(numpy.float32)
            noise_amplitudes[j].append(data)

    for i in range(nb_temp):
        amplitudes = numpy.concatenate(noise_amplitudes.pop(i))
        all_snippets[(i, 'noise')] = amplitudes

    for i in range(nb_temp):
        for j in range(nb_temp):
            if (
             i, j) not in all_snippets:
                all_snippets[(i, j)] = numpy.zeros(0, dtype=(numpy.float32))
            all_snippets[(i, j)] = all_gather_array((all_snippets[(i, j)]), comm, shape=0, dtype='float32')

        all_snippets[(i, 'noise')] = all_gather_array((all_snippets[(i, 'noise')]), comm, shape=0, dtype='float32')

    sps = {}
    nsps = {}
    amplitudes = {}
    for i in range(nb_temp):
        for j in range(nb_temp):
            sps[(i, j)] = all_snippets[(i, j)]
            nsps[(i, j)] = sps[(i, j)] / norm_templates[i]
            amplitudes[(i, j)] = sps[(i, j)] / norm_2[i]

        amplitudes[(i, 'noise')] = all_snippets[(i, 'noise')] / norm_2[i]

    del all_snippets
    purity_level = numpy.zeros((len(all_temp)), dtype=(numpy.float32))
    max_nb_chances = numpy.zeros((len(all_temp)), dtype=(numpy.float32))
    if fine_amplitude:
        bounds = numpy.zeros((len(all_temp), 2), dtype=(numpy.float32))
    for count, i in enumerate(all_temp):
        good_values = amplitudes[(i, i)]
        center = 1
        if normalization:
            tgt_values = nsps[(i, i)]
        else:
            tgt_values = sps[(i, i)]
        bad_values = {}
        neutral_values = {}
        nb_chances = numpy.zeros((all_sizes[i]), dtype=(numpy.int32))
        for j in range(nb_temp):
            if i != j:
                if normalization:
                    ref_values = nsps[(j, j)]
                    values = nsps[(i, j)]
                    ref2_values = nsps[(j, i)]
                else:
                    ref_values = sps[(j, j)]
                    values = sps[(i, j)]
                    ref2_values = sps[(j, i)]
                selection = ref_values <= values
                bad_values[j] = amplitudes[(i, j)][selection]
                selection = ref_values > values
                neutral_values[j] = amplitudes[(i, j)][selection]
                selection = tgt_values <= ref2_values
                nb_chances[selection] += 1

        bad_values['noise'] = amplitudes[(i, 'noise')]
        all_bad_values = numpy.concatenate([values for values in list(bad_values.values())])
        all_neutral_values = numpy.concatenate([values for values in list(neutral_values.values())])
        very_good_values = good_values
        if fine_amplitude:
            res = scipy.optimize.differential_evolution(score, bounds=[(0, 1), (1, 2)], args=(very_good_values, all_bad_values))
            a_min, a_max = res.x
            bounds[count] = [a_min, a_max]
        else:
            a_min, a_max = limits[i]
        error = compute_error(very_good_values, all_bad_values, [a_min, a_max])
        purity_level[count] = min(1, 1 - error)
        mask = (a_min <= good_values) & (good_values <= a_max)
        if numpy.sum(mask) > 0:
            max_nb_chances[count] = numpy.median(nb_chances[mask])
        else:
            max_nb_chances[count] = numpy.nan
        if debug_plots not in ('None', ''):
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(2)
            s = 4
            linewidth = 0.3
            ax[0].axhline(y=0.0, color='gray', linewidth=linewidth)
            ax[0].axhline(y=a_min, color='tab:blue', linewidth=linewidth)
            ax[0].axhline(y=center, color='gray', linewidth=linewidth)
            ax[0].axhline(y=a_max, color='tab:blue', linewidth=linewidth)
            x = numpy.random.uniform(size=(all_neutral_values.size))
            y = all_neutral_values
            color = 'gray'
            ax[0].scatter(x, y, s=s, color=color, alpha=0.1)
            x1 = numpy.random.uniform(size=(good_values.size))
            y = good_values
            color = 'tab:green'
            ax[0].scatter(x1, y, s=s, color=color)
            color = 'tab:green'
            for x_, y_ in zip(x1, y):
                if y_ > a_max:
                    ax[0].plot([x_, x_], [a_max, y_], color=color, linewidth=0.3)
                if y_ < a_min:
                    ax[0].plot([x_, x_], [a_min, y_], color=color, linewidth=0.3)

            x2 = numpy.random.uniform(size=(all_bad_values.size))
            y = all_bad_values
            color = 'tab:red'
            ax[0].scatter(x2, y, s=s, color=color)
            color = 'tab:red'
            for x_, y_ in zip(x2, y):
                if center < y_ < a_max:
                    ax[0].plot([x_, x_], [a_max, y_], color=color, linewidth=0.3)
                if a_min < y_ < center:
                    ax[0].plot([x_, x_], [a_min, y_], color=color, linewidth=0.3)

            ax[0].spines['right'].set_visible(False)
            ax[0].spines['top'].set_visible(False)
            ax[0].set_ylabel('amplitude')
            ax[0].set_xticks([])
            ax[0].set_title('%g good / %g bad / %g error' % (len(good_values), len(all_bad_values), error))
            ax[1].axhline(y=0.0, color='gray', linewidth=linewidth)
            ax[1].axhline(y=a_min, color='tab:blue', linewidth=linewidth)
            ax[1].axhline(y=center, color='gray', linewidth=linewidth)
            ax[1].axhline(y=a_max, color='tab:blue', linewidth=linewidth)
            y = good_values
            r = ax[1].scatter(x1, y, s=s, c=nb_chances)
            fig.colorbar(r, ax=(ax[1]))
            ax[1].spines['right'].set_visible(False)
            ax[1].spines['top'].set_visible(False)
            ax[1].set_title('Average nb_chances %g' % numpy.mean(nb_chances))
            ax[1].set_ylabel('amplitude')
            ax[1].set_xticks([])
            plt.tight_layout()
            output_path = os.path.join(plot_path, 'amplitude_interval_t{}_e{}_c{}.{}'.format(i, clusters_info[i]['electrode_nb'], clusters_info[i]['local_cluster_nb'], debug_plots))
            fig.savefig(output_path)
            plt.close(fig)

    comm.Barrier()
    if fine_amplitude:
        bounds = gather_array(bounds, comm, shape=1)
    purity_level = gather_array(purity_level, comm)
    max_nb_chances = gather_array(max_nb_chances, comm)
    if SHARED_MEMORY:
        for memory in mpi_memory:
            memory.Free()

    if comm.rank == 0:
        file_name = file_out_suff + '.templates.hdf5'
        hfile = h5py.File(file_name, 'r+', libver='earliest')
        indices = []
        for idx in range(comm.size):
            indices += list(numpy.arange(idx, nb_temp, comm.size))

        indices = numpy.argsort(indices)
        if fine_amplitude:
            hfile['limits'][:] = bounds[indices]
        if 'purity' not in list(hfile.keys()):
            hfile.create_dataset('purity', data=(purity_level[indices]))
            hfile.create_dataset('nb_chances', data=(max_nb_chances[indices]))
        else:
            hfile['purity'][:] = purity_level[indices]
            hfile['nb_chances'][:] = max_nb_chances[indices]
        hfile.close()


def delete_mixtures(params, nb_cpu, nb_gpu, use_gpu):
    data_file = params.data_file
    n_e = params.getint('data', 'N_e')
    n_total = params.nb_channels
    n_t = params.getint('detection', 'N_t')
    template_shift = params.getint('detection', 'template_shift')
    cc_merge = params.getfloat('clustering', 'cc_merge')
    mixtures = []
    norm = n_e * n_t
    filename = params.get('data', 'file_out_suff') + '.overlap-mixtures.hdf5'
    norm_templates = load_data(params, 'norm-templates')
    best_elec = load_data(params, 'electrodes')
    limits = load_data(params, 'limits')
    nodes, edges = get_nodes_and_edges(params)
    inv_nodes = numpy.zeros(n_total, dtype=(numpy.int32))
    inv_nodes[nodes] = numpy.arange(len(nodes))
    has_support = test_if_support(params, '')
    adapted_cc = params.getboolean('clustering', 'adapted_cc')
    adapted_thr = params.getint('clustering', 'adapted_thr')
    overlap = get_overlaps(params,
      extension='-mixtures', erase=True, normalize=True, maxoverlap=False, verbose=False, half=True, use_gpu=use_gpu,
      nb_cpu=nb_cpu,
      nb_gpu=nb_gpu,
      decimation=False)
    overlap.close()
    SHARED_MEMORY = get_shared_memory_flag(params)
    if SHARED_MEMORY:
        c_overs, mpi_memory_1 = load_data_memshared(params,
          'overlaps', extension='-mixtures', use_gpu=use_gpu, nb_cpu=nb_cpu, nb_gpu=nb_gpu)
    else:
        c_overs = load_data(params,
          'overlaps', extension='-mixtures')
    if SHARED_MEMORY:
        templates, mpi_memory_2 = load_data_memshared(params, 'templates', normalize=True)
    else:
        templates = load_data(params, 'templates')
    x, n_tm = templates.shape
    nb_temp = int(n_tm // 2)
    offset = n_t - 1
    if has_support:
        supports = load_data(params, 'supports')
    else:
        supports = {}
        supports = numpy.zeros((nb_temp, n_e), dtype=(numpy.bool))
        for t in range(nb_temp):
            elecs = numpy.take(inv_nodes, edges[nodes[best_elec[t]]])
            supports[(t, elecs)] = True

    overlap_0 = numpy.zeros(nb_temp, dtype=(numpy.float32))
    distances = numpy.zeros((nb_temp, nb_temp), dtype=(numpy.int32))
    if adapted_cc:
        common_supports = load_data(params, 'common-supports')
        exponents = numpy.exp(-common_supports / adapted_thr)
    for i in range(nb_temp - 1):
        data = c_overs[i].toarray()
        distances[i, i + 1:] = numpy.argmax(data[i + 1:, :], 1)
        distances[i + 1:, i] = distances[i, i + 1:]
        overlap_0[i] = data[(i, n_t - 1)]

    all_temp = numpy.arange(comm.rank, nb_temp, comm.size)
    sorted_temp = numpy.argsort(norm_templates[:nb_temp])[::-1]
    M = numpy.zeros((2, 2), dtype=(numpy.float32))
    V = numpy.zeros((2, 1), dtype=(numpy.float32))
    to_explore = list(range(comm.rank, nb_temp, comm.size))
    if comm.rank == 0:
        to_explore = get_tqdm_progressbar(params, to_explore)
    for count, k in enumerate(to_explore):
        k = sorted_temp[k]
        overlap_k = c_overs[k]
        electrodes = numpy.where(supports[k])[0]
        candidates = {}
        for t1 in range(nb_temp):
            candidates[t1] = []
            masks = numpy.logical_or(supports[t1], supports[t1:])
            masks = numpy.all(masks[:, electrodes], 1)
            if t1 != k:
                for count, t2 in enumerate(range(t1, nb_temp)):
                    is_candidate = masks[count]
                    if is_candidate and t2 != k and t2 != t1:
                        candidates[t1] += [t2]

        been_found = False
        t_k = None
        for i in list(candidates.keys()):
            t_i = None
            if been_found or len(candidates[i]) > 0:
                overlap_i = c_overs[i]
                M[(0, 0)] = overlap_0[i]
                V[(0, 0)] = overlap_k[(i, distances[(k, i)])]
                for j in candidates[i]:
                    t_j = None
                    value = (distances[(k, i)] - distances[(k, j)]) // 2 + offset
                    M[(1, 1)] = overlap_0[j]
                    M[(1, 0)] = overlap_i[(j, value)]
                    M[(0, 1)] = M[(1, 0)]
                    V[(1, 0)] = overlap_k[(j, distances[(k, j)])]
                    try:
                        a1, a2 = numpy.dot(scipy.linalg.inv(M), V)
                    except Exception:
                        a1, a2 = [
                         0, 0]

                    a1_lim = limits[i]
                    a2_lim = limits[j]
                    is_a1 = a1_lim[0] <= a1 and a1 <= a1_lim[1]
                    is_a2 = a2_lim[0] <= a2 and a2 <= a2_lim[1]
                    if is_a1:
                        if is_a2:
                            if t_k is None:
                                t_k = templates[:, k].toarray().ravel()
                            if t_i is None:
                                t_i = templates[:, i].toarray().ravel()
                            if t_j is None:
                                t_j = templates[:, j].toarray().ravel()
                            new_template = a1 * t_i + a2 * t_j
                            similarity = numpy.corrcoef(t_k, new_template)[(0, 1)]
                            local_overlap = numpy.corrcoef(t_i, t_j)[(0, 1)]
                            if adapted_cc:
                                shared_support = numpy.sum(numpy.logical_or(supports[i], supports[j]) * supports[k])
                                exponent = numpy.exp(-shared_support / adapted_thr)
                                mytest1 = similarity ** exponent > cc_merge
                                mytest2 = local_overlap ** exponents[(i, j)] < 0.5
                            else:
                                mytest1 = similarity > cc_merge
                            mytest2 = local_overlap < 0.5
                        if mytest1 and mytest2 and k not in mixtures:
                            mixtures += [k]
                            been_found = True
                            break

    sys.stderr.flush()
    to_remove = numpy.unique(numpy.array(mixtures, dtype=(numpy.int32)))
    to_remove = all_gather_array(to_remove, comm, 0, dtype='int32')
    if len(to_remove) > 0:
        if comm.rank == 0:
            result = load_data(params, 'clusters')
            slice_templates(params, to_remove)
            slice_clusters(params, result, to_remove=to_remove)
    comm.Barrier()
    del c_overs
    if comm.rank == 0:
        os.remove(filename)
    if SHARED_MEMORY:
        for memory in mpi_memory_1:
            memory.Free()

        for memory in mpi_memory_2:
            memory.Free()

    return [
     nb_temp, len(to_remove)]