# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dirutil\dirutil.py
# Compiled at: 2018-12-25 04:31:32
# Size of source mod 2**32: 1867 bytes
"""Utilities (that should be in python)
"""
__author__ = 'Dmitri Dolzhenko'
__email__ = 'd.dolzhenko@gmail.com'
import os, subprocess, checksumdir, shutil, stat, unittest, collections, tempfile

def im_on_windows():
    return os.name == 'nt'