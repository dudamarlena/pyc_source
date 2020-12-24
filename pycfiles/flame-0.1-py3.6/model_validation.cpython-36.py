# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/stats/model_validation.py
# Compiled at: 2018-06-20 09:13:36
# Size of source mod 2**32: 11887 bytes
import numpy as np, matplotlib.pyplot as plt
from math import sqrt
import sys, pandas as pd, copy, warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
from sklearn.model_selection import learning_curve
from sklearn.model_selection import *
from sklearn.model_selection import LeavePOut
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import LeaveOneOut
from nonconformist.base import ClassifierAdapter, RegressorAdapter
from nonconformist.icp import IcpClassifier, IcpRegressor
from nonconformist.nc import MarginErrFunc
from nonconformist.nc import ClassifierNc, RegressorNc
from nonconformist.nc import AbsErrorErrFunc, SignErrorErrFunc, RegressorNormalizer
from nonconformist.acp import AggregatedCp
from nonconformist.acp import BootstrapSampler, CrossSampler, RandomSubSampler
from nonconformist.acp import BootstrapConformalClassifier
from nonconformist.acp import CrossConformalClassifier
from nonconformist.evaluation import class_mean_errors, class_one_c
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from nonconformist.base import ClassifierAdapter
from nonconformist.icp import IcpClassifier
from nonconformist.nc import ClassifierNc, MarginErrFunc
from nonconformist.evaluation import cross_val_score as conformal_cross_val_score
from nonconformist.evaluation import ClassIcpCvHelper, RegIcpCvHelper
from nonconformist.evaluation import class_avg_c, class_mean_errors
from nonconformist.evaluation import reg_mean_errors, reg_median_size
from nonconformist.evaluation import reg_mean_size
from nonconformist.evaluation import class_mean_errors

def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None, n_jobs=1, train_sizes=np.linspace(0.1, 1.0, 5)):
    """
    Generate a simple plot of the test and training learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:
          - None, to use the default 3-fold cross-validation,
          - integer, to specify the number of folds.
          - An object to be used as a cross-validation generator.
          - An iterable yielding train/test splits.

        For integer/None inputs, if ``y`` is binary or multiclass,
        :class:`StratifiedKFold` used. If the estimator is not a classifier
        or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validators that can be used here.

    n_jobs : integer, optional
        Number of jobs to run in parallel (default 1).
    """
    n_jobs = 1
    plt.figure()
    plt.title(title)
    if ylim is not None:
        (plt.ylim)(*ylim)
    plt.xlabel('Training examples')
    plt.ylabel('Score')
    train_sizes, train_scores, test_scores = learning_curve(estimator,
      X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()
    plt.fill_between(train_sizes, (train_scores_mean - train_scores_std), (train_scores_mean + train_scores_std),
      alpha=0.1, color='r')
    plt.fill_between(train_sizes, (test_scores_mean - test_scores_std), (test_scores_mean + test_scores_std),
      alpha=0.1, color='g')
    plt.plot(train_sizes, train_scores_mean, 'o-', color='r', label='Training score')
    plt.plot(train_sizes, test_scores_mean, 'o-', color='g', label='Cross-validation score')
    plt.legend(loc='best')
    return plt


def getCrossVal(cv, rs, n, p):
    kfold = KFold(n_splits=n, random_state=rs, shuffle=False)
    gkfold = GroupKFold(n_splits=n)
    stkfold = StratifiedKFold(n_splits=n, random_state=rs, shuffle=False)
    logo = LeaveOneGroupOut()
    lpgo = LeavePGroupsOut(n_groups=n)
    loo = LeaveOneOut()
    lpo = LeavePOut(int(p))
    shufsplit = ShuffleSplit(n_splits=n, random_state=rs, test_size=0.25,
      train_size=None)
    gshufplit = GroupShuffleSplit(test_size=10, n_splits=n)
    stshufsplit = StratifiedShuffleSplit(n_splits=n,
      test_size=0.5,
      random_state=0)
    psplit = PredefinedSplit(test_fold=[0, 1, -1, 1])
    tssplit = TimeSeriesSplit(n_splits=n)
    splitClass = {'kfold':kfold, 
     'gkfold':gkfold,  'stkfold':stkfold,  'logo':logo,  'lpgo':lpgo, 
     'loo':loo,  'lpo':lpo,  'shufsplit':shufsplit,  'gshufplit':gshufplit, 
     'stshufsplit':stshufsplit,  'psplit':psplit, 
     'tssplit':tssplit}
    cv = splitClass.get(str(cv))
    return cv


def CF_QualVal(X, Y, estimator, conformalSignificance):
    """ Qualitative conformal predictor validation"""
    print('Starting qualitative conformal prediction validation')
    icp = AggregatedCp(IcpClassifier(ClassifierNc(ClassifierAdapter(estimator), MarginErrFunc())), BootstrapSampler())
    Y = np.asarray(Y).reshape(-1, 1)
    loo = LeaveOneOut()
    predictions = []
    for train, test in loo.split(X):
        Xn = [X[i] for i in train]
        Yn = [Y[i] for i in train]
        Xn, mux = center(Xn)
        Xn, wgx = scale(Xn, True)
        Yn = np.asarray(Yn)
        Xout = X[test]
        Yout = Y[test[0]]
        icp.fit(Xn, Yn)
        predictions.append(icp.predict(Xout, significance=0.15))

    predictions = [x[0].tolist() for x in predictions]
    predictions = np.asarray(predictions)
    table = np.hstack((predictions, Y))
    print('Error rate: {}'.format(class_mean_errors(predictions, Y, 0.15)))
    print('Class one: ', class_one_c(predictions, Y, 0.15))
    return icp


def CF_QuanVal(X, Y, estimator, conformalSignificance):
    print('Starting quantitative conformal prediction validation')
    icp = AggregatedCp(IcpRegressor(RegressorNc(RegressorAdapter(estimator))), BootstrapSampler())
    icp.fit(X[:30], Y[:30])
    prediction = icp.predict(X[30:])
    prediction_sign = icp.predict((X[30:]), significance=0.25)
    interval = prediction_sign[:, 0] - prediction_sign[:, 1]
    print(np.mean(interval))
    print(interval)
    print('\n')
    print(prediction)
    print(prediction_sign)
    return icp


def CF_QualCal(X, Y, estimator):
    """Qualitative conformal predictor calibration"""
    acp = AggregatedCp(IcpClassifier(ClassifierNc(ClassifierAdapter(estimator), MarginErrFunc())), BootstrapSampler())
    acp.fit(X, Y)
    return acp


def CF_QuanCal(X, Y, estimator):
    acp = AggregatedCp(IcpRegressor(RegressorNc(RegressorAdapter(estimator), AbsErrorErrFunc(), RegressorNormalizer(estimator, copy.copy(estimator), AbsErrorErrFunc())), RandomSubSampler()))
    acp.fit(X, Y)
    return acp


def conformal_pred_pred(xb, conformal_pred, significance):
    prediction = conformal_pred.predict(xb, significance=significance)
    table = prediction
    return table