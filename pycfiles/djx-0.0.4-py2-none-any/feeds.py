# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/gis/feeds.py
# Compiled at: 2019-02-14 00:35:16
from __future__ import unicode_literals
from django.contrib.syndication.views import Feed as BaseFeed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed

class GeoFeedMixin(object):
    """
    This mixin provides the necessary routines for SyndicationFeed subclasses
    to produce simple GeoRSS or W3C Geo elements.
    """

    def georss_coords(self, coords):
        """
        In GeoRSS coordinate pairs are ordered by lat/lon and separated by
        a single white space.  Given a tuple of coordinates, this will return
        a unicode GeoRSS representation.
        """
        return (b' ').join(b'%f %f' % (coord[1], coord[0]) for coord in coords)

    def add_georss_point(self, handler, coords, w3c_geo=False):
        """
        Adds a GeoRSS point with the given coords using the given handler.
        Handles the differences between simple GeoRSS and the more popular
        W3C Geo specification.
        """
        if w3c_geo:
            lon, lat = coords[:2]
            handler.addQuickElement(b'geo:lat', b'%f' % lat)
            handler.addQuickElement(b'geo:lon', b'%f' % lon)
        else:
            handler.addQuickElement(b'georss:point', self.georss_coords((coords,)))

    def add_georss_element(self, handler, item, w3c_geo=False):
        """
        This routine adds a GeoRSS XML element using the given item and handler.
        """
        geom = item.get(b'geometry')
        if geom is not None:
            if isinstance(geom, (list, tuple)):
                box_coords = None
                if isinstance(geom[0], (list, tuple)):
                    if len(geom) == 2:
                        box_coords = geom
                    else:
                        raise ValueError(b'Only should be two sets of coordinates.')
                elif len(geom) == 2:
                    self.add_georss_point(handler, geom, w3c_geo=w3c_geo)
                elif len(geom) == 4:
                    box_coords = (geom[:2], geom[2:])
                else:
                    raise ValueError(b'Only should be 2 or 4 numeric elements.')
                if box_coords is not None:
                    if w3c_geo:
                        raise ValueError(b'Cannot use simple GeoRSS box in W3C Geo feeds.')
                    handler.addQuickElement(b'georss:box', self.georss_coords(box_coords))
            else:
                gtype = str(geom.geom_type).lower()
                if gtype == b'point':
                    self.add_georss_point(handler, geom.coords, w3c_geo=w3c_geo)
                else:
                    if w3c_geo:
                        raise ValueError(b'W3C Geo only supports Point geometries.')
                    if gtype in ('linestring', 'linearring'):
                        handler.addQuickElement(b'georss:line', self.georss_coords(geom.coords))
                    elif gtype in ('polygon', ):
                        handler.addQuickElement(b'georss:polygon', self.georss_coords(geom[0].coords))
                    else:
                        raise ValueError(b'Geometry type "%s" not supported.' % geom.geom_type)
        return


class GeoRSSFeed(Rss201rev2Feed, GeoFeedMixin):

    def rss_attributes(self):
        attrs = super(GeoRSSFeed, self).rss_attributes()
        attrs[b'xmlns:georss'] = b'http://www.georss.org/georss'
        return attrs

    def add_item_elements(self, handler, item):
        super(GeoRSSFeed, self).add_item_elements(handler, item)
        self.add_georss_element(handler, item)

    def add_root_elements(self, handler):
        super(GeoRSSFeed, self).add_root_elements(handler)
        self.add_georss_element(handler, self.feed)


class GeoAtom1Feed(Atom1Feed, GeoFeedMixin):

    def root_attributes(self):
        attrs = super(GeoAtom1Feed, self).root_attributes()
        attrs[b'xmlns:georss'] = b'http://www.georss.org/georss'
        return attrs

    def add_item_elements(self, handler, item):
        super(GeoAtom1Feed, self).add_item_elements(handler, item)
        self.add_georss_element(handler, item)

    def add_root_elements(self, handler):
        super(GeoAtom1Feed, self).add_root_elements(handler)
        self.add_georss_element(handler, self.feed)


class W3CGeoFeed(Rss201rev2Feed, GeoFeedMixin):

    def rss_attributes(self):
        attrs = super(W3CGeoFeed, self).rss_attributes()
        attrs[b'xmlns:geo'] = b'http://www.w3.org/2003/01/geo/wgs84_pos#'
        return attrs

    def add_item_elements(self, handler, item):
        super(W3CGeoFeed, self).add_item_elements(handler, item)
        self.add_georss_element(handler, item, w3c_geo=True)

    def add_root_elements(self, handler):
        super(W3CGeoFeed, self).add_root_elements(handler)
        self.add_georss_element(handler, self.feed, w3c_geo=True)


class Feed(BaseFeed):
    """
    This is a subclass of the `Feed` from `django.contrib.syndication`.
    This allows users to define a `geometry(obj)` and/or `item_geometry(item)`
    methods on their own subclasses so that geo-referenced information may
    placed in the feed.
    """
    feed_type = GeoRSSFeed

    def feed_extra_kwargs(self, obj):
        return {b'geometry': self._get_dynamic_attr(b'geometry', obj)}

    def item_extra_kwargs(self, item):
        return {b'geometry': self._get_dynamic_attr(b'item_geometry', item)}