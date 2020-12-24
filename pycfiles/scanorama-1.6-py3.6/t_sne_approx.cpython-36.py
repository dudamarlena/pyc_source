# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scanorama/t_sne_approx.py
# Compiled at: 2018-09-03 09:27:54
# Size of source mod 2**32: 35773 bytes
from time import time
import numpy as np
from scipy import linalg
import scipy.sparse as sp
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.base import BaseEstimator
from sklearn.utils import check_array
from sklearn.utils import check_random_state
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.manifold import _utils
from sklearn.manifold import _barnes_hut_tsne
from sklearn.externals.six import string_types
from sklearn.utils import deprecated
from annoy import AnnoyIndex
MACHINE_EPSILON = np.finfo(np.double).eps

def _joint_probabilities(distances, desired_perplexity, verbose):
    """Compute joint probabilities p_ij from distances.

    Parameters
    ----------
    distances : array, shape (n_samples * (n_samples-1) / 2,)
        Distances of samples are stored as condensed matrices, i.e.
        we omit the diagonal and duplicate entries and store everything
        in a one-dimensional array.

    desired_perplexity : float
        Desired perplexity of the joint probability distributions.

    verbose : int
        Verbosity level.

    Returns
    -------
    P : array, shape (n_samples * (n_samples-1) / 2,)
        Condensed joint probability matrix.
    """
    distances = distances.astype((np.float32), copy=False)
    conditional_P = _utils._binary_search_perplexity(distances, None, desired_perplexity, verbose)
    P = conditional_P + conditional_P.T
    sum_P = np.maximum(np.sum(P), MACHINE_EPSILON)
    P = np.maximum(squareform(P) / sum_P, MACHINE_EPSILON)
    return P


def _joint_probabilities_nn(distances, neighbors, desired_perplexity, verbose):
    """Compute joint probabilities p_ij from distances using just nearest
    neighbors.

    This method is approximately equal to _joint_probabilities. The latter
    is O(N), but limiting the joint probability to nearest neighbors improves
    this substantially to O(uN).

    Parameters
    ----------
    distances : array, shape (n_samples, k)
        Distances of samples to its k nearest neighbors.

    neighbors : array, shape (n_samples, k)
        Indices of the k nearest-neighbors for each samples.

    desired_perplexity : float
        Desired perplexity of the joint probability distributions.

    verbose : int
        Verbosity level.

    Returns
    -------
    P : csr sparse matrix, shape (n_samples, n_samples)
        Condensed joint probability matrix with only nearest neighbors.
    """
    t0 = time()
    n_samples, k = neighbors.shape
    distances = distances.astype((np.float32), copy=False)
    neighbors = neighbors.astype((np.int64), copy=False)
    conditional_P = _utils._binary_search_perplexity(distances, neighbors, desired_perplexity, verbose)
    if not np.all(np.isfinite(conditional_P)):
        raise AssertionError('All probabilities should be finite')
    else:
        P = csr_matrix((conditional_P.ravel(), neighbors.ravel(),
         range(0, n_samples * k + 1, k)),
          shape=(
         n_samples, n_samples))
        P = P + P.T
        sum_P = np.maximum(P.sum(), MACHINE_EPSILON)
        P /= sum_P
        assert np.all(np.abs(P.data) <= 1.0)
    if verbose >= 2:
        duration = time() - t0
        print('[t-SNE] Computed conditional probabilities in {:.3f}s'.format(duration))
    return P


