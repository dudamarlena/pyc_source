# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\dev\pylib\visvis\vvmovie\images2gif.py
# Compiled at: 2017-05-25 20:29:40
# Size of source mod 2**32: 36595 bytes
""" Module images2gif

Provides functionality for reading and writing animated GIF images.
Use writeGif to write a series of numpy arrays or PIL images as an
animated GIF. Use readGif to read an animated gif as a series of numpy
arrays.

Note that since July 2004, all patents on the LZW compression patent have
expired. Therefore the GIF format may now be used freely.

Acknowledgements
----------------

Many thanks to Ant1 for:

* noting the use of "palette=PIL.Image.ADAPTIVE", which significantly
  improves the results.
* the modifications to save each image with its own palette, or optionally
  the global palette (if its the same).

Many thanks to Marius van Voorden for porting the NeuQuant quantization
algorithm of Anthony Dekker to Python (See the NeuQuant class for its
license).

Many thanks to Alex Robinson for implementing the concept of subrectangles,
which (depening on image content) can give a very significant reduction in
file size.

This code is based on gifmaker (in the scripts folder of the source
distribution of PIL)

Useful links
-------------
  * http://tronche.com/computer-graphics/gif/
  * http://en.wikipedia.org/wiki/Graphics_Interchange_Format
  * http://www.w3.org/Graphics/GIF/spec-gif89a.txt

"""
import os, time
try:
    import PIL
    from PIL import Image
    from PIL.GifImagePlugin import getheader, getdata
except ImportError:
    PIL = None

try:
    import numpy as np
except ImportError:
    np = None

def get_cKDTree():
    try:
        from scipy.spatial import cKDTree
    except ImportError:
        cKDTree = None

    return cKDTree


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
            else:
                if im.dtype in [np.float32, np.float64]:
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
                else:
                    if im.ndim == 3:
                        if im.shape[2] not in (3, 4):
                            raise ValueError('This array can not represent an image.')
                    else:
                        raise ValueError('This array can not represent an image.')
        else:
            raise ValueError('Invalid image type: ' + str(type(im)))

    return images2


def intToBin(i):
    """Integer to two bytes"""
    i1 = i % 256
    i2 = int(i / 256)
    return chr(i1) + chr(i2)


