# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nick/accessmap/projects/crossify/venv/lib/python3.5/site-packages/crossify/opensidewalks.py
# Compiled at: 2017-12-11 11:40:22
# Size of source mod 2**32: 957 bytes
import geopandas as gpd
from shapely.geometry import LineString

def make_links(st_crossings, offset=1):
    crs = st_crossings.crs
    links = []
    for idx, row in st_crossings.iterrows():
        geom = row.geometry
        if geom.length > 2 * offset:
            first = geom.interpolate(offset)
            last = geom.interpolate(geom.length - offset)
            sw1 = LineString([geom.coords[0], first])
            sw2 = LineString([geom.coords[(-1)], last])
            new_geom = LineString([first, last])
            for link in [sw1, sw2]:
                links.append({'geometry': link, 
                 'highway': 'footway', 
                 'footway': 'sidewalk', 
                 'layer': row['layer']})

            st_crossings.loc[(idx, 'geometry')] = new_geom

    sw_links = gpd.GeoDataFrame(links)
    sw_links.crs = crs
    st_crossings.crs = crs
    return (
     st_crossings, sw_links)