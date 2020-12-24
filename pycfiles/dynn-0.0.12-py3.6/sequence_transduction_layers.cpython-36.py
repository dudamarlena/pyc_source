# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dynn\layers\sequence_transduction_layers.py
# Compiled at: 2018-09-13 18:49:13
# Size of source mod 2**32: 3884 bytes
"""
Sequence transduction layers
============================

Sequence transduction layers take in a sequence of expression and transduces
them using recurrent layers
"""
from ..util import _generate_mask, _should_mask, mask_batches
from .base_layer import BaseLayer

class UnidirectionalLayer(BaseLayer):

    def __init__(self, cell):
        self.cell = cell

    def init(self, *args, **kwargs):
        """Passes its arguments to the recurrent layer"""
        (self.cell.init)(*args, **kwargs)

    def __call_(self, input_sequence, backward=False, lengths=None, left_padded=True):
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
        batch_size = input_sequence.dim()[1]
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

        state = self.cell.initial_value()
        output_sequence = []
        for step, x in enumerate(input_sequence):
            state = (self.cell)(x, *state)
            if do_masking(step + 1):
                mask = _generate_mask(step + 1, max_length, batch_size, lengths, left_padded)
                state = mask_batches(state, mask, mode='mul')
            output_sequence.append(state)

        return output_sequence