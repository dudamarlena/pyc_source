# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dynn\layers\transduction_layers.py
# Compiled at: 2018-09-14 18:07:06
# Size of source mod 2**32: 9680 bytes
"""
Sequence transduction layers
============================

Sequence transduction layers take in a sequence of expression and runs one
layer over each input. They can be feed-forward (each input is treated
independently, eg. :py:class:`FeedForwardTransductionLayer`) or recurrent
(the output at one step depends on the output at the previous step, eg.
:py:class:`UnidirectionalLayer`).
"""
from ..util import _generate_mask, _should_mask, mask_batches
from .base_layers import BaseLayer

class FeedForwardTransductionLayer(BaseLayer):
    __doc__ = 'Feed forward transduction layer\n\n    This layer runs one cell on a sequence of inputs and returns the list of\n    outputs. Calling it is equivalent to calling:\n\n    .. code-block:: python\n\n        [layer(x) for x in input_sequence]\n\n    Args:\n        cell (:py:class:`base_layers.BaseLayer`): The\n            recurrent cell to use for transduction\n    '

    def __init__(self, layer):
        self.layer = layer

    def init(self, *args, **kwargs):
        """Passes its arguments to the recurrent layer"""
        (self.layer.init)(*args, **kwargs)

    def __call__(self, input_sequence):
        """Runs the layer over the input

        The output is a list of the output of the layer at each step

        Args:
            input_sequence (list): Input as a list of
                :py:class:`dynet.Expression` objects

        Returns:
            list: List of recurrent states (depends on the recurrent layer)
        """
        output_sequence = [self.layer(x) for x in input_sequence]
        return output_sequence


class UnidirectionalLayer(BaseLayer):
    __doc__ = 'Unidirectional transduction layer\n\n    This layer runs a recurrent cell on a sequence of inputs and produces\n    resulting the sequence of recurrent states.\n\n    Example:\n\n    .. code-block:: python\n\n        # LSTM cell\n        lstm_cell = dynn.layers.LSTM(dy.ParameterCollection(), 10, 10)\n        # Transduction layer\n        lstm = dynn.layers.UnidirectionalLayer(lstm_cell)\n        # Inputs\n        dy.renew_cg()\n        xs = [dy.random_uniform(10, batch_size=5) for _ in range(20)]\n        # Initialize layer\n        lstm.init(test=False)\n        # Transduce forward\n        states = lstm(xs)\n        # Retrieve last h\n        h_final = states[-1][0]\n\n    Args:\n        cell (:py:class:`recurrent_layers.RecurrentCell`): The\n            recurrent cell to use for transduction\n    '

    def __init__(self, cell):
        self.cell = cell

    def init(self, *args, **kwargs):
        """Passes its arguments to the recurrent layer"""
        (self.cell.init)(*args, **kwargs)

    def __call__(self, input_sequence, backward=False, lengths=None, left_padded=True):
        """Transduces the sequence using the recurrent cell.

        The output is a list of the output states at each step.
        For instance in an LSTM the output is ``(h1, c1), (h2, c2), ...``

        This assumes that all the input expression have the same batch size.
        If you batch sentences of the same length together you should pad to
        the longest sequence.

        Args:
            input_sequence (list): Input as a list of
                :py:class:`dynet.Expression` objects
            backward (bool, optional): If this is ``True`` the sequence will
                be processed from left to right. The output sequence will
                still be in the same order as the input sequence though.
            lengths (list, optional): If the expressions in the sequence are
                batched, but have different lengths, this should contain a list
                of the sequence lengths (default: ``None``)
            left_padded (bool, optional): If the input sequences have different
                lengths they must be padded to the length of longest sequence.
                Use this to specify whether the sequence is left or right
                padded.

        Returns:
            list: List of recurrent states (depends on the recurrent layer)
        """
        batch_size = input_sequence[0].dim()[1]
        max_length = len(input_sequence)
        if backward:
            input_sequence = reversed(input_sequence)
            left_padded = not left_padded
        else:
            if lengths is None:

                def do_masking(step):
                    return False

            else:

                def do_masking(step):
                    return _should_mask(step, min(lengths), max_length, left_padded)

        state = self.cell.initial_value(batch_size=batch_size)
        output_sequence = []
        for step, x in enumerate(input_sequence):
            state = (self.cell)(x, *state)
            if do_masking(step + 1):
                mask = _generate_mask(step + 1, max_length, batch_size, lengths, left_padded)
                state = mask_batches(state, mask, mode='mul')
            output_sequence.append(state)

        return output_sequence


