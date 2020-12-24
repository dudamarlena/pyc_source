# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tzangms/projects/iloveck101/iloveck101/utils.py
# Compiled at: 2013-12-02 22:34:58
from cStringIO import StringIO
import struct

def get_image_info(data):
    data = str(data)
    size = len(data)
    height = -1
    width = -1
    content_type = ''
    if size >= 10 and data[:6] in ('GIF87a', 'GIF89a'):
        content_type = 'image/gif'
        w, h = struct.unpack('<HH', data[6:10])
        width = int(w)
        height = int(h)
    elif size >= 24 and data.startswith(b'\x89PNG\r\n\x1a\n') and data[12:16] == 'IHDR':
        content_type = 'image/png'
        w, h = struct.unpack('>LL', data[16:24])
        width = int(w)
        height = int(h)
    elif size >= 16 and data.startswith(b'\x89PNG\r\n\x1a\n'):
        content_type = 'image/png'
        w, h = struct.unpack('>LL', data[8:16])
        width = int(w)
        height = int(h)
    elif size >= 2 and data.startswith(b'\xff\xd8'):
        content_type = 'image/jpeg'
        jpeg = StringIO(data)
        jpeg.read(2)
        b = jpeg.read(1)
        try:
            while b and ord(b) != 218:
                while ord(b) != 255:
                    b = jpeg.read(1)

                while ord(b) == 255:
                    b = jpeg.read(1)

                if ord(b) >= 192 and ord(b) <= 195:
                    jpeg.read(3)
                    h, w = struct.unpack('>HH', jpeg.read(4))
                    break
                else:
                    jpeg.read(int(struct.unpack('>H', jpeg.read(2))[0]) - 2)
                b = jpeg.read(1)

            width = int(w)
            height = int(h)
        except struct.error:
            pass
        except ValueError:
            pass

    return (content_type, width, height)