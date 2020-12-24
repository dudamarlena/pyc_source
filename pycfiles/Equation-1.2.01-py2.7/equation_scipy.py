# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Equation\equation_scipy.py
# Compiled at: 2014-06-12 23:02:16
__authors__ = 'Glen Fletcher'
__copyright__ = '(c) 2014, AlphaOmega Technology'
__license__ = 'AlphaOmega Technology Open License Version 1.0'
__contact__ = 'Glen Fletcher <glen.fletcher@alphaomega-technology.com.au>'
try:
    import scipy.constants
    from Equation.util import addConst

    def equation_extend():
        addConst('h', scipy.constants.h)
        addConst('hbar', scipy.constants.hbar)
        addConst('m_e', scipy.constants.m_e)
        addConst('m_p', scipy.constants.m_p)
        addConst('m_n', scipy.constants.m_n)
        addConst('c', scipy.constants.c)
        addConst('N_A', scipy.constants.N_A)
        addConst('mu_0', scipy.constants.mu_0)
        addConst('eps_0', scipy.constants.epsilon_0)
        addConst('k', scipy.constants.k)
        addConst('G', scipy.constants.G)
        addConst('g', scipy.constants.g)
        addConst('q', scipy.constants.e)
        addConst('R', scipy.constants.R)
        addConst('sigma', scipy.constants.e)
        addConst('Rb', scipy.constants.Rydberg)


except ImportError:

    def equation_extend():
        pass