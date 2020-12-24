# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/Products/LinguaFace/browser/utilities.py
# Compiled at: 2010-11-30 09:59:25
__doc__ = ' View used for content importation in XMLRPC\n'
from zope.interface import implements
from Products.Five import BrowserView
from interfaces import ILinguaFaceUtilities

class LinguaFaceUtilities(BrowserView):
    """LinguaFace Utilities view"""
    __module__ = __name__
    implements(ILinguaFaceUtilities)