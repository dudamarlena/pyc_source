# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/filebrowser/__init__.py
# Compiled at: 2014-11-22 02:41:17
from threading import local
_dirs = local()

def get_default_dir():
    return getattr(_dirs, 'current_dir', '')


def set_default_dir(dir):
    setattr(_dirs, 'current_dir', dir)