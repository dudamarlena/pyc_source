# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/AIS/__init__.py
# Compiled at: 2018-10-22 10:40:56
# Size of source mod 2**32: 535 bytes
__doc__ = '\nAIS.py - A Python interface for the Swisscom All-in Signing Service.\n\n:copyright: (c) 2016 by Camptocamp\n:license: AGPLv3, see README and LICENSE for more details\n\n'
from .ais import AIS, Signature
from .pdf import PDF
from .exceptions import AISError, AuthenticationFailed, UnknownAISError, MissingPreparedSignature
__all__ = ('AIS', 'Signature', 'PDF', 'AISError', 'AuthenticationFailed', 'UnknownAISError',
           'MissingPreparedSignature')
__version__ = '0.2.2'