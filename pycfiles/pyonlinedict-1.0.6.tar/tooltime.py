# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/onitool/tooltime.py
# Compiled at: 2015-08-22 11:28:57
from . import onifile as oni
import struct
from collections import defaultdict

def rescale(args, factor, a, b):
    r = oni.Reader(a)
    w = oni.Writer(b, r.h0)
    while True:
        h = r.next()
        if h is None:
            break
        elif h['rt'] == oni.RECORD_SEEK_TABLE:
            w.emitseek(h['nid'])
        elif h['rt'] == oni.RECORD_NEW_DATA:
            hh = oni.parsedatahead(a, h)
            print dict(nid=h['nid'], ps=h['ps'], fs=h['fs'], frameid=hh['frameid'], timestamp=hh['timestamp'])
            w.addframe(h['nid'], hh['frameid'], factor * hh['timestamp'], a.read(h['ps']))
        else:
            w.copyblock(h, a)

    w.finalize()
    return