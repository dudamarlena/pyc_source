# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/common/file_helper.py
# Compiled at: 2011-09-28 13:50:09
import os

def lenient_makedir(dir_path):
    """Create given directory path if it doesn't already exist"""
    if not os.access(dir_path, os.F_OK):
        os.makedirs(dir_path)