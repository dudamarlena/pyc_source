# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/ossf/thumbnail.py
# Compiled at: 2012-10-12 07:02:39
try:
    from PIL import Image
except:
    HAS_PIL = False
else:
    HAS_PIL = True

import json
from coils.core import NotImplementedException, BLOBManager
from filter import OpenGroupwareServerSideFilter
if HAS_PIL:

    class ImageThumbnailOSSFilter(OpenGroupwareServerSideFilter):

        @property
        def handle(self):
            if self._mimetype not in ('image/jpeg', 'image/png'):
                raise Exception('Input type for thumbnail is not a supported image type')
            self.image = Image.open(self._rfile)
            if hasattr(self, '_width'):
                width = int(self._width)
            else:
                width = self.image.size[0]
            if hasattr(self, '_height'):
                height = int(self._height)
            else:
                height = self.image.size[1]
            s = BLOBManager.ScratchFile()
            self.image.thumbnail((width, height), Image.ANTIALIAS)
            self.image.save(s, self.image.format)
            s.seek(0)
            return s

        @property
        def mimetype(self):
            return self._mimetype


else:

    class ImageThumbnailOSSFilter(OpenGroupwareServerSideFilter):

        @property
        def handle(self):
            return self._rfile

        @property
        def mimetype(self):
            return self._mimetype