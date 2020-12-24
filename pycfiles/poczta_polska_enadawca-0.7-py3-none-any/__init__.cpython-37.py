# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/__init__.py
# Compiled at: 2019-11-14 22:32:26
# Size of source mod 2**32: 329 bytes
__title__ = 'pocsuite'
__version__ = '1.5.9'
__author__ = 'Knownsec Security Team'
__author_email__ = 's1@seebug.org'
__license__ = 'GPL 2.0'
__copyright__ = 'Copyright 2018 Knownsec'
__name__ = 'pocsuite3'
__package__ = 'pocsuite3'
from lib.core.common import set_paths
from .cli import module_path
set_paths(module_path())