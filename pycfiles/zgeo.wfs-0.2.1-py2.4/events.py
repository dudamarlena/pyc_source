# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zgeo/wfs/events.py
# Compiled at: 2008-10-27 05:35:22
from zope.interface import implements
from Products.ZCatalog.Catalog import CatalogError
from interfaces import IWebFeatureService, IWebFeatureServiceable, IWFSGeoreferencedEvent
from interfaces import IWFSGeoItem
import logging
logger = logging.getLogger('WFS')

class WFSGeoreferencedEvent(object):
    """Event to notify that object has been georeferenced.
    """
    __module__ = __name__
    implements(IWFSGeoreferencedEvent)

    def __init__(self, context):
        self.context = context


def afterObjectCreated(obj, event):
    """
    """
    geoitem = IWFSGeoItem(obj)
    wfs = geoitem.getWFSParent()
    if wfs is not None:
        cat = wfs.getGeoCatalog()
        cat.catalog_object(geoitem.context, ('/').join(obj.getPhysicalPath()))
        if geoitem.isGeoreferenced():
            wfs.refreshFeatureTypeBoundingBox(geoitem.featureType, geoitem.getGeometry())
    return


def afterObjectModified(obj, event):
    """
    """
    geoitem = IWFSGeoItem(obj)
    wfs = geoitem.getWFSParent()
    if wfs is not None:
        cat = wfs.getGeoCatalog()
        cat.catalog_object(geoitem.context, ('/').join(obj.getPhysicalPath()))
        wfs.computeFeatureTypeBoundingBox(geoitem.featureType)
    return


def afterGeometryModified(event):
    """
    """
    geoitem = event.context
    wfs = geoitem.getWFSParent()
    if wfs is not None:
        cat = wfs.getGeoCatalog()
        cat.catalog_object(geoitem.context, ('/').join(geoitem.context.getPhysicalPath()))
        wfs.computeFeatureTypeBoundingBox(geoitem.featureType)
    return


def beforeObjectRemoved(obj, event):
    """
    """
    geoitem = IWFSGeoItem(obj)
    wfs = geoitem.getWFSParent()
    if wfs is not None:
        try:
            cat = wfs.getGeoCatalog()
            uid = ('/').join(obj.getPhysicalPath())
            if cat.getrid(uid):
                cat.uncatalog_object(uid)
            wfs.computeFeatureTypeBoundingBox(geoitem.featureType)
        except:
            logger.info('cannot remove')

    return