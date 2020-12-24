# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mishmash/__init__.py
# Compiled at: 2020-02-16 13:03:30
# Size of source mod 2**32: 510 bytes
import warnings
warnings.filterwarnings('ignore', message='The psycopg2 wheel package will be renamed')
from nicfit import getLogger
from orm.core import VARIOUS_ARTISTS_NAME
from .__about__ import __version__ as version
log = getLogger(__package__)
__all__ = [
 'log', 'getLogger', 'version', 'VARIOUS_ARTISTS_NAME']