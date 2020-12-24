# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/__main__.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 392 bytes
import os, sys
mod = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if mod not in sys.path:
    sys.path.insert(1, mod)
from pyxrd.core import run_main
run_main()