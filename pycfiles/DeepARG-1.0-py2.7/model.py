# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deeparg/predict/bin/model.py
# Compiled at: 2018-12-06 14:23:01
from lasagne import layers
import lasagne

def model(input_size, output_size):
    return [
     (
      layers.InputLayer, {'shape': (None, input_size)}),
     (
      layers.DenseLayer, {'num_units': 2000}),
     (
      layers.DropoutLayer, {'p': 0.5}),
     (
      layers.DenseLayer, {'num_units': 1000}),
     (
      layers.DropoutLayer, {'p': 0.5}),
     (
      layers.DenseLayer, {'num_units': 500}),
     (
      layers.DropoutLayer, {'p': 0.5}),
     (
      layers.DenseLayer, {'num_units': 100}),
     (
      layers.DenseLayer,
      {'num_units': output_size, 'nonlinearity': lasagne.nonlinearities.softmax})]