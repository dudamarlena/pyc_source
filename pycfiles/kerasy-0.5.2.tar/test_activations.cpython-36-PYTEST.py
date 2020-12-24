# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/test_activations.py
# Compiled at: 2020-05-13 02:37:00
# Size of source mod 2**32: 1374 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy as np
from kerasy.models import Sequential
from kerasy.layers import Input, Conv2D, Dense
conv_input_shape = (28, 28, 1)
dense_input_shape = (10, )
conv_input = np.expand_dims(np.ones(shape=conv_input_shape), axis=0)
dense_input = np.expand_dims(np.ones(shape=dense_input_shape), axis=0)

def _test_activation_conv(activation):
    model = Sequential()
    model.add(Input(input_shape=conv_input_shape))
    model.add(Conv2D(3, activation=activation))
    model.compile(loss='mse', optimizer='adam')
    model.predict(conv_input)


def _test_activation_dense(activation):
    model = Sequential()
    model.add(Input(input_shape=dense_input_shape))
    model.add(Dense(3, activation=activation))
    model.compile(loss='mse', optimizer='adam')
    model.predict(dense_input)


def test_linear():
    _test_activation_conv(activation='linear')
    _test_activation_dense(activation='linear')


def test_softmax():
    _test_activation_conv(activation='softmax')
    _test_activation_dense(activation='softmax')


def test_tanh():
    _test_activation_conv(activation='tanh')
    _test_activation_dense(activation='tanh')


def test_relu():
    _test_activation_conv(activation='relu')
    _test_activation_dense(activation='relu')


def test_sigmoid():
    _test_activation_conv(activation='sigmoid')
    _test_activation_dense(activation='sigmoid')