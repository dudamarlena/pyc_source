# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/moves/tkinter/scrolledtext.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 330 bytes
from __future__ import absolute_import
from future.utils import PY3
if PY3:
    from tkinter.scrolledtext import *
else:
    try:
        from ScrolledText import *
    except ImportError:
        raise ImportError('The ScrolledText module is missing. Does your Py2 installation include tkinter?')