# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zgeo/wfs/geoitem.py
# Compiled at: 2008-10-27 05:35:22
from zope.interface import implements
from Acquisition import aq_chain
from zope.event import notify
from shapely.geometry.polygon import Polygon
from shapely.geometry import asShape
from shapely import wkt
from zgeo.geographer.geo import GeoreferencingAnnotator
from interfaces import IWebFeatureServiceable, IWebFeatureService, IWFSGeoItem
from events import WFSGeoreferencedEvent, afterObjectCreated
import logging
logger = logging.getLogger('WFS')

class WFSGeoItem(GeoreferencingAnnotator):
    """ A georeferenced object exposable through WFS
    """
    __module__ = __name__
    implements(IWFSGeoItem)

    def __init__(self, context):
        """Initialize adapter."""
        self.context = context
        GeoreferencingAnnotator.__init__(self, context)
        self._geom = None

        @property
        def id(self):
            return self.context.id

        return

    @property
    def name(self):
        return self.context.title_or_id()

    @property
    def featureType(self):
        if hasattr(self.context, 'featureType'):
            return self.context.featureType
        if hasattr(self.context, 'getFeatureType'):
            return self.context.getFeatureType()
        return 'default'

    @property
    def uri(self):
        return self.context.absolute_url()

    @property
    def geometry(self):
        return self.getGeometry()

    @property
    def geometryAsWKT(self):
        """ return geometry as WKT string
        """
        if self.isGeoreferenced():
            return self.getGeometry().wkt
        else:
            return
        return

    @property
    def description(self):
        return getattr(self.context, 'description', 'No description')

    def getSRS(self):
        srs = self.crs
        if srs is None:
            srs = 'EPSG:4326'
        return srs

    def getGeometry(self):
        if self._geom is None:
            self._geom = asShape(self.geo)
        return self._geom

    def setGeoInterface(self, type, coordinates, crs=None):
        GeoreferencingAnnotator.setGeoInterface(self, type, coordinates, crs)
        notify(WFSGeoreferencedEvent(self))

    def setGeometryFromWKT(self, fromwkt):
        geometry = wkt.loads(fromwkt)
        type = geometry.type
        if type == 'Point':
            coords = geometry.coords[0]
        elif type == 'Polygon':
            coords = [
             list(geometry.exterior.coords)]
            logger.info(coords)
        else:
            coords = list(geometry.coords)
        self.setGeoInterface(type, coords)

    def isGeoreferenced(self):
        """Return True if the object is "on the map"."""
        return self.coordinates is not None

    def getGML(self):
        """ return geometry as GML string
        """
        if self.isGeoreferenced():
            coords = self.coordinates
            logger.info(str(coords))
            bboxTuple = bboxAsTuple(self.getGeometry())
            strbbox = str(bboxTuple[0]) + ',' + str(bboxTuple[1]) + ' ' + str(bboxTuple[2]) + ',' + str(bboxTuple[3])
            wfs = self.getWFSParent()
            if self.type == 'Polygon':
                outerCoords = coords[0]
                outerPoints = [ str(p[0]) + ',' + str(p[1]) for p in outerCoords ]
                logger.info((' ').join(outerPoints))
                gml = '<myns:' + self.featureType + ' id="' + self.id + '">'
                gml += '<gml:boundedBy> <gml:Box srsName="' + wfs.srs + '"> <gml:coordinates>' + strbbox + '</gml:coordinates> </gml:Box></gml:boundedBy>'
                gml += '<myns:msGeometry><gml:' + self.type + ' srsName="' + wfs.srs + '">'
                gml += '<gml:outerBoundaryIs><gml:LinearRing><gml:coordinates>' + (' ').join(outerPoints) + '</gml:coordinates></gml:LinearRing></gml:outerBoundaryIs>'
                gml += '</gml:' + self.type + '> </myns:msGeometry>' + self.getGMLElement() + '</myns:' + self.featureType + '>'
            elif self.type == 'Point':
                coords = [
                 coords]
                points = [ str(p[0]) + ',' + str(p[1]) for p in coords ]
                gml = '<myns:' + self.featureType + ' id="' + self.id + '"> <gml:boundedBy> <gml:Box srsName="' + wfs.srs + '"> <gml:coordinates>' + strbbox + '</gml:coordinates> </gml:Box> </gml:boundedBy> <myns:msGeometry> <gml:' + self.type + ' srsName="' + wfs.srs + '"> <gml:coordinates>' + (' ').join(points) + '</gml:coordinates> </gml:' + self.type + '> </myns:msGeometry>' + self.getGMLElement() + '</myns:' + self.featureType + '>'
            else:
                points = [ str(p[0]) + ',' + str(p[1]) for p in coords ]
                gml = '<myns:' + self.featureType + ' id="' + self.id + '"> <gml:boundedBy> <gml:Box srsName="' + wfs.srs + '"> <gml:coordinates>' + strbbox + '</gml:coordinates> </gml:Box> </gml:boundedBy> <myns:msGeometry> <gml:' + self.type + ' srsName="' + wfs.srs + '"> <gml:coordinates>' + (' ').join(points) + '</gml:coordinates> </gml:' + self.type + '> </myns:msGeometry>' + self.getGMLElement() + '</myns:' + self.featureType + '>'
            return gml
        else:
            return ''

    def getGMLElement(self):
        gml = ''
        wfs = self.getWFSParent()
        for element in wfs.getElements(self.featureType):
            attr = getattr(self, element)
            if callable(attr):
                attr = attr()
            gml = gml + '<myns:' + element + '>' + str(attr) + '</myns:' + element + '>'

        return gml

    def __getattr__(self, name):
        """Overloads getattr to return context attibutes
        """
        if hasattr(self.context, name):
            return getattr(self.context, name)
        elif hasattr(self.context, 'get' + name.capitalize()):
            return getattr(self.context, 'get' + name.capitalize())()

    def getWFSParent(self):
        """
        """
        parents = self.context.aq_chain
        isWFSenabled = False
        for o in parents:
            if IWebFeatureServiceable.providedBy(o):
                isWFSenabled = True
                break

        if isWFSenabled:
            return IWebFeatureService(o)
        else:
            return
        return


def bboxAsTuple(geometry):
    """ return the geometry bbox as tuple
    """
    envelope = geometry.envelope
    if envelope.geometryType() == 'Point':
        x = envelope.coords[0][0]
        y = envelope.coords[0][1]
        return (x, y, x, y)
    else:
        return envelope.bounds


def bboxFromTuple(bbox_tuple):
    coords = ((bbox_tuple[0], bbox_tuple[1]), (bbox_tuple[0], bbox_tuple[3]), (bbox_tuple[2], bbox_tuple[3]), (bbox_tuple[2], bbox_tuple[1]))
    return Polygon(coords)