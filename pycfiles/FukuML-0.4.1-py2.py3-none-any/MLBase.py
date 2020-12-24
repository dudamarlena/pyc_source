# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fukuball/Projects/fuku-ml/FukuML/MLBase.py
# Compiled at: 2016-12-10 12:07:28
from abc import ABCMeta, abstractmethod
import numpy as np, FukuML.Utility as utility

class Learner(object):
    __metaclass__ = ABCMeta
    status = 'empty'
    train_X = []
    train_Y = []
    W = []
    data_num = 0
    data_demension = 0
    test_X = []
    test_Y = []
    feature_transform_mode = 'polynomial'
    feature_transform_degree = 1

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def load_train_data(self, input_data_file=''):
        pass

    @abstractmethod
    def load_test_data(self, input_data_file=''):
        pass

    def set_feature_transform(self, mode='polynomial', degree=1):
        """
        Transform data feature to high level
        """
        if self.status != 'load_train_data':
            print 'Please load train data first.'
            return self.train_X
        self.feature_transform_mode = mode
        self.feature_transform_degree = degree
        self.train_X = self.train_X[:, 1:]
        self.train_X = utility.DatasetLoader.feature_transform(self.train_X, self.feature_transform_mode, self.feature_transform_degree)
        return self.train_X

    def set_param(self):
        pass

    @abstractmethod
    def init_W(self):
        pass

    @abstractmethod
    def score_function(self, x, W):
        pass

    @abstractmethod
    def error_function(self, y_prediction, y_truth):
        pass

    def calculate_avg_error(self, X, Y, W):
        """
        Calculate avg error from X, Y, W
        """
        data_num = len(Y)
        error_num = 0
        for i in range(data_num):
            error_num = error_num + self.error_function(self.score_function(X[i], W), Y[i])

        avg_error = error_num / float(data_num)
        return avg_error

    def calculate_test_data_avg_error(self):
        """
        Calculate test data avg error
        """
        avg_error = self.calculate_avg_error(self.test_X, self.test_Y, self.W)
        return avg_error

    @abstractmethod
    def train(self):
        pass

    def prediction(self, input_data='', mode='test_data'):
        """
        Make prediction
        input test data
        output the prediction
        """
        prediction = {}
        if self.status != 'train':
            print 'Please load train data and init W then train the W first.'
            return prediction
        else:
            if input_data == '':
                print 'Please input test data for prediction.'
                return prediction
            else:
                if mode == 'future_data':
                    data = input_data.split()
                    input_data_x = [ float(v) for v in data ]
                    input_data_x = utility.DatasetLoader.feature_transform(np.array(input_data_x).reshape(1, -1), self.feature_transform_mode, self.feature_transform_degree)
                    input_data_x = np.ravel(input_data_x)
                    prediction = self.score_function(input_data_x, self.W)
                    return {'input_data_x': input_data_x, 'input_data_y': None, 'prediction': prediction}
                data = input_data.split()
                input_data_x = [ float(v) for v in data[:-1] ]
                input_data_x = utility.DatasetLoader.feature_transform(np.array(input_data_x).reshape(1, -1), self.feature_transform_mode, self.feature_transform_degree)
                input_data_x = np.ravel(input_data_x)
                input_data_y = float(data[(-1)])
                prediction = self.score_function(input_data_x, self.W)
                return {'input_data_x': input_data_x, 'input_data_y': input_data_y, 'prediction': prediction}

            return