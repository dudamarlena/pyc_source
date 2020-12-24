# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: robotreviewer/classifier.py
# Compiled at: 2016-02-06 20:44:32
"""
Lightweight classifier class for linear models trained elsewhere
Requires use of 2^26 (sparse) hashing vectorizer, which (at the
moment) is used for all RobotReviewer models.

Loads 'rbt' model files, which are custom for RobotReviewer. These
are gzipped HDF-5 files which contain the model coefficients and
intercepts in sparse (csr) format. This allows very large models
(often several gigabytes in memory uncompressed) to be loaded
reasonably quickly, and makes for feasible memory usage.
"""
from scipy.sparse import csr_matrix
import hickle, numpy as np, scipy

class MiniClassifier:
    """
    Lightweight classifier
    Does only binary prediction using externally trained data
    """

    def __init__(self, filename):
        raw_data = np.load(filename)
        self.coef = csr_matrix((raw_data['data'], raw_data['indices'], raw_data['indptr']), shape=(1,
                                                                                                   67108864)).todense().A1
        self.intercept = raw_data['intercept']

    def decision_function(self, X):
        scores = X.dot(self.coef.T) + self.intercept
        return scores

    def predict(self, X):
        scores = self.decision_function(X)
        return (scores > 0).astype(np.int)


def main():
    pass


if __name__ == '__main__':
    main()