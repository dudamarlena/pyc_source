# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/XbmImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.6'
import re, string, Image, ImageFile
xbm_head = re.compile('\\s*#define[ \t]+[^_]*_width[ \t]+(?P<width>[0-9]+)[\r\n]+#define[ \t]+[^_]*_height[ \t]+(?P<height>[0-9]+)[\r\n]+(?P<hotspot>#define[ \t]+[^_]*_x_hot[ \t]+(?P<xhot>[0-9]+)[\r\n]+#define[ \t]+[^_]*_y_hot[ \t]+(?P<yhot>[0-9]+)[\r\n]+)?[\\000-\\377]*_bits\\[\\]')

def _accept(prefix):
    return string.lstrip(prefix)[:7] == '#define'


class XbmImageFile(ImageFile.ImageFile):
    format = 'XBM'
    format_description = 'X11 Bitmap'

    def _open(self):
        m = xbm_head.match(self.fp.read(512))
        if m:
            xsize = int(m.group('width'))
            ysize = int(m.group('height'))
            if m.group('hotspot'):
                self.info['hotspot'] = (int(m.group('xhot')), int(m.group('yhot')))
            self.mode = '1'
            self.size = (xsize, ysize)
            self.tile = [
             (
              'xbm', (0, 0) + self.size, m.end(), None)]
        return


def _save(im, fp, filename):
    if im.mode != '1':
        raise IOError, 'cannot write mode %s as XBM' % im.mode
    fp.write('#define im_width %d\n' % im.size[0])
    fp.write('#define im_height %d\n' % im.size[1])
    hotspot = im.encoderinfo.get('hotspot')
    if hotspot:
        fp.write('#define im_x_hot %d\n' % hotspot[0])
        fp.write('#define im_y_hot %d\n' % hotspot[1])
    fp.write('static char im_bits[] = {\n')
    ImageFile._save(im, fp, [('xbm', (0, 0) + im.size, 0, None)])
    fp.write('};\n')
    return


Image.register_open('XBM', XbmImageFile, _accept)
Image.register_save('XBM', _save)
Image.register_extension('XBM', '.xbm')
Image.register_mime('XBM', 'image/xbm')