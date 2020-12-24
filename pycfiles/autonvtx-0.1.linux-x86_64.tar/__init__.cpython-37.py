# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/xgao/anaconda3/lib/python3.7/site-packages/autonvtx/__init__.py
# Compiled at: 2019-12-17 18:35:45
# Size of source mod 2**32: 728 bytes
import torch, functools, sys

def patch(model, name=None):
    if name is None:
        name = type(model).__name__
    else:
        name = name + ': ' + type(model).__name__
    old_forward = type(model).forward

    def wrap_with_name(_name=name, _model=model):

        @functools.wraps(old_forward)
        def wrapped_forward(*args, **kwargs):
            torch.cuda.nvtx.range_push(_name)
            result = old_forward(_model, *args, **kwargs)
            torch.cuda.nvtx.range_pop()
            return result

        return wrapped_forward

    model.forward = wrap_with_name()
    for name, child in model.named_children():
        patch(child, name)

    return model


sys.modules[__name__] = patch