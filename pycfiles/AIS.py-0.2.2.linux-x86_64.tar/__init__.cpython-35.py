# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/AIS/__init__.py
# Compiled at: 2018-10-22 10:40:56
# Size of source mod 2**32: 535 bytes
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""
from .ais import AIS, Signature
from .pdf import PDF
from .exceptions import AISError, AuthenticationFailed, UnknownAISError, MissingPreparedSignature
__all__ = ('AIS', 'Signature', 'PDF', 'AISError', 'AuthenticationFailed', 'UnknownAISError',
           'MissingPreparedSignature')
__version__ = '0.2.2'