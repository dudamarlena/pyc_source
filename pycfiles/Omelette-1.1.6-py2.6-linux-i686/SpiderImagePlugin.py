# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/SpiderImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
import Image, ImageFile, os, string, struct, sys

def isInt(f):
    try:
        i = int(f)
        if f - i == 0:
            return 1
        return 0
    except:
        return 0


iforms = [1, 3, -11, -12, -21, -22]

def isSpiderHeader(t):
    h = (99, ) + t
    for i in [1, 2, 5, 12, 13, 22, 23]:
        if not isInt(h[i]):
            return 0

    iform = int(h[5])
    if iform not in iforms:
        return 0
    labrec = int(h[13])
    labbyt = int(h[22])
    lenbyt = int(h[23])
    if labbyt != labrec * lenbyt:
        return 0
    return labbyt


def isSpiderImage(filename):
    fp = open(filename, 'rb')
    f = fp.read(92)
    fp.close()
    bigendian = 1
    t = struct.unpack('>23f', f)
    hdrlen = isSpiderHeader(t)
    if hdrlen == 0:
        bigendian = 0
        t = struct.unpack('<23f', f)
        hdrlen = isSpiderHeader(t)
    return hdrlen


class SpiderImageFile(ImageFile.ImageFile):
    format = 'SPIDER'
    format_description = 'Spider 2D image'

    def _open(self):
        n = 108
        f = self.fp.read(n)
        try:
            self.bigendian = 1
            t = struct.unpack('>27f', f)
            hdrlen = isSpiderHeader(t)
            if hdrlen == 0:
                self.bigendian = 0
                t = struct.unpack('<27f', f)
                hdrlen = isSpiderHeader(t)
            if hdrlen == 0:
                raise SyntaxError, 'not a valid Spider file'
        except struct.error:
            raise SyntaxError, 'not a valid Spider file'

        h = (99, ) + t
        iform = int(h[5])
        if iform != 1:
            raise SyntaxError, 'not a Spider 2D image'
        self.size = (int(h[12]), int(h[2]))
        self.istack = int(h[24])
        self.imgnumber = int(h[27])
        if self.istack == 0 and self.imgnumber == 0:
            offset = hdrlen
            self.nimages = 1
        elif self.istack > 0 and self.imgnumber == 0:
            self.imgbytes = int(h[12]) * int(h[2]) * 4
            self.hdrlen = hdrlen
            self.nimages = int(h[26])
            offset = hdrlen * 2
            self.imgnumber = 1
        elif self.istack == 0 and self.imgnumber > 0:
            offset = hdrlen + self.stkoffset
            self.istack = 2
        else:
            raise SyntaxError, 'inconsistent stack header values'
        if self.bigendian:
            self.rawmode = 'F;32BF'
        else:
            self.rawmode = 'F;32F'
        self.mode = 'F'
        self.tile = [
         (
          'raw', (0, 0) + self.size, offset,
          (
           self.rawmode, 0, 1))]
        self.__fp = self.fp

    def tell(self):
        if self.imgnumber < 1:
            return 0
        else:
            return self.imgnumber - 1

    def seek(self, frame):
        if self.istack == 0:
            return
        if frame >= self.nimages:
            raise EOFError, 'attempt to seek past end of file'
        self.stkoffset = self.hdrlen + frame * (self.hdrlen + self.imgbytes)
        self.fp = self.__fp
        self.fp.seek(self.stkoffset)
        self._open()

    def convert2byte(self, depth=255):
        (min, max) = self.getextrema()
        m = 1
        if max != min:
            m = depth / (max - min)
        b = -m * min
        return self.point(lambda i, m=m, b=b: i * m + b).convert('L')

    def tkPhotoImage(self):
        import ImageTk
        return ImageTk.PhotoImage(self.convert2byte(), palette=256)


def loadImageSeries(filelist=None):
    """ create a list of Image.images for use in montage """
    if filelist == None or len(filelist) < 1:
        return
    else:
        imglist = []
        for img in filelist:
            if not os.path.exists(img):
                print 'unable to find %s' % img
                continue
            try:
                im = Image.open(img).convert2byte()
            except:
                if not isSpiderImage(img):
                    print img + ' is not a Spider image file'
                continue

            im.info['filename'] = img
            imglist.append(im)

        return imglist


def makeSpiderHeader(im):
    (nsam, nrow) = im.size
    lenbyt = nsam * 4
    labrec = 1024 / lenbyt
    if 1024 % lenbyt != 0:
        labrec += 1
    labbyt = labrec * lenbyt
    hdr = []
    nvalues = labbyt / 4
    for i in range(nvalues):
        hdr.append(0.0)

    if len(hdr) < 23:
        return []
    hdr[1] = 1.0
    hdr[2] = float(nrow)
    hdr[5] = 1.0
    hdr[12] = float(nsam)
    hdr[13] = float(labrec)
    hdr[22] = float(labbyt)
    hdr[23] = float(lenbyt)
    hdr = hdr[1:]
    hdr.append(0.0)
    hdrstr = []
    for v in hdr:
        hdrstr.append(struct.pack('f', v))

    return hdrstr


def _save(im, fp, filename):
    if im.mode[0] != 'F':
        im = im.convert('F')
    hdr = makeSpiderHeader(im)
    if len(hdr) < 256:
        raise IOError, 'Error creating Spider header'
    try:
        fp = open(filename, 'wb')
    except:
        raise IOError, 'Unable to open %s for writing' % filename

    fp.writelines(hdr)
    rawmode = 'F;32NF'
    ImageFile._save(im, fp, [('raw', (0, 0) + im.size, 0, (rawmode, 0, 1))])
    fp.close()


def _save_spider(im, fp, filename):
    (fn, ext) = os.path.splitext(filename)
    Image.register_extension('SPIDER', ext)
    _save(im, fp, filename)


Image.register_open('SPIDER', SpiderImageFile)
Image.register_save('SPIDER', _save_spider)
if __name__ == '__main__':
    if not sys.argv[1:]:
        print 'Syntax: python SpiderImagePlugin.py Spiderimage [outfile]'
        sys.exit()
    filename = sys.argv[1]
    if not isSpiderImage(filename):
        print 'input image must be in Spider format'
        sys.exit()
    outfile = ''
    if len(sys.argv[1:]) > 1:
        outfile = sys.argv[2]
    im = Image.open(filename)
    print 'image: ' + str(im)
    print 'format: ' + str(im.format)
    print 'size: ' + str(im.size)
    print 'mode: ' + str(im.mode)
    print 'max, min: ',
    print im.getextrema()
    if outfile != '':
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        print 'saving a flipped version of %s as %s ' % (os.path.basename(filename), outfile)
        im.save(outfile, 'SPIDER')