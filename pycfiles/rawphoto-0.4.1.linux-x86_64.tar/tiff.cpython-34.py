# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/rawphoto/tiff.py
# Compiled at: 2015-03-28 11:39:14
# Size of source mod 2**32: 8761 bytes
from collections import namedtuple
from io import BytesIO
import os, struct
exif_tags = {1: 'interop_index', 
 2: 'interop_version', 
 11: 'processing_software', 
 254: 'subfile_type', 
 256: 'image_width', 
 257: 'image_height', 
 258: 'bits_per_sample', 
 259: 'compression', 
 262: 'photometric_interpretation', 
 271: 'make', 
 272: 'model', 
 273: 'data_offset', 
 274: 'orientation', 
 277: 'samples_per_pixel', 
 278: 'row_per_strip', 
 279: 'data_length', 
 282: 'x_resolution', 
 283: 'y_resolution', 
 284: 'planar_configuration', 
 296: 'resolution_unit', 
 306: 'datetime', 
 513: 'data_offset', 
 514: 'data_length', 
 16400: 'custom_picture_style_file_name', 
 16416: 'ambience_info', 
 33421: 'cfa_repeat_pattern_dim', 
 33422: 'cfa_pattern_two', 
 33434: 'exposure_time', 
 33437: 'fnumber', 
 34665: 'exif', 
 34853: 'gps_data', 
 37500: 'makernote', 
 50739: 'shadow_scale', 
 50740: 'makernote', 
 50741: 'makernote_safety', 
 50752: 'raw_image_segmentation', 
 65002: 'lens', 
 65100: 'raw_file', 
 65101: 'converter', 
 65102: 'white_balance', 
 65105: 'exposure', 
 65105: 'exposure', 
 65106: 'shadows', 
 65107: 'brightness', 
 65108: 'contrast', 
 65109: 'saturation', 
 65110: 'sharpness', 
 65111: 'smoothness', 
 65112: 'moire_filter'}
endian_flags = {18761: '<', 
 19789: '>'}
tag_types = {1: 'B', 
 2: 's', 
 3: 'H', 
 4: 'L', 
 5: 'L', 
 6: 'b', 
 7: 's', 
 8: 'h', 
 9: 'l', 
 10: 'l', 
 11: 'f', 
 12: 'd', 
 13: 'L'}

def _read_tag(tag_type, fhandle):
    """Read and unpack bytes from a file.

    Args:
        tag_type - A struct format string
        fhandle - A file like object to read from
    """
    buf = fhandle.read(struct.calcsize(tag_type))
    return struct.unpack(tag_type, buf)


_HeaderFields = namedtuple('HeaderFields', [
 'endianness', 'raw_header', 'tiff_magic_word', 'first_ifd_offset'])

class Header(_HeaderFields):
    __slots__ = ()

    def __new__(cls, blob=None):
        endianness, = struct.unpack_from('>H', blob)
        endianness = endian_flags.get(endianness, '@')
        raw_header = struct.unpack(endianness + 'HHL', blob)
        return super(Header, cls).__new__(cls, endianness, raw_header, *raw_header[1:])


_IfdEntryFields = namedtuple('IfdEntryFields', [
 'tag_id', 'tag_name', 'tag_type', 'tag_type_key', 'value_len', 'raw_value'])

class IfdEntry(_IfdEntryFields):
    __slots__ = ()

    def __new__(cls, endianness, file=None, blob=None, offset=None, tags=exif_tags, tag_types=tag_types, rewind=True):
        if sum([i is not None for i in [file, blob]]) > 1:
            raise TypeError('IfdEntry must only specify one input')
        if file is not None:
            fhandle = file
        else:
            if blob is not None:
                fhandle = BytesIO(blob)
            else:
                raise TypeError('IfdEntry must specify at least one input')
            pos = fhandle.tell()
            if offset is not None:
                fhandle.seek(offset)
            tag_id, tag_type_key, value_len = _read_tag(endianness + 'HHL', fhandle)
            if tag_id in tags:
                tag_name = tags[tag_id]
            else:
                tag_name = tag_id
            tag_type = tag_types[tag_type_key]
            size = struct.calcsize(tag_type) * value_len
            if size > 4 or tag_type == 's':
                raw_value, = _read_tag(endianness + 'L', fhandle)
            else:
                if value_len > 1:
                    raw_value = _read_tag('{}{}{}'.format(endianness, value_len, tag_type), fhandle)
                else:
                    raw_value, = _read_tag(endianness + tag_type, fhandle)
        if size < 4:
            fhandle.seek(4 - size, os.SEEK_CUR)
        if rewind:
            fhandle.seek(pos)
        return super(IfdEntry, cls).__new__(cls, tag_id, tag_name, tag_type, tag_type_key, value_len, raw_value)


class Ifd(object):

    def __init__(self, endianness, file=None, blob=None, offset=None, subdirs=[], tags=exif_tags, tag_types=tag_types):
        if sum([i is not None for i in [file, blob]]) > 1:
            raise TypeError('IFD must only specify one input')
        if file is not None:
            self.fhandle = file
        else:
            if blob is not None:
                self.fhandle = BytesIO(blob)
            else:
                raise TypeError('IFD must specify an input')
        self.tags = tags
        self.subdirs = subdirs
        self.tag_types = tag_types
        pos = self.fhandle.tell()
        if offset is not None:
            self.fhandle.seek(offset)
        self.endianness = endianness
        num_entries, = _read_tag(endianness + 'H', self.fhandle)
        self.entries = {}
        self.subifds = {}
        for i in range(num_entries):
            e = IfdEntry(endianness, file=self.fhandle, tags=tags, rewind=False)
            self.entries[e.tag_name] = e
            if e.tag_id in subdirs:
                if e.value_len > 1:
                    i = 0
                    for o in self.get_value(e):
                        self.subifds[e.tag_name[i]] = Ifd(endianness, file=self.fhandle, offset=o, tags=tags, subdirs=subdirs)
                        i += 1

                else:
                    self.subifds[e.tag_name] = Ifd(endianness, file=self.fhandle, offset=e.raw_value, tags=tags, subdirs=subdirs)
                    continue

        self.next_ifd_offset, = _read_tag(endianness + 'H', self.fhandle)
        self.fhandle.seek(pos)

    def get_value(self, entry):
        """Get the value of an entry in the IFD.

        Args:
            entry - The IFDEntry to read the value for.
        """
        tag_type = entry.tag_type
        size = struct.calcsize(self.endianness + tag_type) * entry.value_len
        if size > 4 or tag_type == 's':
            pos = self.fhandle.tell()
            self.fhandle.seek(entry.raw_value)
            if tag_type == 's':
                buf = self.fhandle.read(entry.value_len)
                value, = struct.unpack('{}{}'.format(entry.value_len, tag_type), buf)
                if entry.tag_type_key == 2:
                    value = value.rstrip(b'\x00').decode('utf-8')
            else:
                if entry.value_len > 1:
                    buf = self.fhandle.read(size)
                    if len(buf) >= size:
                        value = struct.unpack_from('{}{}{}'.format(self.endianness, entry.value_len, tag_type), buf)
                    else:
                        value = entry.raw_value
                else:
                    buf = self.fhandle.read(size)
                    if len(buf) >= size:
                        value, = struct.unpack_from(self.endianness + tag_type, buf)
                    else:
                        value = entry.raw_value
            self.fhandle.seek(pos)
            return value
        else:
            return entry.raw_value