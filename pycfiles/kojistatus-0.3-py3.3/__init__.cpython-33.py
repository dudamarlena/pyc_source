# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kojistatus/__init__.py
# Compiled at: 2017-01-27 08:21:42
# Size of source mod 2**32: 103 bytes
from .status import status
from .webapp import app as application
__all__ = ['status', 'application']