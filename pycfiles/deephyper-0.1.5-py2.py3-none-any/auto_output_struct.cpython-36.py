# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/space/struct/auto_output_struct.py
# Compiled at: 2019-07-11 14:24:06
# Size of source mod 2**32: 2388 bytes
from collections.abc import Iterable
from functools import reduce
import networkx as nx
from tensorflow import keras
from tensorflow.python.keras.utils.vis_utils import model_to_dot
from deephyper.core.exceptions.nas.struct import InputShapeOfWrongType, NodeAlreadyAdded, StructureHasACycle, WrongSequenceToSetOperations
from deephyper.search.nas.model.space.node import ConstantNode, Node, VariableNode
from deephyper.search.nas.model.space.op.basic import Tensor
from deephyper.search.nas.model.space.op.merge import Concatenate
from deephyper.search.nas.model.space.op.op1d import Identity
from deephyper.search.nas.model.space.struct import DirectStructure

class AutoOutputStructure(DirectStructure):
    __doc__ = "An AutoOutputStructure represents a search space of neural networks.\n\n    Args:\n        input_shape (list(tuple(int))): list of shapes of all inputs.\n        output_shape (tuple(int)): shape of output.\n        regression (bool): if ``True`` the output will be a simple ``tf.keras.layers.Dense(output_shape[0])`` layer as the output layer. if ``False`` the output will be ``tf.keras.layers.Dense(output_shape[0], activation='softmax').\n\n    Raises:\n        InputShapeOfWrongType: [description]\n    "

    def __init__(self, input_shape, output_shape, regression, *args, **kwargs):
        super().__init__(input_shape, output_shape)
        self.regression = regression

    def create_model(self):
        """Create the tensors corresponding to the structure.

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
          activation=activation)(output_tensor)
        input_tensors = [inode._tensor for inode in self.input_nodes]
        self._model = keras.Model(inputs=input_tensors, outputs=output_tensor)
        return keras.Model(inputs=input_tensors, outputs=output_tensor)