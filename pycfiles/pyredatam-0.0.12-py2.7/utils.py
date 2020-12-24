# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyredatam/utils.py
# Compiled at: 2015-09-21 12:56:27
"""
utils.py

Helper methods.
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import with_statement
import os

def get_data_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), b'data'))