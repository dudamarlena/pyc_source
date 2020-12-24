# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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