def _kl_divergence(params, P, degrees_of_freedom, n_samples, n_components, skip_num_points=0):
    """t-SNE objective function: gradient of the KL divergence
    of p_ijs and q_ijs and the absolute error.

    Parameters
    ----------
    params : array, shape (n_params,)
        Unraveled embedding.

    P : array, shape (n_samples * (n_samples-1) / 2,)
        Condensed joint probability matrix.

    degrees_of_freedom : float
        Degrees of freedom of the Student's-t distribution.

    n_samples : int
        Number of samples.

    n_components : int
        Dimension of the embedded space.

    skip_num_points : int (optional, default:0)
        This does not compute the gradient for points with indices below
        `skip_num_points`. This is useful when computing transforms of new
        data where you'd like to keep the old data fixed.

    Returns
    -------
    kl_divergence : float
        Kullback-Leibler divergence of p_ij and q_ij.

    grad : array, shape (n_params,)
        Unraveled gradient of the Kullback-Leibler divergence with respect to
        the embedding.
    """
    X_embedded = params.reshape(n_samples, n_components)
    dist = pdist(X_embedded, 'sqeuclidean')
    dist += 1.0
    dist /= degrees_of_freedom
    dist **= (degrees_of_freedom + 1.0) / -2.0
    Q = np.maximum(dist / (2.0 * np.sum(dist)), MACHINE_EPSILON)
    kl_divergence = 2.0 * np.dot(P, np.log(np.maximum(P, MACHINE_EPSILON) / Q))
    grad = np.ndarray((n_samples, n_components), dtype=(params.dtype))
    PQd = squareform((P - Q) * dist)
    for i in range(skip_num_points, n_samples):
        grad[i] = np.dot(np.ravel((PQd[i]), order='K'), X_embedded[i] - X_embedded)

    grad = grad.ravel()
    c = 2.0 * (degrees_of_freedom + 1.0) / degrees_of_freedom
    grad *= c
    return (
     kl_divergence, grad)


def _kl_divergence_bh(params, P, degrees_of_freedom, n_samples, n_components, angle=0.5, skip_num_points=0, verbose=False):
    """t-SNE objective function: KL divergence of p_ijs and q_ijs.

    Uses Barnes-Hut tree methods to calculate the gradient that
    runs in O(NlogN) instead of O(N^2)

    Parameters
    ----------
    params : array, shape (n_params,)
        Unraveled embedding.

    P : csr sparse matrix, shape (n_samples, n_sample)
        Sparse approximate joint probability matrix, computed only for the
        k nearest-neighbors and symmetrized.

    degrees_of_freedom : float
        Degrees of freedom of the Student's-t distribution.

    n_samples : int
        Number of samples.

    n_components : int
        Dimension of the embedded space.

    angle : float (default: 0.5)
        This is the trade-off between speed and accuracy for Barnes-Hut T-SNE.
        'angle' is the angular size (referred to as theta in [3]) of a distant
        node as measured from a point. If this size is below 'angle' then it is
        used as a summary node of all points contained within it.
        This method is not very sensitive to changes in this parameter
        in the range of 0.2 - 0.8. Angle less than 0.2 has quickly increasing
        computation time and angle greater 0.8 has quickly increasing error.

    skip_num_points : int (optional, default:0)
        This does not compute the gradient for points with indices below
        `skip_num_points`. This is useful when computing transforms of new
        data where you'd like to keep the old data fixed.

    verbose : int
        Verbosity level.

    Returns
    -------
    kl_divergence : float
        Kullback-Leibler divergence of p_ij and q_ij.

    grad : array, shape (n_params,)
        Unraveled gradient of the Kullback-Leibler divergence with respect to
        the embedding.
    """
    params = params.astype((np.float32), copy=False)
    X_embedded = params.reshape(n_samples, n_components)
    val_P = P.data.astype((np.float32), copy=False)
    neighbors = P.indices.astype((np.int64), copy=False)
    indptr = P.indptr.astype((np.int64), copy=False)
    grad = np.zeros((X_embedded.shape), dtype=(np.float32))
    error = _barnes_hut_tsne.gradient(val_P, X_embedded, neighbors, indptr, grad,
      angle, n_components, verbose, dof=degrees_of_freedom)
    c = 2.0 * (degrees_of_freedom + 1.0) / degrees_of_freedom
    grad = grad.ravel()
    grad *= c
    return (
     error, grad)


