# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dbbase/__init__.py
# Compiled at: 2020-04-01 13:49:33
# Size of source mod 2**32: 238 bytes
"""
This package implements base routines for interacting with a database.
"""
from ._version import __version__
from .utils import db_config
from .base import DB
from . import maint