# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/collective/testing/interfaces.py
# Compiled at: 2007-04-17 11:51:41
from zope.interface import Interface

class ITestObject(Interface):
    """because for some reason, no default view is regged for folders
    in ZTC. this is a static marker"""
    __module__ = __name__