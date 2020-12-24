# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/PermissionComprehensible/_darcs/pristine/tests/base.py
# Compiled at: 2012-01-17 08:01:28
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
    import permissioncomprehensible.portlet.PermissionComprehensible
    zcml.load_config('configure.zcml', permissioncomprehensible.portlet.PermissionComprehensible)
    fiveconfigure.debug_mode = False
    ztc.installPackage('permissioncomprehensible.portlet.PermissionComprehensible')


setup_product()
ptc.setupPloneSite(products=['permissioncomprehensible.portlet.PermissionComprehensible'])

class TestCase(ptc.PloneTestCase):
    """Base class used for test cases
    """


class FunctionalTestCase(ptc.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """