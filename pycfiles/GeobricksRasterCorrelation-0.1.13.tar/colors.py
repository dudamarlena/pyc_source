# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/geobricks/geobricks/server/geobricks_raster_correlation/geobricks_raster_correlation/core/colors.py
# Compiled at: 2015-06-04 04:11:33
from brewer2mpl import get_map as brewer2mpl_get_map
from geobricks_common.core.log import logger
log = logger(__file__)

def get_colors(color_ramp, intervals, reverse=False):
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