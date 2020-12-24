# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/kpages/kpages_init.py
# Compiled at: 2019-01-22 20:15:58
"""
    author comger@gmail.com
    kpages tool for init project 
"""
import sys, os, zipfile, kpages
from kpages import app_path
if __name__ == '__main__':
    path = 'kpages_project'
    if len(sys.argv) > 1:
        path = sys.argv[1]
    root = kpages.__path__[0]
    from_path = root + '/web.zip'
    to_path = app_path(path)
    _file = zipfile.ZipFile(from_path)
    _file.extractall(to_path)
    print ('init project at:', to_path)