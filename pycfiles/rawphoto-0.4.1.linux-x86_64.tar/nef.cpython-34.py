# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/rawphoto/nef.py
# Compiled at: 2015-03-28 11:39:14
# Size of source mod 2**32: 1664 bytes
from rawphoto.raw import Raw
from rawphoto.tiff import Header
from rawphoto.tiff import Ifd
from rawphoto.tiff import exif_tags
tags = exif_tags.copy()
tags.update({330: ('preview_image', 'raw_data'), 
 531: 'ycb_cr_positioning', 
 532: 'reference_black_white', 
 37399: 'sensing_method', 
 37510: 'user_comment'})
subdirs = [
 34665, 330]

class Nef(Raw):

    def __init__(self, blob=None, file=None, filename=None):
        super(Nef, self).__init__(blob=blob, file=file, filename=filename)
        pos = self.tell()
        self.header = Header(self.read(8))
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
        """Read a preview image from the NEF as a JPEG."""
        return self._get_image_data(name='preview_image')

    @property
    def thumbnail_image(self):
        raise NotImplementedError("NEF's do not contain a thumbnail image")

    @property
    def uncompressed_full_size_image(self):
        raise NotImplementedError("NEF's do not contain a full sized jpeg")

    @property
    def raw_data(self):
        """Read the raw image data from the NEF."""
        return self._get_image_data(name='raw_data')