# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/martin/windows/Desarrollo/Python/django-endless-pagination-angular/bin/django-endless-pagination-angular/endless_pagination/__init__.py
# Compiled at: 2016-11-21 17:41:00
# Size of source mod 2**32: 315 bytes
"""Django pagination tools supporting Ajax, multiple and lazy pagination,
Twitter-style and Digg-style pagination.
"""
from __future__ import unicode_literals
VERSION = (1, 2)

def get_version():
    """Return the Django Endless Pagination Angular version as a string."""
    return '.'.join(map(str, VERSION))