class GifWriter:
    __doc__ = ' GifWriter()\n\n    Class that contains methods for helping write the animated GIF file.\n\n    '

    def getheaderAnim(self, im):
        """ getheaderAnim(im)

        Get animation header. To replace PILs getheader()[0]

        """
        bb = 'GIF89a'
        bb += intToBin(im.size[0])
        bb += intToBin(im.size[1])
        bb += '\x87\x00\x00'
        return bb

    def getImageDescriptor(self, im, xy=None):
        """ getImageDescriptor(im, xy=None)

        Used for the local color table properties per image.
        Otherwise global color table applies to all frames irrespective of
        whether additional colors comes in play that require a redefined
        palette. Still a maximum of 256 color per frame, obviously.

        Written by Ant1 on 2010-08-22
        Modified by Alex Robinson in Janurari 2011 to implement subrectangles.

        """
        if xy is None:
            xy = (0, 0)
        bb = ','
        bb += intToBin(xy[0])
        bb += intToBin(xy[1])
        bb += intToBin(im.size[0])
        bb += intToBin(im.size[1])
        bb += '\x87'
        return bb

    def getAppExt(self, loops=float('inf')):
        """ getAppExt(loops=float('inf'))

        Application extention. This part specifies the amount of loops.
        If loops is 0 or inf, it goes on infinitely.

        """
        if loops == 0 or loops == float('inf'):
            loops = 65535
        bb = '!ÿ\x0b'
        bb += 'NETSCAPE2.0'
        bb += '\x03\x01'
        bb += intToBin(loops)
        bb += '\x00'
        return bb

    def getGraphicsControlExt(self, duration=0.1, dispose=2):
        """ getGraphicsControlExt(duration=0.1, dispose=2)

        Graphics Control Extension. A sort of header at the start of
        each image. Specifies duration and transparancy.

        Dispose
        -------
          * 0 - No disposal specified.
          * 1 - Do not dispose. The graphic is to be left in place.
          * 2 - Restore to background color. The area used by the graphic
            must be restored to the background color.
          * 3 - Restore to previous. The decoder is required to restore the
            area overwritten by the graphic with what was there prior to
            rendering the graphic.
          * 4-7 -To be defined.

        """
        bb = '!ù\x04'
        bb += chr((dispose & 3) << 2)
        bb += intToBin(int(duration * 100))
        bb += '\x00'
        bb += '\x00'
        return bb

    def handleSubRectangles(self, images, subRectangles):
        """ handleSubRectangles(images)

        Handle the sub-rectangle stuff. If the rectangles are given by the
        user, the values are checked. Otherwise the subrectangles are
        calculated automatically.

        """
        if isinstance(subRectangles, (tuple, list)):
            xy = subRectangles
            if xy is None:
                xy = (0, 0)
            if hasattr(xy, '__len__'):
                if len(xy) == len(images):
                    xy = [xxyy for xxyy in xy]
                else:
                    raise ValueError("len(xy) doesn't match amount of images.")
            else:
                xy = [xy for im in images]
            xy[0] = (0, 0)
        else:
            if np is None:
                raise RuntimeError('Need Numpy to use auto-subRectangles.')
            for i in range(len(images)):
                im = images[i]
                if isinstance(im, Image.Image):
                    tmp = im.convert()
                    a = np.asarray(tmp)
                    if len(a.shape) == 0:
                        raise MemoryError('Too little memory to convert PIL image to array')
                    images[i] = a

            images, xy = self.getSubRectangles(images)
        return (
         images, xy)

    def getSubRectangles(self, ims):
        """ getSubRectangles(ims)

        Calculate the minimal rectangles that need updating each frame.
        Returns a two-element tuple containing the cropped images and a
        list of x-y positions.

        Calculating the subrectangles takes extra time, obviously. However,
        if the image sizes were reduced, the actual writing of the GIF
        goes faster. In some cases applying this method produces a GIF faster.

        """
        if len(ims) < 2:
            return (ims, [(0, 0) for i in ims])
        else:
            if np is None:
                raise RuntimeError('Need Numpy to calculate sub-rectangles. ')
            ims2 = [
             ims[0]]
            xy = [(0, 0)]
            t0 = time.time()
            prev = ims[0]
            for im in ims[1:]:
                diff = np.abs(im - prev)
                if diff.ndim == 3:
                    diff = diff.sum(2)
                else:
                    X = np.argwhere(diff.sum(0))
                    Y = np.argwhere(diff.sum(1))
                    if X.size:
                        if Y.size:
                            x0, x1 = int(X[0]), int(X[(-1)] + 1)
                            y0, y1 = int(Y[0]), int(Y[(-1)] + 1)
                    x0, x1 = (0, 2)
                    y0, y1 = (0, 2)
                im2 = im[y0:y1, x0:x1]
                prev = im
                ims2.append(im2)
                xy.append((x0, y0))

            return (
             ims2, xy)

    def convertImagesToPIL(self, images, dither, nq=0):
        """ convertImagesToPIL(images, nq=0)

        Convert images to Paletted PIL images, which can then be
        written to a single animaged GIF.

        """
        images2 = []
        for im in images:
            if isinstance(im, Image.Image):
                images2.append(im)
            else:
                if np:
                    if isinstance(im, np.ndarray):
                        if im.ndim == 3:
                            if im.shape[2] == 3:
                                im = Image.fromarray(im, 'RGB')
                            else:
                                if im.ndim == 3 and im.shape[2] == 4:
                                    im = Image.fromarray(im[:, :, :3], 'RGB')
                        elif im.ndim == 2:
                            im = Image.fromarray(im, 'L')
                    images2.append(im)

        images, images2 = images2, []
        if nq >= 1:
            for im in images:
                im = im.convert('RGBA')
                nqInstance = NeuQuant(im, int(nq))
                if dither:
                    im = im.convert('RGB').quantize(palette=(nqInstance.paletteImage()))
                else:
                    im = nqInstance.quantize(im)
                images2.append(im)

        else:
            AD = Image.ADAPTIVE
            for im in images:
                im = im.convert('P', palette=AD, dither=dither)
                images2.append(im)

        return images2

    def writeGifToFile(self, fp, images, durations, loops, xys, disposes):
        """ writeGifToFile(fp, images, durations, loops, xys, disposes)

        Given a set of images writes the bytes to the specified stream.

        """
        palettes, occur = [], []
        for im in images:
            palette = getheader(im)[1]
            if not palette:
                palette = PIL.ImagePalette.ImageColor
                if isinstance(palette, type(os)):
                    data = PIL.ImagePalette.ImagePalette().getdata()
                    palette = data[0].encode('utf-8') + data[1]
                    raise RuntimeError('Cannot get palette. Maybe you should try imageio instead.')
            palettes.append(palette)

        for palette in palettes:
            occur.append(palettes.count(palette))

        globalPalette = palettes[occur.index(max(occur))]
        frames = 0
        firstFrame = True
        for im, palette in zip(images, palettes):
            if firstFrame:
                header = self.getheaderAnim(im)
                appext = self.getAppExt(loops)
                fp.write(header.encode('utf-8'))
                fp.write(globalPalette)
                fp.write(appext.encode('utf-8'))
                firstFrame = False
            else:
                data = getdata(im)
                imdes, data = data[0], data[1:]
                graphext = self.getGraphicsControlExt(durations[frames], disposes[frames])
                lid = self.getImageDescriptor(im, xys[frames])
                if palette != globalPalette or disposes[frames] != 2:
                    fp.write(graphext.encode('utf-8'))
                    fp.write(lid.encode('utf-8'))
                    fp.write(palette)
                    fp.write('\x08'.encode('utf-8'))
                else:
                    fp.write(graphext.encode('utf-8'))
                    fp.write(imdes)
            for d in data:
                fp.write(d)

            frames = frames + 1

        fp.write(';'.encode('utf-8'))
        return frames


