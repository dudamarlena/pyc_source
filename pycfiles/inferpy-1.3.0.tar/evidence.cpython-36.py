# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/contextmanager/evidence.py
# Compiled at: 2019-09-03 11:37:11
# Size of source mod 2**32: 1930 bytes
import contextlib, numpy as np
from inferpy import util

@contextlib.contextmanager
def observe(variables, data):
    sess = util.session.get_session()
    for k, v in data.items():
        if k not in variables:
            pass
        else:
            variables[k].is_observed.load(True, session=sess)
            if hasattr(v, 'shape'):
                if v.shape == variables[k].observed_value.shape:
                    variables[k].observed_value.load(v, session=sess)
                elif len(v.shape) > 0:
                    if v.shape[0] == 1:
                        if v.shape[1:] == variables[k].observed_value.shape:
                            variables[k].observed_value.load((v[0]), session=sess)
                else:
                    variables[k].observed_value.load((np.broadcast_to(v, variables[k].observed_value.shape.as_list())),
                      session=sess)
            else:
                variables[k].observed_value.load((np.broadcast_to(v, variables[k].observed_value.shape.as_list())),
                  session=sess)

    try:
        yield
    finally:
        for k, v in data.items():
            if k not in variables:
                pass
            else:
                variables[k].is_observed.load(False, session=sess)