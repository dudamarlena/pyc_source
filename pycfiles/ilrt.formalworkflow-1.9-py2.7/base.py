# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ilrt/formalworkflow/tests/base.py
# Compiled at: 2013-06-23 12:02:23
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure
import ilrt.formalworkflow, plone.app.iterate

@onsetup
def setup_products():
    """ install ilrt.formalworkflow and any dodgy packages
        that may break Plone if present but not installed
    """
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', ilrt.formalworkflow)
    fiveconfigure.debug_mode = False
    ztc.installPackage('ilrt.formalworkflow')


class BaseTestCase(ptc.PloneTestCase):
    """Base class for test cases.
    """

    def setUp(self):
        super(BaseTestCase, self).setUp()


class BaseFunctionalTestCase(ptc.FunctionalTestCase):
    """Base class for test cases.
    """

    def setUp(self):
        super(BaseFunctionalTestCase, self).setUp()


setup_products()
ptc.setupPloneSite(policy='ilrt.formalworkflow:default', products=[
 'ilrt.formalworkflow'])