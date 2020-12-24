# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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