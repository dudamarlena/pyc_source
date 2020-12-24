# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/lsqfitgp/_gvar_autograd.py
# Compiled at: 2020-04-26 18:37:43
# Size of source mod 2**32: 2406 bytes
import builtins, autograd, gvar
from autograd import numpy as np
__doc__ = '\nModule that replaces gvar.numpy with autograd.numpy.\n'

def switch_numpy(module):
    oldmodule = gvar.numpy
    gvar.numpy = module
    for s in ('_bufferdict', '_gvarcore', '_svec_smat', '_utilities', 'cspline', 'dataset',
              'linalg', 'ode', 'powerseries', 'root'):
        if not hasattr(gvar, s):
            print('*** {} not found'.format(s))
        else:
            gvar_s = getattr(gvar, s)
            if hasattr(gvar_s, 'numpy'):
                gvar_s.numpy = module
            else:
                print('*** no numpy in', s)
    else:
        return oldmodule


def switch_functions(module):
    oldmodule = gvar.numpy
    gvar.numpy = module
    for s in ('sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'fabs', 'sinh', 'cosh', 'tanh',
              'arcsin', 'arccos', 'arctan', 'arctan2', 'arcsinh', 'arccosh', 'arctanh',
              'square'):
        if hasattr(gvar, s):
            hasattr(module, s) or print('*** {} not found'.format(s))
        else:
            setattr(gvar, s, getattr(module, s))
    else:
        return oldmodule


switch_numpy(autograd.numpy)
switch_functions(autograd.numpy)
gvar.erf = autograd.extend.primitive(gvar.erf)
erf_jvp = lambda ans, x: lambda g: g * 2 / np.sqrt(np.pi) * np.exp(-x ** 2)
autograd.extend.defvjp(gvar.erf, erf_jvp)
autograd.extend.defjvp(gvar.erf, erf_jvp)
gvar.BufferDict.extension_fcn['log'] = gvar.exp
gvar.BufferDict.extension_fcn['sqrt'] = gvar.square
gvar.BufferDict.extension_fcn['erfinv'] = gvar.erf
autograd.extend.defvjp(autograd.numpy.asarray, lambda ans, *args, **kw: lambda g: g)
autograd.numpy.numpy_boxes.ArrayBox.item = lambda self: self[((0, ) * len(self.shape))]

def array(A, *args, **kwargs):
    t = builtins.type(A)
    if t in (list, tuple):
        return (autograd.numpy.numpy_wrapper.array_from_args)(args, kwargs, *map(lambda a:         if a.shape:
a # Avoid dead code: a.item(), map(array, A)))
    return autograd.numpy.numpy_wrapper._array_from_scalar_or_array(args, kwargs, A)


autograd.numpy.numpy_wrapper.array = array
autograd.numpy.array = array
try:
    from gvar import _utilities
    from gvar._evalcov_fast import evalcov_blocks
    gvar.evalcov_blocks = evalcov_blocks
    _utilities.evalcov_blocks = evalcov_blocks
except ImportError:
    pass