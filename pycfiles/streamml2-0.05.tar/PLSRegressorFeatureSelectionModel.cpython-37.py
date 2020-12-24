# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\bmccs\Desktop\streamml2_test\streamml2\streamline\feature_selection\models\regressors\PLSRegressorFeatureSelectionModel.py
# Compiled at: 2019-01-21 12:31:01
# Size of source mod 2**32: 922 bytes
from sklearn.cross_decomposition import PLSRegression
from ...AbstractFeatureSelectionModel import AbstractFeatureSelectionModel

class PLSRegressorFeatureSelectionModel(AbstractFeatureSelectionModel):

    def __init__(self, X, y, params, verbose):
        AbstractFeatureSelectionModel.__init__(self, 'plsr', X, y, params, verbose)

    def execute(self):
        super(PLSRegressorFeatureSelectionModel, self).execute()
        pls_model = PLSRegression()
        pls_out = pls_model.fit(self._X, self._y)
        return abs(pls_out.coef_.flatten())