# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/layer/inputs.py
# Compiled at: 2019-11-22 04:38:38
# Size of source mod 2**32: 380 bytes
from notekeras.backend import keras
__all__ = ['get_inputs']

def get_inputs(seq_len):
    """Get input layers.

    See: https://arxiv.org/pdf/1810.04805.pdf

    :param seq_len: Length of the sequence or None.
    """
    names = [
     'Token', 'Segment', 'Masked']
    return [keras.layers.Input(shape=(seq_len,), name=('Input-%s' % name)) for name in names]