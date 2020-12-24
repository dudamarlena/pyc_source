# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ss/tensorspace-converter/tensorspacejs/tf/tensorflow_conversion.py
# Compiled at: 2019-03-19 05:53:03
"""
@author syt123450 / https://github.com/syt123450
"""
import os
from tf.saved_model import preprocess_saved_model
from tf.frozen_model import preprocess_frozen_model
from tf.keras_model import preprocess_hdf5_combined_model, preprocess_hdf5_separated_model

def show_tf_model_summary(path_model):
    print path_model
    print 'tensorflow Model Summary...'


def preprocess_tensorflow_model(input_format, path_model, path_output_dir, output_node_names=None):
    os.makedirs(path_output_dir, exist_ok=True)
    if input_format == 'tf_saved':
        preprocess_saved_model(path_model, path_output_dir, output_node_names)
    elif input_format == 'tf_frozen':
        preprocess_frozen_model(path_model, path_output_dir, output_node_names)
    elif input_format == 'tf_keras':
        preprocess_hdf5_combined_model(path_model, path_output_dir, output_node_names)
    elif input_format == 'tf_keras_separated':
        preprocess_hdf5_separated_model(path_model, path_output_dir, output_node_names)
    else:
        print 'Preprocess nothing for tensorflow model.'
    print 'Mission Complete!!!'