def _gradient_descent(objective, p0, it, n_iter, n_iter_check=1, n_iter_without_progress=300, momentum=0.8, learning_rate=200.0, min_gain=0.01, min_grad_norm=1e-07, verbose=0, args=None, kwargs=None):
    """Batch gradient descent with momentum and individual gains.

    Parameters
    ----------
    objective : function or callable
        Should return a tuple of cost and gradient for a given parameter
        vector. When expensive to compute, the cost can optionally
        be None and can be computed every n_iter_check steps using
        the objective_error function.

    p0 : array-like, shape (n_params,)
        Initial parameter vector.

    it : int
        Current number of iterations (this function will be called more than
        once during the optimization).

    n_iter : int
        Maximum number of gradient descent iterations.

    n_iter_check : int
        Number of iterations before evaluating the global error. If the error
        is sufficiently low, we abort the optimization.

    n_iter_without_progress : int, optional (default: 300)
        Maximum number of iterations without progress before we abort the
        optimization.

    momentum : float, within (0.0, 1.0), optional (default: 0.8)
        The momentum generates a weight for previous gradients that decays
        exponentially.

    learning_rate : float, optional (default: 200.0)
        The learning rate for t-SNE is usually in the range [10.0, 1000.0]. If
        the learning rate is too high, the data may look like a 'ball' with any
        point approximately equidistant from its nearest neighbours. If the
        learning rate is too low, most points may look compressed in a dense
        cloud with few outliers.

    min_gain : float, optional (default: 0.01)
        Minimum individual gain for each parameter.

    min_grad_norm : float, optional (default: 1e-7)
        If the gradient norm is below this threshold, the optimization will
        be aborted.

    verbose : int, optional (default: 0)
        Verbosity level.

    args : sequence
        Arguments to pass to objective function.

    kwargs : dict
        Keyword arguments to pass to objective function.

    Returns
    -------
    p : array, shape (n_params,)
        Optimum parameters.

    error : float
        Optimum.

    i : int
        Last iteration.
    """
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}
    p = p0.copy().ravel()
    update = np.zeros_like(p)
    gains = np.ones_like(p)
    error = np.finfo(np.float).max
    best_error = np.finfo(np.float).max
    best_iter = i = it
    tic = time()
    for i in range(it, n_iter):
        error, grad = objective(p, *args, **kwargs)
        grad_norm = linalg.norm(grad)
        inc = update * grad < 0.0
        dec = np.invert(inc)
        gains[inc] += 0.2
        gains[dec] *= 0.8
        np.clip(gains, min_gain, (np.inf), out=gains)
        grad *= gains
        update = momentum * update - learning_rate * grad
        p += update
        if (i + 1) % n_iter_check == 0:
            toc = time()
            duration = toc - tic
            tic = toc
            if verbose >= 2:
                print('[t-SNE] Iteration %d: error = %.7f, gradient norm = %.7f (%s iterations in %0.3fs)' % (
                 i + 1, error, grad_norm, n_iter_check, duration))
            if error < best_error:
                best_error = error
                best_iter = i
            else:
                if i - best_iter > n_iter_without_progress:
                    if verbose >= 2:
                        print('[t-SNE] Iteration %d: did not make any progress during the last %d episodes. Finished.' % (
                         i + 1, n_iter_without_progress))
                    break
                if grad_norm <= min_grad_norm:
                    if verbose >= 2:
                        print('[t-SNE] Iteration %d: gradient norm %f. Finished.' % (
                         i + 1, grad_norm))
                    break

    return (
     p, error, i)


def trustworthiness(X, X_embedded, n_neighbors=5, precomputed=False):
    """Expresses to what extent the local structure is retained.

    The trustworthiness is within [0, 1]. It is defined as

    .. math::

        T(k) = 1 - \x0crac{2}{nk (2n - 3k - 1)} \\sum^n_{i=1}
            \\sum_{j \\in U^{(k)}_i} (r(i, j) - k)

    where :math:`r(i, j)` is the rank of the embedded datapoint j
    according to the pairwise distances between the embedded datapoints,
    :math:`U^{(k)}_i` is the set of points that are in the k nearest
    neighbors in the embedded space but not in the original space.

    * "Neighborhood Preservation in Nonlinear Projection Methods: An
      Experimental Study"
      J. Venna, S. Kaski
    * "Learning a Parametric Embedding by Preserving Local Structure"
      L.J.P. van der Maaten

    Parameters
    ----------
    X : array, shape (n_samples, n_features) or (n_samples, n_samples)
        If the metric is 'precomputed' X must be a square distance
        matrix. Otherwise it contains a sample per row.

    X_embedded : array, shape (n_samples, n_components)
        Embedding of the training data in low-dimensional space.

    n_neighbors : int, optional (default: 5)
        Number of neighbors k that will be considered.

    precomputed : bool, optional (default: False)
        Set this flag if X is a precomputed square distance matrix.

    Returns
    -------
    trustworthiness : float
        Trustworthiness of the low-dimensional embedding.
    """
    if precomputed:
        dist_X = X
    else:
        dist_X = pairwise_distances(X, squared=True)
    dist_X_embedded = pairwise_distances(X_embedded, squared=True)
    ind_X = np.argsort(dist_X, axis=1)
    ind_X_embedded = np.argsort(dist_X_embedded, axis=1)[:, 1:n_neighbors + 1]
    n_samples = X.shape[0]
    t = 0.0
    ranks = np.zeros(n_neighbors)
    for i in range(n_samples):
        for j in range(n_neighbors):
            ranks[j] = np.where(ind_X[i] == ind_X_embedded[(i, j)])[0][0]

        ranks -= n_neighbors
        t += np.sum(ranks[(ranks > 0)])

    t = 1.0 - t * (2.0 / (n_samples * n_neighbors * (2.0 * n_samples - 3.0 * n_neighbors - 1.0)))
    return t


