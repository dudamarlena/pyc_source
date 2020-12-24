# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/Products/BigramSplitter/tests/base.py
# Compiled at: 2010-12-06 08:30:44
from Testing import ZopeTestCase
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_bigramsplitter():
    fiveconfigure.debug_mode = True
    from Products import BigramSplitter
    zcml.load_config('configure.zcml', BigramSplitter)
    fiveconfigure.debug_mode = False
    ZopeTestCase.installPackage('BigramSplitter')


setup_bigramsplitter()
PRODUCTS = []
PloneTestCase.setupPloneSite(products=PRODUCTS)

class BigramSplitterTestCase(PloneTestCase.PloneTestCase):
    __module__ = __name__

    class Session(dict):
        __module__ = __name__

        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()
        from Products.BigramSplitter import BigramSplitter