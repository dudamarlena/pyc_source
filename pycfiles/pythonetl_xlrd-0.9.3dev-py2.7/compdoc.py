# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xlrd\compdoc.py
# Compiled at: 2013-10-17 14:03:42
from __future__ import nested_scopes, print_function
import sys
from struct import unpack
from .timemachine import *
import array
SIGNATURE = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
EOCSID = -2
FREESID = -1
SATSID = -3
MSATSID = -4
EVILSID = -5

class CompDocError(Exception):
    pass


class DirNode(object):

    def __init__(self, DID, dent, DEBUG=0, logfile=sys.stdout):
        self.DID = DID
        self.logfile = logfile
        cbufsize, self.etype, self.colour, self.left_DID, self.right_DID, self.root_DID = unpack('<HBBiii', dent[64:80])
        self.first_SID, self.tot_size = unpack('<ii', dent[116:124])
        if cbufsize == 0:
            self.name = UNICODE_LITERAL('')
        else:
            self.name = unicode(dent[0:cbufsize - 2], 'utf_16_le')
        self.children = []
        self.parent = -1
        self.tsinfo = unpack('<IIII', dent[100:116])
        if DEBUG:
            self.dump(DEBUG)

    def dump(self, DEBUG=1):
        fprintf(self.logfile, 'DID=%d name=%r etype=%d DIDs(left=%d right=%d root=%d parent=%d kids=%r) first_SID=%d tot_size=%d\n', self.DID, self.name, self.etype, self.left_DID, self.right_DID, self.root_DID, self.parent, self.children, self.first_SID, self.tot_size)
        if DEBUG == 2:
            print('timestamp info', self.tsinfo, file=self.logfile)


def _build_family_tree(dirlist, parent_DID, child_DID):
    if child_DID < 0:
        return
    _build_family_tree(dirlist, parent_DID, dirlist[child_DID].left_DID)
    dirlist[parent_DID].children.append(child_DID)
    dirlist[child_DID].parent = parent_DID
    _build_family_tree(dirlist, parent_DID, dirlist[child_DID].right_DID)
    if dirlist[child_DID].etype == 1:
        _build_family_tree(dirlist, child_DID, dirlist[child_DID].root_DID)


