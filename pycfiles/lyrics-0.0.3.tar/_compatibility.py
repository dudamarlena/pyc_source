# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/david/source/lyrics/lyrics/_compatibility.py
# Compiled at: 2013-01-25 19:32:11
"""
This is a compatibility module, to make it possible to use lyrics also with
older python versions.
"""
import sys
is_py3k = sys.version_info >= (3, )
try:
    unicode = unicode
except NameError:
    unicode = str