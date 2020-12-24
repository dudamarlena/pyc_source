# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\dsx.AD3\Code\amaptor\amaptor\classes\map_frame.py
# Compiled at: 2017-02-16 16:41:35
# Size of source mod 2**32: 1380 bytes
import logging
log = logging.getLogger('amaptor')
from amaptor.version_check import mp
from amaptor.errors import *

class MapFrame(object):

    def __init__(self, map_frame_object, layout):
        self._map_frame_object = map_frame_object
        self.layout = layout
        try:
            self._map = layout.project.find_map(map_frame_object.map.name)
        except MapNotFoundError:
            pass

    def _set_map(self, amaptor_map):
        self._map = amaptor_map
        self._map._index_frames()
        self._map_frame_object.map = amaptor_map.map_object

    def set_extent(self, extent_object):
        self._map_frame_object.camera.setExtent(extent_object)

    def get_extent(self):
        return self._map_frame_object.camera.getExtent()

    @property
    def name(self):
        return self._map_frame_object.name

    @name.setter
    def name(self, value):
        self._map_frame_object.name = value

    @property
    def map(self):
        return self._map

    @map.setter
    def map(self, value):
        self._set_map(value)