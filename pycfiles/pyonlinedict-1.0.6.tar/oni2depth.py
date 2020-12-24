# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/onitool/oni2depth.py
# Compiled at: 2015-06-08 17:33:34
import struct
from onifile import *
from xndec import *
if __name__ == '__main__':
    import sys, os
    if len(sys.argv) == 0:
        print 'Required: ONIfilename'
        sys.exit(-1)
    docolor = len(sys.argv) > 3
    filesize = os.stat(sys.argv[1]).st_size
    a = open(sys.argv[1], 'rb')
    h0 = readhead1(a)
    mid = 0
    prelast = None
    last = None
    st = None
    offdict = dict()
    count = 0
    ob = allocoutput16(217088)
    while True:
        h = readrechead(a)
        if h is None:
            break
        prelast = last
        last = h
        if h['nid'] > mid:
            mid = h['nid']
        if h['nid'] == 1:
            if h['rt'] == RECORD_NEW_DATA:
                pd = parsedata(a, h)
                print pd['dataoffset'], h['ps'], h['fs']
                z = a.read(h['ps'])
                count += 1
                if count == 50:
                    code, size = doXnStreamUncompressDepth16ZWithEmbTable(z, ob)
                    print 'decoded ', code, size, 'vs input', len(z), 'output', len(ob)
                    o = open('x.depth', 'wb')
                    o.write(ob)
                    o.close()
                    break
        if h['rt'] == RECORD_END:
            continue
        a.seek(h['nextheader'], 0)

    a.close()