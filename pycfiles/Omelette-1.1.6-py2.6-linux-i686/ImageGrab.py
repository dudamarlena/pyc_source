# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/ImageGrab.py
# Compiled at: 2007-09-25 20:00:35
import Image
try:
    grabber = Image.core.grabscreen
except AttributeError:
    import _grabscreen
    grabber = _grabscreen.grab

def grab(bbox=None):
    (size, data) = grabber()
    im = Image.fromstring('RGB', size, data, 'raw', 'BGR', size[0] * 3 + 3 & -4, -1)
    if bbox:
        im = im.crop(bbox)
    return im


def grabclipboard():
    debug = 0
    data = Image.core.grabclipboard(debug)
    if Image.isStringType(data):
        import BmpImagePlugin, StringIO
        return BmpImagePlugin.DibImageFile(StringIO.StringIO(data))
    return data