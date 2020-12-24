# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/space/auto_keras_search_space.py
# Compiled at: 2019-09-05 10:20:48
# Size of source mod 2**32: 2270 bytes
from collections.abc import Iterable
from functools import reduce
import networkx as nx, tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras.utils.vis_utils import model_to_dot
from deephyper.core.exceptions.nas.space import InputShapeOfWrongType, NodeAlreadyAdded, StructureHasACycle, WrongSequenceToSetOperations
from . import KSearchSpace
from .node import ConstantNode, Node, VariableNode
from op.basic import Tensor
from op.merge import Concatenate
from op.op1d import Identity

class AutoKSearchSpace(KSearchSpace):
    __doc__ = "An AutoKSearchSpace represents a search space of neural networks.\n\n    Args:\n        input_shape (list(tuple(int))): list of shapes of all inputs.\n        output_shape (tuple(int)): shape of output.\n        regression (bool): if ``True`` the output will be a simple ``tf.keras.layers.Dense(output_shape[0])`` layer as the output layer. if ``False`` the output will be ``tf.keras.layers.Dense(output_shape[0], activation='softmax')``.\n\n    Raises:\n        InputShapeOfWrongType: [description]\n    "

    def __init__(self, input_shape, output_shape, regression, *args, **kwargs):
        super().__init__(input_shape, output_shape)
        self.regression = regression

    def create_model(self):
        """Create the tensors corresponding to the search_space.

        Returns:
            The output tensor.
        """
        if self.regression:
            activation = None
        else:
            activation = 'softmax'
        output_tensor = self.create_tensor_aux(self.graph, self.output_node)
        if len(output_tensor.get_shape()) > 2:
            output_tensor = keras.layers.Flatten()(output_tensor)
        output_tensor = keras.layers.Dense((self.output_shape[0]),
          activation=activation, kernel_initializer=tf.keras.initializers.glorot_uniform(seed=(self.seed)))(output_tensor)
        input_tensors = [inode._tensor for inode in self.input_nodes]
        self._model = keras.Model(inputs=input_tensors, outputs=output_tensor)
        return keras.Model(inputs=input_tensors, outputs=output_tensor)