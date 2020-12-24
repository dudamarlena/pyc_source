# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/tests.py
# Compiled at: 2019-02-15 13:51:23
import doctest, unittest
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
import emrt.necd.content
OPTION_FLAGS = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
ptc.setupPloneSite(products=['emrt.necd.content'])

class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            zcml.load_config('configure.zcml', emrt.necd.content)

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([
     ztc.ZopeDocFileSuite('INTEGRATION.txt', package='emrt.necd.content', optionflags=OPTION_FLAGS, test_class=TestCase)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')