# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mtcnn/network.py
# Compiled at: 2019-11-14 12:16:36
# Size of source mod 2**32: 3935 bytes
import tensorflow as tf
__author__ = 'Iván de Paz Centeno'

class Network(object):

    def __init__(self, session, trainable: bool=True):
        """
        Initializes the network.
        :param trainable: flag to determine if this network should be trainable or not.
        """
        self._session = session
        self._Network__trainable = trainable
        self._Network__layers = {}
        self._Network__last_layer_name = None
        with tf.compat.v1.variable_scope(self.__class__.__name__.lower()):
            self._config()

    def _config(self):
        """
        Configures the network layers.
        It is usually done using the LayerFactory() class.
        """
        raise NotImplementedError('This method must be implemented by the network.')

    def add_layer(self, name: str, layer_output):
        """
        Adds a layer to the network.
        :param name: name of the layer to add
        :param layer_output: output layer.
        """
        self._Network__layers[name] = layer_output
        self._Network__last_layer_name = name

    def get_layer(self, name: str=None):
        """
        Retrieves the layer by its name.
        :param name: name of the layer to retrieve. If name is None, it will retrieve the last added layer to the
        network.
        :return: layer output
        """
        if name is None:
            name = self._Network__last_layer_name
        return self._Network__layers[name]

    def is_trainable(self):
        """
        Getter for the trainable flag.
        """
        return self._Network__trainable

    def set_weights(self, weights_values: dict, ignore_missing=False):
        """
        Sets the weights values of the network.
        :param weights_values: dictionary with weights for each layer
        """
        network_name = self.__class__.__name__.lower()
        with tf.compat.v1.variable_scope(network_name):
            for layer_name in weights_values:
                with tf.compat.v1.variable_scope(layer_name, reuse=True):
                    for param_name, data in weights_values[layer_name].items():
                        try:
                            var = tf.compat.v1.get_variable(param_name, use_resource=False)
                            self._session.run(var.assign(data))
                        except ValueError:
                            if not ignore_missing:
                                raise

    def feed(self, image):
        """
        Feeds the network with an image
        :param image: image (perhaps loaded with CV2)
        :return: network result
        """
        network_name = self.__class__.__name__.lower()
        with tf.compat.v1.variable_scope(network_name):
            return self._feed(image)

    def _feed(self, image):
        raise NotImplementedError('Method not implemented.')