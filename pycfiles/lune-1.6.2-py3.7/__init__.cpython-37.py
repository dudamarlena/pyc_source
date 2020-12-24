# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/lune/__init__.py
# Compiled at: 2020-05-07 04:53:46
# Size of source mod 2**32: 664 bytes
"""From a date given in parameter,
the algorithm returns respectively dates for :
- the new moon;
- the first quarter;
- the full moon;
- last quarter
Author : Keller Stéphane.
Enseignant de mathématiques, physique chimie, informatique et SNT.
Lycée agricole Louis Pasteur - Marmilhat.  B.P. 116 - 63 370 Lempdes
stephane.keller@yahoo.com
https://github.com/KELLERStephane/KELLER-Stephane-Tests2maths
"""
__version__ = '1.6.2'
from lune.phase import angle
from lune.phase import jj2date
from lune.phase import calcul_Ci
from lune.phase import lunar_phase
from lune.phase import between_dates