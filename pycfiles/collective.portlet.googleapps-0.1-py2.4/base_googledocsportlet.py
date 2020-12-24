# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/portlet/googleapps/tests/base_googledocsportlet.py
# Compiled at: 2009-08-03 02:55:10
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
    import collective.portlet.googleapps.portlets
    zcml.load_config('configure.zcml', collective.portlet.googleapps.portlets)
    fiveconfigure.debug_mode = False
    ztc.installPackage('collective.portlet.googleapps.portlets')


setup_product()
ptc.setupPloneSite(products=['collective.portlet.googleapps.portlets'])

class TestCase(ptc.PloneTestCase):
    """Base class used for test cases
    """
    __module__ = __name__


class FunctionalTestCase(ptc.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """
    __module__ = __name__