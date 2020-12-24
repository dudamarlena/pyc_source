# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\pylib\visvis\vvmovie\images2ims.py
# Compiled at: 2016-03-22 04:56:47
# Size of source mod 2**32: 7368 bytes
""" Module images2ims

Use PIL to create a series of images.

"""
import os
try:
    import numpy as np
except ImportError:
    np = None

try:
    import PIL
    from PIL import Image
except ImportError:
    PIL = None

def checkImages(images):
    """ checkImages(images)
    Check numpy images and correct intensity range etc.
    The same for all movie formats.
    """
    images2 = []
    for im in images:
        if PIL and isinstance(im, PIL.Image.Image):
            images2.append(im)
        else:
            if np and isinstance(im, np.ndarray):
                if im.dtype == np.uint8:
                    images2.append(im)
                else:
                    if im.dtype in [np.float32, np.float64]:
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
                else:
                    if im.ndim == 3:
                        if im.shape[2] not in (3, 4):
                            raise ValueError('This array can not represent an image.')
                    else:
                        raise ValueError('This array can not represent an image.')
            else:
                raise ValueError('Invalid image type: ' + str(type(im)))

    return images2


def _getFilenameParts(filename):
    if '*' in filename:
        return tuple(filename.split('*', 1))
    else:
        return os.path.splitext(filename)


def _getFilenameWithFormatter(filename, N):
    formatter = '%04i'
    if N < 10:
        formatter = '%i'
    else:
        if N < 100:
            formatter = '%02i'
        elif N < 1000:
            formatter = '%03i'
    part1, part2 = _getFilenameParts(filename)
    return part1 + formatter + part2


def _getSequenceNumber(filename, part1, part2):
    seq = filename[len(part1):-len(part2)]
    seq2 = ''
    for c in seq:
        if c in '0123456789':
            seq2 += c
        else:
            break

    return int(seq2)


def writeIms(filename, images):
    """ writeIms(filename, images)
    
    Export movie to a series of image files. If the filenenumber 
    contains an asterix, a sequence number is introduced at its 
    location. Otherwise the sequence number is introduced right 
    before the final dot.
    
    To enable easy creation of a new directory with image files, 
    it is made sure that the full path exists.
    
    Images should be a list consisting of PIL images or numpy arrays. 
    The latter should be between 0 and 255 for integer types, and 
    between 0 and 1 for float types.
    
    """
    if PIL is None:
        raise RuntimeError('Need PIL to write series of image files.')
    images = checkImages(images)
    filename = os.path.abspath(filename)
    dirname, filename = os.path.split(filename)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    filename = _getFilenameWithFormatter(filename, len(images))
    seq = 0
    for frame in images:
        seq += 1
        fname = os.path.join(dirname, filename % seq)
        if np and isinstance(frame, np.ndarray):
            frame = PIL.Image.fromarray(frame)
        frame.save(fname)


def readIms(filename, asNumpy=True):
    """ readIms(filename, asNumpy=True)
    
    Read images from a series of images in a single directory. Returns a 
    list of numpy arrays, or, if asNumpy is false, a list if PIL images.
    
    """
    if PIL is None:
        raise RuntimeError('Need PIL to read a series of image files.')
    if asNumpy and np is None:
        raise RuntimeError('Need Numpy to return numpy arrays.')
    filename = os.path.abspath(filename)
    dirname, filename = os.path.split(filename)
    if not os.path.isdir(dirname):
        raise IOError('Directory not found: ' + str(dirname))
    part1, part2 = _getFilenameParts(filename)
    images = []
    for fname in os.listdir(dirname):
        if fname.startswith(part1) and fname.endswith(part2):
            nr = _getSequenceNumber(fname, part1, part2)
            im = PIL.Image.open(os.path.join(dirname, fname))
            images.append((im.copy(), nr))

    images.sort(key=lambda x: x[1])
    images = [im[0] for im in images]
    if asNumpy:
        images2 = images
        images = []
        for im in images2:
            if im.mode == 'P':
                im = im.convert()
            a = np.asarray(im)
            if len(a.shape) == 0:
                raise MemoryError('Too little memory to convert PIL image to array')
            images.append(a)

    return images