# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/functions/is_symbolic.py
# Compiled at: 2020-05-07 20:26:31
# Size of source mod 2**32: 97 bytes
import casadi.casadi as cs

def is_symbolic(u):
    return isinstance(u, (cs.SX, cs.MX, cs.DM))