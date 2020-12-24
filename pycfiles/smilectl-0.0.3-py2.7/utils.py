# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/smilectl/utils.py
# Compiled at: 2018-09-22 01:53:44
"""Utility module for smilectl."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os

def libsm_abs_path(dir_path, rel):
    """Parse the libsm file full path."""
    lib_path = os.path.join(os.path.dirname(__file__), 'lib')
    test_paths = [ os.path.join(base_path, rel) for base_path in [dir_path, lib_path] ]
    return next((test_path for test_path in test_paths if os.path.exists(test_path)), None)