def writeGif(filename, images, duration=0.1, repeat=True, dither=False, nq=0, subRectangles=True, dispose=None):
    """ writeGif(filename, images, duration=0.1, repeat=True, dither=False,
                    nq=0, subRectangles=True, dispose=None)

    Write an animated gif from the specified images.

    Parameters
    ----------
    filename : string
        The name of the file to write the image to.
    images : list
        Should be a list consisting of PIL images or numpy arrays.
        The latter should be between 0 and 255 for integer types, and
        between 0 and 1 for float types.
    duration : scalar or list of scalars
        The duration for all frames, or (if a list) for each frame.
    repeat : bool or integer
        The amount of loops. If True, loops infinitetely.
    dither : bool
        Whether to apply dithering
    nq : integer
        If nonzero, applies the NeuQuant quantization algorithm to create
        the color palette. This algorithm is superior, but slower than
        the standard PIL algorithm. The value of nq is the quality
        parameter. 1 represents the best quality. 10 is in general a
        good tradeoff between quality and speed. When using this option,
        better results are usually obtained when subRectangles is False.
    subRectangles : False, True, or a list of 2-element tuples
        Whether to use sub-rectangles. If True, the minimal rectangle that
        is required to update each frame is automatically detected. This
        can give significant reductions in file size, particularly if only
        a part of the image changes. One can also give a list of x-y
        coordinates if you want to do the cropping yourself. The default
        is True.
    dispose : int
        How to dispose each frame. 1 means that each frame is to be left
        in place. 2 means the background color should be restored after
        each frame. 3 means the decoder should restore the previous frame.
        If subRectangles==False, the default is 2, otherwise it is 1.

    """
    if PIL is None:
        raise RuntimeError('Need PIL to write animated gif files.')
    else:
        images = checkImages(images)
        gifWriter = GifWriter()
        if repeat is False:
            loops = 1
        else:
            if repeat is True:
                loops = 0
            else:
                loops = int(repeat)
            if hasattr(duration, '__len__'):
                if len(duration) == len(images):
                    duration = [d for d in duration]
                else:
                    raise ValueError("len(duration) doesn't match amount of images.")
            else:
                duration = [duration for im in images]
            if subRectangles:
                images, xy = gifWriter.handleSubRectangles(images, subRectangles)
                defaultDispose = 1
            else:
                xy = [(0, 0) for im in images]
                defaultDispose = 2
            if dispose is None:
                dispose = defaultDispose
            if hasattr(dispose, '__len__'):
                if len(dispose) != len(images):
                    raise ValueError("len(xy) doesn't match amount of images.")
            else:
                dispose = [dispose for im in images]
    images = gifWriter.convertImagesToPIL(images, dither, nq)
    fp = open(filename, 'wb')
    try:
        gifWriter.writeGifToFile(fp, images, duration, loops, xy, dispose)
    finally:
        fp.close()


