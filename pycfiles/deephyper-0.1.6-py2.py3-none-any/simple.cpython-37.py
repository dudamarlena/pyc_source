# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/baseline/simple.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 451 bytes
import tensorflow as tf
from ..space import AutoKSearchSpace
from space.node import VariableNode
from space.op.op1d import Dense

def create_search_space(input_shape=(2,), output_shape=(1,), **kwargs):
    struct = AutoKSearchSpace(input_shape, output_shape, regression=True)
    vnode1 = VariableNode()
    for i in range(1, 11):
        vnode1.add_op(Dense(i, tf.nn.relu))

    struct.connect(struct.input_nodes[0], vnode1)
    return struct