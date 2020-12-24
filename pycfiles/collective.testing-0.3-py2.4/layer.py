# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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