# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/decorators/lizer.py
# Compiled at: 2007-12-02 16:26:56


def lizer(func):

    def pythonic(*targs):
        args = []
        for a in targs:
            if not isinstance(a, list):
                a = [
                 a]
            args.append(a)

        args[0] = args[0][0]
        res = func(*args)
        if isinstance(res, list):
            res = res[0]
        return res

    pythonic.lized = func
    return pythonic


from salamoia.tests import *
runDocTests()