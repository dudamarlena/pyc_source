# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/ageliaco/rd2/tests.py
# Compiled at: 2013-02-25 07:53:41
import doctest, unittest
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup
import ageliaco.rd2
OPTION_FLAGS = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
ptc.setupPloneSite(products=['ageliaco.rd2'])

class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            zcml.load_config('configure.zcml', ageliaco.rd2)

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([
     ztc.ZopeDocFileSuite('INTEGRATION.txt', package='ageliaco.rd2', optionflags=OPTION_FLAGS, test_class=TestCase)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')