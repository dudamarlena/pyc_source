# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/archetypes/schematuning/tests/base.py
# Compiled at: 2010-01-22 07:59:46
from zope import component
from Products.Archetypes.Schema.factory import instanceSchemaFactory
from Products.Archetypes.tests import attestcase as atc
from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase import layer
SiteLayer = layer.PloneSite
configuration = '    <configure xmlns="http://namespaces.zope.org/zope">\n        <include package="archetypes.schemaextender" />\n        <include package="plone.memoize" />\n    </configure>\n    '

class SchemaTuningLayer(SiteLayer):
    __module__ = __name__

    @classmethod
    def setUp(cls):
        PRODUCTS = [
         'plone.memoize', 'archetypes.schemaextender', 'archetypes.schematuning']
        ptc.setupPloneSite(products=PRODUCTS)
        fiveconfigure.debug_mode = True
        import archetypes.schemaextender
        zcml.load_config('configure.zcml', archetypes.schemaextender)
        import archetypes.schematuning
        zcml.load_config('configure.zcml', archetypes.schematuning)
        zcml.load_string(configuration)
        fiveconfigure.debug_mode = False
        component.provideAdapter(instanceSchemaFactory)
        SiteLayer.setUp()


class SchemaTuningTestCase(ptc.PloneTestCase, atc.ATTestCase):
    """We use this base class for all the tests in this package. If necessary,
       we can put common utility or setup code in here.
    """
    __module__ = __name__
    layer = SchemaTuningLayer