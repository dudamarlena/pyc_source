# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/utils/dim_to_var.py
# Compiled at: 2016-04-20 00:05:45
import theano.tensor as T

def dim_to_var(ndim, name='k'):
    if ndim == 1:
        return T.vector(name)
    if ndim == 2:
        return T.matrix(name)
    if ndim == 3:
        return T.tensor3(name)
    if ndim == 4:
        return T.tensor4(name)
    raise NotImplementedError