class BidirectionalLayer(BaseLayer):
    __doc__ = 'Bidirectional transduction layer\n\n    This layer runs a recurrent cell on in each direction on a sequence of\n    inputs and produces resulting the sequence of recurrent states.\n\n    Example:\n\n    .. code-block:: python\n\n        # Parameter collection\n        pc = dy.ParameterCollection()\n        # LSTM cell\n        fwd_lstm_cell = dynn.layers.LSTM(pc, 10, 10)\n        bwd_lstm_cell = dynn.layers.LSTM(pc, 10, 10)\n        # Transduction layer\n        bilstm = dynn.layers.BidirectionalLayer(fwd_lstm_cell, bwd_lstm_cell)\n        # Inputs\n        dy.renew_cg()\n        xs = [dy.random_uniform(10, batch_size=5) for _ in range(20)]\n        # Initialize layer\n        bilstm.init(test=False)\n        # Transduce forward\n        fwd_states, bwd_states = bilstm(xs)\n        # Retrieve last h\n        fwd_h_final = fwd_states[-1][0]\n        # For the backward LSTM the final state is at\n        # the beginning of the sequence (assuming left padding)\n        bwd_h_final = fwd_states[0][0]\n\n    Args:\n        forward_cell (:py:class:`recurrent_layers.RecurrentCell`):The\n            recurrent cell to use for forward transduction\n        backward_cell (:py:class:`recurrent_layers.RecurrentCell`): The\n            recurrent cell to use for backward transduction\n    '

    def __init__(self, forward_cell, backward_cell):
        self.forward_transductor = UnidirectionalLayer(forward_cell)
        self.backward_transductor = UnidirectionalLayer(backward_cell)

    def init(self, *args, **kwargs):
        """Passes its arguments to the recurrent layers"""
        (self.forward_transductor.init)(*args, **kwargs)
        (self.backward_transductor.init)(*args, **kwargs)

    def __call__(self, input_sequence, lengths=None, left_padded=True):
        """Transduces the sequence in both directions

        The output is a tuple ``forward_states, backward_states``  where each
        ``forward_states`` is a list of the output states of the forward
        recurrent cell at each step (and ``backward_states`` for the backward
        cell). For instance in a BiLSTM the output is
        ``[(fwd_h1, fwd_c1), ...], [(bwd_h1, bwd_c1), ...]``

        This assumes that all the input expression have the same batch size.
        If you batch sentences of the same length together you should pad to
        the longest sequence.

        Args:
            input_sequence (list): Input as a list of
                :py:class:`dynet.Expression` objects
            lengths (list, optional): If the expressions in the sequence are
                batched, but have different lengths, this should contain a list
                of the sequence lengths (default: ``None``)
            left_padded (bool, optional): If the input sequences have different
                lengths they must be padded to the length of longest sequence.
                Use this to specify whether the sequence is left or right
                padded.

        Returns:
            tuple: List of forward and backward recurrent states
                (depends on the recurrent layer)
        """
        forward_states = self.forward_transductor(input_sequence,
          lengths=lengths,
          backward=False,
          left_padded=left_padded)
        backward_states = self.backward_transductor(input_sequence,
          lengths=lengths,
          backward=True,
          left_padded=left_padded)
        return (
         forward_states, backward_states)