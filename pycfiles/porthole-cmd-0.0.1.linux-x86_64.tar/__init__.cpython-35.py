# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/porthole/__init__.py
# Compiled at: 2020-03-19 22:11:29
# Size of source mod 2**32: 64 bytes
from .server import serve, onGet
from .client import fetch, test