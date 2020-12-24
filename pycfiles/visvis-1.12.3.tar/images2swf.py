# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\pylib\visvis\vvmovie\images2swf.py
# Compiled at: 2016-03-22 04:56:47
""" Module images2swf

Provides a function (writeSwf) to store a series of PIL images or numpy
arrays in an SWF movie, that can be played on a wide range of OS's.

This module came into being because I wanted to store a series of images
in a movie that can be viewed by other people, and which I can embed in
flash presentations. For writing AVI or MPEG you really need a c/c++
library, and allthough the filesize is then very small, the quality is
sometimes not adequate. Besides I'd like to be independant of yet another
package. I tried writing animated gif using PIL (which is widely available),
but the quality is so poor because it only allows for 256 different colors.
[EDIT: thanks to Ant1, now the quality of animated gif isn't so bad!]
I also looked into MNG and APNG, two standards similar to the PNG stanard.
Both standards promise exactly what I need. However, hardly any application
can read those formats, and I cannot import them in flash.

Therefore I decided to check out the swf file format, which is very well
documented. This is the result: a pure python module to create an SWF file
that shows a series of images. The images are stored using the DEFLATE
algorithm (same as PNG and ZIP and which is included in the standard Python
distribution). As this compression algorithm is much more effective than
that used in GIF images, we obtain better quality (24 bit colors + alpha
channel) while still producesing smaller files (a test showed ~75%).
Although SWF also allows for JPEG compression, doing so would probably
require a third party library (because encoding JPEG is much harder).

This module requires Python 2.x and numpy.

sources and tools:

- SWF on wikipedia
- Adobes "SWF File Format Specification" version 10
  (http://www.adobe.com/devnet/swf/pdf/swf_file_format_spec_v10.pdf)
- swftools (swfdump in specific) for debugging
- iwisoft swf2avi can be used to convert swf to avi/mpg/flv with really
  good quality, while file size is reduced with factors 20-100.
  A good program in my opinion. The free version has the limitation
  of a watermark in the upper left corner.

"""
import os, sys, time, zlib
try:
    import numpy as np
except ImportError:
    np = None

try:
    import PIL.Image
except ImportError:
    PIL = None

import types
PY3 = sys.version_info[0] == 3
if PY3:
    string_types = (
     str,)
    integer_types = (int,)
    class_types = (type,)
    text_type = str
    binary_type = bytes
else:
    string_types = (
     basestring,)
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str

def checkImages(images):
    """ checkImages(images)
    Check numpy images and correct intensity range etc.
    The same for all movie formats.
    """
    images2 = []
    for im in images:
        if PIL and isinstance(im, PIL.Image.Image):
            images2.append(im)
        elif np and isinstance(im, np.ndarray):
            if im.dtype == np.uint8:
                images2.append(im)
            elif im.dtype in [np.float32, np.float64]:
                theMax = im.max()
                if theMax > 128 and theMax < 300:
                    pass
                else:
                    im = im.copy()
                    im[im < 0] = 0
                    im[im > 1] = 1
                    im *= 255
                images2.append(im.astype(np.uint8))
            else:
                im = im.astype(np.uint8)
                images2.append(im)
            if im.ndim == 2:
                pass
            elif im.ndim == 3:
                if im.shape[2] not in (3, 4):
                    raise ValueError('This array can not represent an image.')
            else:
                raise ValueError('This array can not represent an image.')
        else:
            raise ValueError('Invalid image type: ' + str(type(im)))

    return images2


