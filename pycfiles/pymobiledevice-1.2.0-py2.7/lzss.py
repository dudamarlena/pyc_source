# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/util/lzss.py
# Compiled at: 2019-03-03 16:57:38
"""
/**************************************************************
 LZSS.C -- A Data Compression Program
***************************************************************
    4/6/1989 Haruhiko Okumura
    Use, distribute, and modify this program freely.
    Please send me your improved versions.
        PC-VAN      SCIENCE
        NIFTY-Serve PAF01022
        CompuServe  74050,1022

**************************************************************/
/*
 *  lzss.c - Package for decompressing lzss compressed objects
 *
 *  Copyright (c) 2003 Apple Computer, Inc.
 *
 *  DRI: Josh de Cesare
 */
"""
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