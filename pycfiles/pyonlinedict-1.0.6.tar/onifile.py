# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/onitool/onifile.py
# Compiled at: 2016-07-09 03:32:03
import struct, sys
from collections import defaultdict
RECORD_END = 11
HEADER_MAGIC_SIZE = 4
MAGIC = 5392718
MAGICS = 'NIR\x00'
RHMAGIC = 'NI10'
HEADER_SIZE = 28

def XN_CODEC_ID(c1, c2, c3, c4):
    c1 = ord(c1)
    c2 = ord(c2)
    c3 = ord(c3)
    c4 = ord(c4)
    return c4 << 24 | c3 << 16 | c2 << 8 | c1


NODE_TYPE_DEVICE = 1
NODE_TYPE_DEPTH = 2
NODE_TYPE_IMAGE = 3
NODE_TYPE_IR = 4
XN_CODEC_UNCOMPRESSED = XN_CODEC_ID('N', 'O', 'N', 'E')
XN_CODEC_16Z = XN_CODEC_ID('1', '6', 'z', 'P')
XN_CODEC_16Z_EMB_TABLES = XN_CODEC_ID('1', '6', 'z', 'T')
XN_CODEC_8Z = XN_CODEC_ID('I', 'm', '8', 'z')
XN_CODEC_JPEG = XN_CODEC_ID('J', 'P', 'E', 'G')
ONI_PIXEL_FORMAT_DEPTH_1_MM = 100
ONI_PIXEL_FORMAT_DEPTH_100_UM = 101
ONI_PIXEL_FORMAT_SHIFT_9_2 = 102
ONI_PIXEL_FORMAT_SHIFT_9_3 = 103
ONI_PIXEL_FORMAT_RGB888 = 200
ONI_PIXEL_FORMAT_YUV422 = 201
ONI_PIXEL_FORMAT_GRAY8 = 202
ONI_PIXEL_FORMAT_GRAY16 = 203
ONI_PIXEL_FORMAT_JPEG = 204
ONI_PIXEL_FORMAT_YUYV = 205
RECORD_NODE_ADDED_1_0_0_4 = 2
RECORD_INT_PROPERTY = 3
RECORD_REAL_PROPERTY = 4
RECORD_STRING_PROPERTY = 5
RECORD_GENERAL_PROPERTY = 6
RECORD_NODE_REMOVED = 7
RECORD_NODE_DATA_BEGIN = 8
RECORD_NODE_STATE_READY = 9
RECORD_NEW_DATA = 10
RECORD_END = 11
RECORD_NODE_ADDED_1_0_0_5 = 12
RECORD_NODE_ADDED = 13
RECORD_SEEK_TABLE = 14
IMAGE_REGISTRATION_OFF = 0
IMAGE_REGISTRATION_DEPTH_TO_COLOR = 1

def parseint(a):
    return struct.unpack('i', a.read(4))[0]


def parseint64(a):
    return struct.unpack('Q', a.read(8))[0]


def makeint64(a):
    return struct.pack('Q', a)


def parsedatahead(a, h):
    """Parsed the header of the data block containing timestamp and seek table position
    https://github.com/OpenNI/OpenNI2/blob/master/Source/Core/OniDataRecords.cpp"""
    a.seek(h['poffset'], 0)
    ts = parseint64(a)
    frameid = parseint(a)
    return dict(timestamp=ts, frameid=frameid)


def writedatahead(a, h, hh):
    a.seek(h['poffset'], 0)
    a.write(struct.pack('=qi', hh['timestamp'], hh['frameid']))


def patchtime(a, h, ot):
    a.seek(h['poffset'], 0)
    a.write(makeint64(ot))


def parsestr(a):
    namelen = parseint(a)
    name = a.read(namelen)[0:-1]
    return name


def makeindexentry(a):
    """encodes the DataIndexEntry made of a timestamp, config and offset"""
    if type(a) == tuple:
        return struct.pack('=QiQ', a[0], a[1], a[2])
    else:
        return struct.pack('=QiQ', a['timestamp'], a['config'], a['offset'])


def parseindexentry(a):
    """decodes the DataIndexEntry made of a timestamp, config and offset as dictionary"""
    ts, cid, pos = struct.unpack('=QiQ', a.read(20))
    return dict(timestamp=ts, config=cid, offset=pos)


def parseseek(a, h):
    a.seek(h['poffset'] + h['fs'] - HEADER_SIZE, 0)
    r = []
    n = h['ps'] / 20
    for i in range(0, n):
        t = parseindexentry(a)
        t['frameid'] = i
        r.append(t)

    h['data'] = r
    return h


def makestr(s):
    return struct.pack('=i', len(s) + 1) + s + '\x00'


