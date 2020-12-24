# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/pynfold/Regularization.py
# Compiled at: 2018-05-17 07:32:02
from pymc import Potential, Container
from tikhonov import tikhonov
potentialdict = {'Tikhonov': tikhonov}

class Regularization(object):

    def __init__(self, regname='', parameters=[]):
        self.regname = regname
        self.parameterslist = parameters
        self.ndiffbins = len(parameters) if len(parameters) > 0 else 1
        if self.regname in potentialdict:
            self.function = potentialdict[self.regname]
        else:
            print 'WARNING: potential name not found!'
            print 'Falling back to no potential...'

    def wrapper(self, truth=None, parameters={}):
        default_args = dict(value=truth)
        args = dict(default_args.items() + parameters.items())
        potential = self.function(**args)
        return potential

    def getpotential(self, truth):
        ntotbins = len(truth)
        step = ntotbins / self.ndiffbins
        edges = [ (ii, ii + step) for ii in range(0, ntotbins, step) ]
        potentials = [ Potential(self.wrapper, self.regname, self.regname, {'truth': truth[start:end], 'parameters': params}) for params, (start, end) in zip(self.parameterslist, edges)
                     ]
        return Container(potentials)