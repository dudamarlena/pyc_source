# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tw/openlayers/layer.py
# Compiled at: 2008-08-17 14:53:17
from tw.api import Widget, JSLink, js_symbol
__all__ = [
 'Grid', 'WMS', 'Google', 'Yahoo',
 'VirtualEarth', 'Vector', 'GML']

class LayerBase(Widget):
    """ Base class for Layer Widgets. """
    params = []

    @property
    def all_params(self):
        d = {}
        for param in self.params:
            d[param] = getattr(self, param)

        return d

    def update_params(self, d):
        super(LayerBase, self).update_params(d)


class Layer(Widget):
    """ An OpenLayers Layer widget.

    This widget can be used to create a layer object for OpenLayers.
    Used as a list, the Layers object can be passed to an OpenLayers
    Map widget to render the layer in a map.

    For detailed documentation on the OpenLayers API, visit the OpenLayers
    homepage: http://www.openlayers.org/
    """
    template = '\n    '
    params = ['id', 'name', 'isBaseLayer', 'displayInLayerSwitcher',
     'visibility', 'attribution', 'url', 'options', 'display']
    url = []
    url_doc = 'Base URL for Layer'
    options = {}
    options_doc = 'Extra options to tag onto the layer'
    display = {}
    display_doc = 'Display options for the layer'
    isBaseLayer = False
    isBaseLayer_doc = 'Whether or not the layer is a base layer.This should be set individually by all subclasses'
    displayInLayerSwitcher = True
    displayInLayerSwitcher_doc = "Display the layer's name inthe layer switcher."
    visibility = True
    visibility_doc = 'The layer should be displayed in the map.'
    attribution = ''
    attribition_doc = 'An attribution string'

    def update_params(self, d):
        super(Layer, self).update_params(d)


class Grid(Layer):
    """Base class for layer types that use tiles, e.g. WMS
    """
    params = [
     'tileSize', 'singleTile', 'ratio', 'buffer', 'numLoadingTiles']
    tileSize = None
    tileSize_doc = 'The size of a tile in the grid.'
    singleTile = False
    singleTile_doc = 'Moves the layer into single-tile mode,meaning that only one tile will be loaded.'
    ratio = 1.5
    ratio_doc = 'Used only when in single-tile mode, this specifiesthe ratio of the size of the single tile to thesize of the map.'
    buffer = 2
    buffer_doc = 'Used only when in gridded mode, this specifies thethe ratio of the number of extra rows and columns oftiles on each side which will surround the minimum gridtiles to cover the map.'

    def update_params(self, d):
        super(Grid, self).update_params(d)


class WMS(Grid):
    """OpenLayers WMS Layer widget. It loads tiles from images
    rendered by an OGC Web Map Service (WMS) server.
    """
    params = [
     'url', 'options']
    url = None
    url_doc = 'The url for the WMS service'
    options = {}
    options_doc = 'A dictionary of options for WMS layer. Read the WMSlayer options in  the OpenLayers documentation.'

    def update_params(self, d):
        super(WMS, self).update_params(d)


class OSMMapnik(Grid):
    """OpenLayers Mapnik Layer widget for OpenStreetMap. It loads
    Mapnik tiles served by an OpenStreetMap Tile Server. 
    """
    params = [
     'url', 'options']
    url = None
    url_doc = 'The url for the OSM tile service'
    options = {}
    options_doc = 'A dictionary of options for OSM Mapnik layer. Readthe OSM Mapnik layer options in  the OpenStreetMap documentation.'

    def update_params(self, d):
        super(OSMMapnik, self).update_params(d)


class OSMRenderer(Grid):
    """OpenLayers OpenStreetMap Layer widget. It loads OSMRenderer tiles
    served by OpenStreetMap OSMRenderer Server.
    """
    params = [
     'url', 'options']
    url = None
    url_doc = 'The url for the OSMRenderer service'
    options = {}
    options_doc = 'A dictionary of options for OSMRenderer layer. Read theOSMRenderer documentation at OpenStreetMap site.'

    def update_params(self, d):
        super(OSMRenderer, self).update_params(d)


class Google(Layer):
    """This creates layer for Google Maps.
    """
    params = [
     'type', 'sphericalMercator', 'apikey']
    type = None
    type_doc = 'Type of Google Map. One of None (default),G_SATELLITE_MAP' or 'G_HYBRID_MAP'
    sphericalMercator = False
    sphericalMercator_doc = 'Whether Spherical Mercator Projectionis to be used.'
    apikey = ''
    apikey_doc = 'The api key for accessing google maps api.Register at google maps to obtain an api key.'

    def update_params(self, d):
        super(Google, self).update_params(d)


class Yahoo(Layer):
    """Creates a layer for Yahoo Maps.
    """
    params = [
     'sphericalMercator', 'apikey']
    sphericalMercator = False
    sphericalMercator_doc = 'Whether Spherical Mercator Projectionis to be used.'
    apikey = ''
    apikey_doc = 'The api key (aka appid) for accessing yahoo maps.Register at yahoo maps to obtain an appid.'

    def update_params(self, d):
        super(Yahoo, self).update_params(d)


class VirtualEarth(Layer):
    """Creates a layer for Microsoft Virtual Earth Maps.
    """
    params = [
     'sphericalMercator', 'apikey']
    sphericalMercator = False
    sphericalMercator_doc = 'Whether Spherical Mercator Projectionis to be used.'
    apikey = ''
    apikey_doc = 'The api key for Virtual Earth.'

    def update_params(self, d):
        super(VirtualEarth, self).update_params(d)


class Vector(Layer):
    """Base layer for all layers containing vector Features e.g. GML.
    """
    params = [
     'isBaseLayer', 'isFixed', 'isVector',
     'reportError', 'style', 'geometryType']
    isBaseLayer = True
    isBaseLayer_doc = 'Whether the layer is a base layer'
    isFixed = False
    isFixed_doc = 'Whether the layer remains at one place while dragging'
    isVector = True
    isVector_doc = 'Whether the layer is a vector layer'
    reportError = False
    reportError_doc = 'Whether to report error via alertswhen loading of renderers fails.'
    style_doc = 'Default style for the layer'
    geometryType_doc = 'This allows limiting the types of geometriesthis layer supports. This shoud be set tosomething like *OpenLayers.Geometry.Point*to limit access.'

    def update_params(self, d):
        super(Vector, self).update_params(d)


class GML(Vector):
    """Creats a vector layer where the features are loaded from a feature
    server. Although the layer is known as GML for Geography Markup Language
    it may be used for feaures in other formats like GeoJSON, GeoRSS, etc.
    """
    params = [
     'format', 'formatOptions']
    format = 'GML'
    format_doc = 'The format the data should be parsed in'
    formatOptions = {}
    formatOptions_doc = 'A dictionary of options for the format'

    def update_params(self, d):
        super(GML, self).update_params(d)