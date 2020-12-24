# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paab/policy/tests/base.py
# Compiled at: 2008-03-09 13:46:41
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_paab_policy():
    """Set up the additional products required for the paab site policy
    """
    fiveconfigure.debug_mode = True
    import paab.policy
    zcml.load_config('configure.zcml', paab.policy)
    fiveconfigure.debug_mode = False
    ztc.installPackage('paab.policy')


setup_paab_policy()
ptc.setupPloneSite(products=['paab.policy'])

class PaabPolicyTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package.
    """
    __module__ = __name__