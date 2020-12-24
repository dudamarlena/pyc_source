# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\bmccs\Desktop\streamml2\streamml2\streamline\model_selection\models\AbstractClassifierPredictiveModel.py
# Compiled at: 2019-01-25 22:37:28
# Size of source mod 2**32: 4580 bytes
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import log_loss
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.utils import shuffle
from ..AbstractPredictiveModel import *

class AbstractClassifierPredictiveModel(AbstractPredictiveModel):
    _options = [
     'auc',
     'precision',
     'recall',
     'f1',
     'accuracy',
     'kappa',
     'log_loss']
    _validation_results = None

    def __init__(self, modelType, X, y, params, nfolds, n_jobs, scoring, random_grid, n_iter, verbose):
        assert modelType == 'classifier', 'You are creating a classifier, but have not specified it to be one.'
        self._modelType = modelType
        self._y = y
        self._scoring = scoring
        AbstractPredictiveModel.__init__(self, X, params, nfolds, n_jobs, random_grid, n_iter, verbose)

    def validate(self, Xtest, ytest, metrics, verbose=False):
        assert any([isinstance(metrics, str), isinstance(metrics, list)]), 'Your classifier error metric must be a str or list'
        assert all([i in self._options for i in metrics]), 'Your clasifier error metric must be in valid: ' + ' '.join([i for i in self._options])
        self._validation_results = {}
        for m in metrics:
            if m == 'auc':
                ypred = self._model.predict(Xtest)
                self._validation_results['auc'] = roc_auc_score(ytest, ypred, average='macro')
            elif m == 'precision':
                ypred = self._model.predict(Xtest)
                self._validation_results['precision'] = precision_score(ytest, ypred, average='macro')
            elif m == 'recall':
                ypred = self._model.predict(Xtest)
                self._validation_results['recall'] = recall_score(ytest, ypred, average='macro')
            elif m == 'f1':
                ypred = self._model.predict(Xtest)
                self._validation_results['f1'] = f1_score(ytest, ypred, average='macro')
            elif m == 'accuracy':
                ypred = self._model.predict(Xtest)
                self._validation_results['accuracy'] = accuracy_score(ytest, ypred)
            elif m == 'kappa':
                ypred = self._model.predict(Xtest)
                self._validation_results['kappa'] = cohen_kappa_score(ytest, ypred)
            elif m == 'log_loss':
                print('Currently not supported: log_loss')
                raise Exception
            else:
                print(str(m) + ' not a valid classifier metric, skipping.')

        return self._validation_results

    def constructClassifier(self, model, random_grid):
        self._pipe = Pipeline([(self._code, model)])
        self._X, self._y = shuffle((self._X), (self._y), random_state=0)
        if not random_grid:
            self._grid = GridSearchCV((self._pipe), param_grid=(self._params),
              n_jobs=(self._n_jobs),
              cv=(self._nfolds))
        else:
            self._grid = RandomizedSearchCV((self._pipe), param_distributions=(self._params),
              n_jobs=(self._n_jobs),
              cv=(self._nfolds),
              n_iter=(self._n_iter))
        self._model = self._grid.fit(self._X, self._y).best_estimator_.named_steps[self._code]
        return self._model

    def getValidationResults(self):
        return self._validation_results