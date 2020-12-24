# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\phaseshifts\__init__.py
# Compiled at: 2014-01-31 06:22:49
from pkg_resources import get_distribution, DistributionNotFound
__project__ = 'phaseshifts'
__version__ = None
try:
    __version__ = get_distribution(__project__).version
except DistributionNotFound:
    VERSION = __project__ + '-' + '(local)'
else:
    VERSION = __project__ + '-' + __version__