# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/anz/dashboard/tests/base.py
# Compiled at: 2010-09-26 21:53:53
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():
    """Set up the package and its dependencies.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer. We could have created our
    own layer, but this is the easiest way for Plone integration tests.
    """
    fiveconfigure.debug_mode = True
    import anz.dashboard
    zcml.load_config('configure.zcml', anz.dashboard)
    fiveconfigure.debug_mode = False
    ztc.installPackage('anz.dashboard')


setup_product()
ptc.setupPloneSite(products=('anz.dashboard', ), extension_profiles=['Products.CMFPlone:testfixture'])

class AnzDashBoardTestCase(ptc.PloneTestCase):
    """ """
    __module__ = __name__