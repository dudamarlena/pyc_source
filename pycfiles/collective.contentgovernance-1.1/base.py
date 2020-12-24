# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/contentgenerator/tests/base.py
# Compiled at: 2009-01-19 09:24:11
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure
import collective.contentgenerator

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', collective.contentgenerator)
    fiveconfigure.debug_mode = False
    ztc.installPackage('collective.contentgenerator')


class BaseTestCase(ptc.PloneTestCase):
    """Base class for test cases.
    """
    __module__ = __name__

    def setUp(self):
        super(BaseTestCase, self).setUp()


class BaseFunctionalTestCase(ptc.FunctionalTestCase):
    """Base class for test cases.
    """
    __module__ = __name__

    def setUp(self):
        super(BaseFunctionalTestCase, self).setUp()


setup_product()
ptc.setupPloneSite(policy='collective.contentgenerator:default', products=['collective.contentgenerator'])