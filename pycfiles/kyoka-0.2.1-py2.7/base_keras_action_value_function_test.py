# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/kyoka/value_function/base_keras_action_value_function_test.py
# Compiled at: 2016-10-08 03:49:35
import os
from tests.base_unittest import BaseUnitTest
from kyoka.value_function.base_keras_action_value_function import BaseKerasActionValueFunction
from mock import Mock

class BaseKerasActionValueFunctionTest(BaseUnitTest):

    def setUp(self):
        self.func = self.TestImplementation()
        self.func.setUp()

    def test_calculate_value(self):
        state, action = (5, 7)
        self.eq(36, self.func.calculate_value(state, action))

    def test_update_function(self):
        state, action, reward = (5, 7, 10)
        delta = self.func.update_function(state, action, reward)
        self.func.model.train_on_batch.assert_called_with(35, reward)
        self.eq(2, delta)
        delta = self.func.update_function(state, action, reward)
        self.eq(0, delta)

    def test_save_model_weights(self):
        filepath = 'hoge'
        self.func.save_model_weights(filepath)
        self.func.model.save_weights.assert_called_with(filepath)

    def test_load_model_weights(self):
        filepath = 'hoge'
        self.func.load_model_weights(filepath)
        self.func.model.load_weights.assert_called_with(filepath)

    class TestImplementation(BaseKerasActionValueFunction):

        def generate_model(self):
            model = Mock()
            model.train_on_batch.return_value = [1, 2]
            return model

        def transform_state_action_into_input(self, state, action):
            return state * action

        def predict_value(self, model, X):
            return X + 1

        def fetch_training_metric(self, metrics):
            return metrics[1]