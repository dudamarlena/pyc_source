# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/Products/LinguaFace/browser/utilities.py
# Compiled at: 2010-11-30 09:59:25
""" View used for content importation in XMLRPC
"""
from zope.interface import implements
from Products.Five import BrowserView
from interfaces import ILinguaFaceUtilities

class LinguaFaceUtilities(BrowserView):
    """LinguaFace Utilities view"""
    __module__ = __name__
    implements(ILinguaFaceUtilities)