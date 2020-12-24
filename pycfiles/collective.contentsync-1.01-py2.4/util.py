# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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