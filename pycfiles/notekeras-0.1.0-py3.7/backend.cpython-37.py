# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/backend.py
# Compiled at: 2020-04-22 04:46:57
# Size of source mod 2**32: 1005 bytes
import os
from tensorflow import keras
from tensorflow.keras.backend import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
__all__ = [
 'keras', 'utils', 'activations', 'applications', 'backend', 'datasets',
 'layers', 'preprocessing', 'wrappers', 'callbacks', 'constraints', 'initializers',
 'metrics', 'models', 'losses', 'optimizers', 'regularizers',
 'Dense', 'plot_model',
 'Layer', 'Model']
utils = keras.utils
activations = keras.activations
applications = keras.applications
backend = keras.backend
datasets = keras.datasets
preprocessing = keras.preprocessing
wrappers = keras.wrappers
callbacks = keras.callbacks
constraints = keras.constraints
initializers = keras.initializers
metrics = keras.metrics
models = keras.models
losses = keras.losses
optimizers = keras.optimizers
regularizers = keras.regularizers
plot_model = keras.utils.plot_model
layers = keras.layers
Layer = layers.Layer
Dense = layers.Dense
Model = keras.models.Model