# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nn_wtf/neural_network_graph_mixin.py
# Compiled at: 2016-12-17 04:58:38
import tensorflow as tf
__author__ = 'Lene Preuss <lene.preuss@gmail.com>'
DEFAULT_TRAIN_DIR = '.nn_wtf-data'

class NeuralNetworkGraphMixin:

    def __init__(self, session, train_dir=DEFAULT_TRAIN_DIR):
        assert isinstance(session, tf.Session), 'session must be set when initializing ' + type(self).__name__
        self.session = session
        self.train_dir = ensure_is_dir(train_dir)


def ensure_is_dir(train_dir_string):
    if not train_dir_string[(-1)] == '/':
        train_dir_string += '/'
    return train_dir_string