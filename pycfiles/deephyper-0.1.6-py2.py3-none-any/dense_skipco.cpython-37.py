# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/baseline/dense_skipco.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 1641 bytes
import collections, tensorflow as tf
from ..space import AutoKSearchSpace
from space.node import ConstantNode, VariableNode
from space.op.basic import Tensor
from space.op.connect import Connect
from space.op.merge import AddByProjecting
from space.op.op1d import Dense, Identity

def add_dense_to_(node):
    node.add_op(Identity())
    activations = [
     None, tf.nn.relu, tf.nn.tanh, tf.nn.sigmoid]
    for units in range(16, 97, 16):
        for activation in activations:
            node.add_op(Dense(units=units, activation=activation))


def create_search_space(input_shape=(10,), output_shape=(7,), num_layers=10, *args, **kwargs):
    arch = AutoKSearchSpace(input_shape, output_shape, regression=True)
    source = prev_input = arch.input_nodes[0]
    anchor_points = collections.deque([source], maxlen=3)
    for _ in range(num_layers):
        vnode = VariableNode()
        add_dense_to_(vnode)
        arch.connect(prev_input, vnode)
        cell_output = vnode
        cmerge = ConstantNode()
        cmerge.set_op(AddByProjecting(arch, [cell_output], activation='relu'))
        for anchor in anchor_points:
            skipco = VariableNode()
            skipco.add_op(Tensor([]))
            skipco.add_op(Connect(arch, anchor))
            arch.connect(skipco, cmerge)

        prev_input = cmerge
        anchor_points.append(prev_input)

    return arch