# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/baseline/simple_deep.py
# Compiled at: 2019-07-11 14:24:06
# Size of source mod 2**32: 600 bytes
import tensorflow as tf
from deephyper.search.nas.model.space.struct import AutoOutputStructure
from deephyper.search.nas.model.space.node import VariableNode
from deephyper.search.nas.model.space.op.op1d import Dense

def create_structure(input_shape=(2,), output_shape=(1,), **kwargs):
    struct = AutoOutputStructure(input_shape, output_shape, regression=True)
    prev_node = struct.input_nodes[0]
    for _ in range(20):
        vnode = VariableNode()
        for i in range(1, 11):
            vnode.add_op(Dense(i, tf.nn.relu))

        struct.connect(prev_node, vnode)

    return struct