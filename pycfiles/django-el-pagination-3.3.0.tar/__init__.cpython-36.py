# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/berg/wss/ws-github/django-el-pagination/el_pagination/__init__.py
# Compiled at: 2020-02-11 16:02:54
# Size of source mod 2**32: 304 bytes
"""Django pagination tools supporting Ajax, multiple and lazy pagination,
Twitter-style and Digg-style pagination.
"""
from __future__ import unicode_literals
VERSION = (3, 3, 0)

def get_version():
    """Return the Django EL Pagination version as a string."""
    return '.'.join(map(str, VERSION))