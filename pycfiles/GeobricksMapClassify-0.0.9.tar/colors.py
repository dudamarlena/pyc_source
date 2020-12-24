# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_sld/geobricks_mapclassify/core/colors.py
# Compiled at: 2015-03-03 10:44:16
from brewer2mpl import get_map as brewer2mpl_get_map
from geobricks_common.core.log import logger
log = logger(__file__)

def get_colors(data, intervals):
    reverse = False if 'reverse' not in data else data['reverse']
    intervals = 3 if intervals < 3 else intervals
    if 'colors' in data and data['colors'] is not None:
        if reverse:
            return data['colors'][::-1]
        else:
            return data['colors']

    else:
        color_ramp = data['colorramp']
        try:
            return brewer2mpl_get_map(color_ramp, 'Sequential', intervals, reverse=reverse).hex_colors
        except Exception as e:
            log.warn(e)

        try:
            return brewer2mpl_get_map(color_ramp, 'Diverging', intervals, reverse=reverse).hex_colors
        except Exception as e:
            log.warn(e)

        try:
            return brewer2mpl_get_map(color_ramp, 'Qualitative', intervals, reverse=reverse).hex_colors
        except Exception as e:
            log.warn(e)

    return