codec2id = dict(raw=XN_CODEC_UNCOMPRESSED, jpeg=XN_CODEC_JPEG)
codec2id['16z'] = XN_CODEC_16Z
codec2id['8z'] = XN_CODEC_8Z
codec2id['16zt'] = XN_CODEC_16Z_EMB_TABLES

def writedadded(a, h, hh):
    a.seek(h['poffset'], 0)
    a.write(makestr(hh['name']))
    ocodec = codec2id.get(hh['codec'], hh['codec'])
    a.write(struct.pack('=iiiQQQ', hh['nodetype'], ocodec, hh['frames'], hh['mints'], hh['maxts'], hh['seektable']))


def parseadded(a, h):
    a.seek(h['poffset'], 0)
    name = parsestr(a)
    nodetype = parseint(a)
    codec = parseint(a)
    nframes = parseint(a)
    mints = parseint64(a)
    maxts = parseint64(a)
    seektable = parseint64(a)
    ocodec = codec
    if codec == XN_CODEC_UNCOMPRESSED:
        codec = 'raw'
    elif codec == XN_CODEC_16Z:
        codec = '16z'
    elif codec == XN_CODEC_16Z_EMB_TABLES:
        codec = '16zt'
    elif codec == XN_CODEC_8Z:
        codec = '8z'
    elif codec == XN_CODEC_JPEG:
        codec = 'jpeg'
    return dict(name=name, nodetype=nodetype, codec=codec, frames=nframes, mints=mints, maxts=maxts, seektable=seektable)


def parseprop(a, h):
    a.seek(h['poffset'], 0)
    name = parsestr(a)
    datalen = parseint(a) - 4
    data = a.read(datalen)
    if h['rt'] == RECORD_INT_PROPERTY:
        if datalen == 8:
            data = struct.unpack('q', data)[0]
        else:
            data = struct.unpack('i', data)[0]
    elif h['rt'] == RECORD_REAL_PROPERTY:
        if datalen == 8:
            data = struct.unpack('d', data)[0]
        else:
            data = struct.unpack('f', data)[0]
    return dict(name=name, data=data, datalen=datalen)


def addprop(a, nid, name, type, value, datalen=0):
    if type == RECORD_INT_PROPERTY:
        if datalen == 8:
            c = makestr(name) + struct.pack('=iq', 12, value)
        else:
            c = makestr(name) + struct.pack('=iii', 8, value, 0)
        writehead(a, dict(rt=type, nid=nid, ps=0, fs=HEADER_SIZE + len(c), undopos=0))
        a.write(c)
    elif type == RECORD_GENERAL_PROPERTY:
        c = makestr(name) + struct.pack('=i', 4 + len(value)) + value
        writehead(a, dict(rt=type, nid=nid, ps=0, fs=HEADER_SIZE + len(c), undopos=0))
        a.write(c)
    elif type == RECORD_REAL_PROPERTY:
        c = makestr(name) + struct.pack('=if', 8, value)
        writehead(a, dict(rt=type, nid=nid, ps=0, fs=HEADER_SIZE + len(c), undopos=0))
        a.write(c)
    else:
        print 'prop type unsupported', type
        sys.exit(-1)


def writeprop(a, h, z):
    a.seek(h['poffset'], 0)
    if h['rt'] == RECORD_INT_PROPERTY:
        c = makestr(z['name']) + struct.pack('=ii', 8, z['data'])
        a.write(c)
    else:
        print 'prop type unsupported', h, z
        sys.exit(-1)


def emptyhead1():
    return dict(magic='NI10', version=(1, 0, 1, 0), maxnid=0, ts=0)


def writehead1(a, h):
    """writes a new header"""
    a.seek(0)
    version = struct.pack('bbhi', *h['version'])
    ts = struct.pack('Q', h['ts'])
    maxnodeid = struct.pack('i', h['maxnid'])
    a.write(h['magic'] + version + ts + maxnodeid)


def readhead1(a):
    """read the main file header"""
    magic = a.read(HEADER_MAGIC_SIZE)
    version = struct.unpack('bbhi', a.read(8))
    ts = struct.unpack('Q', a.read(8))[0]
    maxnodeid = struct.unpack('i', a.read(4))[0]
    if magic != RHMAGIC:
        print 'bad magic', magic
        return False
    else:
        return dict(version=version, maxnid=maxnodeid, ts=ts, magic=magic)


def writeend(a):
    """writes the end record"""
    w = (
     MAGIC, 11, 0, HEADER_SIZE, 0)
    a.write(struct.pack('5i', *w) + struct.pack('Q', 0))


