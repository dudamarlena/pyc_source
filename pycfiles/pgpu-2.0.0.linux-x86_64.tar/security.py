# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pgpu/security.py
# Compiled at: 2012-10-15 14:33:37
"""
This module has been renamed encoding, with some deprecated functions left 
here. This module will be removed in a few releases.

AUTHORS:
v0.2.0+             --> pydsigner
v1.2.0+             --> pydsigner
"""
import warnings, math, random
from .encoding import *
from . import iter_utils
warnings.warn('This module has been deprecated in favor of encoding.py, which has the rand_key() and multi_pass() functions removed.')

def rand_key(L=10):
    """
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    res = ''
    while len(res) < L:
        v = str(math.log((random.randint(1, 33) * math.pi) ** 2))
        res += iter_utils.remove_many(v, 'e-.')

    return res[:L]


def multi_pass(user, pswd, times=1000, hasher=SHA512()):
    """
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    for i in range(times):
        pswd = hasher.encode(pswd + user + str(i))

    return pswd