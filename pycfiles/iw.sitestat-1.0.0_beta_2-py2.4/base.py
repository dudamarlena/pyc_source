# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/sitestat/tests/base.py
# Compiled at: 2008-10-10 10:13:58
"""
Common testing resources
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
from Testing import ZopeTestCase
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
import iw.sitestat.config
from iw.sitestat.config import PRODUCTNAME, HAVE_COLLAGE, HAVE_PLONEARTICLE, HAVE_SIMPLEALIAS
import iw.sitestat
if HAVE_COLLAGE:
    import Products.Collage
if HAVE_PLONEARTICLE:
    import Products.PloneArticle
iw.sitestat.config.ZOPETESTCASE = True

@onsetup
def setUpsitestat():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', iw.sitestat)
    fiveconfigure.debug_mode = False
    ZopeTestCase.installPackage(PRODUCTNAME)


setUpsitestat()

def baseSetup(component, name):
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', component)
    fiveconfigure.debug_mode = False
    ZopeTestCase.installProduct(name)


if HAVE_COLLAGE:

    @onsetup
    def setUpCollage():
        baseSetup(Products.Collage, 'Collage')


    setUpCollage()
if HAVE_PLONEARTICLE:

    @onsetup
    def setUpPloneArticle():
        baseSetup(Products.PloneArticle, 'PloneArticle')


    setUpPloneArticle()
if HAVE_SIMPLEALIAS:

    @onsetup
    def setupSimpleAlias():
        baseSetup(Products.SimpleAlias, 'SimpleAlias')


    setupSimpleAlias()
products = [PRODUCTNAME]
extension_profiles = ['%s:default' % PRODUCTNAME]
if HAVE_COLLAGE:
    products.append('Collage')
    extension_profiles.append('Products.Collage:default')
if HAVE_PLONEARTICLE:
    products.append('PloneArticle')
    extension_profiles.append('Products.PloneArticle:default')
if HAVE_SIMPLEALIAS:
    products.append('SimpleAlias')
    extension_profiles.append('Products.SimpleAlias:default')
PloneTestCase.setupPloneSite(products=products, extension_profiles=extension_profiles)

class sitestatTestCase(PloneTestCase.PloneTestCase):
    __module__ = __name__

    class Session(dict):
        __module__ = __name__

        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()


class sitestatFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    __module__ = __name__

    class Session(dict):
        __module__ = __name__

        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.FunctionalTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()