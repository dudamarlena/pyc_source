# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/porthole/__init__.py
# Compiled at: 2020-03-19 22:11:29
# Size of source mod 2**32: 64 bytes
from .server import serve, onGet
from .client import fetch, test