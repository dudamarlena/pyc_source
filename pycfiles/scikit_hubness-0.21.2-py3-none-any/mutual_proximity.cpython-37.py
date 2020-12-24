# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/reduction/mutual_proximity.py
# Compiled at: 2019-10-30 06:53:25
# Size of source mod 2**32: 6030 bytes
from __future__ import annotations
import warnings, numpy as np
from scipy import stats
from sklearn.utils.validation import check_is_fitted, check_consistent_length, check_array
from tqdm.auto import tqdm
from .base import HubnessReduction

class MutualProximity(HubnessReduction):
    __doc__ = " Hubness reduction with Mutual Proximity [1]_.\n\n    Parameters\n    ----------\n    method: 'normal' or 'empiric', default = 'normal'\n        Model distance distribution with 'method'.\n\n        - 'normal' or 'gaussi' model distance distributions with independent Gaussians (fast)\n        - 'empiric' or 'exact' model distances with the empiric distributions (slow)\n\n    verbose: int, default = 0\n        If verbose > 0, show progress bar.\n\n    References\n    ----------\n    .. [1] Schnitzer, D., Flexer, A., Schedl, M., & Widmer, G. (2012).\n           Local and global scaling reduce hubs in space. The Journal of Machine\n           Learning Research, 13(1), 2871–2902.\n    "

    def __init__(self, method='normal', verbose=0, **kwargs):
        (super().__init__)(**kwargs)
        self.method = method
        self.verbose = verbose

    def fit(self, neigh_dist, neigh_ind, X=None, assume_sorted=None, *args, **kwargs) -> 'MutualProximity':
        """ Fit the model using neigh_dist and neigh_ind as training data.

        Parameters
        ----------
        neigh_dist: np.ndarray, shape (n_samples, n_neighbors)
            Distance matrix of training objects (rows) against their
            individual k nearest neighbors (columns).

        neigh_ind: np.ndarray, shape (n_samples, n_neighbors)
            Neighbor indices corresponding to the values in neigh_dist.

        X: ignored

        assume_sorted: ignored
        """
        check_consistent_length(neigh_ind, neigh_dist)
        check_consistent_length(neigh_ind.T, neigh_dist.T)
        check_array(neigh_dist, force_all_finite=False)
        check_array(neigh_ind)
        self.n_train = neigh_dist.shape[0]
        if self.method in ('exact', 'empiric'):
            self.method = 'empiric'
            self.neigh_dist_train_ = neigh_dist
            self.neigh_ind_train_ = neigh_ind
        else:
            if self.method in ('normal', 'gaussi'):
                self.method = 'normal'
                self.mu_train_ = np.nanmean(neigh_dist, axis=1)
                self.sd_train_ = np.nanstd(neigh_dist, axis=1, ddof=0)
            else:
                raise ValueError(f'Mutual proximity method "{self.method}" not recognized. Try "normal" or "empiric".')
        return self

    def transform(self, neigh_dist, neigh_ind, X=None, assume_sorted=None, *args, **kwargs):
        """ Transform distance between test and training data with Mutual Proximity.

        Parameters
        ----------
        neigh_dist: np.ndarray
            Distance matrix of test objects (rows) against their individual
            k nearest neighbors among the training data (columns).

        neigh_ind: np.ndarray
            Neighbor indices corresponding to the values in neigh_dist

        X: ignored

        assume_sorted: ignored

        Returns
        -------
        hub_reduced_dist, neigh_ind
            Mutual Proximity distances, and corresponding neighbor indices

        Notes
        -----
        The returned distances are NOT sorted! If you use this class directly,
        you will need to sort the returned matrices according to hub_reduced_dist.
        Classes from :mod:`skhubness.neighbors` do this automatically.
        """
        check_is_fitted(self, ['mu_train_', 'sd_train_', 'neigh_dist_train_', 'neigh_ind_train_'], all_or_any=any)
        check_array(neigh_dist, force_all_finite='allow-nan')
        check_array(neigh_ind)
        n_test, n_indexed = neigh_dist.shape
        if n_indexed == 1:
            warnings.warn('Cannot perform hubness reduction with a single neighbor per query. Skipping hubness reduction, and returning untransformed distances.')
            return (
             neigh_dist, neigh_ind)
        else:
            hub_reduced_dist = np.empty_like(neigh_dist)
            disable_tqdm = False if self.verbose else True
            range_n_test = tqdm((range(n_test)), desc=f"MP ({self.method})",
              disable=disable_tqdm)
            if self.method == 'normal':
                mu_train = self.mu_train_
                sd_train = self.sd_train_
                for i in range_n_test:
                    j_mom = neigh_ind[i]
                    mu = np.nanmean(neigh_dist[i])
                    sd = np.nanstd((neigh_dist[i]), ddof=0)
                    p1 = stats.norm.sf(neigh_dist[i, :], mu, sd)
                    p2 = stats.norm.sf(neigh_dist[i, :], mu_train[j_mom], sd_train[j_mom])
                    hub_reduced_dist[i, :] = (1 - p1 * p2).ravel()

            else:
                if self.method == 'empiric':
                    max_ind = self.neigh_ind_train_.max()
                    for i in range_n_test:
                        dI = neigh_dist[i, :][np.newaxis, :]
                        dJ = np.zeros((dI.size, n_indexed))
                        for j in range(n_indexed):
                            tmp = np.zeros(max_ind + 1) + (self.neigh_dist_train_[(neigh_ind[(i, j)], -1)] + 1e-06)
                            tmp[self.neigh_ind_train_[neigh_ind[(i, j)]]] = self.neigh_dist_train_[neigh_ind[(i, j)]]
                            dJ[j, :] = tmp[neigh_ind[i]]

                        d = dI.T
                        hub_reduced_dist[i, :] = 1.0 - np.sum(((dI > d) & (dJ > d)), axis=1) / n_indexed

                else:
                    raise ValueError(f"Internal: Invalid method {self.method}.")
        return (hub_reduced_dist, neigh_ind)