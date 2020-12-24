# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datascienceutils/modelStacking.py
# Compiled at: 2017-11-27 01:36:20
# Size of source mod 2**32: 937 bytes
from .utils import *

def trainVotingClassifier(dataframe, target, **kwargs):
    from sklearn.linear_model import LogisticRegression
    from sklearn.naive_bayes import GaussianNB
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.ensemble import VotingClassifier
    clf1 = get_model_obj('knn', random_state=123)
    clf2 = get_model_obj('randomForest', random_state=123)
    clf3 = get_model_obj(*('gaussianNB', ), **kwargs)
    eclf = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='soft',
      weights=[
     1, 1, 5])
    return eclf


def predictVotingClassify(model, dataframe):
    probas = [c.fit(dataframe, target).predict_proba(dataframe) for c in model.classifiers]