def copyblock(a, h, b, frame=None, timestamp=None):
    a.seek(h['poffset'], 0)
    hout = dict(rt=h['rt'], nid=h['nid'], fs=h['fs'], ps=h['ps'], undopos=h['undopos'], poffset=0, hoffset=b.tell(), nextheader=0)
    writehead(b, hout)
    if h['fs'] > HEADER_SIZE:
        if h['rt'] == RECORD_NEW_DATA and frame is not None:
            oldts = parseint64(a)
            oldframeid = parseint(a)
            b.write(struct.pack('=qi', timestamp, frame))
        else:
            b.write(a.read(h['fs'] - HEADER_SIZE))
    done = 0
    while done < h['ps']:
        left = h['ps'] - done
        if left > 65536:
            left = 65536
        b.write(a.read(left))
        done += left

    hout['poffset'] = b.tell()
    hout['nextheader'] = hout['hoffset'] + hout['fs'] + hout['ps']
    return hout


def writehead(a, h):
    a.write(struct.pack('5i', MAGIC, h['rt'], h['nid'], h['fs'], h['ps']) + struct.pack('Q', h['undopos']))


def readrechead(a):
    """read record: the resulting dictionary contains:
    - rt  = recordType
    - nid = identifier/stream
    - fs  = field size
    - ps  = payload size
    - poffset = offset to the content
    - hoffset = offset to the header
    - nextheader = next header
    - h2 = undo record pos (one uint64)

    The header stored is:
    - magic (32bit) 0x0052494E
    - rt
    - nid
    - fs = sizeof(*m_header)
    - ps 
    - undorecord
    """
    p = a.tell()
    h1 = a.read(HEADER_SIZE)
    if h1 == '':
        return None
    else:
        magic, rt, nid, fs, ps, undopos = struct.unpack('=5iQ', h1)
        if magic != MAGIC:
            print 'bad magic record', magic
            return None
        r = dict(rt=rt, nid=nid, fs=fs, ps=ps, poffset=a.tell(), hoffset=p, nextheader=p + ps + fs, undopos=undopos, magic=magic)
        return r


class StreamInfo:
    """Class for transcoding"""

    def __init__(self):
        self.oldtimestamp = 0
        self.oldframes = 0
        self.oldbasetime = None
        self.newtimestamp = 0
        self.newframes = 0
        self.maxts = None
        self.mints = None
        self.configid = 0
        self.emitted = False
        self.removeemitted = False
        self.headerblock = None
        self.headerdata = None
        self.framesoffset = [(0, 0, 0)]
        self.headerseek = None
        return

    def assignnodeadded(self, h, hh):
        self.headerblock = h
        self.headerdata = hh

    def addframe(self, preoffset, dataheader, file, configid):
        ts = dataheader['timestamp']
        self.newtime(ts)
        self.framesoffset.append((ts, configid, preoffset))
        self.newframes += 1

    def newtime(self, t):
        if self.maxts is None:
            self.maxts = t
            self.mints = t
        else:
            if t > self.maxts:
                self.maxts = t
            if t < self.mints:
                self.mints = t
        self.newtimestamp = t
        return

    def writeseek(self, a, noseek):
        self.emitted = True
        q = self
        off = a.tell()
        if not noseek:
            q.headerseek = dict(rt=RECORD_SEEK_TABLE, ps=len(self.framesoffset) * 20, fs=HEADER_SIZE, nid=self.headerblock['nid'], undopos=0)
            q.headerdata['maxts'] = q.maxts is not None and q.maxts or 0
            q.headerdata['mints'] = q.mints is not None and q.mints or 0
            q.headerdata['frames'] = q.newframes
            if len(self.framesoffset) > 1:
                q.headerdata['seektable'] = off
                writehead(a, self.headerseek)
                for t in self.framesoffset:
                    a.write(makeindexentry(t))

            else:
                q.headerdata['seektable'] = 0
        else:
            q.headerdata['seektable'] = 0
        return

    def fixnodeadded(self, a):
        writedadded(a, self.headerblock, self.headerdata)


class Reader:

    def __init__(self, file, h0=None):
        self.file = file
        self.lasth = None
        self.nodeinfo = dict()
        self.nodetype2nid = dict()
        if h0 is None:
            h0 = readhead1(self.file)
        self.h0 = h0
        self.pseektable = dict()
        self.pend = None
        return

    def getseektable(self, nid):
        if nid not in self.pseektable:
            return None
        else:
            return parseseek(self.file, self.pseektable[nid])

    @property
    def streams(self):
        return self.nodeinfo

    def next(self):
        if self.lasth:
            self.file.seek(self.lasth['nextheader'])
        h = readrechead(self.file)
        self.lasth = h
        if h is None or h['magic'] == 0:
            return
        if h['rt'] == RECORD_NEW_DATA:
            pass
        elif h['rt'] == RECORD_NODE_ADDED:
            hh = parseadded(self.file, h)
            self.nodeinfo[h['nid']] = hh
            self.nodetype2nid[hh['nodetype']] = h['nid']
        elif h['rt'] == RECORD_GENERAL_PROPERTY:
            pp = parseprop(self.file, h)
            if pp['name'] == 'xnMapOutputMode':
                xres, yres = struct.unpack('ii', pp['data'])
                hhnode = self.nodeinfo[h['nid']]
                hhnode['size'] = (xres, yres)
        elif h['rt'] == RECORD_NEW_DATA:
            hh = parsedatahead(self.file, h)
            q = self.nodeinfo[hh['nid']]
            q['maxts'] = hh['timestamp']
        elif h['rt'] == RECORD_SEEK_TABLE:
            self.pseektable[h['nid']] = h
        elif h['rt'] == RECORD_END:
            self.pend = h
        return h


