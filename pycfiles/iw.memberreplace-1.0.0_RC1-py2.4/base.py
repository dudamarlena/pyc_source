# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/memberreplace/tests/base.py
# Compiled at: 2009-03-07 19:02:29
"""
Common testing resources
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
from Testing import ZopeTestCase
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.Five.testbrowser import Browser
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
import iw.memberreplace
from iw.memberreplace.config import PRODUCTNAME

@onsetup
def setUpmemberreplace():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', iw.memberreplace)
    fiveconfigure.debug_mode = False
    ZopeTestCase.installPackage(PRODUCTNAME)


setUpmemberreplace()
PloneTestCase.setupPloneSite(products=[PRODUCTNAME], extension_profiles=['%s:default' % PRODUCTNAME])

class memberreplaceTestCase(PloneTestCase.PloneTestCase):
    __module__ = __name__

    class Session(dict):
        __module__ = __name__

        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()


class memberreplaceFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    __module__ = __name__

    class Session(dict):
        __module__ = __name__

        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.FunctionalTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()
        self.browser = Browser()