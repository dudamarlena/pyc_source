# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/KyunghoonKim/anaconda/lib/python2.7/site-packages/umap/get.py
# Compiled at: 2016-01-20 11:28:38
from vincenty import vincenty
from bson.son import SON
from IPython.display import HTML
import folium

def distance(source, target):
    """
    1 = 1km
    :param source:
    :param target:
    :return:
    """
    return vincenty(source, target)


def nearest(database, name, location, maxkm):
    u"""
    MongoDB GeoSpatial Search
    :param database: db.test
    :param name: field name 'gps'
    :param location: [lat, lon]
    "All documents must store location data in the same order.
    If you use latitude and longitude as your coordinate system,
    always store longitude first.
    MongoDB’s 2d spherical index operators only recognize
    [longitude, latitude] ordering."
    :param maxkm: limit of distance
    :return: count, database
    """
    query = {name: SON([('$near', location),
            (
             '$maxDistance', maxkm / 111.12)])}
    data = database.find(query)
    return (data.count(), data)


def inline_map(map):
    """
    Embeds the HTML source of the map directly into the IPython notebook.

    This method will not work if the map depends on any files (json data). Also this uses
    the HTML5 srcdoc attribute, which may not be supported in all browsers.
    """
    if isinstance(map, folium.Map):
        map._build_map()
        srcdoc = map.HTML.replace('"', '&quot;')
        embed = HTML(('<iframe srcdoc="{srcdoc}" style="width: 100%; height: 500px; border: none"></iframe>').format(srcdoc=srcdoc))
    else:
        raise ValueError('{!r} is not a folium Map instance.')
    return embed


def embed_map(map, path='map.html'):
    path = path
    map.create_map(path=path)
    return HTML(('<iframe src="files/{path}" style="width: 100%; height: 510px; border: none"></iframe>').format(path=path))


class Map:
    """
    Map with folium
    """

    def __init__(self):
        """
        lat, lon, zoom_start
        """
        self.lat = 37.27
        self.lon = 127.01
        self.zoom_start = 7
        self.m = folium.Map(location=[self.lat, self.lon], zoom_start=self.zoom_start)
        self.circles = []

    def reset(self):
        """
        reset circles, map
        :return:
        """
        self.circles = []
        self.m = folium.Map(location=[self.lat, self.lon], zoom_start=self.zoom_start)

    def drawing(self):
        """
        Map drawing
        :return: iframe map
        """
        if len(self.circles) > 0:
            for c in self.circles:
                self.m.circle_marker(location=c[0], radius=c[1], fill_opacity=c[2], popup=c[3], fill_color=c[4], line_color=c[5])

        self.m._build_map()
        srcdoc = self.m.HTML.replace('"', '&quot;')
        embed = HTML(('<iframe srcdoc="{srcdoc}" style="width: 100%; height: 500px; border: none"></iframe>').format(srcdoc=srcdoc))
        return embed

    def add_circle(self, location, radius=50, fill_opacity=0.8, popup='', fill_color='black', line_color='None'):
        """
        Add a circle in the map
        :param location: [lat, lon]
        :param radius: circle radius
        :param fill_opacity: transparency
        :param popup: text
        :param fill_color:
        :param line_color: circle line color
        :return:
        """
        if type(popup) == unicode:
            popup = popup.encode('utf8')
        self.circles.append([location[::-1], radius, fill_opacity, popup, fill_color, line_color])

    def get_circles(self):
        """
        Get a list of circles
        :return: list
        """
        return self.circles