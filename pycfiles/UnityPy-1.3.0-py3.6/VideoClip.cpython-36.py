# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\VideoClip.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 1446 bytes
from .NamedObject import NamedObject
from ..helpers.ResourceReader import get_resource_data

class VideoClip(NamedObject):

    def __init__(self, reader):
        super().__init__(reader=reader)
        self.original_path = reader.read_aligned_string()
        self.proxy_width = reader.read_u_int()
        self.proxy_height = reader.read_u_int()
        self.width = reader.read_u_int()
        self.height = reader.read_u_int()
        if self.version[0] > 2017 or self.version[0] == 2017 and self.version[1] >= 2:
            self.pixel_aspec_ratio_num = reader.read_u_int()
            self.pixel_aspec_ratio_den = reader.read_u_int()
        else:
            self.frame_rate = reader.read_double()
            self.frame_count = reader.read_u_long()
            self.format = reader.read_int()
            self.audio_channel_count = reader.read_u_short_array()
            reader.align_stream()
            self.audio_sample_rate = reader.read_u_int_array()
            self.audio_language = reader.read_string_array()
            source = reader.read_aligned_string()
            offset = reader.read_u_long()
            size = reader.read_u_long()
            self.has_split_alpha = reader.read_boolean()
            if source:
                self.VideoData = get_resource_data(source, self.assets_file, offset, size)
            else:
                self.VideoData = reader.read(size)