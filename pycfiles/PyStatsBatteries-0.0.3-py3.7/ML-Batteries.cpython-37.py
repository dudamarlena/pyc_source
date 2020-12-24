# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PyStatsBatteries/ML-Batteries.py
# Compiled at: 2020-02-04 11:18:50
# Size of source mod 2**32: 2051 bytes
import pandas as pd
from tensorflow import keras
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.multioutput import MultiOutputRegressor
plt.style.use('ggplot')
__all__ = [
 'PrintDot', 'EnsembleTrees']

class PrintDot(keras.callbacks.Callback):
    __doc__ = '\n    Do not take care about this class\n    '

    def on_epoch_end(self, epoch):
        """
        do what it has to do
        """
        if epoch % 100 == 0:
            print('')
        print('.', end='')


class EnsembleTrees:
    __doc__ = '\n    This module provides all possibilities for using ensemble methods for Machine Learning\n    '

    def Regression_Trees(self, XTrain, YTrain, XTest, model, param_grid):
        """

        :param XTrain: a dataframe with the training set
        :param YTrain: a dataframe with the training list of outputs
        :param XTest: a dataframe with the test set
        :param model: a function with the desired model
        :param param_grid: a dictionnary with all the hyperparameters of the model
        :return: a list with the best estimator found and a dataframe with predictions
        """
        if YTrain.shape[1] > 1:
            estimator = GridSearchCV((MultiOutputRegressor(model)), param_grid=param_grid)
            estimator = estimator.fit(XTrain, YTrain)
            print('Score = ' + str(estimator.score(XTrain, YTrain)))
            best_estimator = estimator.best_estimator_
            predictions = best_estimator.predict(XTest)
        else:
            estimator = GridSearchCV(model, param_grid=param_grid, refit=True)
            estimator = estimator.fit(XTrain, YTrain)
            print('Score = ' + str(estimator.score(XTrain, YTrain)))
            print('Oob error = ' + str(1 - estimator.best_estimator_.oob_score_))
            best_estimator = estimator.best_estimator_
            predictions = best_estimator.predict(XTest)
        return (best_estimator, pd.DataFrame(predictions, columns=(YTrain.columns)))