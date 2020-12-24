# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mantis_ml/modules/supervised_learn/classifiers/ensemble_lib.py
# Compiled at: 2019-11-14 14:47:11
# Size of source mod 2**32: 2841 bytes
import numpy as np
from sklearn.model_selection import KFold
from keras.optimizers import Adam
rf_params = {'n_jobs':-1, 
 'n_estimators':100, 
 'max_features':'auto', 
 'max_depth':15, 
 'min_samples_leaf':2, 
 'min_samples_split':4, 
 'warm_start':False, 
 'verbose':0}
et_params = {'n_jobs':-1, 
 'n_estimators':100, 
 'max_features':'auto', 
 'max_depth':15, 
 'min_samples_leaf':2, 
 'min_samples_split':5, 
 'verbose':0}
svc_params = {'C':0.01, 
 'kernel':'linear', 
 'gamma':'auto', 
 'probability':True, 
 'shrinking':True}
gb_params = {'n_estimators':500, 
 'max_features':'sqrt', 
 'max_depth':20, 
 'min_samples_leaf':4, 
 'min_samples_split':5, 
 'verbose':0}
xgb_params = {'learning_rate':0.01, 
 'n_estimators':300, 
 'max_depth':5, 
 'min_child_weight':3, 
 'gamma':0, 
 'subsample':0.8, 
 'colsample_bytree':0.8, 
 'objective':'binary:logistic', 
 'nthread':-1, 
 'scale_pos_weight':1}
dnn_params = {'regl':0.01, 
 'hidden_layer_nodes':[
  32, 32], 
 'add_dropout':True, 
 'dropout_ratio':0.3, 
 'optimizer':'Adagrad', 
 'epochs':50, 
 'batch_size':128, 
 'verbose':False, 
 'make_plots':False}
ensemble_clf_params = {'RandomForestClassifier':rf_params, 
 'ExtraTreesClassifier':et_params, 
 'GradientBoostingClassifier':gb_params, 
 'SVC':svc_params, 
 'DNN':dnn_params, 
 'XGBoost':xgb_params}

def get_oof(clf, X_train, y_train, X_test, n_splits=5):
    """
    Train on out-of-fold (out-of-bag) dataset
    :param clf: 
    :param X_train: 
    :param y_train: 
    :param X_test: 
    :param seed: 
    :param n_splits: 
    :return: 
    """
    n_train = len(X_train)
    n_test = len(X_test)
    cv = KFold(n_splits=n_splits, random_state=0)
    kf = cv.split(X_train, y_train)
    oof_train = np.zeros((n_train,))
    oof_test = np.zeros((n_test,))
    oof_test_skf = np.empty((n_splits, n_test))
    for i, (train_index, test_index) in enumerate(kf):
        x_tr = X_train[train_index]
        y_tr = y_train[train_index]
        x_te = X_train[test_index]
        clf.train(x_tr, y_tr)
        oof_train[test_index] = clf.predict(x_te)
        oof_test_skf[i, :] = clf.predict(X_test)

    oof_test[:] = oof_test_skf.mean(axis=0)
    return (
     oof_train.reshape(-1, 1), oof_test.reshape(-1, 1))