class BitArray:
    """ Dynamic array of bits that automatically resizes
    with factors of two.
    Append bits using .Append() or +=
    You can reverse bits using .Reverse()
    """

    def __init__(self, initvalue=None):
        self.data = np.zeros((16, ), dtype=np.uint8)
        self._len = 0
        if initvalue is not None:
            self.Append(initvalue)
        return

    def __len__(self):
        return self._len

    def __repr__(self):
        return self.data[:self._len].tostring().decode('ascii')

    def _checkSize(self):
        arraylen = self.data.shape[0]
        if self._len >= arraylen:
            tmp = np.zeros((arraylen * 2,), dtype=np.uint8)
            tmp[:(self._len)] = self.data[:self._len]
            self.data = tmp

    def __add__(self, value):
        self.Append(value)
        return self

    def Append(self, bits):
        if isinstance(bits, BitArray):
            bits = str(bits)
        if isinstance(bits, int):
            bits = str(bits)
        if not isinstance(bits, string_types):
            raise ValueError('Append bits as strings or integers!')
        for bit in bits:
            self.data[self._len] = ord(bit)
            self._len += 1
            self._checkSize()

    def Reverse(self):
        """ In-place reverse. """
        tmp = self.data[:self._len].copy()
        self.data[:(self._len)] = np.flipud(tmp)

    def ToBytes(self):
        """ Convert to bytes. If necessary,
        zeros are padded to the end (right side).
        """
        bits = str(self)
        nbytes = 0
        while nbytes * 8 < len(bits):
            nbytes += 1

        bits = bits.ljust(nbytes * 8, '0')
        bb = binary_type()
        for i in range(nbytes):
            tmp = int(bits[i * 8:(i + 1) * 8], 2)
            bb += intToUint8(tmp)

        return bb


if PY3:

    def intToUint32(i):
        return int(i).to_bytes(4, 'little')


    def intToUint16(i):
        return int(i).to_bytes(2, 'little')


    def intToUint8(i):
        return int(i).to_bytes(1, 'little')


