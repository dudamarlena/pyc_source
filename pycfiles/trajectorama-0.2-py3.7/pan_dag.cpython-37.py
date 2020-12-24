# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trajectorama/pan_dag.py
# Compiled at: 2020-01-31 12:39:05
# Size of source mod 2**32: 11745 bytes
from anndata import AnnData
from joblib import Parallel, delayed
import numpy as np, scanpy as sc
from sklearn.preprocessing import normalize
import os, sys, uuid, warnings
from ._louvain import louvain
from .utils import *

def louvain_worker(X, resolution):
    log_uuid = str(uuid.uuid4())
    tmp_log_fname = 'target/tmp/{}_louvain.log'.format(log_uuid)
    adata = AnnData(X=X)
    sc.pp.neighbors(adata, use_rep='X')
    louvain(adata, resolution=resolution, key_added='louvain', log_fname=tmp_log_fname)
    return tmp_log_fname


class PanDAG(object):

    def __init__(self, cluster_method='louvain', sketch_size='auto', sketch_method='auto', reduce_dim=None, verbose=False):
        """
        Initializes pan clustering DAG object.
        """
        self.cluster_method = cluster_method
        self.sketch_size = sketch_size
        self.sketch_method = sketch_method
        self.sketch_neighbors = None
        self.reduce_dim = reduce_dim
        self.verbose = verbose
        self.features = None
        self.children = []
        self.sample_idx = []
        self.n_leaves = len(self.sample_idx)
        self.nodes = [self]

    def check_and_sketch(self, X):
        """
        Determines sketch size and method based on dataset size and
        underlying DAG construction method.

        Parameters
        ----------
        X: `numpy.ndarray` or `scipy.sparse.csr_matrix`
            Dataset tot be sketched.

        Returns
        -------
        X_sketch
            Sketched version of dataset `X`.
        """
        n_samples = X.shape[0]
        if self.sketch_size is None:
            return X
        if self.sketch_method not in set(['auto', 'geometric', 'uniform']):
            raise ValueError('Invalid sketching method {}'.format(self.sketch_method))
        elif self.sketch_size == 'auto':
            if self.cluster_method == 'agg_ward':
                if n_samples > 5000:
                    self.sketch_size = 5000
                    if self.sketch_method == 'auto':
                        self.sketch_method = 'geometric'
                else:
                    return X
            elif self.cluster_method == 'louvain':
                if n_samples > 1000000:
                    self.sketch_size = 1000000
                    if self.sketch_method == 'auto':
                        self.sketch_method = 'uniform'
                else:
                    return X
            else:
                self.sketch_size = 20000
                if self.sketch_method == 'auto':
                    self.sketch_method = 'geometric'
        elif self.sketch_method == 'auto':
            self.sketch_method = 'geometric'
        if self.sketch_method == 'geometric':
            if self.reduce_dim is None:
                X = reduce_dimensionality((normalize(X)), dim_red_k=100)
        return self.sketch(X)

    def sketch(self, X):
        """
        Actually sketches the dataset and saves nearest neighbor mappings
        from sketch elements to sample observations in full dataset in
        the `self.sketch_neighbors` variable.

        Parameters
        ----------
        X: `numpy.ndarray` or `scipy.sparse.csr_matrix`
            Dataset tot be sketched.

        Returns
        -------
        X_sketch
            Sketched version of dataset `X`.
        """
        n_samples = X.shape[0]
        if self.verbose > 1:
            tprint('Sketching...')
        elif self.sketch_method == 'geometric':
            from geosketch import gs
            sketch_idx = gs(X, (self.sketch_size), replace=False)
        else:
            if self.sketch_method == 'uniform':
                sketch_idx = sorted(np.random.choice(n_samples,
                  size=(self.sketch_size), replace=False))
            else:
                return X
        X_sketch = X[sketch_idx]
        self.sketch_neighbors = nearest_approx(X, X_sketch)
        return X[sketch_idx]

    def create_dag_agg(self, Z, n_samples):
        """
        Form hierarchical structure among `n_samples` observations
        according to a linkage matrix outputted by a hierarchical
        clustering algorithm.

        Parameters
        ----------
        Z: `numpy.ndarray`
            Linkage matrix outputted by agglomerative clustering.
        n_samples: `int`
            The number of samples in the dataset.
        """
        self.nodes = []
        for i in range(Z.shape[0]):
            if i == Z.shape[0] - 1:
                node = self
            else:
                node = PanDAG()
            if Z[(i, 0)] < n_samples:
                if self.sketch_neighbors is None:
                    node.sample_idx.append(Z[(i, 0)])
                else:
                    [node.sample_idx.append(idx) for idx in self.sketch_neighbors[Z[(i, 0)]]]
            else:
                prev_node = self.nodes[(Z[(i, 0)] - n_samples)]
                node.children.append(prev_node)
                node.sample_idx += prev_node.sample_idx
            if Z[(i, 1)] < n_samples:
                if self.sketch_neighbors is None:
                    node.sample_idx.append(Z[(i, 1)])
                else:
                    [node.sample_idx.append(idx) for idx in self.sketch_neighbors[Z[(i, 1)]]]
            else:
                prev_node = self.nodes[(Z[(i, 1)] - n_samples)]
                node.children.append(prev_node)
                node.sample_idx += prev_node.sample_idx
            node.n_leaves = len(node.sample_idx)
            node.features = self.features
            self.nodes.append(node)

        return self

    def create_dag_louvain(self, X):
        """
        Form hierarchical structure among observed samples in `X`
        according to the Louvain clustering algorithm that iteratively
        merges nodes into larger "communities."

        Parameters
        ----------
        X: `numpy.ndarray` or `scipy.sparse.csr_matrix`
            Matrix with rows corresponding to all of the samples that
            define the DAG and columns corresponding to features that
            define the correlation matrices.
        """
        mkdir_p('target/tmp')
        resolutions = [
         1.0, 0.1, 10.0]
        results = Parallel(n_jobs=3, backend='multiprocessing')((delayed(louvain_worker)(X, resolution) for resolution in resolutions))
        for tmp_log_fname in results:
            nodes = {}
            v_to_node = {}
            max_iter = 0
            with open(tmp_log_fname) as (f):
                for line in f:
                    fields = line.rstrip().split()
                    sample = int(fields[0])
                    community, iter_ = fields[1], int(fields[2])
                    if iter_ > max_iter:
                        max_iter = iter_
                    node_id = (community, iter_)
                    if node_id not in nodes:
                        nodes[node_id] = PanDAG()
                    if sample not in v_to_node:
                        v_to_node[sample] = []
                    v_to_node[sample].append(node_id)
                    node = nodes[node_id]
                    if self.sketch_neighbors is None:
                        node.sample_idx.append(sample)
                    else:
                        [node.sample_idx.append(idx) for idx in self.sketch_neighbors[sample]]

            os.remove(tmp_log_fname)
            nodes[('0', max_iter + 1)] = self
            if self.sketch_neighbors is None:
                self.sample_idx = list(range(X.shape[0]))
            else:
                self.sample_idx = [idx for sample in self.sketch_neighbors for idx in self.sketch_neighbors[sample]]
            for node_id in nodes:
                node = nodes[node_id]
                child_ids = set()
                subdag_ids = set()
                for sample in node.sample_idx:
                    if sample not in v_to_node:
                        continue
                    for sample_node_id in v_to_node[sample]:
                        if sample_node_id[1] == node_id[1] - 1:
                            child_ids.add(sample_node_id)
                        if sample_node_id[1] < node_id[1]:
                            subdag_ids.add(sample_node_id)

                for child_id in sorted(child_ids):
                    node.children.append(nodes[child_id])

                for subdag_id in sorted(subdag_ids):
                    node.nodes.append(nodes[subdag_id])

                node.n_leaves = len(node.sample_idx)

        return self

    def fit(self, X, y=None, features=None):
        """
        Constructs DAG according to `self.cluster_method`.

        Parameters
        ----------
        X: `numpy.ndarray` or `scipy.sparse.csr_matrix`
            Matrix with rows corresponding to all of the samples that
            define the DAG and columns corresponding to features.
        y
            Ignored
        features: `numpy.ndarray` of `str`
            A list of strings with feature labels.
        """
        if features is None:
            self.features = np.array(range(X.shape[1]))
        else:
            if self.reduce_dim is None:
                X_ = X
            else:
                if issubclass(type(self.reduce_dim), np.ndarray):
                    X_ = self.reduce_dim
                else:
                    if isinstance(self.reduce_dim, int):
                        X_ = reduce_dimensionality(X, dim_red_k=(self.reduce_dim))
                    else:
                        raise ValueError('`reduce_dim` has invalid type {}'.format(type(self.reduce_dim)))
            X_ = self.check_and_sketch(X_)
            if self.verbose > 1:
                tprint('Constructing DAG...')
            elif self.cluster_method == 'agg_ward':
                from sklearn.cluster.hierarchical import ward_tree
                ret = ward_tree(X_, n_clusters=None, return_distance=True)
                children, n_components, n_leaves, parent, distances = ret
                assert n_components == 1
                self.create_dag_agg(children, X_.shape[0])
            else:
                if self.cluster_method == 'louvain':
                    self.create_dag_louvain(X_)
                else:
                    raise ValueError('Invalid DAG construction method {}'.format(self.cluster_method))
        if len(self.sample_idx) != X.shape[0]:
            warnings.warn('Some samples have been orphaned during DAG construction, {} orphans detected'.format(X.shape[0] - len(self.sample_idx)), RuntimeWarning)
        return self