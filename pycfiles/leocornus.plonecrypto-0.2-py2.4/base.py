# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/leocornus/plonecrypto/tests/base.py
# Compiled at: 2010-04-12 00:27:33
"""
The base unit test cases for Leocornus Plone Cryptography toolkit
"""
from Testing import ZopeTestCase
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
import leocornus.plonecrypto
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

@onsetup
def setup_product():
    """
    we need install our product so the testing zope server know it.
    """
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', leocornus.plonecrypto)
    ZopeTestCase.installPackage('leocornus.plonecrypto')


setup_product()
PloneTestCase.setupPloneSite(products=['leocornus.plonecrypto'])

class PlonecryptoTestCase(PloneTestCase.PloneTestCase):
    """
    General steps for all test cases.
    """
    __module__ = __name__

    def afterSetUp(self):
        self.loginAsPortalOwner()


class PlonecryptoFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    """
    base test case class for functional test case.
    """
    __module__ = __name__

    def afterSetUp(self):
        self.loginAsPortalOwner()