else:

    def intToUint32(i):
        number = int(i)
        n1, n2, n3, n4 = (1, 256, 65536, 16777216)
        b4, number = number // n4, number % n4
        b3, number = number // n3, number % n3
        b2, number = number // n2, number % n2
        b1 = number
        return chr(b1) + chr(b2) + chr(b3) + chr(b4)


    def intToUint16(i):
        i = int(i)
        i1 = i % 256
        i2 = int(i // 256)
        return chr(i1) + chr(i2)


    def intToUint8(i):
        return chr(int(i))


def intToBits(i, n=None):
    """ convert int to a string of bits (0's and 1's in a string),
    pad to n elements. Convert back using int(ss,2). """
    ii = i
    bb = BitArray()
    while ii > 0:
        bb += str(ii % 2)
        ii = ii >> 1

    bb.Reverse()
    if n is not None:
        if len(bb) > n:
            raise ValueError('intToBits fail: len larger than padlength.')
        bb = str(bb).rjust(n, '0')
    return BitArray(bb)


def bitsToInt(bb, n=8):
    value = ''
    for i in range(len(bb)):
        b = bb[i:i + 1]
        tmp = bin(ord(b))[2:]
        value = tmp.rjust(8, '0') + value

    return int(value[:n], 2)


def getTypeAndLen(bb):
    """ bb should be 6 bytes at least
    Return (type, length, length_of_full_tag)
    """
    value = ''
    for i in range(2):
        b = bb[i:i + 1]
        tmp = bin(ord(b))[2:]
        value = tmp.rjust(8, '0') + value

    type = int(value[:10], 2)
    L = int(value[10:], 2)
    L2 = L + 2
    if L == 63:
        value = ''
        for i in range(2, 6):
            b = bb[i:i + 1]
            tmp = bin(ord(b))[2:]
            value = tmp.rjust(8, '0') + value

        L = int(value, 2)
        L2 = L + 6
    return (
     type, L, L2)


def signedIntToBits(i, n=None):
    """ convert signed int to a string of bits (0's and 1's in a string),
    pad to n elements. Negative numbers are stored in 2's complement bit
    patterns, thus positive numbers always start with a 0.
    """
    ii = i
    if i < 0:
        ii = abs(ii) - 1
    bb = BitArray()
    while ii > 0:
        bb += str(ii % 2)
        ii = ii >> 1

    bb.Reverse()
    bb = '0' + str(bb)
    if n is not None:
        if len(bb) > n:
            raise ValueError('signedIntToBits fail: len larger than padlength.')
        bb = bb.rjust(n, '0')
    if i < 0:
        bb = bb.replace('0', 'x').replace('1', '0').replace('x', '1')
    return BitArray(bb)


def twitsToBits(arr):
    """ Given a few (signed) numbers, store them
    as compactly as possible in the wat specifief by the swf format.
    The numbers are multiplied by 20, assuming they
    are twits.
    Can be used to make the RECT record.
    """
    maxlen = 1
    for i in arr:
        tmp = len(signedIntToBits(i * 20))
        if tmp > maxlen:
            maxlen = tmp

    bits = intToBits(maxlen, 5)
    for i in arr:
        bits += signedIntToBits(i * 20, maxlen)

    return bits


def floatsToBits(arr):
    """ Given a few (signed) numbers, convert them to bits,
    stored as FB (float bit values). We always use 16.16.
    Negative numbers are not (yet) possible, because I don't
    know how the're implemented (ambiguity).
    """
    bits = intToBits(31, 5)
    for i in arr:
        if i < 0:
            raise ValueError('Dit not implement negative floats!')
        i1 = int(i)
        i2 = i - i1
        bits += intToBits(i1, 15)
        bits += intToBits(i2 * 65536, 16)

    return bits


def _readFrom(fp, n):
    bb = binary_type()
    try:
        while len(bb) < n:
            tmp = fp.read(n - len(bb))
            bb += tmp
            if not tmp:
                break

    except EOFError:
        pass

    return bb


class Tag:

    def __init__(self):
        self.bytes = binary_type()
        self.tagtype = -1

    def ProcessTag(self):
        """ Implement this to create the tag. """
        raise NotImplemented()

    def GetTag(self):
        """ Calls processTag and attaches the header. """
        self.ProcessTag()
        bits = intToBits(self.tagtype, 10)
        bits += '111111'
        bb = intToUint16(int(str(bits), 2))
        bb += intToUint32(len(self.bytes))
        bb += self.bytes
        return bb

    def MakeRectRecord(self, xmin, xmax, ymin, ymax):
        """ Simply uses makeCompactArray to produce
        a RECT Record. """
        return twitsToBits([xmin, xmax, ymin, ymax])

    def MakeMatrixRecord(self, scale_xy=None, rot_xy=None, trans_xy=None):
        if scale_xy is None and rot_xy is None and trans_xy is None:
            return '00000000'
        else:
            bits = BitArray()
            if scale_xy:
                bits += '1'
                bits += floatsToBits([scale_xy[0], scale_xy[1]])
            else:
                bits += '0'
            if rot_xy:
                bits += '1'
                bits += floatsToBits([rot_xy[0], rot_xy[1]])
            else:
                bits += '0'
            if trans_xy:
                bits += twitsToBits([trans_xy[0], trans_xy[1]])
            else:
                bits += twitsToBits([0, 0])
            return bits


class ControlTag(Tag):

    def __init__(self):
        Tag.__init__(self)


class FileAttributesTag(ControlTag):

    def __init__(self):
        ControlTag.__init__(self)
        self.tagtype = 69

    def ProcessTag(self):
        self.bytes = ('\x00').encode('ascii') * 4


class ShowFrameTag(ControlTag):

    def __init__(self):
        ControlTag.__init__(self)
        self.tagtype = 1

    def ProcessTag(self):
        self.bytes = binary_type()


class SetBackgroundTag(ControlTag):
    """ Set the color in 0-255, or 0-1 (if floats given). """

    def __init__(self, *rgb):
        self.tagtype = 9
        if len(rgb) == 1:
            rgb = rgb[0]
        self.rgb = rgb

    def ProcessTag(self):
        bb = binary_type()
        for i in range(3):
            clr = self.rgb[i]
            if isinstance(clr, float):
                clr = clr * 255
            bb += intToUint8(clr)

        self.bytes = bb


class DoActionTag(Tag):

    def __init__(self, action='stop'):
        Tag.__init__(self)
        self.tagtype = 12
        self.actions = [action]

    def Append(self, action):
        self.actions.append(action)

    def ProcessTag(self):
        bb = binary_type()
        for action in self.actions:
            action = action.lower()
            if action == 'stop':
                bb += ('\x07').encode('ascii')
            elif action == 'play':
                bb += ('\x06').encode('ascii')
            else:
                print 'warning, unkown action: %s' % action

        bb += intToUint8(0)
        self.bytes = bb


class DefinitionTag(Tag):
    counter = 0

    def __init__(self):
        Tag.__init__(self)
        DefinitionTag.counter += 1
        self.id = DefinitionTag.counter


class BitmapTag(DefinitionTag):

    def __init__(self, im):
        DefinitionTag.__init__(self)
        self.tagtype = 36
        if len(im.shape) == 3:
            if im.shape[2] in (3, 4):
                tmp = np.ones((im.shape[0], im.shape[1], 4), dtype=np.uint8) * 255
                for i in range(3):
                    tmp[:, :, i + 1] = im[:, :, i]

                if im.shape[2] == 4:
                    tmp[:, :, 0] = im[:, :, 3]
            else:
                raise ValueError('Invalid shape to be an image.')
        elif len(im.shape) == 2:
            tmp = np.ones((im.shape[0], im.shape[1], 4), dtype=np.uint8) * 255
            for i in range(3):
                tmp[:, :, i + 1] = im[:, :]

        else:
            raise ValueError('Invalid shape to be an image.')
        self._data = zlib.compress(tmp.tostring(), zlib.DEFLATED)
        self.imshape = im.shape

    def ProcessTag(self):
        bb = binary_type()
        bb += intToUint16(self.id)
        bb += intToUint8(5)
        bb += intToUint16(self.imshape[1])
        bb += intToUint16(self.imshape[0])
        bb += self._data
        self.bytes = bb


class PlaceObjectTag(ControlTag):

    def __init__(self, depth, idToPlace=None, xy=(0, 0), move=False):
        ControlTag.__init__(self)
        self.tagtype = 26
        self.depth = depth
        self.idToPlace = idToPlace
        self.xy = xy
        self.move = move

    def ProcessTag(self):
        depth = self.depth
        xy = self.xy
        id = self.idToPlace
        bb = binary_type()
        if self.move:
            bb += ('\x07').encode('ascii')
        else:
            bb += ('\x06').encode('ascii')
        bb += intToUint16(depth)
        bb += intToUint16(id)
        bb += self.MakeMatrixRecord(trans_xy=xy).ToBytes()
        self.bytes = bb


class ShapeTag(DefinitionTag):

    def __init__(self, bitmapId, xy, wh):
        DefinitionTag.__init__(self)
        self.tagtype = 2
        self.bitmapId = bitmapId
        self.xy = xy
        self.wh = wh

    def ProcessTag(self):
        """ Returns a defineshape tag. with a bitmap fill """
        bb = binary_type()
        bb += intToUint16(self.id)
        xy, wh = self.xy, self.wh
        tmp = self.MakeRectRecord(xy[0], wh[0], xy[1], wh[1])
        bb += tmp.ToBytes()
        bb += intToUint8(1)
        bb += ('A').encode('ascii')
        bb += intToUint16(self.bitmapId)
        bb += self.MakeMatrixRecord(scale_xy=(20, 20)).ToBytes()
        bb += intToUint8(0)
        bb += ('D').encode('ascii')
        self.bytes = bb
        bits = BitArray()
        bits += self.MakeStyleChangeRecord(0, 1, moveTo=(self.wh[0],
         self.wh[1]))
        bits += self.MakeStraightEdgeRecord(-self.wh[0], 0)
        bits += self.MakeStraightEdgeRecord(0, -self.wh[1])
        bits += self.MakeStraightEdgeRecord(self.wh[0], 0)
        bits += self.MakeStraightEdgeRecord(0, self.wh[1])
        bits += self.MakeEndShapeRecord()
        self.bytes += bits.ToBytes()

    def MakeStyleChangeRecord(self, lineStyle=None, fillStyle=None, moveTo=None):
        bits = BitArray()
        bits += '0'
        bits += '0'
        if lineStyle:
            bits += '1'
        else:
            bits += '0'
        if fillStyle:
            bits += '1'
        else:
            bits += '0'
        bits += '0'
        if moveTo:
            bits += '1'
        else:
            bits += '0'
        if moveTo:
            bits += twitsToBits([moveTo[0], moveTo[1]])
        if fillStyle:
            bits += intToBits(fillStyle, 4)
        if lineStyle:
            bits += intToBits(lineStyle, 4)
        return bits

    def MakeStraightEdgeRecord(self, *dxdy):
        if len(dxdy) == 1:
            dxdy = dxdy[0]
        xbits = signedIntToBits(dxdy[0] * 20)
        ybits = signedIntToBits(dxdy[1] * 20)
        nbits = max([len(xbits), len(ybits)])
        bits = BitArray()
        bits += '11'
        bits += intToBits(nbits - 2, 4)
        bits += '1'
        bits += signedIntToBits(dxdy[0] * 20, nbits)
        bits += signedIntToBits(dxdy[1] * 20, nbits)
        return bits

    def MakeEndShapeRecord(self):
        bits = BitArray()
        bits += '0'
        bits += '00000'
        return bits


def buildFile(fp, taglist, nframes=1, framesize=(500, 500), fps=10, version=8):
    """ Give the given file (as bytes) a header. """
    bb = binary_type()
    bb += ('F').encode('ascii')
    bb += ('WS').encode('ascii')
    bb += intToUint8(version)
    bb += ('0000').encode('ascii')
    bb += Tag().MakeRectRecord(0, framesize[0], 0, framesize[1]).ToBytes()
    bb += intToUint8(0) + intToUint8(fps)
    bb += intToUint16(nframes)
    fp.write(bb)
    for tag in taglist:
        fp.write(tag.GetTag())

    fp.write(('\x00\x00').encode('ascii'))
    sze = fp.tell()
    fp.seek(4)
    fp.write(intToUint32(sze))


def writeSwf(filename, images, duration=0.1, repeat=True):
    """Write an swf-file from the specified images. If repeat is False,
    the movie is finished with a stop action. Duration may also
    be a list with durations for each frame (note that the duration
    for each frame is always an integer amount of the minimum duration.)

    Images should be a list consisting of PIL images or numpy arrays.
    The latter should be between 0 and 255 for integer types, and
    between 0 and 1 for float types.

    """
    if np is None:
        raise RuntimeError('Need Numpy to write an SWF file.')
    images2 = []
    images = checkImages(images)
    if not images:
        raise ValueError('Image list is empty!')
    for im in images:
        if PIL and isinstance(im, PIL.Image.Image):
            if im.mode == 'P':
                im = im.convert()
            im = np.asarray(im)
            if len(im.shape) == 0:
                raise MemoryError('Too little memory to convert PIL image to array')
        images2.append(im)

    taglist = [
     FileAttributesTag(), SetBackgroundTag(0, 0, 0)]
    if hasattr(duration, '__len__'):
        if len(duration) == len(images2):
            duration = [ d for d in duration ]
        else:
            raise ValueError("len(duration) doesn't match amount of images.")
    else:
        duration = [ duration for im in images2 ]
    minDuration = float(min(duration))
    delays = [ round(d / minDuration) for d in duration ]
    delays = [ max(1, int(d)) for d in delays ]
    fps = 1.0 / minDuration
    t0 = time.time()
    nframes = 0
    for im in images2:
        bm = BitmapTag(im)
        wh = (im.shape[1], im.shape[0])
        sh = ShapeTag(bm.id, (0, 0), wh)
        po = PlaceObjectTag(1, sh.id, move=nframes > 0)
        taglist.extend([bm, sh, po])
        for i in range(delays[nframes]):
            taglist.append(ShowFrameTag())

        nframes += 1

    if not repeat:
        taglist.append(DoActionTag('stop'))
    t1 = time.time()
    fp = open(filename, 'wb')
    try:
        try:
            buildFile(fp, taglist, nframes=nframes, framesize=wh, fps=fps)
        except Exception:
            raise

    finally:
        fp.close()

    t2 = time.time()
    return


def _readPixels(bb, i, tagType, L1):
    """ With pf's seed after the recordheader, reads the pixeldata.
    """
    if np is None:
        raise RuntimeError('Need Numpy to read an SWF file.')
    charId = bb[i:i + 2]
    i += 2
    format = ord(bb[i:i + 1])
    i += 1
    width = bitsToInt(bb[i:i + 2], 16)
    i += 2
    height = bitsToInt(bb[i:i + 2], 16)
    i += 2
    if format != 5:
        print 'Can only read 24bit or 32bit RGB(A) lossless images.'
    else:
        offset = 7
        bb2 = bb[i:i + (L1 - offset)]
        data = zlib.decompress(bb2)
        a = np.frombuffer(data, dtype=np.uint8)
        if tagType == 20:
            try:
                a.shape = (
                 height, width, 3)
            except Exception:
                print 'Cannot read image due to byte alignment'

        if tagType == 36:
            a.shape = (height, width, 4)
            b = a
            a = np.zeros_like(a)
            a[:, :, 0] = b[:, :, 1]
            a[:, :, 1] = b[:, :, 2]
            a[:, :, 2] = b[:, :, 3]
            a[:, :, 3] = b[:, :, 0]
        return a
    return


def readSwf(filename, asNumpy=True):
    """Read all images from an SWF (shockwave flash) file. Returns a list
    of numpy arrays, or, if asNumpy is false, a list if PIL images.

    Limitation: only read the PNG encoded images (not the JPG encoded ones).

    """
    if not os.path.isfile(filename):
        raise IOError('File not found: ' + str(filename))
    if not asNumpy and PIL is None:
        raise RuntimeError('Need PIL to return as PIL images.')
    if np is None:
        raise RuntimeError('Need Numpy to read SWF files.')
    images = []
    fp = open(filename, 'rb')
    bb = fp.read()
    try:
        tmp = bb[0:3].decode('ascii', 'ignore')
        if tmp.upper() == 'FWS':
            pass
        else:
            if tmp.upper() == 'CWS':
                bb = bb[:8] + zlib.decompress(bb[8:])
            else:
                raise IOError('Not a valid SWF file: ' + str(filename))
            i = 8
            nbits = bitsToInt(bb[i:i + 1], 5)
            nbits = 5 + nbits * 4
            Lrect = nbits / 8.0
            if Lrect % 1:
                Lrect += 1
            Lrect = int(Lrect)
            i += Lrect + 4
            counter = 0
            while True:
                counter += 1
                head = bb[i:i + 6]
                if not head:
                    break
                T, L1, L2 = getTypeAndLen(head)
                if not L2:
                    print 'Invalid tag length, could not proceed'
                    break
                if T in (20, 36):
                    im = _readPixels(bb, i + 6, T, L1)
                    if im is not None:
                        images.append(im)
                elif T in (6, 21, 35, 90):
                    print 'Ignoring JPEG image: cannot read JPEG.'
                if T == 0:
                    break
                i += L2

    finally:
        fp.close()

    if not asNumpy:
        images2 = images
        images = []
        for im in images2:
            images.append(PIL.Image.fromarray(im))

    return images