# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/garbas/forum/tests.py
# Compiled at: 2008-09-26 21:59:24
import doctest, unittest
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    import garbas.forum
    zcml.load_config('configure.zcml', garbas.forum)
    fiveconfigure.debug_mode = False
    ztc.installPackage('garbas.forum')


setup_product()
ptc.setupPloneSite(products=['garbas.forum'])

class FunctionalTestCase(ptc.FunctionalTestCase):
    """ functional test case """
    __module__ = __name__


def test_suite():
    return unittest.TestSuite([ztc.ZopeDocFileSuite('content.txt', package='garbas.forum', test_class=FunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('notification.txt', package='garbas.forum', test_class=FunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('browser.txt', package='garbas.forum', test_class=FunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')