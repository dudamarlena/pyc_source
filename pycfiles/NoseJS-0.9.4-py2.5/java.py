# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/nosejs/java.py
# Compiled at: 2009-03-04 11:10:12
"""A *very* minimal implementation of Java :)

This is for using Rhino compatible scripts in Spidermonkey that create java objects
"""
import os

class _SM_JavaFile(file):

    def getParent(self):
        return os.path.dirname(self.name)