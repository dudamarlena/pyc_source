# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ilrt/migrationtool/tests/base.py
# Compiled at: 2009-04-17 18:09:25
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.Five import fiveconfigure
import ilrt.migrationtool

@onsetup
def setup_products():
    fiveconfigure.debug_mode = True
    fiveconfigure.debug_mode = False
    ztc.installPackage('ilrt.migrationtool')


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


setup_products()
ptc.setupPloneSite(policy='ilrt.migrationtool:default', products=['ilrt.migrationtool'])