# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/portlet/staticnav/tests/base.py
# Compiled at: 2009-07-03 09:34:02
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():
    """Set up additional products and ZCML required to test this product.

    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    fiveconfigure.debug_mode = True
    import wwp.portlet.staticnav
    zcml.load_config('configure.zcml', wwp.portlet.staticnav)
    fiveconfigure.debug_mode = False
    ztc.installPackage('wwp.portlet.staticnav')


setup_product()
ptc.setupPloneSite(products=['wwp.portlet.staticnav'])

class TestCase(ptc.PloneTestCase):
    """Base class used for test cases
    """
    __module__ = __name__


class FunctionalTestCase(ptc.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """
    __module__ = __name__