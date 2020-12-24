# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/igwtools/imageproc.py
# Compiled at: 2007-06-06 18:00:01
import sys, pylab, Image, numpy
from math import log

def justshowit():
    filename = sys.argv[1]
    im = Image.open(filename, 'r')
    (xsize, ysize) = im.size
    data = im.getdata()
    newarr = numpy.array(data, dtype='uint8')
    if im.mode == 'RGB':
        newarr = newarr.reshape((ysize, xsize, 3))
    else:
        pylab.gray()
        newarr = newarr.reshape((ysize, xsize))
    pylab.imshow(newarr)
    pylab.show()