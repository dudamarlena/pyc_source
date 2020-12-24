# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ledermac/devel/plone41/zeocluster/src/collective.geo.opensearch/collective/geo/opensearch/browser/maplayers.py
# Compiled at: 2013-01-29 07:14:40
import urllib
from collective.geo.mapwidget.browser.widget import MapLayers
from collective.geo.mapwidget.maplayers import MapLayer

class FeedMapLayer(MapLayer):
    """
    a layer for a Feed
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'
        query_string = 'searchTerms=' + urllib.quote_plus(self.request.form.get('searchTerms', ''))
        return 'function() {\n                return new OpenLayers.Layer.Vector("%s", {\n                    protocol: new OpenLayers.Protocol.HTTP({\n                      url: "%s@@opensearch_link.kml?%s",\n                      format: new OpenLayers.Format.KML({\n                        extractStyles: true,\n                        extractAttributes: true})\n                      }),\n                    strategies: [new OpenLayers.Strategy.Fixed()],\n                    visibility: true,\n                    /*eventListeners: { \'loadend\': function(event) {\n                                 var extent = this.getDataExtent()\n                                 this.map.zoomToExtent(extent);\n                                }\n                            },*/\n                    projection: cgmap.createDefaultOptions().displayProjection\n                  });\n                } ' % (self.context.Title().replace("'", '&apos;'),
         context_url, query_string)


class KMLMapLayers(MapLayers):
    """
    create all layers for this view.
    """

    def layers(self):
        layers = super(KMLMapLayers, self).layers()
        layers.append(FeedMapLayer(self.context, self.request))
        return layers


class KMLFolderMapLayers(MapLayers):
    """
    create all layers for this view.
    """

    def layers(self):
        layers = super(KMLFolderMapLayers, self).layers()
        type_filter = {'portal_type': ['Link']}
        for r in self.context.getFolderContents(contentFilter=type_filter):
            obj = r.getObject()
            if obj.getLayout() == 'feed_map_view.html':
                layers.append(FeedMapLayer(obj, self.request))

        return layers