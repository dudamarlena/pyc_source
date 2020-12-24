# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/rnn/rnn.py
# Compiled at: 2017-05-19 06:10:34
# Size of source mod 2**32: 1309 bytes
import tensorflow as tf
from . import cell
from ..util import func_scope
_DEFAULT_CELL = cell.gru
__all__ = [
 'rnn', 'bidirectional_rnn']

@func_scope()
def rnn(inputs, output_size, *, sequence_length=None, cell=_DEFAULT_CELL, output_state=False):
    outputs, state = tf.nn.dynamic_rnn((cell(output_size)),
      inputs,
      sequence_length=sequence_length,
      dtype=(inputs.dtype),
      swap_memory=True)
    if output_state:
        return _unpack_state_tuple(state)
    else:
        return outputs


@func_scope()
def bidirectional_rnn(inputs, output_size, *, sequence_length=None, cell=_DEFAULT_CELL, output_state=False):

    def create_cell():
        return cell(output_size)

    outputs, states = tf.nn.bidirectional_dynamic_rnn((create_cell()),
      (create_cell()),
      inputs,
      sequence_length=sequence_length,
      dtype=(inputs.dtype),
      swap_memory=True)
    if output_state:
        return tf.concat([_unpack_state_tuple(state) for state in states], 1)
    else:
        return tf.concat(outputs, 2)


@func_scope()
def _unpack_state_tuple(state):
    if isinstance(state, tf.nn.rnn_cell.LSTMStateTuple):
        return state.h
    else:
        return state