# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/pysde/__init__.py
# Compiled at: 2016-09-09 22:45:16
# Size of source mod 2**32: 1205 bytes
"""
python SDE -- Python for Stochastic Differential Equations

Try to possibly do symbolic stochastic calculation directory in minimum resources.
  
This package is developed referenced to the following resources:
  
1. Kendall,W.S.: Symbolic Ito calculus in AXIOM: an ongoing story,
   http://www.warwick.ac.uk/statsdept/staff/WSK/abstracts.html#327
2. Sasha Cyganowski: Solving Stochastic Differential Equations with
   Maple, http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.134.7739&rep=rep1&type=pdf
3. Sasha Cyganowski: Maple stochastic package, 
   http://www.math.uni-frankfurt.de/~numerik/maplestoch/

Packages:

sde.py : Main package
test.py: demo file

Necessary Python packages required:

Symbolic:
Sympy: symbolic calculation, http://www.sympy.org

Numerical and simulation plotting:
Numpy: data generating, http://www.scipy.org
scitools: StringFunction for math function
matplotlib: plot library, http://matplotlib.sf.net

developers:
chu-ching huang,
Math group, Center for General Education,
Chang-Gung University, Taiwan

Email- cchuang@mail.cgu.edu.tw

"""
__version__ = '0.1'
version = __version__
__author__ = 'chu-ching huang'
author = __author__
from pysde.sde import *