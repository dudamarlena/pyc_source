# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stuart/GitHub/SWAT/pysac/astropy_helpers/astropy_helpers/__init__.py
# Compiled at: 2015-11-25 06:17:20
try:
    from .version import version as __version__
    from .version import githash as __githash__
except ImportError:
    __version__ = ''
    __githash__ = ''