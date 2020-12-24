# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\文档\python\SafeU\safeu\data_quality\LEAD.py
# Compiled at: 2019-05-29 14:10:33
# Size of source mod 2**32: 11851 bytes
"""
This module implements the algorithm LEAD.

References
----------
..  [1] Yu-Feng Li, Shao-Bo Wang and Zhi-Hua Zhou. Graph Quality Judgement:
    A Large Margin Expedition. In: Proceedings of the 25th International
    Joint Confernece on Artificial Intelligence (IJCAI'16), New York, NY, 2016.

..  [2] R.-E. Fan, K.-W. Chang, C.-J. Hsieh, X.-R. Wang, and C.-J. Lin. 
    LIBLINEAR: A library for large linear classification. Journal of Machine 
    Learning Research 9(2008), 1871-1874.

License:
    MIT
"""
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from libs.liblinearutil import train
from ..base import TransductiveEstimatorwithGraph
from datasets.data_manipulate import check_inputs, modify_y

class LEAD(TransductiveEstimatorwithGraph):
    __doc__ = "\n    Parameters\n    ----------\n    C1 : float (default=1.0)\n        weight for the hinge loss of labeled instances. It was set as 1 in\n        our paper.\n\n    C2 : float (default=0.01)\n        weight for the hinge loss of unlabeled instances. It was set as\n        0.01 in our paper.\n\n    Examples\n    --------\n    >>> from safeu.data_quality.LEAD import LEAD\n    >>> from safeu.datasets import data_manipulate, base\n    >>> X, y = base.load_covtype(True)\n    >>> W = base.load_graph_covtype(True)\n    >>> _, test_idxs, labeled_idxs, unlabeled_idxs = \\\n    >>>                     data_manipulate.inductive_split(X=X, y=y)\n    >>> lead = LEAD(C1 = 1.0, C2 = 0.01)\n    >>> lead.fit(X,y,labeled_idxs,W)\n    >>> lead.predict(unlabeled_idxs)\n    [1,-1,-1,1,1...,1]\n\n    References\n    ---------\n    LEAD implements the LEAD algorithm in [1].\n\n    LEAD employs the Python version of liblinear [2] (available at \n    http://www.csie.ntu.edu.tw/~cjlin/liblinear/).\n\n    ..  [1] Yu-Feng Li, Shao-Bo Wang and Zhi-Hua Zhou. Graph Quality Judgement:\n        A Large Margin Expedition. In: Proceedings of the 25th International \n        Joint Confernece on Artificial Intelligence \n        (IJCAI'16), New York, NY, 2016.\n    ..  [2] R.-E. Fan, K.-W. Chang, C.-J. Hsieh, X.-R. Wang, and C.-J. Lin. \n        LIBLINEAR: A library for large linear classification. Journal of \n        Machine Learning Research 9(2008), 1871-1874.\n    "

    def __init__(self, C1=1.0, C2=0.01):
        super(LEAD, self).__init__()
        self.C1 = C1
        self.C2 = C2
        self.baseline_pred = None
        self.pred_values = None
        self.fallback_ind = None
        self.n_labels = None

    def set_params(self, param):
        """Parameter setting function.

        Parameters
        ----------
        param ：dict
            Store parameter names and corresponding values {'name': value}.
        """
        if isinstance(param, dict):
            self.__dict__.update(param)
        self.pred_values = None
        self.fallback_ind = None
        self.baseline_pred = None
        self.n_labels = None

    def fit(self, gssl_value, label, l_ind, W):
        """Given prediction from gssl, train method judge the quality of
        prediction with large-margin model

        Parameters
        ----------
        gssl_value : array-like
            a matrix with size n * T, where n is the number of instances and T
            is the number of graphs that gssl takes.Each row is a set of
            predictive values of an instance.

        label : array-like
            a column binary vector with length n. Each element is +1 or -1 for
            labeled instances. For unlabeled instances, this parameter could
            be used for computing accuracy if the ground truth is available.

        l_ind : array-like
            a row vector with length l, where l is the number of labeled
            instance. Each element is an index of a labeled instance.

        W: matrix
            affinity matrix, labels should be at the left-top corner, should be
            in sparse form.
        """
        param = '-q -s 3 -B 1'
        gssl_value_, label_, self.n_labels = check_inputs(gssl_value, label)
        u_ind = np.linspace(0, np.size(label_) - 1, np.size(label_)).astype(np.int32)
        u_ind = np.delete(u_ind, l_ind)
        self._baseline_predict(gssl_value_, label_, l_ind, u_ind)
        y = np.zeros(np.size(label_))
        for i in l_ind:
            y[i] = label_[i]

        pos_ratio = np.sum(y[l_ind] == 1, 0) / np.size(l_ind)
        y[u_ind] = self._self_predict(np.sum(gssl_value_[u_ind, :], 1), pos_ratio)
        z = gssl_value_
        weight = np.zeros(np.size(y))
        weight[l_ind] = self._weight_balance(y[l_ind], self.C1)
        c2 = 1e-06
        while c2 < self.C2:
            weight[u_ind] = self._weight_balance(y[u_ind], c2)
            last_obj = float('inf')
            svm_model = train(weight.tolist(), y.tolist(), z.tolist(), param)
            w = np.hstack(svm_model.get_decfun())
            y[u_ind] = self._self_predict(np.dot(self._phi(z[u_ind, :]), np.transpose(w)), pos_ratio)
            obj = self._objective_value(np.transpose(w), self._phi(z), y, weight)
            while obj < last_obj:
                svm_model = train(weight.tolist(), y.tolist(), z.tolist(), param)
                y[u_ind] = self._self_predict(np.dot(self._phi(z[u_ind, :]), np.transpose(w)), pos_ratio)
                last_obj = obj
                obj = self._objective_value(np.transpose(w), self._phi(z), y, weight)

            c2 = c2 * 2

        self.w = np.hstack(svm_model.get_decfun())
        t1 = np.where(y * np.dot(self._phi(z), np.transpose(w)) < 1)[0]
        self.fallback_ind = list(set(tuple(t1)).intersection(set(tuple(u_ind))))
        self.pred_values = y.reshape(-1, 1)

    def predict(self, u_ind, baseline_pred=None):
        """
        predict method replace the unsafe prediction with the baseline_pred 
        to improve the safeness.

        Parameters
        ----------
        u_ind : array-like
            a row vector with length l, where l is the number of unlabeled
            instance. Each element is an index of a unlabeled instance.

        baseline_pred : array-like
            a column vector with length n. Each element is a baseline
            predictive result of the corresponding instance. LEAD will replace
            the result of S3VM with this if the instance locates in the margin
            of S3VM.

        Returns
        -------
        pred : a column vector with length n. Each element is a prediction for
            the label of the instance, including labeled and unlabeled
            instances, even though for labeled instances the prediction is
            consistent with the true label.
        """
        if baseline_pred is not None:
            self.baseline_pred = baseline_pred
        else:
            if self.baseline_pred is None:
                raise ValueError('Must provide baseline prediction matrix.')
        self.baseline_pred = self.baseline_pred.reshape(-1, 1)
        self.pred_values = modify_y(self.pred_values, range(0, len(self.pred_values)), self.n_labels)
        self.pred_values[self.fallback_ind] = self.baseline_pred[self.fallback_ind]
        return self.pred_values[u_ind]

    def _baseline_predict(self, X, y, l_ind, u_ind):
        """Use 1nn to provide baseline predictions, and when the 'estimators'
         is not None, provide the own baseline for selection.

        Parameters
        ----------
        X : array-like
            Data matrix with [n_samples, n_features].The data will be used to
            train models.

        y : array-like
            Each element is +1 or -1 for labeled instances. For unlabeled
            instances, this parameter could be used for computing accuracy if
            the ground truth is available.

        l_ind : array-like
            A row vector with length l, where l is the number of labeled
            instance. Each element is an index of a labeled instance.

        u_ind : array-like
            a row vector with length l, where l is the number of unlabeled
            instance. Each element is an index of a unlabeled instance.
        """
        knn = KNeighborsClassifier()
        knn.fit(X[l_ind], y[l_ind].reshape(1, -1)[0].astype(int))
        baseline_pred = y
        baseline_pred[u_ind] = knn.predict(X[u_ind]).reshape(-1, 1)
        self.baseline_pred = modify_y(baseline_pred, np.linspace(0, len(baseline_pred) - 1, len(baseline_pred)).astype(np.int), self.n_labels)

    def _accuracy(self, pred, target):
        """Compute accuracy for current prediction.

        Parameters
        ----------
        pred : array-like, shape = [n_samples]
            Labels of samples predicted by model.

        target : array-like, shape = [n_samples]
            True labels of samples.
        
        Returns
        -------
        acc : float
            Accuracy of predictions.
        """
        if np.size(pred) != np.size(target):
            raise ValueError('The sizes of prediction and target are not matched.')
        return np.sum(pred == np.transpose(target)) / np.size(pred)

    def _phi(self, x):
        """
        
        """
        return np.hstack((x, np.ones((np.size(x, 0), 1))))

    def _weight_balance(self, y, C):
        """Compute weight of instances.

        Patameters
        ----------
        y : array-like, shape = [n_samples]
            Labels of samples.

        C : float
            Weight for the hinge loss of instances

        Returns
        -------
        weight : array-like, shape = [n_samples]
            weight of instances.
        """
        weight = np.ones(y.shape) * C
        weight[y == -1] = np.sum(y == 1) / np.sum(y == -1) * C
        return weight

    def _self_predict(self, f, r):
        """Fix w and update the solution of y^ via Eq.(3) in paper [1].
        Corresponding to line 7 of Algo. 1

        Parameters
        ----------
        f : Predicting vector

        r : The ranks of the predictions on the unlabeled data.

        Returns
        -------
        y : Updating y^
        """
        beta = 0
        u = np.size(f)
        y = np.sign(f)
        y[y == 0] = np.random.randint(1, 3, size=(np.sum(y == 0))) * 2 - 3
        rk = np.zeros((u, 1))
        ind = np.argsort(-f)
        for i in range(0, u):
            rk[ind[i]] = i

        for i in range(0, np.size(rk)):
            if (rk[i] - 1) / u <= r - beta:
                y[i] = 1

        assert np.all(y != 0)
        return y

    def _objective_value(self, w, x, y, weight):
        """Compute value of objective function.

        Patameters
        ----------
        w : array-like
            Decision functions.

        x : array-like
            GSSL values.

        y : array-like
            Values of unlabeled instances.

        weight : array-like, shape = [n_samples]
            weight of instances.

        Returns
        -------
        obj : float
            Compute value of objective function.
        """
        t = 1 - y * np.dot(x, w)
        t[t < 0] = 0
        return np.dot(np.transpose(w), w / 2) + np.dot(np.transpose(weight), t)