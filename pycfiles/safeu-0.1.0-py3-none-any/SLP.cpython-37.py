# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\文档\python\SafeU\safeu\data_quality\SLP.py
# Compiled at: 2019-05-29 14:10:33
# Size of source mod 2**32: 7004 bytes
"""
This module implements the algorithm SLP.

References
----------
..  [1] D.-M. Liang and Y.-F. Li. Lightweight Label Propagation for 
    Large-Scale Network Data. In: 27th International Joint Conference 
    on Artificial Intelligence (IJCAI'18), Stockholm, Sweden, 2018.

Author:
    De-Ming Liang <XXX@gmail.com>
    Xiao-Shuang Lv <XXX@XXX.com>

License:
    MIT
"""
import platform, numpy as np, re
import scipy.sparse as sp
import sys
from ctypes import CDLL
from os.path import join, dirname
from ..base import TransductiveEstimatorwithGraph
version = platform.python_version()
if sys.platform == 'win32':
    if re.search('3.6.*', version):
        from utils.slp_tool_win.slp_tool_v36 import iteration
    else:
        if re.search('3.7.*', version):
            from utils.slp_tool_win.slp_tool_v37 import iteration
        else:
            raise EnvironmentError('Only support 3.6 or 3.7 version.')
else:
    module_path = join(dirname(__file__), 'utils', 'slp_tool_linux', 'lib')
    if re.search('3.6.*', version):
        CDLL(join(module_path, 'libboost_python36.so.1.70.0'))
        CDLL(join(module_path, 'libboost_numpy36.so.1.70.0'))
        from utils.slp_tool_linux.slp_tool_v36 import iteration
    else:
        if re.search('3.7.*', version):
            CDLL(join(module_path, 'libboost_python37.so.1.70.0'))
            CDLL(join(module_path, 'libboost_numpy37.so.1.70.0'))
            from utils.slp_tool_linux.slp_tool_v37 import iteration
        else:
            raise EnvironmentError('Only support 3.6 or 3.7 version.')

class SLP(TransductiveEstimatorwithGraph):
    __doc__ = "\n    This is a python implementation of SLP, which can do label propagation\n    on large-scale graphs.\n\n    Read more in the :ref:`User Guide <svm_classification>`.\n\n    Parameters\n    ----------\n    stepSize: coefficient, optical (default=0.1)\n        step size.\n\n    T: coefficient,optical (default=6)\n        running epoches.\n\n    Examples\n    --------\n    >>> from safeu.data_quality.SLP import SLP\n    >>> from safeu.datasets import data_manipulate, base\n    >>> X, y = base.load_covtype(True)\n    >>> W = base.load_graph_covtype(True)\n    >>> _, test_idxs, labeled_idxs, unlabeled_idxs = \\\n    >>>                       data_manipulate.inductive_split(X=X, y=y)\n    >>> slp = SLP(stepSize=0.1, T=6)\n    >>> slp.fit(X,y,labeled_idxs,W)\n    >>> slp.predict(unlabeled_idxs)\n    [1,-1,-1,1,1...,1]\n\n    References\n    ----------\n    SLP implements the LEAD algorithm in [1].\n\n    ..  [1] D.-M. Liang and Y.-F. Li. Lightweight Label Propagation for \n        Large-Scale Network Data. In: 27th International Joint Conference on \n        Artificial Intelligence (IJCAI'18), Stockholm, Sweden, 2018.\n\n    "

    def __init__(self, stepSize=0.1, T=6):
        """

        Parameters
        ----------
        stepSize: coefficient, optical (default=0.1)
            step size.
        T: coefficient,optical (default=6)
            running epoches.
        """
        super(SLP, self).__init__()
        self.stepSize = stepSize
        self.T = T
        self.pred = None
        self.labels = None

    def set_params(self, param):
        """Parameter setting function.

        Parameters
        ----------
        param ：dict
            Store parameter names and corresponding values {'name': value}.
        """
        if isinstance(param, dict):
            self.__dict__.update(param)
        self.pred = None
        self.labels = None

    def fit(self, X, y, l_ind, W):
        """Fit the model to data.

        Parameters
        ----------
        W : sparse matrix
            affinity matrix, labels should be at the left-top corner,
            should be in sparse form.

        y : array-like
            label vector with different labels [n_samples].

        l_ind : array-like
            a row vector with length l, where l is the number of labeled
            instance. Each element is an index of a labeled instance.

        Returns
        -------
        pred : array-like
            prediction of labels [n_samples, n_labels], in the original sort.
        """
        N = W.shape[0]
        u_ind = np.linspace(0, N - 1, N).astype(np.int)
        u_ind = np.delete(u_ind, l_ind)
        y_mat = self._format_label(N, y)
        fu = self._Sgd(W, y_mat, l_ind, u_ind)
        self.pred = np.zeros([N, y_mat.shape[1]])
        self.pred[l_ind] = y_mat[l_ind]
        self.pred[u_ind] = fu

    def predict(self, u_ind):
        """Compute the most possible label for samples in W.

        Parameters
        ----------
        u_ind : array-like
            a row vector with length l, where l is the number of unlabeled
            instance. Each element is an index of a unlabeled instance.

        Returns
        -------
        pred : array-like
            Each row is the most likely label for a sample [n_samples].
        """
        pred = np.zeros((self.pred.shape[0], 1))
        max = np.argmax((self.pred), axis=1)
        for i in range(len(max)):
            pred[i] = self.labels[max[i]]

        return pred[u_ind]

    def predict_proba(self, u_ind):
        """Compute probabilities of possible labels for samples in W.

        Parameters
        ----------
        u_ind : array-like
            a row vector with length l, where l is the number of unlabeled
            instance. Each element is an index of a unlabeled instance.

        Returns
        -------
        pred : array-like
            Each line is the probability of possible labels of a sample
            involved in the calculation of the prediction
            [n_samples, n_labels].
        """
        sum = np.sum((self.pred), axis=1).reshape(self.pred.shape[0], 1)
        pred = np.zeros_like(self.pred)
        for i in range(sum.shape[0]):
            if sum[i] != 0.0:
                pred[i, :] = self.pred[i, :] / sum[i]

        return pred[u_ind]

    def _Sgd(self, W, f_mat, l_ind, u_ind):
        l_num = l_ind.shape[0]
        n, d = f_mat.shape
        f = np.zeros_like(f_mat)
        f[l_ind, :] = f_mat[l_ind]
        W_coo = sp.coo_matrix(W)
        row = W_coo.row
        col = W_coo.col
        if sp.issparse(W):
            Jc = W.indptr
            W_data = W.data
            f = iteration(row, col, l_ind, l_num, n, f, Jc, W_data, self.stepSize, self.T)
        else:
            raise ValueError('W should be sparse matrix.')
        fu = f[u_ind, :]
        return fu

    def _format_label(self, N, y):
        y = y.T[0]
        self.labels = np.unique(y)
        y_mat = np.zeros((N, len(self.labels)))
        for idx, label in enumerate(self.labels):
            y_mat[(y == label, idx)] = 1

        return y_mat