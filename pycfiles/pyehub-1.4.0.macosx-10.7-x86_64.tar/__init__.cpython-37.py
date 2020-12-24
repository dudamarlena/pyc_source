# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/__init__.py
# Compiled at: 2019-07-03 19:21:52
# Size of source mod 2**32: 237 bytes
"""
The package of everything EHub related.
"""
import os, sys, inspect
CURRENT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(CURRENT_DIR)