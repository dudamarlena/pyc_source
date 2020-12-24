# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/Products/LinguaFace/tests/base.py
# Compiled at: 2010-11-30 09:59:25
__docformat__ = 'restructuredtext'
from Testing import ZopeTestCase
from Products.LinguaPlone.tests.LinguaPloneTestCase import LinguaPloneTestCase
_MARKER = '»»»'
ZopeTestCase.installProduct('LinguaFace', quiet=1)

class LinguaFaceTestCase(LinguaPloneTestCase):
    """Base class for all class with test cases on LinguaFace"""
    __module__ = __name__

    def _setup(self):
        LinguaPloneTestCase._setup(self)
        self.addProduct('LinguaFace')