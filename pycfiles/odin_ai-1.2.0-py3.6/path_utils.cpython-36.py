# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/utils/path_utils.py
# Compiled at: 2019-01-24 05:01:19
# Size of source mod 2**32: 471 bytes
from __future__ import print_function, division, absolute_import
import os, sys, shutil

def get_script_path():
    """Return the path of the script that calling this methods"""
    path = os.path.dirname(sys.argv[0])
    path = os.path.join('.', path)
    return os.path.abspath(path)


def get_script_name():
    """Return the name of the running scipt file without extension"""
    name = os.path.basename(sys.argv[0])
    name = os.path.splitext(name)[0]
    return name