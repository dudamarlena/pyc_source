# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\utils\math\DEMO\DEMO.py
# Compiled at: 2018-06-06 09:43:47
# Size of source mod 2**32: 2435 bytes
"""
Module for DEMO: Differential Evolutionary Multi-objective Optimization
=======================================================================

Port from matlab code:
    `https://github.com/fcampelo/DEMO <https://github.com/fcampelo/DEMO>`_

Reference:
    1. T Robic and B Filipic. (2005)
    DEMO: Differential evolution for multiobjective optimization. 
    Evolutionary Multi-Criterion Optimization, 520–533.
    2. Eckart Zitzler and S Kunzli.(2004)
    Indicator-based selection in multiobjective search. 
    Parallel Problem Solving from Nature-PPSN VIII, (i):1–11.
    3. Kalyanmoy Deb, J. Sundar, Rao N. Udaya Bhaskara, and Shamik Chaudhuri. (2006)
    Reference Point Based Multi-Objective Optimization Using Evolutionary Algorithms. 
    International Journal of Computational Intelligence Research, 2(3):273– 286.
    4. Lothar Thiele, Kaisa Miettinen, PJ Korhonen, and Julian Molina. (2009) 
    A preference- based evolutionary algorithm for multi-objective optimization. 
    Evolutionary Computation, 17(3):411–436.
    5. Fillipe Goulart and Felipe Campelo. (2016) 
    Preference-guided evolutionary algorithms for many-objective optimization. 
    Information Sciences, 329:236 – 255. Special issue on Discovery Science.
    
.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from .demo_opt import *
__all__ = [
 'demo_opt', 'fobjeval', 'mutation', 'recombination', 'repair', 'selection', 'init_options', 'ndset', 'crowdingdistance', 'dtlz2', 'dtlz_range']