class Patcher(Reader):

    def __init__(self, file, h0):
        Reader.__init__(file, h0)
        self.stats = defaultdict(StreamInfo)

    def finalize(self):
        for q in self.stats.values():
            q.patchframeheader(self.file)
            q.writeseek(self.file, False)

        self.h0['ts'] = max([ q.maxts for q in self.stats.values() ])
        writehead1(self.file, self.h0)
        writeend(self.file)


class Writer:

    def __init__(self, file, h0=None):
        self.file = file
        self.stats = defaultdict(StreamInfo)
        self.mid = -1
        self.noseek = False
        self.configid = 0
        if h0 is None:
            self.h0 = emptyhead1()
        else:
            self.h0 = dict()
            self.h0.update(h0)
        writehead1(self.file, self.h0)
        self.endemitted = False
        return

    def addproperty(self, header, content):
        writehead(self.file, header)
        header['poffset'] = self.file.tell()
        writeprop(self.file, header, content)
        self.configid += 1

    def addprop(self, nid, name, type, value, datalen=0):
        addprop(self.file, nid, name, type, value, datalen)
        self.configid += 1

    def copyblock(self, header, file):
        if header['nid'] > self.mid:
            self.mid = header['nid']
        file.seek(header['poffset'])
        d = file.read(header['ps'] + header['fs'] - HEADER_SIZE)
        preoffset = self.file.tell()
        writehead(self.file, header)
        po = self.file.tell()
        self.file.write(d)
        rt = header['rt']
        if rt == RECORD_NODE_ADDED:
            hh = dict()
            hh.update(header)
            hh['poffset'] = po
            hd = parseadded(file, header)
            self.stats[header['nid']].assignnodeadded(hh, hd)
        elif rt == RECORD_INT_PROPERTY or rt == RECORD_REAL_PROPERTY or rt == RECORD_GENERAL_PROPERTY:
            self.configid += 1
        elif rt == RECORD_NODE_REMOVED:
            self.stats[header['nid']].removeemitted = True
        elif rt == RECORD_END:
            self.endemitted = True
        elif rt == RECORD_NEW_DATA:
            q = self.stats[header['nid']]
            dataheader = parsedatahead(file, header)
            q.addframe(preoffset, dataheader, self.file, self.configid)

    def addframe(self, nid, frameid, timestamp, content):
        if nid > self.mid:
            self.mid = nid
        h = dict(rt=RECORD_NEW_DATA, nid=nid, fs=40, ps=len(content), undopos=0)
        preoffset = self.file.tell()
        writehead(self.file, h)
        h['poffset'] = self.file.tell()
        dataheader = dict(frameid=frameid, timestamp=timestamp)
        writedatahead(self.file, h, hh)
        self.file.write(content)
        q = self.stats[h['nid']]
        q.addframe(preoffset, dataheader, self.file, self.configid)

    def emitseek(self, nid, ofile=None, hofile=None):
        for k, q in self.stats.iteritems():
            if q.headerblock['nid'] == nid and not q.emitted:
                if ofile is not None:
                    pp = parseseek(ofile, hofile)
                    configid = pp['data'][1]['config']
                    print 'newconfigid', configid
                    self.configid = configid
                    for i, o in enumerate(q.framesoffset):
                        q.framesoffset[i] = (
                         o[0], configid, o[2])

                    q.framesoffset[0] = (0, 0, 0)
                q.writeseek(self.file, self.noseek)

        return

    def finalize(self):
        if not self.endemitted:
            writeend(self.file)
            self.endemitted = True
        for q in self.stats.values():
            if not q.emitted:
                if not q.removeemitted:
                    pass
                q.writeseek(self.file, self.noseek)

        for q in self.stats.values():
            q.fixnodeadded(self.file)

        self.h0['maxnid'] = self.mid
        self.h0['ts'] = max([ q.maxts for q in self.stats.values() ])
        if self.h0['ts'] is None:
            self.h0['ts'] = 0
            print 'WARNING issue with stats', self.stats
        writehead1(self.file, self.h0)
        return