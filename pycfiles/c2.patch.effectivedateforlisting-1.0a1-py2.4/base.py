# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/c2/patch/effectivedateforlisting/tests/base.py
# Compiled at: 2010-01-29 08:59:20
"""
base.py

Created by Manabu Terada on 2010-01-29.
Copyright (c) 2010 CMScom. All rights reserved.
"""
from Testing import ZopeTestCase
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    import c2.patch.effectivedateforlisting
    zcml.load_config('configure.zcml', c2.patch.effectivedateforlisting)
    fiveconfigure.debug_mode = False
    ZopeTestCase.installPackage('c2.patch.effectivedateforlisting')


setup_product()
PRODUCTS = []
PloneTestCase.setupPloneSite(products=PRODUCTS)

class ProductTestCase(PloneTestCase.PloneTestCase):
    __module__ = __name__

    class Session(dict):
        __module__ = __name__

        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()