class CompDoc(object):

    def __init__(self, mem, logfile=sys.stdout, DEBUG=0):
        self.logfile = logfile
        self.DEBUG = DEBUG
        if mem[0:8] != SIGNATURE:
            raise CompDocError('Not an OLE2 compound document')
        if mem[28:30] != b'\xfe\xff':
            raise CompDocError('Expected "little-endian" marker, found %r' % mem[28:30])
        revision, version = unpack('<HH', mem[24:28])
        if DEBUG:
            print('\nCompDoc format: version=0x%04x revision=0x%04x' % (version, revision), file=logfile)
        self.mem = mem
        ssz, sssz = unpack('<HH', mem[30:34])
        if ssz > 20:
            print('WARNING: sector size (2**%d) is preposterous; assuming 512 and continuing ...' % ssz, file=logfile)
            ssz = 9
        if sssz > ssz:
            print('WARNING: short stream sector size (2**%d) is preposterous; assuming 64 and continuing ...' % sssz, file=logfile)
            sssz = 6
        self.sec_size = sec_size = 1 << ssz
        self.short_sec_size = 1 << sssz
        if self.sec_size != 512 or self.short_sec_size != 64:
            print('@@@@ sec_size=%d short_sec_size=%d' % (self.sec_size, self.short_sec_size), file=logfile)
        SAT_tot_secs, self.dir_first_sec_sid, _unused, self.min_size_std_stream, SSAT_first_sec_sid, SSAT_tot_secs, MSATX_first_sec_sid, MSATX_tot_secs = unpack('<iiiiiiii', mem[44:76])
        mem_data_len = len(mem) - 512
        mem_data_secs, left_over = divmod(mem_data_len, sec_size)
        if left_over:
            mem_data_secs += 1
            print('WARNING *** file size (%d) not 512 + multiple of sector size (%d)' % (
             len(mem), sec_size), file=logfile)
        self.mem_data_secs = mem_data_secs
        self.mem_data_len = mem_data_len
        seen = self.seen = array.array('B', [0]) * mem_data_secs
        if DEBUG:
            print('sec sizes', ssz, sssz, sec_size, self.short_sec_size, file=logfile)
            print('mem data: %d bytes == %d sectors' % (mem_data_len, mem_data_secs), file=logfile)
            print('SAT_tot_secs=%d, dir_first_sec_sid=%d, min_size_std_stream=%d' % (
             SAT_tot_secs, self.dir_first_sec_sid, self.min_size_std_stream), file=logfile)
            print('SSAT_first_sec_sid=%d, SSAT_tot_secs=%d' % (SSAT_first_sec_sid, SSAT_tot_secs), file=logfile)
            print('MSATX_first_sec_sid=%d, MSATX_tot_secs=%d' % (MSATX_first_sec_sid, MSATX_tot_secs), file=logfile)
        nent = sec_size // 4
        fmt = '<%di' % nent
        trunc_warned = 0
        MSAT = list(unpack('<109i', mem[76:512]))
        SAT_sectors_reqd = (mem_data_secs + nent - 1) // nent
        expected_MSATX_sectors = max(0, (SAT_sectors_reqd - 109 + nent - 2) // (nent - 1))
        actual_MSATX_sectors = 0
        if MSATX_tot_secs == 0 and MSATX_first_sec_sid in (EOCSID, FREESID, 0):
            pass
        else:
            sid = MSATX_first_sec_sid
            while sid not in (EOCSID, FREESID):
                if DEBUG > 1:
                    print('MSATX: sid=%d (0x%08X)' % (sid, sid), file=logfile)
                if sid >= mem_data_secs:
                    msg = 'MSAT extension: accessing sector %d but only %d in file' % (sid, mem_data_secs)
                    if DEBUG > 1:
                        print(msg, file=logfile)
                        break
                    raise CompDocError(msg)
                elif sid < 0:
                    raise CompDocError('MSAT extension: invalid sector id: %d' % sid)
                if seen[sid]:
                    raise CompDocError('MSAT corruption: seen[%d] == %d' % (sid, seen[sid]))
                seen[sid] = 1
                actual_MSATX_sectors += 1
                if DEBUG and actual_MSATX_sectors > expected_MSATX_sectors:
                    print('[1]===>>>', mem_data_secs, nent, SAT_sectors_reqd, expected_MSATX_sectors, actual_MSATX_sectors, file=logfile)
                offset = 512 + sec_size * sid
                MSAT.extend(unpack(fmt, mem[offset:offset + sec_size]))
                sid = MSAT.pop()

            if DEBUG and actual_MSATX_sectors != expected_MSATX_sectors:
                print('[2]===>>>', mem_data_secs, nent, SAT_sectors_reqd, expected_MSATX_sectors, actual_MSATX_sectors, file=logfile)
            if DEBUG:
                print('MSAT: len =', len(MSAT), file=logfile)
                dump_list(MSAT, 10, logfile)
            self.SAT = []
            actual_SAT_sectors = 0
            dump_again = 0
            for msidx in xrange(len(MSAT)):
                msid = MSAT[msidx]
                if msid in (FREESID, EOCSID):
                    continue
                if msid >= mem_data_secs:
                    if not trunc_warned:
                        print('WARNING *** File is truncated, or OLE2 MSAT is corrupt!!', file=logfile)
                        print('INFO: Trying to access sector %d but only %d available' % (
                         msid, mem_data_secs), file=logfile)
                        trunc_warned = 1
                    MSAT[msidx] = EVILSID
                    dump_again = 1
                    continue
                elif msid < -2:
                    raise CompDocError('MSAT: invalid sector id: %d' % msid)
                if seen[msid]:
                    raise CompDocError('MSAT extension corruption: seen[%d] == %d' % (msid, seen[msid]))
                seen[msid] = 2
                actual_SAT_sectors += 1
                if DEBUG and actual_SAT_sectors > SAT_sectors_reqd:
                    print('[3]===>>>', mem_data_secs, nent, SAT_sectors_reqd, expected_MSATX_sectors, actual_MSATX_sectors, actual_SAT_sectors, msid, file=logfile)
                offset = 512 + sec_size * msid
                self.SAT.extend(unpack(fmt, mem[offset:offset + sec_size]))

            if DEBUG:
                print('SAT: len =', len(self.SAT), file=logfile)
                dump_list(self.SAT, 10, logfile)
                print(file=logfile)
            if DEBUG and dump_again:
                print('MSAT: len =', len(MSAT), file=logfile)
                dump_list(MSAT, 10, logfile)
                for satx in xrange(mem_data_secs, len(self.SAT)):
                    self.SAT[satx] = EVILSID

                print('SAT: len =', len(self.SAT), file=logfile)
                dump_list(self.SAT, 10, logfile)
            dbytes = self._get_stream(self.mem, 512, self.SAT, self.sec_size, self.dir_first_sec_sid, name='directory', seen_id=3)
            dirlist = []
            did = -1
            for pos in xrange(0, len(dbytes), 128):
                did += 1
                dirlist.append(DirNode(did, dbytes[pos:pos + 128], 0, logfile))

        self.dirlist = dirlist
        _build_family_tree(dirlist, 0, dirlist[0].root_DID)
        if DEBUG:
            for d in dirlist:
                d.dump(DEBUG)

        sscs_dir = self.dirlist[0]
        assert sscs_dir.etype == 5
        if sscs_dir.first_SID < 0 or sscs_dir.tot_size == 0:
            self.SSCS = ''
        else:
            self.SSCS = self._get_stream(self.mem, 512, self.SAT, sec_size, sscs_dir.first_SID, sscs_dir.tot_size, name='SSCS', seen_id=4)
        self.SSAT = []
        if SSAT_tot_secs > 0 and sscs_dir.tot_size == 0:
            print('WARNING *** OLE2 inconsistency: SSCS size is 0 but SSAT size is non-zero', file=logfile)
        if sscs_dir.tot_size > 0:
            sid = SSAT_first_sec_sid
            nsecs = SSAT_tot_secs
            while sid >= 0 and nsecs > 0:
                if seen[sid]:
                    raise CompDocError('SSAT corruption: seen[%d] == %d' % (sid, seen[sid]))
                seen[sid] = 5
                nsecs -= 1
                start_pos = 512 + sid * sec_size
                news = list(unpack(fmt, mem[start_pos:start_pos + sec_size]))
                self.SSAT.extend(news)
                sid = self.SAT[sid]

            if DEBUG:
                print('SSAT last sid %d; remaining sectors %d' % (sid, nsecs), file=logfile)
            assert nsecs == 0 and sid == EOCSID
        if DEBUG:
            print('SSAT', file=logfile)
            dump_list(self.SSAT, 10, logfile)
        if DEBUG:
            print('seen', file=logfile)
            dump_list(seen, 20, logfile)

    def _get_stream(self, mem, base, sat, sec_size, start_sid, size=None, name='', seen_id=None):
        sectors = []
        s = start_sid
        if size is None:
            while s >= 0:
                if seen_id is not None:
                    if self.seen[s]:
                        raise CompDocError('%s corruption: seen[%d] == %d' % (name, s, self.seen[s]))
                    self.seen[s] = seen_id
                start_pos = base + s * sec_size
                sectors.append(mem[start_pos:start_pos + sec_size])
                try:
                    s = sat[s]
                except IndexError:
                    raise CompDocError('OLE2 stream %r: sector allocation table invalid entry (%d)' % (
                     name, s))

            assert s == EOCSID
        else:
            todo = size
            while s >= 0:
                if seen_id is not None:
                    if self.seen[s]:
                        raise CompDocError('%s corruption: seen[%d] == %d' % (name, s, self.seen[s]))
                    self.seen[s] = seen_id
                start_pos = base + s * sec_size
                grab = sec_size
                if grab > todo:
                    grab = todo
                todo -= grab
                sectors.append(mem[start_pos:start_pos + grab])
                try:
                    s = sat[s]
                except IndexError:
                    raise CompDocError('OLE2 stream %r: sector allocation table invalid entry (%d)' % (
                     name, s))

        assert s == EOCSID
        if todo != 0:
            fprintf(self.logfile, 'WARNING *** OLE2 stream %r: expected size %d, actual size %d\n', name, size, size - todo)
        return ('').join(sectors)

    def _dir_search(self, path, storage_DID=0):
        head = path[0]
        tail = path[1:]
        dl = self.dirlist
        for child in dl[storage_DID].children:
            if dl[child].name.lower() == head.lower():
                et = dl[child].etype
                if et == 2:
                    return dl[child]
                if et == 1:
                    if not tail:
                        raise CompDocError("Requested component is a 'storage'")
                    return self._dir_search(tail, child)
                dl[child].dump(1)
                raise CompDocError("Requested stream is not a 'user stream'")

        return

    def get_named_stream(self, qname):
        d = self._dir_search(qname.split('/'))
        if d is None:
            return
        else:
            if d.tot_size >= self.min_size_std_stream:
                return self._get_stream(self.mem, 512, self.SAT, self.sec_size, d.first_SID, d.tot_size, name=qname, seen_id=d.DID + 6)
            else:
                return self._get_stream(self.SSCS, 0, self.SSAT, self.short_sec_size, d.first_SID, d.tot_size, name=qname + ' (from SSCS)', seen_id=None)

            return

    def locate_named_stream(self, qname):
        d = self._dir_search(qname.split('/'))
        if d is None:
            return (None, 0, 0)
        else:
            if d.tot_size > self.mem_data_len:
                raise CompDocError('%r stream length (%d bytes) > file data size (%d bytes)' % (
                 qname, d.tot_size, self.mem_data_len))
            if d.tot_size >= self.min_size_std_stream:
                result = self._locate_stream(self.mem, 512, self.SAT, self.sec_size, d.first_SID, d.tot_size, qname, d.DID + 6)
                if self.DEBUG:
                    print('\nseen', file=self.logfile)
                    dump_list(self.seen, 20, self.logfile)
                return result
            return (
             self._get_stream(self.SSCS, 0, self.SSAT, self.short_sec_size, d.first_SID, d.tot_size, qname + ' (from SSCS)', None),
             0,
             d.tot_size)
            return

    def _locate_stream(self, mem, base, sat, sec_size, start_sid, expected_stream_size, qname, seen_id):
        s = start_sid
        if s < 0:
            raise CompDocError('_locate_stream: start_sid (%d) is -ve' % start_sid)
        p = -99
        start_pos = -9999
        end_pos = -8888
        slices = []
        tot_found = 0
        found_limit = (expected_stream_size + sec_size - 1) // sec_size
        while s >= 0:
            if self.seen[s]:
                print('_locate_stream(%s): seen' % qname, file=self.logfile)
                dump_list(self.seen, 20, self.logfile)
                raise CompDocError('%s corruption: seen[%d] == %d' % (qname, s, self.seen[s]))
            self.seen[s] = seen_id
            tot_found += 1
            if tot_found > found_limit:
                raise CompDocError('%s: size exceeds expected %d bytes; corrupt?' % (
                 qname, found_limit * sec_size))
            if s == p + 1:
                end_pos += sec_size
            else:
                if p >= 0:
                    slices.append((start_pos, end_pos))
                start_pos = base + s * sec_size
                end_pos = start_pos + sec_size
            p = s
            s = sat[s]

        assert s == EOCSID
        if not tot_found == found_limit:
            raise AssertionError
            return slices or (
             mem, start_pos, expected_stream_size)
        slices.append((start_pos, end_pos))
        return (
         ('').join([ mem[start_pos:end_pos] for start_pos, end_pos in slices ]), 0, expected_stream_size)


def x_dump_line(alist, stride, f, dpos, equal=0):
    print('%5d%s' % (dpos, ' ='[equal]), end=' ', file=f)
    for value in alist[dpos:dpos + stride]:
        print(str(value), end=' ', file=f)

    print(file=f)


def dump_list(alist, stride, f=sys.stdout):

    def _dump_line(dpos, equal=0):
        print('%5d%s' % (dpos, ' ='[equal]), end=' ', file=f)
        for value in alist[dpos:dpos + stride]:
            print(str(value), end=' ', file=f)

        print(file=f)

    pos = None
    oldpos = None
    for pos in xrange(0, len(alist), stride):
        if oldpos is None:
            _dump_line(pos)
            oldpos = pos
        elif alist[pos:pos + stride] != alist[oldpos:oldpos + stride]:
            if pos - oldpos > stride:
                _dump_line(pos - stride, equal=1)
            _dump_line(pos)
            oldpos = pos

    if oldpos is not None and pos is not None and pos != oldpos:
        _dump_line(pos, equal=1)
    return