# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\dsx\code\amaptor\amaptor\classes\map_frame.py
# Compiled at: 2017-06-28 23:31:29
# Size of source mod 2**32: 1474 bytes
import logging
log = logging.getLogger('amaptor')
from amaptor.version_check import mp
from amaptor.errors import MapNotFoundError

class MapFrame(object):

    def __init__(self, map_frame_object, layout):
        self._map_frame_object = map_frame_object
        self.layout = layout
        try:
            self._map = layout.project.find_map(map_frame_object.map.name)
        except MapNotFoundError:
            self._map = None

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