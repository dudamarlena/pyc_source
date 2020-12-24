# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/PalmImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '1.0'
import Image, ImageFile, StringIO
_Palm8BitColormapValues = (
 (255, 255, 255), (255, 204, 255), (255, 153, 255), (255, 102, 255),
 (255, 51, 255), (255, 0, 255), (255, 255, 204), (255, 204, 204),
 (255, 153, 204), (255, 102, 204), (255, 51, 204), (255, 0, 204),
 (255, 255, 153), (255, 204, 153), (255, 153, 153), (255, 102, 153),
 (255, 51, 153), (255, 0, 153), (204, 255, 255), (204, 204, 255),
 (204, 153, 255), (204, 102, 255), (204, 51, 255), (204, 0, 255),
 (204, 255, 204), (204, 204, 204), (204, 153, 204), (204, 102, 204),
 (204, 51, 204), (204, 0, 204), (204, 255, 153), (204, 204, 153),
 (204, 153, 153), (204, 102, 153), (204, 51, 153), (204, 0, 153),
 (153, 255, 255), (153, 204, 255), (153, 153, 255), (153, 102, 255),
 (153, 51, 255), (153, 0, 255), (153, 255, 204), (153, 204, 204),
 (153, 153, 204), (153, 102, 204), (153, 51, 204), (153, 0, 204),
 (153, 255, 153), (153, 204, 153), (153, 153, 153), (153, 102, 153),
 (153, 51, 153), (153, 0, 153), (102, 255, 255), (102, 204, 255),
 (102, 153, 255), (102, 102, 255), (102, 51, 255), (102, 0, 255),
 (102, 255, 204), (102, 204, 204), (102, 153, 204), (102, 102, 204),
 (102, 51, 204), (102, 0, 204), (102, 255, 153), (102, 204, 153),
 (102, 153, 153), (102, 102, 153), (102, 51, 153), (102, 0, 153),
 (51, 255, 255), (51, 204, 255), (51, 153, 255), (51, 102, 255),
 (51, 51, 255), (51, 0, 255), (51, 255, 204), (51, 204, 204),
 (51, 153, 204), (51, 102, 204), (51, 51, 204), (51, 0, 204),
 (51, 255, 153), (51, 204, 153), (51, 153, 153), (51, 102, 153),
 (51, 51, 153), (51, 0, 153), (0, 255, 255), (0, 204, 255),
 (0, 153, 255), (0, 102, 255), (0, 51, 255), (0, 0, 255),
 (0, 255, 204), (0, 204, 204), (0, 153, 204), (0, 102, 204),
 (0, 51, 204), (0, 0, 204), (0, 255, 153), (0, 204, 153),
 (0, 153, 153), (0, 102, 153), (0, 51, 153), (0, 0, 153),
 (255, 255, 102), (255, 204, 102), (255, 153, 102), (255, 102, 102),
 (255, 51, 102), (255, 0, 102), (255, 255, 51), (255, 204, 51),
 (255, 153, 51), (255, 102, 51), (255, 51, 51), (255, 0, 51),
 (255, 255, 0), (255, 204, 0), (255, 153, 0), (255, 102, 0),
 (255, 51, 0), (255, 0, 0), (204, 255, 102), (204, 204, 102),
 (204, 153, 102), (204, 102, 102), (204, 51, 102), (204, 0, 102),
 (204, 255, 51), (204, 204, 51), (204, 153, 51), (204, 102, 51),
 (204, 51, 51), (204, 0, 51), (204, 255, 0), (204, 204, 0),
 (204, 153, 0), (204, 102, 0), (204, 51, 0), (204, 0, 0),
 (153, 255, 102), (153, 204, 102), (153, 153, 102), (153, 102, 102),
 (153, 51, 102), (153, 0, 102), (153, 255, 51), (153, 204, 51),
 (153, 153, 51), (153, 102, 51), (153, 51, 51), (153, 0, 51),
 (153, 255, 0), (153, 204, 0), (153, 153, 0), (153, 102, 0),
 (153, 51, 0), (153, 0, 0), (102, 255, 102), (102, 204, 102),
 (102, 153, 102), (102, 102, 102), (102, 51, 102), (102, 0, 102),
 (102, 255, 51), (102, 204, 51), (102, 153, 51), (102, 102, 51),
 (102, 51, 51), (102, 0, 51), (102, 255, 0), (102, 204, 0),
 (102, 153, 0), (102, 102, 0), (102, 51, 0), (102, 0, 0),
 (51, 255, 102), (51, 204, 102), (51, 153, 102), (51, 102, 102),
 (51, 51, 102), (51, 0, 102), (51, 255, 51), (51, 204, 51),
 (51, 153, 51), (51, 102, 51), (51, 51, 51), (51, 0, 51),
 (51, 255, 0), (51, 204, 0), (51, 153, 0), (51, 102, 0),
 (51, 51, 0), (51, 0, 0), (0, 255, 102), (0, 204, 102),
 (0, 153, 102), (0, 102, 102), (0, 51, 102), (0, 0, 102),
 (0, 255, 51), (0, 204, 51), (0, 153, 51), (0, 102, 51),
 (0, 51, 51), (0, 0, 51), (0, 255, 0), (0, 204, 0),
 (0, 153, 0), (0, 102, 0), (0, 51, 0), (17, 17, 17),
 (34, 34, 34), (68, 68, 68), (85, 85, 85), (119, 119, 119),
 (136, 136, 136), (170, 170, 170), (187, 187, 187), (221, 221, 221),
 (238, 238, 238), (192, 192, 192), (128, 0, 0), (128, 0, 128),
 (0, 128, 0), (0, 128, 128), (0, 0, 0), (0, 0, 0),
 (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
 (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
 (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
 (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
 (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
 (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0))

def build_prototype_image():
    image = Image.new('L', (1, len(_Palm8BitColormapValues)))
    image.putdata(range(len(_Palm8BitColormapValues)))
    palettedata = ()
    for i in range(len(_Palm8BitColormapValues)):
        palettedata = palettedata + _Palm8BitColormapValues[i]

    for i in range(256 - len(_Palm8BitColormapValues)):
        palettedata = palettedata + (0, 0, 0)

    image.putpalette(palettedata)
    return image


Palm8BitColormapImage = build_prototype_image()
_FLAGS = {'custom-colormap': 16384, 
   'is-compressed': 32768, 
   'has-transparent': 8192}
_COMPRESSION_TYPES = {'none': 255, 
   'rle': 1, 
   'scanline': 0}

def o16b(i):
    return chr(i >> 8 & 255) + chr(i & 255)


def _save(im, fp, filename, check=0):
    if im.mode == 'P':
        rawmode = 'P'
        bpp = 8
        version = 1
    elif im.mode == 'L' and im.encoderinfo.has_key('bpp') and im.encoderinfo['bpp'] in (1,
                                                                                        2,
                                                                                        4):
        bpp = im.encoderinfo['bpp']
        im = im.point(lambda x, shift=8 - bpp, maxval=(1 << bpp) - 1: maxval - (x >> shift))
        im.mode = 'P'
        rawmode = 'P;' + str(bpp)
        version = 1
    elif im.mode == 'L' and im.info.has_key('bpp') and im.info['bpp'] in (1, 2, 4):
        bpp = im.info['bpp']
        im = im.point(lambda x, maxval=(1 << bpp) - 1: maxval - (x & maxval))
        im.mode = 'P'
        rawmode = 'P;' + str(bpp)
        version = 1
    elif im.mode == '1':
        rawmode = '1;I'
        bpp = 1
        version = 0
    else:
        raise IOError, 'cannot write mode %s as Palm' % im.mode
    if check:
        return check
    im.load()
    cols = im.size[0]
    rows = im.size[1]
    rowbytes = (cols + (16 / bpp - 1)) / (16 / bpp) * 2
    transparent_index = 0
    compression_type = _COMPRESSION_TYPES['none']
    flags = 0
    if im.mode == 'P' and im.info.has_key('custom-colormap'):
        flags = flags & _FLAGS['custom-colormap']
        colormapsize = 1026
        colormapmode = im.palette.mode
        colormap = im.getdata().getpalette()
    else:
        colormapsize = 0
    if im.info.has_key('offset'):
        offset = (rowbytes * rows + 16 + 3 + colormapsize) / 4
    else:
        offset = 0
    fp.write(o16b(cols) + o16b(rows) + o16b(rowbytes) + o16b(flags))
    fp.write(chr(bpp))
    fp.write(chr(version))
    fp.write(o16b(offset))
    fp.write(chr(transparent_index))
    fp.write(chr(compression_type))
    fp.write(o16b(0))
    if colormapsize > 0:
        fp.write(o16b(256))
        for i in range(256):
            fp.write(chr(i))
            if colormapmode == 'RGB':
                fp.write(chr(colormap[(3 * i)]) + chr(colormap[(3 * i + 1)]) + chr(colormap[(3 * i + 2)]))
            elif colormapmode == 'RGBA':
                fp.write(chr(colormap[(4 * i)]) + chr(colormap[(4 * i + 1)]) + chr(colormap[(4 * i + 2)]))

    ImageFile._save(im, fp, [('raw', (0, 0) + im.size, 0, (rawmode, rowbytes, 1))])
    fp.flush()


Image.register_save('Palm', _save)
Image.register_extension('Palm', '.palm')
Image.register_mime('Palm', 'image/palm')