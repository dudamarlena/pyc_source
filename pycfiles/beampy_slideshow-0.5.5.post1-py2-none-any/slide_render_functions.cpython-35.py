# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/slide_render_functions.py
# Compiled at: 2016-04-19 16:40:19
# Size of source mod 2**32: 1423 bytes
"""
Created on Fri May 15 16:27:48 2015

@author: hugo
"""
from beampy.document import document
import time

def compute_equal_space(available_size, all_elements_size, offset=0):
    """
        Function to return an equal space between elements
    """
    available_size -= offset
    total_content_size = sum(all_elements_size)
    dspace = (available_size - total_content_size) / float(len(all_elements_size) + 1)
    return dspace


def auto_place_elements(all_size, container_size, axis, contents, ytop):
    """
        container_size = (document._width, document._height)
    """
    if axis == 'x':
        max_size = container_size[0]
    if axis == 'y':
        max_size = container_size[1]
    ds = compute_equal_space(max_size, [k['height'] for k in all_size.values()], ytop)
    cpts = ds + ytop
    for data in all_size.values():
        elem = data['id']
        height = data['height']
        if axis == 'y':
            contents[elem].positionner.y['shift'] = cpts
            contents[elem].positionner.y['align'] = 'top'
            contents[elem].positionner.y['unit'] = 'px'
        if axis == 'x':
            contents[elem].positionner.x['shift'] = cpts
            contents[elem].positionner.x['align'] = 'left'
            contents[elem].positionner.x['unit'] = 'px'
        contents[elem].positionner.place(container_size, ytop=ytop)
        cpts += ds + height