# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/functions/rosenbrock.py
# Compiled at: 2020-05-07 20:26:31
# Size of source mod 2**32: 533 bytes
from opengen.functions.is_symbolic import is_symbolic

def rosenbrock(u_, p_):
    """Rosenbrock functions with parameters <code>p = [a, b]</code>"""
    if not is_symbolic(p_) or p_.size()[0] != 2:
        raise Exception('illegal parameter p_ (must be SX of size (2,1))')
    if not is_symbolic(u_):
        raise Exception('illegal parameter u_ (must be SX)')
    nu = u_.size()[0]
    a = p_[0]
    b = p_[1]
    ros_fun = 0
    for i in range(nu - 1):
        ros_fun += b * (u_[(i + 1)] - u_[i] ** 2) ** 2 + (a - u_[i]) ** 2

    return ros_fun