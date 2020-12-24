# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/util/random_variable.py
# Compiled at: 2019-02-25 04:13:09
# Size of source mod 2**32: 429 bytes
from tensorflow_probability import edward2 as ed

def set_values(**model_kwargs):
    """Creates a value-setting interceptor."""

    def interceptor(f, *args, **kwargs):
        name = kwargs.get('name')
        if name in model_kwargs:
            kwargs['value'] = model_kwargs[name]
        return (ed.interceptable(f))(*args, **kwargs)

    return interceptor