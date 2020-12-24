# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/util/lzss.py
# Compiled at: 2019-03-03 16:57:38
__doc__ = '\n/**************************************************************\n LZSS.C -- A Data Compression Program\n***************************************************************\n    4/6/1989 Haruhiko Okumura\n    Use, distribute, and modify this program freely.\n    Please send me your improved versions.\n        PC-VAN      SCIENCE\n        NIFTY-Serve PAF01022\n        CompuServe  74050,1022\n\n**************************************************************/\n/*\n *  lzss.c - Package for decompressing lzss compressed objects\n *\n *  Copyright (c) 2003 Apple Computer, Inc.\n *\n *  DRI: Josh de Cesare\n */\n'
from array import array
import struct
N = 4096
F = 18
THRESHOLD = 2
NIL = N

def decompress_lzss(str):
    if str[:8] != 'complzss':
        print 'decompress_lzss: complzss magic missing'
        return
    decompsize = struct.unpack('>L', str[12:16])[0]
    text_buf = array('B', ' ' * (N + F - 1))
    src = array('B', str[384:])
    srclen = len(src)
    dst = array('B', ' ' * decompsize)
    r = N - F
    srcidx, dstidx, flags, c = (0, 0, 0, 0)
    while True:
        flags >>= 1
        if flags & 256 == 0:
            if srcidx >= srclen:
                break
            c = src[srcidx]
            srcidx += 1
            flags = c | 65280
        if flags & 1:
            if srcidx >= srclen:
                break
            c = src[srcidx]
            srcidx += 1
            dst[dstidx] = c
            dstidx += 1
            text_buf[r] = c
            r += 1
            r &= N - 1
        else:
            if srcidx >= srclen:
                break
            i = src[srcidx]
            srcidx += 1
            if srcidx >= srclen:
                break
            j = src[srcidx]
            srcidx += 1
            i |= (j & 240) << 4
            j = (j & 15) + THRESHOLD
            for k in range(j + 1):
                c = text_buf[(i + k & N - 1)]
                dst[dstidx] = c
                dstidx += 1
                text_buf[r] = c
                r += 1
                r &= N - 1

    return dst.tostring()