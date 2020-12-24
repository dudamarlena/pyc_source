# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/harness/pipeline.py
# Compiled at: 2016-09-14 09:24:20
# Size of source mod 2**32: 1441 bytes
"""setup"""
import pandas
from sklearn import *
import sklearn
from pandas import np
from typing import Iterable
from whatever.callables import DictCallable
from toolz.curried import *
from whatever import *
import time
from typing import Callable
__all__ = [
 'EasyPipeline']

class EasyPipeline(object):
    __doc__ = 'Build a pipeline from a list.'

    def __new__(self, *pipeline, n_jobs=1):
        pipeline = list(pipeline)
        for i, model in enumerate(pipeline):
            if not isinstance(model, Iterable):
                model = [
                 model]
            model = _X(model) * callables.Dispatch({Callable: preprocessing.FunctionTransformer}, default=identity) > list
            if _X(model).map(lambda x: isinstance(x, sklearn.base.ClassifierMixin)) > all:
                pipeline[i] = sklearn.ensemble.VotingClassifier(_X(model) * [
                 _X().str[this().split('(', 1)[0].f].f, identity] > list)
            else:
                pipeline[i] = sklearn.pipeline.make_union(*model)

        return sklearn.pipeline.make_pipeline(*pipeline)


shoot = EasyPipeline([
 decomposition.PCA(), decomposition.IncrementalPCA()], [
 discriminant_analysis.LinearDiscriminantAnalysis(), tree.DecisionTreeClassifier()])