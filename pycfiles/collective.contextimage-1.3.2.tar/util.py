# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/contentsync/browser/util.py
# Compiled at: 2009-05-11 14:25:19
from zope.interface import implements
from Products.Five import BrowserView
from interfaces import IProgressView

class ProgressView(BrowserView):
    """
    Progress view
    """
    __module__ = __name__
    implements(IProgressView)