# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/maps/google/gmap.py
# Compiled at: 2018-07-11 18:15:30
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.six.moves import xrange
from django.contrib.gis.maps.google.overlays import GPolygon, GPolyline, GMarker

class GoogleMapException(Exception):
    pass


GOOGLE_MAPS_URL = 'http://maps.google.com/maps?file=api&v=%s&key='

class GoogleMap(object):
    """A class for generating Google Maps JavaScript."""
    onunload = mark_safe('onunload="GUnload()"')
    vml_css = mark_safe('v\\:* {behavior:url(#default#VML);}')
    xmlns = mark_safe('xmlns:v="urn:schemas-microsoft-com:vml"')

    def __init__(self, key=None, api_url=None, version=None, center=None, zoom=None, dom_id='map', kml_urls=[], polylines=None, polygons=None, markers=None, template='gis/google/google-map.js', js_module='geodjango', extra_context={}):
        if not key:
            try:
                self.key = settings.GOOGLE_MAPS_API_KEY
            except AttributeError:
                raise GoogleMapException('Google Maps API Key not found (try adding GOOGLE_MAPS_API_KEY to your settings).')

        else:
            self.key = key
        if not version:
            self.version = getattr(settings, 'GOOGLE_MAPS_API_VERSION', '2.x')
        else:
            self.version = version
        if not api_url:
            self.api_url = getattr(settings, 'GOOGLE_MAPS_URL', GOOGLE_MAPS_URL) % self.version
        else:
            self.api_url = api_url
        self.dom_id = dom_id
        self.extra_context = extra_context
        self.js_module = js_module
        self.template = template
        self.kml_urls = kml_urls
        overlay_info = [
         [
          GMarker, markers, 'markers'],
         [
          GPolygon, polygons, 'polygons'],
         [
          GPolyline, polylines, 'polylines']]
        for overlay_class, overlay_list, varname in overlay_info:
            setattr(self, varname, [])
            if overlay_list:
                for overlay in overlay_list:
                    if isinstance(overlay, overlay_class):
                        getattr(self, varname).append(overlay)
                    else:
                        getattr(self, varname).append(overlay_class(overlay))

        self.calc_zoom = False
        if self.polygons or self.polylines or self.markers:
            if center is None or zoom is None:
                self.calc_zoom = True
        if zoom is None:
            zoom = 4
        self.zoom = zoom
        if center is None:
            center = (0, 0)
        self.center = center
        return

    def render(self):
        """
        Generates the JavaScript necessary for displaying this Google Map.
        """
        params = {'calc_zoom': self.calc_zoom, 'center': self.center, 
           'dom_id': self.dom_id, 
           'js_module': self.js_module, 
           'kml_urls': self.kml_urls, 
           'zoom': self.zoom, 
           'polygons': self.polygons, 
           'polylines': self.polylines, 
           'icons': self.icons, 
           'markers': self.markers}
        params.update(self.extra_context)
        return render_to_string(self.template, params)

    @property
    def body(self):
        """Returns HTML body tag for loading and unloading Google Maps javascript."""
        return format_html('<body {0} {1}>', self.onload, self.onunload)

    @property
    def onload(self):
        """Returns the `onload` HTML <body> attribute."""
        return format_html('onload="{0}.{1}_load()"', self.js_module, self.dom_id)

    @property
    def api_script(self):
        """Returns the <script> tag for the Google Maps API javascript."""
        return format_html('<script src="{0}{1}" type="text/javascript"></script>', self.api_url, self.key)

    @property
    def js(self):
        """Returns only the generated Google Maps JavaScript (no <script> tags)."""
        return self.render()

    @property
    def scripts(self):
        """Returns all <script></script> tags required with Google Maps JavaScript."""
        return format_html('{0}\n  <script type="text/javascript">\n//<![CDATA[\n{1}//]]>\n  </script>', self.api_script, mark_safe(self.js))

    @property
    def style(self):
        """Returns additional CSS styling needed for Google Maps on IE."""
        return format_html('<style type="text/css">{0}</style>', self.vml_css)

    @property
    def xhtml(self):
        """Returns XHTML information needed for IE VML overlays."""
        return format_html('<html xmlns="http://www.w3.org/1999/xhtml" {0}>', self.xmlns)

    @property
    def icons(self):
        """Returns a sequence of GIcon objects in this map."""
        return set([ marker.icon for marker in self.markers if marker.icon ])


class GoogleMapSet(GoogleMap):

    def __init__(self, *args, **kwargs):
        """
        A class for generating sets of Google Maps that will be shown on the
        same page together.

        Example:
         gmapset = GoogleMapSet( GoogleMap( ... ), GoogleMap( ... ) )
         gmapset = GoogleMapSet( [ gmap1, gmap2] )
        """
        template = kwargs.pop('template', 'gis/google/google-multi.js')
        self.map_template = kwargs.pop('map_template', 'gis/google/google-single.js')
        super(GoogleMapSet, self).__init__(**kwargs)
        self.template = template
        if isinstance(args[0], (tuple, list)):
            self.maps = args[0]
        else:
            self.maps = args
        self.dom_ids = [ 'map%d' % i for i in xrange(len(self.maps)) ]

    def load_map_js(self):
        """
        Returns JavaScript containing all of the loading routines for each
        map in this set.
        """
        result = []
        for dom_id, gmap in zip(self.dom_ids, self.maps):
            tmp = (
             gmap.template, gmap.dom_id)
            gmap.template = self.map_template
            gmap.dom_id = dom_id
            result.append(gmap.js)
            gmap.template, gmap.dom_id = tmp

        return mark_safe(('').join(result))

    def render(self):
        """
        Generates the JavaScript for the collection of Google Maps in
        this set.
        """
        params = {'js_module': self.js_module, 'dom_ids': self.dom_ids, 
           'load_map_js': self.load_map_js(), 
           'icons': self.icons}
        params.update(self.extra_context)
        return render_to_string(self.template, params)

    @property
    def onload(self):
        """Returns the `onload` HTML <body> attribute."""
        return mark_safe('onload="%s.load()"' % self.js_module)

    @property
    def icons(self):
        """Returns a sequence of all icons in each map of the set."""
        icons = set()
        for map in self.maps:
            icons |= map.icons

        return icons