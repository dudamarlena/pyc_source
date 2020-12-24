# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/atlas/fields.py
# Compiled at: 2015-04-21 15:30:03
import re
from django import forms
from django.contrib.gis.db import models
from django.contrib.gis.forms import fields
from django.forms.widgets import MultiWidget, TextInput
from django.conf import settings

class LonLatWidget(MultiWidget):

    def __init__(self, **kwargs):
        self.longitude = 0
        self.latitude = 0
        attrs = kwargs['attrs'] if 'attrs' in kwargs else None
        defaults = {'widgets': (TextInput(attrs=attrs), TextInput(attrs=attrs))}
        defaults.update(kwargs)
        super(LonLatWidget, self).__init__(**defaults)
        return

    def decompress(self, value):
        if value:
            if isinstance(value, list) and len(value) == 2:
                return value
            else:
                m = re.match('POINT \\((?P<lon>[-+]?\\d+(\\.\\d*)?) (?P<lat>[-+]?\\d+(\\.\\d*)?)\\)', str(value))
                return [m.group('lon'), m.group('lat')]

        return [
         None, None]

    def render(self, name, value, attrs=None):
        vals = self.decompress(value)
        if vals[0] and vals[1]:
            self.longitude = float(vals[0])
            self.latitude = float(vals[1])
        return super(LonLatWidget, self).render(name, value, attrs)

    def format_output(self, rendered_widgets):
        pat = 'id="(?P<label>\\w+)"'
        id1 = re.search(pat, rendered_widgets[0]).group('label')
        id2 = re.search(pat, rendered_widgets[1]).group('label')
        map_code = ''
        map_key = settings.DJANGO_ATLAS.get('google_maps_api_key', None)
        if map_key:
            map_code = '<script type="text/javascript">\n                                LonLatWidget = {\n                                    initialize: function() {\n                                        var lon = %f, lat = %f;\n                                        var hasLocation = !(lon == 0 && lat == 0);\n                                        var mapOptions = {\n                                            zoom: hasLocation ? 12 : 2,\n                                            center: new google.maps.LatLng(lat, lon),\n                                            mapTypeId: google.maps.MapTypeId.ROADMAP,\n                                            panControl: false,\n                                            zoomControl: true,\n                                            mapTypeControl: false,\n                                            scaleControl: false,\n                                            streetViewControl: false,\n                                            overviewMapControl: false,\n                                        }\n                                        var max_width = $(document).width() > 600 ? 600 : $(document).width();\n                                        var map_el = $("#map_canvas").width(max_width).height(max_width)[0];\n                                        var map = new google.maps.Map(map_el, mapOptions);\n                                        var marker = new google.maps.Marker({\n                                            map: map,\n                                            title: \'Selected location\'\n                                        });\n                                        if (hasLocation) {\n                                            marker.setPosition(new google.maps.LatLng(lat, lon));\n                                        }\n                                        google.maps.event.addListener(map, \'click\', function(event) {\n                                            var pos = event.latLng;\n                                            document.getElementById("%s").value = pos.lng();\n                                            document.getElementById("%s").value = pos.lat();\n                                            marker.setPosition(pos);\n                                        });\n                                        \n                                        this.marker = marker;\n                                        this.map = map;\n                                        this.geocoder = new google.maps.Geocoder();\n                                    },\n\n                                    loadScript: function() {\n                                        var script = document.createElement("script");\n                                        script.type = "text/javascript";\n                                        script.src = "//maps.googleapis.com/maps/api/js?key=%s&sensor=false&callback=LonLatWidget.initialize";\n                                        document.body.appendChild(script);\n                                    },\n                                    \n                                    search: function(address) {\n                                        var marker = this.marker;\n                                        var map = this.map;\n                                        this.geocoder.geocode(\n                                            {\'address\': address}, \n                                            function(results, status) { \n                                                if (status == google.maps.GeocoderStatus.OK) { \n                                                    var pos = results[0].geometry.location;\n                                                    document.getElementById("%s").value = pos.lng();\n                                                    document.getElementById("%s").value = pos.lat();\n                                                    marker.setPosition(pos);\n                                                    map.setCenter(pos);\n                                                    map.setZoom(12);\n                                                } \n                                                else {\n                                                    alert("Your search returned no results."); \n                                                } \n                                            }\n                                        );\n                                    }\n                                };\n                                \n                                if (window.addEventListener) {\n                                    window.addEventListener(\'load\', LonLatWidget.loadScript, false);\n                                } \n                                else if (window.attachEvent) {\n                                    window.attachEvent(\'onload\', LonLatWidget.loadScript);\n                                }\n                            </script>' % (
             self.longitude, self.latitude, id1, id2, map_key, id1, id2)
            map_code += '<div><div style="margin: 16px 0px 8px 0px;"><input style="vertical-align: middle; width: 30em;" type="text" id="search_address" value=""/>\n            <input type="submit" style="vertical-align: middle;" onclick="LonLatWidget.search(document.getElementById(\'search_address\').value); return false;" value="Search"/></div>\n            <div id="map_canvas"></div></div>'
        return '<table><tr><td><label for="%s">Longitude:</label></td><td>%s</td></tr>\n                <tr><td><label for="%s">Latitude:</label></td><td>%s</td></tr></table>%s' % (
         id1, rendered_widgets[0], id2, rendered_widgets[1], map_code)


class CoordinateFormField(fields.GeometryField, forms.MultiValueField):

    def __init__(self, *args, **kwargs):
        defaults = {'widget': LonLatWidget, 
           'fields': (
                    forms.CharField, forms.CharField)}
        defaults.update(kwargs)
        fields.GeometryField.__init__(self, *args, **defaults)
        defaults.pop('srid', None)
        defaults.pop('null', None)
        defaults.pop('geom_type', None)
        forms.MultiValueField.__init__(self, *args, **defaults)
        return

    def clean(self, value):
        lon = value[0]
        lat = value[1]
        try:
            lon = float(lon)
        except ValueError:
            raise forms.ValidationError('Longitude is not a valid number')

        try:
            lat = float(lat)
        except ValueError:
            raise forms.ValidationError('Latitude is not a valid number')

        if lon < -180 or lon > 180:
            raise forms.ValidationError('Longitude is not within -180 to 180')
        if lat < -90 or lat > 90:
            raise forms.ValidationError('Latitude is not within -90 to 90')
        val = 'POINT (%s %s)' % (value[0], value[1])
        return super(CoordinateFormField, self).clean(val)

    def compress(self, values):
        return 'POINT (%s %s)' % (value[0], value[1])


class CoordinateField(models.PointField):

    def formfield(self, **kwargs):
        defaults = {'form_class': CoordinateFormField}
        defaults.update(kwargs)
        return super(CoordinateField, self).formfield(**defaults)