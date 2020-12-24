# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gratia/graphs/animated_thumbnail.py
# Compiled at: 2008-01-18 12:47:40
import Image, ImageChops, string, struct
from GifImagePlugin import getheader, getdata

class image_sequence:
    __module__ = __name__

    def __init__(self, im):
        self.im = im

    def __getitem__(self, ix):
        try:
            if ix:
                self.im.seek(ix)
            return self.im
        except EOFError:
            raise IndexError


def makedelta(fp, sequence):
    """Convert list of image frames to a GIF animation file"""
    frames = 0
    previous = None
    for im in sequence:
        if not previous:
            for s in getheader(im) + [get_loop(), get_image_control(500)] + getdata(im):
                fp.write(s)

        else:
            delta = ImageChops.subtract_modulo(im, previous)
            bbox = delta.getbbox()
            if bbox:
                for s in [get_image_control(500)] + getdata(im.crop(bbox), offset=bbox[:2]):
                    fp.write(s)

            else:
                raise Exception('Undefined bbox.')
        previous = im.copy()
        frames = frames + 1

    fp.write(';')
    return frames


def get_loop():
    return struct.pack('BBB11sBBHB', 33, 255, 11, 'NETSCAPE2.0', 3, 1, 0, 0)


def get_image_control(delay):
    return struct.pack('BBBBHBB', 33, 249, 4, 0, delay, 0, 0)


def animated_gif(outfile, infiles, height, greyscale=True):
    ims = []
    for infile in infiles:
        im = Image.open(infile)
        im.load()
        im.thumbnail(height, Image.ANTIALIAS)
        if greyscale and im.mode != 'L':
            im = im.convert('L')
        if not greyscale and im.mode != 'P':
            im = im.convert('P')
        ims.append(im)

    fp = open(outfile, 'wb')
    makedelta(fp, ims)
    fp.close()