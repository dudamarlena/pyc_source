# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/ImageFileIO.py
# Compiled at: 2007-09-25 20:00:35
from StringIO import StringIO

class ImageFileIO(StringIO):

    def __init__(self, fp):
        data = fp.read()
        StringIO.__init__(self, data)


if __name__ == '__main__':
    import Image
    fp = open('/images/clenna.im', 'rb')
    im = Image.open(ImageFileIO(fp))
    im.load()
    print im.mode, im.size