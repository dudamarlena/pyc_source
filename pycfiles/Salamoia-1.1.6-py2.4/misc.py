# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/decorators/misc.py
# Compiled at: 2007-12-02 16:26:56


def vars_private(func):
    """
    creates automatically private variabile (prefixed with _) called after the names
    of the arguments
    """

    def wrapper(*args):
        for (i, arg) in enumerate(args[1:]):
            setattr(args[0], '_' + func.func_code.co_varnames[(i + 1)], arg)

        return func(*args)

    return wrapper


from salamoia.tests import *
runDocTests()