class TSNEApprox(BaseEstimator):
    __doc__ = 't-distributed Stochastic Neighbor Embedding.\n\n    t-SNE [1] is a tool to visualize high-dimensional data. It converts\n    similarities between data points to joint probabilities and tries\n    to minimize the Kullback-Leibler divergence between the joint\n    probabilities of the low-dimensional embedding and the\n    high-dimensional data. t-SNE has a cost function that is not convex,\n    i.e. with different initializations we can get different results.\n\n    It is highly recommended to use another dimensionality reduction\n    method (e.g. PCA for dense data or TruncatedSVD for sparse data)\n    to reduce the number of dimensions to a reasonable amount (e.g. 50)\n    if the number of features is very high. This will suppress some\n    noise and speed up the computation of pairwise distances between\n    samples. For more tips see Laurens van der Maaten\'s FAQ [2].\n\n    Read more in the :ref:`User Guide <t_sne>`.\n\n    Parameters\n    ----------\n    n_components : int, optional (default: 2)\n        Dimension of the embedded space.\n\n    perplexity : float, optional (default: 30)\n        The perplexity is related to the number of nearest neighbors that\n        is used in other manifold learning algorithms. Larger datasets\n        usually require a larger perplexity. Consider selecting a value\n        between 5 and 50. The choice is not extremely critical since t-SNE\n        is quite insensitive to this parameter.\n\n    early_exaggeration : float, optional (default: 12.0)\n        Controls how tight natural clusters in the original space are in\n        the embedded space and how much space will be between them. For\n        larger values, the space between natural clusters will be larger\n        in the embedded space. Again, the choice of this parameter is not\n        very critical. If the cost function increases during initial\n        optimization, the early exaggeration factor or the learning rate\n        might be too high.\n\n    learning_rate : float, optional (default: 200.0)\n        The learning rate for t-SNE is usually in the range [10.0, 1000.0]. If\n        the learning rate is too high, the data may look like a \'ball\' with any\n        point approximately equidistant from its nearest neighbours. If the\n        learning rate is too low, most points may look compressed in a dense\n        cloud with few outliers. If the cost function gets stuck in a bad local\n        minimum increasing the learning rate may help.\n\n    n_iter : int, optional (default: 1000)\n        Maximum number of iterations for the optimization. Should be at\n        least 250.\n\n    n_iter_without_progress : int, optional (default: 300)\n        Maximum number of iterations without progress before we abort the\n        optimization, used after 250 initial iterations with early\n        exaggeration. Note that progress is only checked every 50 iterations so\n        this value is rounded to the next multiple of 50.\n\n        .. versionadded:: 0.17\n           parameter *n_iter_without_progress* to control stopping criteria.\n\n    min_grad_norm : float, optional (default: 1e-7)\n        If the gradient norm is below this threshold, the optimization will\n        be stopped.\n\n    metric : string or callable, optional\n        The metric to use when calculating distance between instances in a\n        feature array. If metric is a string, it must be one of the options\n        allowed by scipy.spatial.distance.pdist for its metric parameter, or\n        a metric listed in pairwise.PAIRWISE_DISTANCE_FUNCTIONS.\n        If metric is "precomputed", X is assumed to be a distance matrix.\n        Alternatively, if metric is a callable function, it is called on each\n        pair of instances (rows) and the resulting value recorded. The callable\n        should take two arrays from X as input and return a value indicating\n        the distance between them. The default is "euclidean" which is\n        interpreted as squared euclidean distance.\n\n    init : string or numpy array, optional (default: "random")\n        Initialization of embedding. Possible options are \'random\', \'pca\',\n        and a numpy array of shape (n_samples, n_components).\n        PCA initialization cannot be used with precomputed distances and is\n        usually more globally stable than random initialization.\n\n    verbose : int, optional (default: 0)\n        Verbosity level.\n\n    random_state : int, RandomState instance or None, optional (default: None)\n        If int, random_state is the seed used by the random number generator;\n        If RandomState instance, random_state is the random number generator;\n        If None, the random number generator is the RandomState instance used\n        by `np.random`.  Note that different initializations might result in\n        different local minima of the cost function.\n\n    method : string (default: \'barnes_hut\')\n        By default the gradient calculation algorithm uses Barnes-Hut\n        approximation running in O(NlogN) time. method=\'exact\'\n        will run on the slower, but exact, algorithm in O(N^2) time. The\n        exact algorithm should be used when nearest-neighbor errors need\n        to be better than 3%. However, the exact method cannot scale to\n        millions of examples.\n\n        .. versionadded:: 0.17\n           Approximate optimization *method* via the Barnes-Hut.\n\n    angle : float (default: 0.5)\n        Only used if method=\'barnes_hut\'\n        This is the trade-off between speed and accuracy for Barnes-Hut T-SNE.\n        \'angle\' is the angular size (referred to as theta in [3]) of a distant\n        node as measured from a point. If this size is below \'angle\' then it is\n        used as a summary node of all points contained within it.\n        This method is not very sensitive to changes in this parameter\n        in the range of 0.2 - 0.8. Angle less than 0.2 has quickly increasing\n        computation time and angle greater 0.8 has quickly increasing error.\n\n    Attributes\n    ----------\n    embedding_ : array-like, shape (n_samples, n_components)\n        Stores the embedding vectors.\n\n    kl_divergence_ : float\n        Kullback-Leibler divergence after optimization.\n\n    n_iter_ : int\n        Number of iterations run.\n\n    Examples\n    --------\n\n    >>> import numpy as np\n    >>> from sklearn.manifold import TSNE\n    >>> X = np.array([[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]])\n    >>> X_embedded = TSNE(n_components=2).fit_transform(X)\n    >>> X_embedded.shape\n    (4, 2)\n\n    References\n    ----------\n\n    [1] van der Maaten, L.J.P.; Hinton, G.E. Visualizing High-Dimensional Data\n        Using t-SNE. Journal of Machine Learning Research 9:2579-2605, 2008.\n\n    [2] van der Maaten, L.J.P. t-Distributed Stochastic Neighbor Embedding\n        http://homepage.tudelft.nl/19j49/t-SNE.html\n\n    [3] L.J.P. van der Maaten. Accelerating t-SNE using Tree-Based Algorithms.\n        Journal of Machine Learning Research 15(Oct):3221-3245, 2014.\n        http://lvdmaaten.github.io/publications/papers/JMLR_2014.pdf\n    '
    _EXPLORATION_N_ITER = 250
    _N_ITER_CHECK = 50

    def __init__(self, n_components=2, perplexity=30.0, early_exaggeration=12.0, learning_rate=200.0, n_iter=1000, n_iter_without_progress=300, min_grad_norm=1e-07, metric='euclidean', init='random', verbose=0, random_state=None, method='barnes_hut', angle=0.5):
        self.n_components = n_components
        self.perplexity = perplexity
        self.early_exaggeration = early_exaggeration
        self.learning_rate = learning_rate
        self.n_iter = n_iter
        self.n_iter_without_progress = n_iter_without_progress
        self.min_grad_norm = min_grad_norm
        self.metric = metric
        self.init = init
        self.verbose = verbose
        self.random_state = random_state
        self.method = method
        self.angle = angle

    def _fit(self, X, skip_num_points=0):
        """Fit the model using X as training data.

        Note that sparse arrays can only be handled by method='exact'.
        It is recommended that you convert your sparse array to dense
        (e.g. `X.toarray()`) if it fits in memory, or otherwise using a
        dimensionality reduction technique (e.g. TruncatedSVD).

        Parameters
        ----------
        X : array, shape (n_samples, n_features) or (n_samples, n_samples)
            If the metric is 'precomputed' X must be a square distance
            matrix. Otherwise it contains a sample per row. Note that this
            when method='barnes_hut', X cannot be a sparse array and if need be
            will be converted to a 32 bit float array. Method='exact' allows
            sparse arrays and 64bit floating point inputs.

        skip_num_points : int (optional, default:0)
            This does not compute the gradient for points with indices below
            `skip_num_points`. This is useful when computing transforms of new
            data where you'd like to keep the old data fixed.
        """
        if self.method not in ('barnes_hut', 'exact'):
            raise ValueError("'method' must be 'barnes_hut' or 'exact'")
        elif self.angle < 0.0 or self.angle > 1.0:
            raise ValueError("'angle' must be between 0.0 - 1.0")
        elif self.metric == 'precomputed':
            if isinstance(self.init, string_types):
                if self.init == 'pca':
                    raise ValueError('The parameter init="pca" cannot be used with metric="precomputed".')
                else:
                    if X.shape[0] != X.shape[1]:
                        raise ValueError('X should be a square distance matrix')
                    if np.any(X < 0):
                        raise ValueError('All distances should be positive, the precomputed distances given as X is not correct')
            elif self.method == 'barnes_hut' and sp.issparse(X):
                raise TypeError('A sparse matrix was passed, but dense data is required for method="barnes_hut". Use X.toarray() to convert to a dense numpy array if the array is small enough for it to fit in memory. Otherwise consider dimensionality reduction techniques (e.g. TruncatedSVD)')
            else:
                X = check_array(X, accept_sparse=['csr', 'csc', 'coo'], dtype=[
                 np.float32, np.float64])
            if self.method == 'barnes_hut':
                if self.n_components > 3:
                    raise ValueError("'n_components' should be inferior to 4 for the barnes_hut algorithm as it relies on quad-tree or oct-tree.")
            random_state = check_random_state(self.random_state)
            if self.early_exaggeration < 1.0:
                raise ValueError('early_exaggeration must be at least 1, but is {}'.format(self.early_exaggeration))
        else:
            if self.n_iter < 250:
                raise ValueError('n_iter should be at least 250')
            else:
                n_samples = X.shape[0]
                neighbors_nn = None
                if self.method == 'exact':
                    if self.metric == 'precomputed':
                        distances = X
                    else:
                        if self.verbose:
                            print('[t-SNE] Computing pairwise distances...')
                        else:
                            if self.metric == 'euclidean':
                                distances = pairwise_distances(X, metric=(self.metric), squared=True)
                            else:
                                distances = pairwise_distances(X, metric=(self.metric))
                            if np.any(distances < 0):
                                raise ValueError('All distances should be positive, the metric given is not correct')
                            P = _joint_probabilities(distances, self.perplexity, self.verbose)
                            assert np.all(np.isfinite(P)), 'All probabilities should be finite'
                        assert np.all(P >= 0), 'All probabilities should be non-negative'
                    assert np.all(P <= 1), 'All probabilities should be less or then equal to one'
                else:
                    k = min(n_samples - 1, int(3.0 * self.perplexity + 1))
                    if self.verbose:
                        print('[t-SNE] Computing {} nearest neighbors...'.format(k))
                    neighbors_method = 'ball_tree'
                    if self.metric == 'precomputed':
                        neighbors_method = 'brute'
                    knn = AnnoyIndex((X.shape[1]), metric='euclidean')
                    t0 = time()
                    for i in range(n_samples):
                        knn.add_item(i, X[i, :])

                    knn.build(50)
                    duration = time() - t0
                    if self.verbose:
                        print('[t-SNE] Indexed {} samples in {:.3f}s...'.format(n_samples, duration))
                    t0 = time()
                    neighbors_nn = np.zeros((n_samples, k), dtype=int)
                    distances_nn = np.zeros((n_samples, k))
                    for i in range(n_samples):
                        neighbors_nn[i, :], distances_nn[i, :] = knn.get_nns_by_vector((X[i, :]),
                          k, include_distances=True)

                    duration = time() - t0
                    if self.verbose:
                        print('[t-SNE] Computed neighbors for {} samples in {:.3f}s...'.format(n_samples, duration))
                    del knn
                    if self.metric == 'euclidean':
                        distances_nn **= 2
                    P = _joint_probabilities_nn(distances_nn, neighbors_nn, self.perplexity, self.verbose)
            if isinstance(self.init, np.ndarray):
                X_embedded = self.init
            else:
                if self.init == 'pca':
                    pca = PCA(n_components=(self.n_components), svd_solver='randomized', random_state=random_state)
                    X_embedded = pca.fit_transform(X).astype((np.float32), copy=False)
                else:
                    if self.init == 'random':
                        X_embedded = 0.0001 * random_state.randn(n_samples, self.n_components).astype(np.float32)
                    else:
                        raise ValueError("'init' must be 'pca', 'random', or a numpy array")
        degrees_of_freedom = max(self.n_components - 1.0, 1)
        return self._tsne(P, degrees_of_freedom, n_samples, random_state, X_embedded=X_embedded,
          neighbors=neighbors_nn,
          skip_num_points=skip_num_points)

    @property
    @deprecated('Attribute n_iter_final was deprecated in version 0.19 and will be removed in 0.21. Use ``n_iter_`` instead')
    def n_iter_final(self):
        return self.n_iter_

    def _tsne(self, P, degrees_of_freedom, n_samples, random_state, X_embedded, neighbors=None, skip_num_points=0):
        """Runs t-SNE."""
        params = X_embedded.ravel()
        opt_args = {'it':0, 
         'n_iter_check':self._N_ITER_CHECK, 
         'min_grad_norm':self.min_grad_norm, 
         'learning_rate':self.learning_rate, 
         'verbose':self.verbose, 
         'kwargs':dict(skip_num_points=skip_num_points), 
         'args':[
          P, degrees_of_freedom, n_samples, self.n_components], 
         'n_iter_without_progress':self._EXPLORATION_N_ITER, 
         'n_iter':self._EXPLORATION_N_ITER, 
         'momentum':0.5}
        if self.method == 'barnes_hut':
            obj_func = _kl_divergence_bh
            opt_args['kwargs']['angle'] = self.angle
            opt_args['kwargs']['verbose'] = self.verbose
        else:
            obj_func = _kl_divergence
        P *= self.early_exaggeration
        params, kl_divergence, it = _gradient_descent(obj_func, params, **opt_args)
        if self.verbose:
            print('[t-SNE] KL divergence after %d iterations with early exaggeration: %f' % (
             it + 1, kl_divergence))
        P /= self.early_exaggeration
        remaining = self.n_iter - self._EXPLORATION_N_ITER
        if it < self._EXPLORATION_N_ITER or remaining > 0:
            opt_args['n_iter'] = self.n_iter
            opt_args['it'] = it + 1
            opt_args['momentum'] = 0.8
            opt_args['n_iter_without_progress'] = self.n_iter_without_progress
            params, kl_divergence, it = _gradient_descent(obj_func, params, **opt_args)
        self.n_iter_ = it
        if self.verbose:
            print('[t-SNE] Error after %d iterations: %f' % (
             it + 1, kl_divergence))
        X_embedded = params.reshape(n_samples, self.n_components)
        self.kl_divergence_ = kl_divergence
        return X_embedded

    def fit_transform(self, X, y=None):
        """Fit X into an embedded space and return that transformed
        output.

        Parameters
        ----------
        X : array, shape (n_samples, n_features) or (n_samples, n_samples)
            If the metric is 'precomputed' X must be a square distance
            matrix. Otherwise it contains a sample per row.

        Returns
        -------
        X_new : array, shape (n_samples, n_components)
            Embedding of the training data in low-dimensional space.
        """
        embedding = self._fit(X)
        self.embedding_ = embedding
        return self.embedding_

    def fit(self, X, y=None):
        """Fit X into an embedded space.

        Parameters
        ----------
        X : array, shape (n_samples, n_features) or (n_samples, n_samples)
            If the metric is 'precomputed' X must be a square distance
            matrix. Otherwise it contains a sample per row. If the method
            is 'exact', X may be a sparse matrix of type 'csr', 'csc'
            or 'coo'.
        """
        self.fit_transform(X)
        return self