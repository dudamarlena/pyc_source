# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.openbsd-6.5-amd64/egg/xps/__init__.py
# Compiled at: 2019-10-13 08:14:42
# Size of source mod 2**32: 362 bytes
__author__ = 'David Kalliecharan'
__author_email__ = 'david@david.science'
__license__ = 'ISC'
try:
    from .xps import *
    from . import parser
    from . import sfwagner
    from . import scatter
    sf = sfwagner.SensitivityFactors()
except ImportError as err:
    print(err)