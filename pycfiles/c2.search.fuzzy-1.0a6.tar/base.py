# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/c2/search/customdescription/tests/base.py
# Compiled at: 2009-11-11 06:51:32
__doc__ = '\nbase.py\n\nCreated by Manabu Terada on 2009-11-11.\nCopyright (c) 2009 CMScom. All rights reserved.\n'
from Testing import ZopeTestCase
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    import c2.search.customdescription
    zcml.load_config('configure.zcml', c2.search.customdescription)
    fiveconfigure.debug_mode = False
    ZopeTestCase.installPackage('c2.search.customdescription')


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