def readGif(filename, asNumpy=True):
    """ readGif(filename, asNumpy=True)

    Read images from an animated GIF file.  Returns a list of numpy
    arrays, or, if asNumpy is false, a list if PIL images.

    """
    if PIL is None:
        raise RuntimeError('Need PIL to read animated gif files.')
    else:
        if np is None:
            raise RuntimeError('Need Numpy to read animated gif files.')
        else:
            if not os.path.isfile(filename):
                raise IOError('File not found: ' + str(filename))
            pilIm = PIL.Image.open(filename)
            pilIm.seek(0)
            images = []
            try:
                while True:
                    tmp = pilIm.convert()
                    a = np.asarray(tmp)
                    if len(a.shape) == 0:
                        raise MemoryError('Too little memory to convert PIL image to array')
                    images.append(a)
                    pilIm.seek(pilIm.tell() + 1)

            except EOFError:
                pass

        if not asNumpy:
            images2 = images
            images = []
            for im in images2:
                images.append(PIL.Image.fromarray(im))

    return images


class NeuQuant:
    __doc__ = ' NeuQuant(image, samplefac=10, colors=256)\n\n    samplefac should be an integer number of 1 or higher, 1\n    being the highest quality, but the slowest performance.\n    With avalue of 10, one tenth of all pixels are used during\n    training. This value seems a nice tradeof between speed\n    and quality.\n\n    colors is the amount of colors to reduce the image to. This\n    should best be a power of two.\n\n    See also:\n    http://members.ozemail.com.au/~dekker/NEUQUANT.HTML\n\n    License of the NeuQuant Neural-Net Quantization Algorithm\n    ---------------------------------------------------------\n\n    Copyright (c) 1994 Anthony Dekker\n    Ported to python by Marius van Voorden in 2010\n\n    NEUQUANT Neural-Net quantization algorithm by Anthony Dekker, 1994.\n    See "Kohonen neural networks for optimal colour quantization"\n    in "network: Computation in Neural Systems" Vol. 5 (1994) pp 351-367.\n    for a discussion of the algorithm.\n    See also  http://members.ozemail.com.au/~dekker/NEUQUANT.HTML\n\n    Any party obtaining a copy of these files from the author, directly or\n    indirectly, is granted, free of charge, a full and unrestricted\n    irrevocable, world-wide, paid up, royalty-free, nonexclusive right and\n    license to deal in this software and documentation files (the "Software"),\n    including without limitation the rights to use, copy, modify, merge,\n    publish, distribute, sublicense, and/or sell copies of the Software, and\n    to permit persons who receive copies from any such party to do so, with\n    the only requirement being that this copyright notice remain intact.\n\n    '
    NCYCLES = None
    NETSIZE = None
    SPECIALS = None
    BGCOLOR = None
    CUTNETSIZE = None
    MAXNETPOS = None
    INITRAD = None
    RADIUSBIASSHIFT = None
    RADIUSBIAS = None
    INITBIASRADIUS = None
    RADIUSDEC = None
    ALPHABIASSHIFT = None
    INITALPHA = None
    GAMMA = None
    BETA = None
    BETAGAMMA = None
    network = None
    colormap = None
    netindex = None
    bias = None
    freq = None
    pimage = None
    PRIME1 = 499
    PRIME2 = 491
    PRIME3 = 487
    PRIME4 = 503
    MAXPRIME = PRIME4
    pixels = None
    samplefac = None
    a_s = None

    def setconstants(self, samplefac, colors):
        self.NCYCLES = 100
        self.NETSIZE = colors
        self.SPECIALS = 3
        self.BGCOLOR = self.SPECIALS - 1
        self.CUTNETSIZE = self.NETSIZE - self.SPECIALS
        self.MAXNETPOS = self.NETSIZE - 1
        self.INITRAD = self.NETSIZE / 8
        self.RADIUSBIASSHIFT = 6
        self.RADIUSBIAS = 1 << self.RADIUSBIASSHIFT
        self.INITBIASRADIUS = self.INITRAD * self.RADIUSBIAS
        self.RADIUSDEC = 30
        self.ALPHABIASSHIFT = 10
        self.INITALPHA = 1 << self.ALPHABIASSHIFT
        self.GAMMA = 1024.0
        self.BETA = 0.0009765625
        self.BETAGAMMA = self.BETA * self.GAMMA
        self.network = np.empty((self.NETSIZE, 3), dtype='float64')
        self.colormap = np.empty((self.NETSIZE, 4), dtype='int32')
        self.netindex = np.empty(256, dtype='int32')
        self.bias = np.empty((self.NETSIZE), dtype='float64')
        self.freq = np.empty((self.NETSIZE), dtype='float64')
        self.pixels = None
        self.samplefac = samplefac
        self.a_s = {}

    def __init__(self, image, samplefac=10, colors=256):
        if np is None:
            raise RuntimeError('Need Numpy for the NeuQuant algorithm.')
        else:
            if image.size[0] * image.size[1] < NeuQuant.MAXPRIME:
                raise IOError('Image is too small')
            if image.mode != 'RGBA':
                raise IOError('Image mode should be RGBA.')
        self.setconstants(samplefac, colors)
        self.pixels = np.fromstring(image.tostring(), np.uint32)
        self.setUpArrays()
        self.learn()
        self.fix()
        self.inxbuild()

    def writeColourMap(self, rgb, outstream):
        for i in range(self.NETSIZE):
            bb = self.colormap[(i, 0)]
            gg = self.colormap[(i, 1)]
            rr = self.colormap[(i, 2)]
            outstream.write(rr if rgb else bb)
            outstream.write(gg)
            outstream.write(bb if rgb else rr)

        return self.NETSIZE

    def setUpArrays(self):
        self.network[(0, 0)] = 0.0
        self.network[(0, 1)] = 0.0
        self.network[(0, 2)] = 0.0
        self.network[(1, 0)] = 255.0
        self.network[(1, 1)] = 255.0
        self.network[(1, 2)] = 255.0
        for i in range(self.SPECIALS):
            self.freq[i] = 1.0 / self.NETSIZE
            self.bias[i] = 0.0

        for i in range(self.SPECIALS, self.NETSIZE):
            p = self.network[i]
            p[:] = 255.0 * (i - self.SPECIALS) / self.CUTNETSIZE
            self.freq[i] = 1.0 / self.NETSIZE
            self.bias[i] = 0.0

    def altersingle(self, alpha, i, b, g, r):
        """Move neuron i towards biased (b, g, r) by factor alpha"""
        n = self.network[i]
        n[0] -= alpha * (n[0] - b)
        n[1] -= alpha * (n[1] - g)
        n[2] -= alpha * (n[2] - r)

    def geta(self, alpha, rad):
        try:
            return self.a_s[(alpha, rad)]
        except KeyError:
            length = rad * 2 - 1
            mid = int(length // 2)
            q = np.array(list(range(mid - 1, -1, -1)) + list(range(-1, mid)))
            a = alpha * (rad * rad - q * q) / (rad * rad)
            a[mid] = 0
            self.a_s[(alpha, rad)] = a
            return a

    def alterneigh(self, alpha, rad, i, b, g, r):
        if i - rad >= self.SPECIALS - 1:
            lo = i - rad
            start = 0
        else:
            lo = self.SPECIALS - 1
            start = self.SPECIALS - 1 - (i - rad)
        if i + rad <= self.NETSIZE:
            hi = i + rad
            end = rad * 2 - 1
        else:
            hi = self.NETSIZE
            end = self.NETSIZE - (i + rad)
        a = self.geta(alpha, rad)[start:end]
        p = self.network[lo + 1:hi]
        p -= np.transpose(np.transpose(p - np.array([b, g, r])) * a)

    def contest(self, b, g, r):
        """Search for biased BGR values
        Finds closest neuron (min dist) and updates self.freq
        finds best neuron (min dist-self.bias) and returns position
        for frequently chosen neurons, self.freq[i] is high and self.bias[i]
        is negative self.bias[i] = self.GAMMA * ((1/self.NETSIZE)-self.freq[i])
        """
        i, j = self.SPECIALS, self.NETSIZE
        dists = abs(self.network[i:j] - np.array([b, g, r])).sum(1)
        bestpos = i + np.argmin(dists)
        biasdists = dists - self.bias[i:j]
        bestbiaspos = i + np.argmin(biasdists)
        self.freq[i:j] *= 1 - self.BETA
        self.bias[i:j] += self.BETAGAMMA * self.freq[i:j]
        self.freq[bestpos] += self.BETA
        self.bias[bestpos] -= self.BETAGAMMA
        return bestbiaspos

    def specialFind(self, b, g, r):
        for i in range(self.SPECIALS):
            n = self.network[i]
            if n[0] == b:
                if n[1] == g:
                    if n[2] == r:
                        return i

        return -1

    def learn(self):
        biasRadius = self.INITBIASRADIUS
        alphadec = 30 + (self.samplefac - 1) / 3
        lengthcount = self.pixels.size
        samplepixels = lengthcount / self.samplefac
        delta = samplepixels / self.NCYCLES
        alpha = self.INITALPHA
        i = 0
        rad = biasRadius * 2 ** self.RADIUSBIASSHIFT
        if rad <= 1:
            rad = 0
        else:
            print('Beginning 1D learning: samplepixels = %1.2f  rad = %i' % (
             samplepixels, rad))
            step = 0
            pos = 0
            if lengthcount % NeuQuant.PRIME1 != 0:
                step = NeuQuant.PRIME1
            else:
                if lengthcount % NeuQuant.PRIME2 != 0:
                    step = NeuQuant.PRIME2
                else:
                    if lengthcount % NeuQuant.PRIME3 != 0:
                        step = NeuQuant.PRIME3
                    else:
                        step = NeuQuant.PRIME4
        i = 0
        printed_string = ''
        while i < samplepixels:
            if i % 100 == 99:
                tmp = '\x08' * len(printed_string)
                printed_string = str((i + 1) * 100 / samplepixels) + '%\n'
                print(tmp + printed_string)
            else:
                p = self.pixels[pos]
                r = p >> 16 & 255
                g = p >> 8 & 255
                b = p & 255
                if i == 0:
                    self.network[self.BGCOLOR] = [
                     b, g, r]
                j = self.specialFind(b, g, r)
                if j < 0:
                    j = self.contest(b, g, r)
                if j >= self.SPECIALS:
                    a = 1.0 * alpha / self.INITALPHA
                    self.altersingle(a, j, b, g, r)
                    if rad > 0:
                        self.alterneigh(a, rad, j, b, g, r)
            pos = (pos + step) % lengthcount
            i += 1
            if i % delta == 0:
                alpha -= alpha / alphadec
                biasRadius -= biasRadius / self.RADIUSDEC
                rad = biasRadius * 2 ** self.RADIUSBIASSHIFT
                if rad <= 1:
                    rad = 0

        finalAlpha = 1.0 * alpha / self.INITALPHA
        print('Finished 1D learning: final alpha = %1.2f!' % finalAlpha)

    def fix(self):
        for i in range(self.NETSIZE):
            for j in range(3):
                x = int(0.5 + self.network[(i, j)])
                x = max(0, x)
                x = min(255, x)
                self.colormap[(i, j)] = x

            self.colormap[(i, 3)] = i

    def inxbuild(self):
        previouscol = 0
        startpos = 0
        for i in range(self.NETSIZE):
            p = self.colormap[i]
            q = None
            smallpos = i
            smallval = p[1]
            for j in range(i + 1, self.NETSIZE):
                q = self.colormap[j]
                if q[1] < smallval:
                    smallpos = j
                    smallval = q[1]

            q = self.colormap[smallpos]
            if i != smallpos:
                p[:], q[:] = q, p.copy()
            if smallval != previouscol:
                self.netindex[previouscol] = startpos + i >> 1
                for j in range(previouscol + 1, smallval):
                    self.netindex[j] = i

                previouscol = smallval
                startpos = i

        self.netindex[previouscol] = startpos + self.MAXNETPOS >> 1
        for j in range(previouscol + 1, 256):
            self.netindex[j] = self.MAXNETPOS

    def paletteImage(self):
        """PIL weird interface for making a paletted image: create an image
        which already has the palette, and use that in Image.quantize. This
        function returns this palette image."""
        if self.pimage is None:
            palette = []
            for i in range(self.NETSIZE):
                palette.extend(self.colormap[i][:3])

            palette.extend([0] * (256 - self.NETSIZE) * 3)
            self.pimage = Image.new('P', (1, 1), 0)
            self.pimage.putpalette(palette)
        return self.pimage

    def quantize(self, image):
        """ Use a kdtree to quickly find the closest palette colors for the pixels """
        if get_cKDTree():
            return self.quantize_with_scipy(image)
        else:
            print('Scipy not available, falling back to slower version.')
            return self.quantize_without_scipy(image)

    def quantize_with_scipy(self, image):
        w, h = image.size
        px = np.asarray(image).copy()
        px2 = px[:, :, :3].reshape((w * h, 3))
        cKDTree = get_cKDTree()
        kdtree = cKDTree((self.colormap[:, :3]), leafsize=10)
        result = kdtree.query(px2)
        colorindex = result[1]
        print('Distance: %1.2f' % (result[0].sum() / (w * h)))
        px2[:] = self.colormap[colorindex, :3]
        return Image.fromarray(px).convert('RGB').quantize(palette=(self.paletteImage()))

    def quantize_without_scipy(self, image):
        """" This function can be used if no scipy is availabe.
        It's 7 times slower though.
        """
        w, h = image.size
        px = np.asarray(image).copy()
        memo = {}
        for j in range(w):
            for i in range(h):
                key = (
                 px[(i, j, 0)], px[(i, j, 1)], px[(i, j, 2)])
                try:
                    val = memo[key]
                except KeyError:
                    val = (self.convert)(*key)
                    memo[key] = val

                px[(i, j, 0)], px[(i, j, 1)], px[(i, j, 2)] = val

        return Image.fromarray(px).convert('RGB').quantize(palette=(self.paletteImage()))

    def convert(self, *color):
        i = (self.inxsearch)(*color)
        return self.colormap[i, :3]

    def inxsearch(self, r, g, b):
        """Search for BGR values 0..255 and return colour index"""
        dists = self.colormap[:, :3] - np.array([r, g, b])
        a = np.argmin((dists * dists).sum(1))
        return a


if __name__ == '__main__':
    im = np.zeros((200, 200), dtype=(np.uint8))
    im[10:30, :] = 100
    im[:, 80:120] = 255
    im[-50:-40, :] = 50
    images = [
     im * 1.0, im * 0.8, im * 0.6, im * 0.4, im * 0]
    writeGif('lala3.gif', images, duration=0.5, dither=0)