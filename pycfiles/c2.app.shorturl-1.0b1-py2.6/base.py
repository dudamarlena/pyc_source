# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/c2/app/shorturl/tests/base.py
# Compiled at: 2010-08-19 05:10:30
"""
base.py

Created by Manabu Terada on 2010-08-03.
Copyright (c) 2010 CMScom. All rights reserved.
"""
from Testing import ZopeTestCase
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_app():
    fiveconfigure.debug_mode = True
    import c2.app.shorturl
    zcml.load_config('configure.zcml', c2.app.shorturl)
    fiveconfigure.debug_mode = False
    ZopeTestCase.installPackage('c2.app.shorturl')


setup_app()
PRODUCTS = []
PloneTestCase.setupPloneSite(products=PRODUCTS)

class BaseTestCase(PloneTestCase.PloneTestCase):

    class Session(dict):

        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()