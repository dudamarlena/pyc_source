# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/utils/model.py
# Compiled at: 2020-04-21 02:51:47
# Size of source mod 2**32: 372 bytes


def freeze(model):
    """ Set all layers in a model to non-trainable.

    The weights for these layers will not be updated during training.

    This function modifies the given model in-place,
    but it also returns the modified model to allow easy chaining with other functions.
    """
    for layer in model.layers:
        layer.trainable = False

    return model