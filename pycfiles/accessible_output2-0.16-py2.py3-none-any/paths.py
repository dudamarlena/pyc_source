# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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