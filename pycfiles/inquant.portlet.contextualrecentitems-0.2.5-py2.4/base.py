# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/inquant/portlet/contextualrecentitems/tests/base.py
# Compiled at: 2008-02-18 06:05:55
__author__ = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 58591 $'
__version__ = '$Revision: 58591 $'[11:-2]
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
    import inquant.portlet.contextualrecentitems
    zcml.load_config('configure.zcml', inquant.portlet.contextualrecentitems)
    fiveconfigure.debug_mode = False
    ztc.installPackage('inquant.portlet.contextualrecentitems')


setup_product()
ptc.setupPloneSite(products=['inquant.portlet.contextualrecentitems'])

class TestCase(ptc.PloneTestCase):
    """Base class used for test cases
    """
    __module__ = __name__


class FunctionalTestCase(ptc.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """
    __module__ = __name__