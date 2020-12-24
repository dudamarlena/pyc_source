# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pathlib_mate-project/pathlib_mate/__init__.py
# Compiled at: 2020-03-14 13:30:32
# Size of source mod 2**32: 668 bytes
"""
pathlib_mate provide extensive methods, attributes for pathlib.
"""
from __future__ import print_function
from ._version import __version__
__short_description__ = 'An extended and more powerful pathlib.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
import os
try:
    from .pathlib2 import Path, WindowsPath, PosixPath
    PathCls = WindowsPath if os.name == 'nt' else PosixPath
except ImportError as e:
    pass
except Exception as e:
    print(e)