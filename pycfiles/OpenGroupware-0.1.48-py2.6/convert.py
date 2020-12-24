# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/ossf/convert.py
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

    class ImageConvertOSSFilter(OpenGroupwareServerSideFilter):

        @property
        def handle(self):
            return self._rfile

        @property
        def mimetype(self):
            return self._mimetype


else:

    class ImageConvertOSSFilter(OpenGroupwareServerSideFilter):

        @property
        def handle(self):
            return self._rfile

        @property
        def mimetype(self):
            return self._mimetype