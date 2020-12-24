# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/onitool/toolinfo.py
# Compiled at: 2016-07-09 03:21:41
from . import onifile as oni
import struct, binascii

def info(args, a):
    r = oni.Reader(a)
    print 'fileheader', r.h0
    while True:
        h = r.next()
        if h is None:
            break
        elif h['rt'] == oni.RECORD_NEW_DATA:
            break

    for k, v in r.streams.iteritems():
        print k, v

    return


def seeks(args, a):
    """prints seeks"""
    r = oni.Reader(a)
    while True:
        h = r.next()
        if h is None:
            break
        if h['rt'] == oni.RECORD_SEEK_TABLE:
            q = oni.parseseek(a, h)
            for qq in q['data']:
                print h['nid'], qq

    return


def times(args, a):
    """prints times info"""
    r = oni.Reader(a)
    while True:
        h = r.next()
        if h is None:
            break
        if h['rt'] == oni.RECORD_NEW_DATA:
            hh = oni.parsedatahead(a, h)
            print h['nid'], hh['frameid'], hh['timestamp']

    return


def compare(args, action, a, b):
    ra = oni.Reader(a)
    rb = oni.Reader(b)
    while True:
        ha = ra.next()
        hb = rb.next()
        if ha != hb:
            print 'mismatch in header a=', ha, 'b=', hb
        elif ha is None:
            print 'ended', ha, hb
            break
        a.seek(ha['poffset'])
        da = a.read(ha['fs'] - oni.HEADER_SIZE)
        b.seek(hb['poffset'])
        db = b.read(hb['fs'] - oni.HEADER_SIZE)
        if da != db:
            print 'mismatch in header extra a=', ha, 'b=', hb, len(da), len(db)
        else:
            a.seek(ha['poffset'] + ha['fs'])
            da = a.read(ha['ps'])
            b.seek(ha['poffset'] + ha['fs'])
            db = b.read(ha['ps'])
            if da != db:
                print 'mismatch in payload a=', ha, 'b=', hb, len(da), len(db)
                if ha['rt'] == oni.RECORD_SEEK_TABLE:
                    oni.parseseek(a, ha)
                    oni.parseseek(b, hb)
                    print 'firstseek', ('\n\t').join([ str(x) for x in ha['data'][0:10] ])
                    print 'secondseek', ('\n\t').join([ str(x) for x in hb['data'][0:10] ])

    return


def checkregistered(args, a):
    r = oni.Reader(a)
    last = None
    mid = -1
    found = False
    while True:
        h = r.next()
        pt = a.tell()
        if h is None:
            break
        prelast = last
        last = h
        if mid < h['nid']:
            mid = h['nid']
        elif h['rt'] == oni.RECORD_NODE_DATA_BEGIN:
            break
        elif h['rt'] == oni.RECORD_INT_PROPERTY:
            q = oni.parseprop(a, h)
            if q['name'] == 'RegistrationType':
                print q['data']
                found = True
                break

    if not found:
        print 'RegistrationType MISSING'
    return


def dump(args, a):
    r = oni.Reader(a)
    last = None
    mid = -1
    print 'fileheader', r.h0
    while True:
        h = r.next()
        pt = a.tell()
        if h is None:
            break
        prelast = last
        last = h
        if mid < h['nid']:
            mid = h['nid']
        if h['rt'] == oni.RECORD_NEW_DATA:
            print 'newdata', h['nid'], oni.parsedatahead(a, h), h['ps']
        elif h['rt'] == oni.RECORD_NODE_DATA_BEGIN:
            print 'nodebegin', h['nid'], h
        elif h['rt'] == oni.RECORD_NODE_ADDED:
            print 'nodeadded', h['nid'], h
            print '\tnodeadded-details', oni.parseadded(a, h)
        elif h['rt'] == oni.RECORD_INT_PROPERTY:
            print 'intprop', h['nid'], oni.parseprop(a, h), h['poffset'], h['fs']
        elif h['rt'] == oni.RECORD_REAL_PROPERTY:
            print 'realprop', h['nid'], oni.parseprop(a, h), h['poffset'], h['fs']
        elif h['rt'] == oni.RECORD_GENERAL_PROPERTY:
            pp = oni.parseprop(a, h)
            print 'genprop', h['nid'], pp
            if pp['name'] == 'xnMapOutputMode':
                xres, yres = struct.unpack('ii', pp['data'])
                data = dict(xres=xres, yres=yres)
                print '\t', data
        elif h['rt'] == oni.RECORD_NODE_STATE_READY:
            print 'ready', h
        elif h['rt'] == oni.RECORD_NODE_REMOVED:
            print 'removed', h
        elif h['rt'] == oni.RECORD_SEEK_TABLE:
            print 'seektable', h
        elif h['rt'] == oni.RECORD_END:
            print 'end', h
        else:
            print h['rt']

    if True:
        print 'blocks stats:'
        print '\tprelast', prelast
        print '\tlast', last
        print '\tmaxnodeid', mid
    print 'streams stats:'
    for k, v in r.streams.iteritems():
        print '\t', k, v

    return