# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/collective/testing/interfaces.py
# Compiled at: 2007-04-17 11:51:41
from zope.interface import Interface

class ITestObject(Interface):
    """because for some reason, no default view is regged for folders
    in ZTC. this is a static marker"""
    __module__ = __name__