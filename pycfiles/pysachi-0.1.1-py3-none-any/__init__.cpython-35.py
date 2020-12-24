# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/stuart/Git/SWAT/pysac/astropy_helpers/astropy_helpers/__init__.py
# Compiled at: 2015-11-25 06:17:20
# Size of source mod 2**32: 163 bytes
try:
    from .version import version as __version__
    from .version import githash as __githash__
except ImportError:
    __version__ = ''
    __githash__ = ''