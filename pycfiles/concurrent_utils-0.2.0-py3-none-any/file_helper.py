# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/common/file_helper.py
# Compiled at: 2011-09-28 13:50:09
import os

def lenient_makedir(dir_path):
    """Create given directory path if it doesn't already exist"""
    if not os.access(dir_path, os.F_OK):
        os.makedirs(dir_path)