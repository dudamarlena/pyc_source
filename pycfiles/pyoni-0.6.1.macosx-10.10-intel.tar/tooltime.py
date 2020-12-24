# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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