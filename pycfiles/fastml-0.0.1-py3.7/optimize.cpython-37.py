# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\fastml\optimize.py
# Compiled at: 2019-10-19 11:02:08
# Size of source mod 2**32: 3418 bytes
import os, numpy as np, pandas as pd, lightgbm
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, validation_curve
import bayes_opt, hyperopt
import matplotlib.pyplot as plt

class Optimize:

    def __init__(self, X, y):
        self.X = X
        self.y = y

    def _estimator(self, num_leaves, max_depth, learning_rate, n_estimators, **kwargs):
        return (lightgbm.LGBMClassifier)(boosting_type='gbdt', 
         num_leaves=int(num_leaves), 
         max_depth=int(max_depth), 
         learning_rate=float(learning_rate), 
         n_estimators=int(n_estimators), **kwargs)

    def predictModel(self, X, y, param):
        model = (self._estimator)(**param)
        model.fit(X, y)
        return model

    def cv(self, num_leaves, max_depth, learning_rate, n_estimators, **kwargs):
        return cross_val_score(estimator=(self._estimator)(num_leaves, max_depth, learning_rate, n_estimators, **kwargs),
          X=(self.X),
          y=(self.y),
          cv=5,
          scoring='accuracy').mean()

    def v_cv(self, space):
        return -(self.cv)(**space)

    def bestLine(self, params):
        return (self.cv)(**params)

    def baseLine(self, boosting_type='gbdt', **kwargs):
        base_model = (lightgbm.LGBMClassifier)(boosting_type=boosting_type, **kwargs)
        return cross_val_score(base_model, (self.X), (self.y), cv=5, scoring='accuracy').mean()

    def bayesOpt(self, opt_alg='ucb', opt_freq=25):
        bo = bayes_opt.BayesianOptimization(f=(self.cv),
          pbounds={'num_leaves':(31, 255), 
         'max_depth':(5, 8), 
         'learning_rate':(0.001, 0.1), 
         'n_estimators':(50, 800)})
        bo.maximize(init_points=5, n_iter=opt_freq, acq=opt_alg)
        return bo.max

    def hyperOpt(self, opt_alg='tpe', opt_freq=25):
        ho_params = hyperopt.fmin(fn=(self.v_cv),
          space={'num_leaves':hyperopt.hp.quniform('num_leaves', 31, 255, 1), 
         'max_depth':hyperopt.hp.quniform('max_depth', 3, 9, 1), 
         'learning_rate':hyperopt.hp.uniform('learning_rate', 0.001, 0.1), 
         'n_estimators':hyperopt.hp.quniform('n_estimators', 50, 800, 1)},
          algo=(hyperopt.partial(eval('hyperopt.{}.suggest'.format(opt_alg)))),
          max_evals=opt_freq,
          verbose=2)
        return {'target':self.bestLine(ho_params), 
         'params':ho_params}

    def cvCurvePlot(self, **kwargs):
        xx, yy = validation_curve(**kwargs)
        print(xx)
        print(yy)
        plt.plot(list(range(len(xx))), [ix.mean() for ix in xx])
        plt.plot(list(range(len(xx))), [iy.mean() for iy in yy])
        plt.show()