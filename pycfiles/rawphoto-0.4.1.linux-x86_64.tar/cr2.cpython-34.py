# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/rawphoto/cr2.py
# Compiled at: 2015-03-28 11:39:14
# Size of source mod 2**32: 3335 bytes
from collections import namedtuple
from rawphoto.raw import Raw
from rawphoto.tiff import endian_flags
from rawphoto.tiff import exif_tags
from rawphoto.tiff import Ifd
import struct
_HeaderFields = namedtuple('HeaderFields', [
 'endianness', 'raw_header', 'tiff_magic_word', 'tiff_offset',
 'magic_word', 'major_version', 'minor_version', 'raw_ifd_offset'])
subdirs = [
 34665]
tags = exif_tags.copy()
tags.update({1: 'canon_camera_settings', 
 2: 'canon_focal_length', 
 4: 'canon_shot_info', 
 5: 'canon_panorama', 
 6: 'canon_image_type', 
 7: 'canon_firmware_version', 
 8: 'file_number', 
 9: 'owner_name', 
 12: 'serial_number', 
 13: 'canon_camera_info', 
 14: 'canon_file_length', 
 15: 'custom_functions', 
 16: 'canon_model_id', 
 17: 'canon_movie_info', 
 18: 'canon_af_info', 
 19: 'thumbnail_image_valid_area', 
 21: 'serial_number_format', 
 26: 'super_macro', 
 28: 'date_stamp_mode', 
 29: 'my_colors', 
 30: 'firmware_revision', 
 35: 'categories', 
 36: 'face_detection_1', 
 37: 'face_detection_2', 
 38: 'canon_af_info_2', 
 39: 'contrast_info', 
 40: 'image_unique_id', 
 47: 'face_detection_3', 
 53: 'time_info', 
 60: 'canon_af_info_3', 
 129: 'raw_data_offset', 
 131: 'original_decision_data_offset', 
 149: 'lens_model', 
 150: 'serial_info', 
 174: 'color_temperature', 
 180: 'color_space'})

class Header(_HeaderFields):
    __slots__ = ()

    def __new__(cls, blob=None):
        endianness, = struct.unpack_from('>H', blob)
        endianness = endian_flags.get(endianness, '@')
        raw_header = struct.unpack(endianness + 'HHLHBBL', blob)
        return super(Header, cls).__new__(cls, endianness, raw_header, *raw_header[1:])


class Cr2(Raw):

    def __init__(self, blob=None, file=None, filename=None):
        super(Cr2, self).__init__(blob=blob, file=file, filename=filename)
        pos = self.tell()
        self.header = Header(self.read(16))
        self.ifds = []
        self.ifds.append(Ifd(self.endianness, file=self.fhandle, tags=tags, subdirs=subdirs))
        next_ifd_offset = self.ifds[0].next_ifd_offset
        while next_ifd_offset != 0:
            self.seek(next_ifd_offset)
            self.ifds.append(Ifd(self.endianness, file=self.fhandle, tags=tags, subdirs=subdirs))
            next_ifd_offset = self.ifds[(len(self.ifds) - 1)].next_ifd_offset

        self.seek(pos)

    @property
    def preview_image(self):
        """Read a quarter sized image as RGB data from the CR2 file."""
        return self._get_image_data()

    @property
    def thumbnail_image(self):
        """Read a thumbnail image from the CR2."""
        return self._get_image_data(num=1)

    @property
    def uncompressed_full_size_image(self):
        """Read uncompressed JPEG data with no WB settings from the CR2."""
        return self._get_image_data(num=2)

    @property
    def raw_data(self):
        """Read the raw image data from the CR2."""
        return self._get_image_data(num=3)