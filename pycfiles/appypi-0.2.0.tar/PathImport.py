# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/appy/pod/test/contexts/PathImport.py
# Compiled at: 2009-09-30 05:37:25
import os.path, appy

def getAppyPath():
    return os.path.dirname(appy.__file__)