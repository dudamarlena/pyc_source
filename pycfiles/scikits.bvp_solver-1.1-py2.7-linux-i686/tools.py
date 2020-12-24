# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scikits/bvp_solver/tools.py
# Compiled at: 2011-07-22 15:26:36
import numpy

def has_nans(arg):
    return not numpy.isfinite(arg).all()


def preparg(arg):
    """
    prepares an argument the user passed for use
    """
    if arg is not None:
        if not isinstance(arg, numpy.ndarray):
            try:
                arg = numpy.array(arg, dtype=numpy.float)
            except ValueError:
                raise ValueError('argument not castable to array with dtype float: ' + str(arg))

        if has_nans(arg):
            raise ValueError('argument has NaNs, Infs or -Infs')
    return arg


def farg(arg):
    """
    prepares an array argument for passing to fortran code by filtering out None's
    """
    if arg is None:
        return numpy.array([])
    else:
        return arg
        return


def showdiff(arg1, arg2):
    """
    show the non-equality of two values
    """
    return ' <' + str(arg1) + ' != ' + str(arg2) + '> '


def argShapeTest(arg, shape, argName='', recommendation=''):
    """
    Test whether an argument is a numpy array and whether it has the right shape, otherwise raise an error
    """
    if not isinstance(arg, numpy.ndarray):
        raise ValueError(argName + ' is not a numpy array but a ' + str(type(arg)))
    if has_nans(arg):
        raise ValueError(argName + ' has NaNs, Infs or -Infs')
    if arg.shape != shape:
        raise ValueError(argName + ' is not the right shape. ' + recommendation + '\n' + showdiff(arg.shape, shape))


def fromf(arg):
    if arg is not None:
        return arg.copy()
    else:
        return arg
        return