# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/rc/policy/tests/base.py
# Compiled at: 2009-05-28 09:52:20
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_rc_policy():
    fiveconfigure.debug_mode = True
    import rc.policy
    zcml.load_config('configure.zcml', rc.policy)
    fiveconfigure.debug_mode = False
    ztc.installPackage('rc.policy')


setup_rc_policy()
ptc.setupPloneSite(products=['rc.policy'])

class RcPolicyTestCase(ptc.PloneTestCase):
    """This base class is used for all tests in this package.
    Utility or setup code can be added if necessary.
    """
    __module__ = __name__