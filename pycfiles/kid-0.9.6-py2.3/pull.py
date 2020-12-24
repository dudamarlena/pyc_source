# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/kid/pull.py
# Compiled at: 2007-07-16 07:02:53
"""Pull-style interface for ElementTree.

The kid.pull module has been deprecated in favor of kid.parser.

"""
__revision__ = '$Rev: 429 $'
__date__ = '$Date: 2006-10-26 15:24:33 +0200 (Do, 26 Okt 2006) $'
__author__ = 'Ryan Tomayko (rtomayko@gmail.com)'
__copyright__ = 'Copyright 2004-2005, Ryan Tomayko'
__license__ = 'MIT <http://www.opensource.org/licenses/mit-license.php>'
import warnings
warnings.warn('kid.pull has been superseded by kid.parser', DeprecationWarning)
from kid.parser import *