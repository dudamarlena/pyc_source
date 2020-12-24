# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zgeo/wfs/geocatalog/catalog.py
# Compiled at: 2008-10-27 05:35:22
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.ZCatalog.Catalog import CatalogError
from Products.ZCatalog.ZCatalog import Catalog
from Missing import MV
from Products.PluginIndexes.FieldIndex.FieldIndex import FieldIndex
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore.utils import UniqueObject
from zgeo.wfs.geocatalog.geometryindex import GeometryIndex
from zgeo.wfs.geocatalog.geofeatureindex import GeoFeatureIndex
from zgeo.wfs.interfaces import IWFSGeoItem

class GeoCatalog(UniqueObject, ZCatalog, ActionProviderBase):
    """ ZCatalog to index all the geo items
        """
    __module__ = __name__

    def __init__(self, oid, **kw):
        """
                """
        ZCatalog.__init__(self, oid)
        self._catalog = GeoGMLCatalog()
        self._catalog.addIndex('featureType', GeoFeatureIndex('featureType'))
        self._catalog.addIndex('name', GeoFeatureIndex('name'))
        self._catalog.addIndex('geometry', GeometryIndex('geometry'))
        self.addIndex('id', 'FieldIndex')
        self.addColumn('getGML')
        self.addColumn('geometryAsWKT')
        self.addColumn('Title')
        self.addColumn('name')

    def declareFTElement(self, elementname, elementtype):
        """
                """
        try:
            self.addIndex(elementname, 'FieldIndex')
            self.addColumn(elementname)
            self.refreshCatalog()
        except CatalogError:
            pass

    def removeFTElement(self, elementname):
        """
                """
        try:
            self.delIndex(elementname)
            self.delColumn(elementname)
            self.refreshCatalog()
        except CatalogError:
            pass


try:
    from DocumentTemplate.cDocumentTemplate import safe_callable
except ImportError:

    def safe_callable(ob):
        if hasattr(ob, '__class__'):
            return hasattr(ob, '__call__') or isinstance(ob, types.ClassType)
        else:
            return callable(ob)


class GeoGMLCatalog(Catalog):
    """(just overloads recordify method)
        """
    __module__ = __name__

    def recordify(self, object):
        """ turns an object into a record tuple """
        geoitem = IWFSGeoItem(object)
        record = []
        for x in self.names:
            if hasattr(geoitem, x):
                attr = getattr(geoitem, x, MV)
            else:
                attr = getattr(object, x, MV)
            if attr is not MV and safe_callable(attr):
                attr = attr()
            record.append(attr)

        return tuple(record)