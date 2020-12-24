# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/__init__.py
# Compiled at: 2017-09-13 20:11:23
# Size of source mod 2**32: 232 bytes
from nicfit import getLogger
from .__about__ import __version__ as version
from .jid import Jid
from .client import ClientStream, Credentials
__all__ = ['Jid', 'ClientStream', 'Credentials', 'version']
log = getLogger(__package__)