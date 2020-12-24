# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.8/site-packages/MetaStalk/modules/GPSCheck.py
# Compiled at: 2020-05-08 18:09:31
# Size of source mod 2**32: 1351 bytes
"""Makes geo chart with plots of GPS data"""
import logging
import plotly.express as px
import MetaStalk.utils as utils
log = logging.getLogger('MetaStalk')

def gps_check(photos: list) -> px.scatter_mapbox:
    """GPS_Check

    Takes a list of photos and creates a geo plot of them

    Arguments:
        photos {list} -- A list of dictionaries with phot information.

    Returns
        px.scatter_mapbox -- Map plot with photos plotted.
    """
    log.info('Starting GPS Chart')
    lats = []
    longs = []
    gps_photos = []
    for each in photos:
        if 'GPS GPSLatitudeRef' in each.keys():
            gps_photos.append(each['item'])
            gps_data = utils.gps_parse(each)
            lats.append(gps_data['latitude'])
            longs.append(gps_data['longitude'])
            log.debug('%s has GPS data', each['item'])
        else:
            log.info('%s has no GPS data', each['item'])
    else:
        points = []
        for x, _ in enumerate(gps_photos):
            points.append((lats[x], longs[x]))
        else:
            fig = px.scatter_mapbox(lon=longs, lat=lats,
              hover_name=gps_photos,
              title='Geo Locations')
            fig.update_layout(mapbox_style='open-street-map', title_x=0.5)
            return fig