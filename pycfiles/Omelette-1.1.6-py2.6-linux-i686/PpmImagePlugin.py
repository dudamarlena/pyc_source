# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/PpmImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.2'
import string, Image, ImageFile
MODES = {'P4': '1', 
   'P5': 'L', 
   'P6': 'RGB', 
   'P0CMYK': 'CMYK', 
   'PyP': 'P', 
   'PyRGBA': 'RGBA', 
   'PyCMYK': 'CMYK'}

def _accept(prefix):
    return prefix[0] == 'P' and prefix[1] in '0456y'


class PpmImageFile(ImageFile.ImageFile):
    format = 'PPM'
    format_description = 'Pbmplus image'

    def _token(self, s=''):
        while 1:
            c = self.fp.read(1)
            if not c or c in string.whitespace:
                break
            s = s + c

        return s

    def _open(self):
        s = self.fp.read(1)
        if s != 'P':
            raise SyntaxError, 'not a PPM file'
        mode = MODES[self._token(s)]
        if mode == '1':
            self.mode = '1'
            rawmode = '1;I'
        else:
            self.mode = rawmode = mode
        for ix in range(3):
            while 1:
                while 1:
                    s = self.fp.read(1)
                    if s not in string.whitespace:
                        break

                if s != '#':
                    break
                s = self.fp.readline()

            s = int(self._token(s))
            if ix == 0:
                xsize = s
            elif ix == 1:
                ysize = s
                if mode == '1':
                    break

        self.size = (
         xsize, ysize)
        self.tile = [
         ('raw',
          (
           0, 0, xsize, ysize),
          self.fp.tell(),
          (
           rawmode, 0, 1))]


def _save(im, fp, filename):
    if im.mode == '1':
        (rawmode, head) = ('1;I', 'P4')
    elif im.mode == 'L':
        (rawmode, head) = ('L', 'P5')
    elif im.mode == 'RGB':
        (rawmode, head) = ('RGB', 'P6')
    elif im.mode == 'RGBA':
        (rawmode, head) = ('RGB', 'P6')
    else:
        raise IOError, 'cannot write mode %s as PPM' % im.mode
    fp.write(head + '\n%d %d\n' % im.size)
    if head != 'P4':
        fp.write('255\n')
    ImageFile._save(im, fp, [('raw', (0, 0) + im.size, 0, (rawmode, 0, 1))])


Image.register_open('PPM', PpmImageFile, _accept)
Image.register_save('PPM', _save)
Image.register_extension('PPM', '.pbm')
Image.register_extension('PPM', '.pgm')
Image.register_extension('PPM', '.ppm')