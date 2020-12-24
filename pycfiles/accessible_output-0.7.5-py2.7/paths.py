# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\accessible_output\paths.py
# Compiled at: 2010-10-23 22:06:20
import os.path, sys

def root(file=None):
    if hasattr(sys, 'frozen'):
        from win32api import GetModuleFileName
        path = os.path.dirname(GetModuleFileName(0))
    else:
        path = os.path.split(os.path.realpath(__file__))[0]
    if file:
        path = os.path.join(path, file)
    return path