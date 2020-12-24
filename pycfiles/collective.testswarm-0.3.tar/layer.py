# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/collective/testing/layer.py
# Compiled at: 2007-04-17 13:17:54
from utils import setDebugMode
from debug import dfunc
try:
    from Products.PloneTestCase.layer import ZCML as ZCMLLayer
except ImportError:

    class ZCMLLayer:
        __module__ = __name__

        @classmethod
        def setUp(cls):
            setDebugMode(1)
            from Products.Five import zcml
            zcml.load_site()
            setDebugMode(0)

        @classmethod
        def tearDown(cls):
            from zope.testing.cleanup import cleanUp
            cleanUp()
            import Products.Five.zcml
            Products.Five.zcml._initialized = False