# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/extjslayer/tests.py
# Compiled at: 2009-03-11 02:27:20
import os, doctest, unittest
from zope.configuration import xmlconfig
from zope.app.testing import functional

def zcml(s, execute=True):
    """ZCML registration helper"""
    from zope.app.appsetup.appsetup import __config_context as context
    try:
        xmlconfig.string(s, context, execute=execute)
    except:
        context.end()
        raise


ExtJsLayerFunctionalLayer = functional.ZCMLLayer(os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'), __name__, 'ExtJsLayerFunctionalLayer')

def test_suite():
    suite = functional.FunctionalDocFileSuite('README.txt', globs={'zcml': zcml}, optionflags=doctest.NORMALIZE_WHITESPACE + doctest.ELLIPSIS)
    suite.layer = ExtJsLayerFunctionalLayer
    return unittest.TestSuite((suite, doctest.DocTestSuite()))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')