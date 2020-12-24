# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\GitHub\AeroSandbox\aerosandbox\aerodynamics\aerodynamics.py
# Compiled at: 2020-01-08 21:36:38
# Size of source mod 2**32: 1099 bytes
import numpy as np
from autograd import grad
import scipy.linalg as sp_linalg
from numba import jit
import matplotlib.pyplot as plt
import matplotlib as mpl, sys
from ..plotting import *
from ..geometry import *
from ..performance import *
import cProfile, functools, os

class AeroProblem:

    def __init__(self, airplane, op_point):
        self.airplane = airplane
        self.op_point = op_point


def profile(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        try:
            profiler.enable()
            ret = func(*args, **kwargs)
            profiler.disable()
            return ret
        finally:
            filename = os.path.expanduser(os.path.join('~', func.__name__ + '.pstat'))
            profiler.dump_stats(filename)

    return wrapper