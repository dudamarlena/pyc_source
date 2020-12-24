# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/devel/metasyntactic/metasyntactic/__init__.py
# Compiled at: 2020-01-09 15:57:09
# Size of source mod 2**32: 567 bytes
"""metasyntactic - Themed metasyntactic variables names"""
VERSION = (1, 0, 14)
__version__ = '.'.join(map(str, VERSION[0:3])) + ''.join(VERSION[3:])
__author__ = 'Ask Solem'
__contact__ = 'ask@celeryproject.org'
__homepage__ = 'http://github.com/ask/metasyntactic/'
__docformat__ = 'restructuredtext en'
import os, sys
if not os.environ.get('MS_NO_EVAL', False):
    from metasyntactic.themes import all_themes, get, iterate, random, UnknownTheme
__all__ = [
 'all_themes', 'get', 'iterate', 'random', 'UnknownTheme']