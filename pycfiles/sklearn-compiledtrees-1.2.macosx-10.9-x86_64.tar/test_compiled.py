# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tulloch/.virtualenvs/sklearn-dev/lib/python2.7/site-packages/compiledtrees/tests/test_compiled.py
# Compiled at: 2014-04-04 11:22:35
from sklearn import ensemble, tree
from compiledtrees.compiled import CompiledRegressionPredictor
from sklearn.utils.testing import assert_array_almost_equal, assert_raises, assert_equal
import numpy as np
REGRESSORS = {
 ensemble.GradientBoostingRegressor,
 ensemble.RandomForestRegressor,
 tree.DecisionTreeRegressor}
CLASSIFIERS = {
 ensemble.GradientBoostingClassifier,
 ensemble.RandomForestClassifier,
 tree.DecisionTreeClassifier}

def assert_equal_predictions(cls, X, y):
    clf = cls()
    clf.fit(X, y)
    compiled = CompiledRegressionPredictor(clf)
    assert_array_almost_equal(clf.predict(X), compiled.predict(X))


def test_rejects_unfitted_regressors_as_compilable():
    for cls in REGRESSORS:
        assert_equal(CompiledRegressionPredictor.compilable(cls()), False)
        assert_raises(ValueError, CompiledRegressionPredictor, cls())


def test_rejects_classifiers_as_compilable():
    for cls in CLASSIFIERS:
        assert_equal(CompiledRegressionPredictor.compilable(cls()), False)
        assert_raises(ValueError, CompiledRegressionPredictor, cls())


def test_correct_predictions():
    num_features = 100
    num_examples = 100
    X = np.random.normal(size=(num_examples, num_features))
    y = np.random.choice([-1, 1], size=num_examples)
    for cls in REGRESSORS:
        assert_equal_predictions(cls, X, y)