# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dpl1_main/deployment_util.py
# Compiled at: 2014-02-26 07:44:47
"""This file contains developments useful for deployment
"""
import os, sys

def correct_sys_path(relative_dir=os.pardir):
    """Adds to sys.path the directory given directory (relative to the current)

    :param relative_dir: the relative folder address
    """
    try:
        sys.path.remove(os.getcwd())
    except ValueError:
        pass

    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), relative_dir)))
    sys.path = list(set(sys.path))