# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/pysde/__init__.py
# Compiled at: 2016-09-09 22:45:16
# Size of source mod 2**32: 1205 bytes
__doc__ = '\npython SDE -- Python for Stochastic Differential Equations\n\nTry to possibly do symbolic stochastic calculation directory in minimum resources.\n  \nThis package is developed referenced to the following resources:\n  \n1. Kendall,W.S.: Symbolic Ito calculus in AXIOM: an ongoing story,\n   http://www.warwick.ac.uk/statsdept/staff/WSK/abstracts.html#327\n2. Sasha Cyganowski: Solving Stochastic Differential Equations with\n   Maple, http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.134.7739&rep=rep1&type=pdf\n3. Sasha Cyganowski: Maple stochastic package, \n   http://www.math.uni-frankfurt.de/~numerik/maplestoch/\n\nPackages:\n\nsde.py : Main package\ntest.py: demo file\n\nNecessary Python packages required:\n\nSymbolic:\nSympy: symbolic calculation, http://www.sympy.org\n\nNumerical and simulation plotting:\nNumpy: data generating, http://www.scipy.org\nscitools: StringFunction for math function\nmatplotlib: plot library, http://matplotlib.sf.net\n\ndevelopers:\nchu-ching huang,\nMath group, Center for General Education,\nChang-Gung University, Taiwan\n\nEmail- cchuang@mail.cgu.edu.tw\n\n'
__version__ = '0.1'
version = __version__
__author__ = 'chu-ching huang'
author = __author__
from pysde.sde import *