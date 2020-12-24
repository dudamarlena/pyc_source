# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/lib/pyExcelerator/CompoundDoc.py
# Compiled at: 2008-03-17 12:58:02
import sys, struct
__rev_id__ = '$Id: CompoundDoc.py,v 1.7 2005/10/26 07:44:24 rvk Exp $'

class Reader:

    def __init__(self, filename, dump=False):
        self.dump = dump
        self.STREAMS = {}
        doc = file(filename, 'rb').read()
        self.header, self.data = doc[0:512], doc[512:]
        del doc
        self.__build_header()
        self.__build_MSAT()
        self.__build_SAT()
        self.__build_directory()
        self.__build_short_sectors_data()
        if len(self.short_sectors_data) > 0:
            self.__build_SSAT()
        else:
            if self.dump and (self.total_ssat_sectors != 0 or self.ssat_start_sid != -2):
                print 'NOTE: header says that must be', self.total_ssat_sectors, 'short sectors'
                print 'NOTE: starting at', self.ssat_start_sid, 'sector'
                print 'NOTE: but file does not contains data in short sectors'
            self.ssat_start_sid = -2
            self.total_ssat_sectors = 0
            self.SSAT = [-2]
        for dentry in self.dir_entry_list[1:]:
            (did, sz, name, t, c, did_left, did_right, did_root, dentry_start_sid, stream_size) = dentry
            stream_data = ''
            if stream_size > 0:
                if stream_size >= self.min_stream_size:
                    args = (
                     self.data, self.SAT, dentry_start_sid, self.sect_size)
                else:
                    args = (
                     self.short_sectors_data, self.SSAT, dentry_start_sid, self.short_sect_size)
                stream_data = self.get_stream_data(*args)
            if name != '':
                self.STREAMS[name] = stream_data

    def __build_header(self):
        self.doc_magic = self.header[0:8]
        if self.doc_magic != b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1':
            raise Exception, 'Not an OLE file.'
        self.file_uid = self.header[8:24]
        self.rev_num = self.header[24:26]
        self.ver_num = self.header[26:28]
        self.byte_order = self.header[28:30]
        (self.log2_sect_size,) = struct.unpack('<H', self.header[30:32])
        (self.log2_short_sect_size,) = struct.unpack('<H', self.header[32:34])
        (self.total_sat_sectors,) = struct.unpack('<L', self.header[44:48])
        (self.dir_start_sid,) = struct.unpack('<l', self.header[48:52])
        (self.min_stream_size,) = struct.unpack('<L', self.header[56:60])
        (self.ssat_start_sid,) = struct.unpack('<l', self.header[60:64])
        (self.total_ssat_sectors,) = struct.unpack('<L', self.header[64:68])
        (self.msat_start_sid,) = struct.unpack('<l', self.header[68:72])
        (self.total_msat_sectors,) = struct.unpack('<L', self.header[72:76])
        self.sect_size = 1 << self.log2_sect_size
        self.short_sect_size = 1 << self.log2_short_sect_size
        if self.dump:
            print 'file magic: '
            print_bin_data(self.doc_magic)
            print 'file uid: '
            print_bin_data(self.file_uid)
            print 'revision number: '
            print_bin_data(self.rev_num)
            print 'version number: '
            print_bin_data(self.ver_num)
            print 'byte order: '
            print_bin_data(self.byte_order)
            print 'sector size                                :', hex(self.sect_size), self.sect_size
            print 'short sector size                          :', hex(self.short_sect_size), self.short_sect_size
            print 'Total number of sectors used for the SAT   :', hex(self.total_sat_sectors), self.total_sat_sectors
            print 'SID of first sector of the directory stream:', hex(self.dir_start_sid), self.dir_start_sid
            print 'Minimum size of a standard stream          :', hex(self.min_stream_size), self.min_stream_size
            print 'SID of first sector of the SSAT            :', hex(self.ssat_start_sid), self.ssat_start_sid
            print 'Total number of sectors used for the SSAT  :', hex(self.total_ssat_sectors), self.total_ssat_sectors
            print 'SID of first additional sector of the MSAT :', hex(self.msat_start_sid), self.msat_start_sid
            print 'Total number of sectors used for the MSAT  :', hex(self.total_msat_sectors), self.total_msat_sectors

    def __build_MSAT(self):
        self.MSAT = list(struct.unpack('<109l', self.header[76:]))
        next = self.msat_start_sid
        while next > 0:
            msat_sector = struct.unpack('<128l', self.data[next * self.sect_size:(next + 1) * self.sect_size])
            self.MSAT.extend(msat_sector[:127])
            next = msat_sector[(-1)]

        if self.dump:
            print 'MSAT (header part): \n', self.MSAT[:109]
            print 'additional MSAT sectors: \n', self.MSAT[109:]

    def __build_SAT(self):
        sat_stream = ('').join([ self.data[i * self.sect_size:(i + 1) * self.sect_size] for i in self.MSAT if i >= 0 ])
        sat_sids_count = len(sat_stream) >> 2
        self.SAT = struct.unpack('<%dl' % sat_sids_count, sat_stream)
        if self.dump:
            print 'SAT sid count:\n', sat_sids_count
            print 'SAT content:\n', self.SAT

    def __build_SSAT(self):
        ssat_stream = self.get_stream_data(self.data, self.SAT, self.ssat_start_sid, self.sect_size)
        ssids_count = len(ssat_stream) >> 2
        self.SSAT = struct.unpack('<%dl' % ssids_count, ssat_stream)
        if self.dump:
            print 'SSID count:', ssids_count
            print 'SSAT content:\n', self.SSAT

    def __build_directory(self):
        dir_stream = self.get_stream_data(self.data, self.SAT, self.dir_start_sid, self.sect_size)
        self.dir_entry_list = []
        i = 0
        while i < len(dir_stream):
            dentry = dir_stream[i:i + 128]
            i += 128
            did = len(self.dir_entry_list)
            (sz,) = struct.unpack('<H', dentry[64:66])
            if sz > 0:
                name = dentry[0:sz - 2].decode('utf_16_le', 'replace')
            else:
                name = ''
            (t,) = struct.unpack('B', dentry[66])
            (c,) = struct.unpack('B', dentry[67])
            (did_left,) = struct.unpack('<l', dentry[68:72])
            (did_right,) = struct.unpack('<l', dentry[72:76])
            (did_root,) = struct.unpack('<l', dentry[76:80])
            (dentry_start_sid,) = struct.unpack('<l', dentry[116:120])
            (stream_size,) = struct.unpack('<L', dentry[120:124])
            self.dir_entry_list.extend([
             (did, sz, name, t, c,
              did_left, did_right, did_root,
              dentry_start_sid, stream_size)])

        if self.dump:
            dentry_types = {0: 'Empty', 1: 'User storage', 
               2: 'User stream', 
               3: 'LockBytes', 
               4: 'Property', 
               5: 'Root storage'}
            node_colours = {0: 'Red', 
               1: 'Black'}
            print 'total directory entries:', len(self.dir_entry_list)
            for dentry in self.dir_entry_list:
                (did, sz, name, t, c, did_left, did_right, did_root, dentry_start_sid, stream_size) = dentry
                print 'DID', did
                print 'Size of the used area of the character buffer of the name:', sz
                print 'dir entry name:', repr(name)
                print 'type of entry:', t, dentry_types[t]
                print 'entry colour:', c, node_colours[c]
                print 'left child DID :', did_left
                print 'right child DID:', did_right
                print 'root DID       :', did_root
                print 'start SID       :', dentry_start_sid
                print 'stream size     :', stream_size
                if stream_size == 0:
                    print 'stream is empty'
                elif stream_size >= self.min_stream_size:
                    print 'stream stored as normal stream'
                else:
                    print 'stream stored as short-stream'

    def __build_short_sectors_data(self):
        (did, sz, name, t, c, did_left, did_right, did_root, dentry_start_sid, stream_size) = self.dir_entry_list[0]
        assert t == 5
        if stream_size == 0:
            self.short_sectors_data = ''
        else:
            self.short_sectors_data = self.get_stream_data(self.data, self.SAT, dentry_start_sid, self.sect_size)

    def get_stream_data(self, data, SAT, start_sid, sect_size):
        sid = start_sid
        chunks = [(sid, sid)]
        stream_data = ''
        while SAT[sid] >= 0:
            next_in_chain = SAT[sid]
            (last_chunk_start, last_chunk_finish) = chunks[(-1)]
            if next_in_chain - last_chunk_finish <= 1:
                chunks[-1] = (
                 last_chunk_start, next_in_chain)
            else:
                chunks.extend([(next_in_chain, next_in_chain)])
            sid = next_in_chain

        for (s, f) in chunks:
            stream_data += data[s * sect_size:(f + 1) * sect_size]

        return stream_data


def print_bin_data(data):
    i = 0
    while i < len(data):
        j = 0
        while i < len(data) and j < 16:
            c = '0x%02X' % ord(data[i])
            sys.stdout.write(c)
            sys.stdout.write(' ')
            i += 1
            j += 1

        print

    if i == 0:
        print '<NO DATA>'


class XlsDoc:
    SECTOR_SIZE = 512
    MIN_LIMIT = 4096
    SID_FREE_SECTOR = -1
    SID_END_OF_CHAIN = -2
    SID_USED_BY_SAT = -3
    SID_USED_BY_MSAT = -4

    def __init__(self):
        self.book_stream_sect = []
        self.dir_stream = ''
        self.dir_stream_sect = []
        self.packed_SAT = ''
        self.SAT_sect = []
        self.packed_MSAT_1st = ''
        self.packed_MSAT_2nd = ''
        self.MSAT_sect_2nd = []
        self.header = ''

    def __build_directory(self):
        self.dir_stream = ''
        dentry_name = ('\x00').join('Root Entry\x00') + '\x00'
        dentry_name_sz = len(dentry_name)
        dentry_name_pad = '\x00' * (64 - dentry_name_sz)
        dentry_type = 5
        dentry_colour = 1
        dentry_did_left = -1
        dentry_did_right = -1
        dentry_did_root = 1
        dentry_start_sid = -2
        dentry_stream_sz = 0
        self.dir_stream += struct.pack('<64s H 2B 3l 9L l L L', dentry_name + dentry_name_pad, dentry_name_sz, dentry_type, dentry_colour, dentry_did_left, dentry_did_right, dentry_did_root, 0, 0, 0, 0, 0, 0, 0, 0, 0, dentry_start_sid, dentry_stream_sz, 0)
        dentry_name = ('\x00').join('Workbook\x00') + '\x00'
        dentry_name_sz = len(dentry_name)
        dentry_name_pad = '\x00' * (64 - dentry_name_sz)
        dentry_type = 2
        dentry_colour = 1
        dentry_did_left = -1
        dentry_did_right = -1
        dentry_did_root = -1
        dentry_start_sid = 0
        dentry_stream_sz = self.book_stream_len
        self.dir_stream += struct.pack('<64s H 2B 3l 9L l L L', dentry_name + dentry_name_pad, dentry_name_sz, dentry_type, dentry_colour, dentry_did_left, dentry_did_right, dentry_did_root, 0, 0, 0, 0, 0, 0, 0, 0, 0, dentry_start_sid, dentry_stream_sz, 0)
        dentry_name = ''
        dentry_name_sz = len(dentry_name)
        dentry_name_pad = '\x00' * (64 - dentry_name_sz)
        dentry_type = 0
        dentry_colour = 1
        dentry_did_left = -1
        dentry_did_right = -1
        dentry_did_root = -1
        dentry_start_sid = -2
        dentry_stream_sz = 0
        self.dir_stream += struct.pack('<64s H 2B 3l 9L l L L', dentry_name + dentry_name_pad, dentry_name_sz, dentry_type, dentry_colour, dentry_did_left, dentry_did_right, dentry_did_root, 0, 0, 0, 0, 0, 0, 0, 0, 0, dentry_start_sid, dentry_stream_sz, 0) * 2

    def __build_sat(self):
        book_sect_count = self.book_stream_len >> 9
        dir_sect_count = len(self.dir_stream) >> 9
        total_sect_count = book_sect_count + dir_sect_count
        SAT_sect_count = 0
        MSAT_sect_count = 0
        SAT_sect_count_limit = 109
        while total_sect_count > 128 * SAT_sect_count or SAT_sect_count > SAT_sect_count_limit:
            SAT_sect_count += 1
            total_sect_count += 1
            if SAT_sect_count > SAT_sect_count_limit:
                MSAT_sect_count += 1
                total_sect_count += 1
                SAT_sect_count_limit += 127

        SAT = [self.SID_FREE_SECTOR] * 128 * SAT_sect_count
        sect = 0
        while sect < book_sect_count - 1:
            self.book_stream_sect.append(sect)
            SAT[sect] = sect + 1
            sect += 1

        self.book_stream_sect.append(sect)
        SAT[sect] = self.SID_END_OF_CHAIN
        sect += 1
        while sect < book_sect_count + MSAT_sect_count:
            self.MSAT_sect_2nd.append(sect)
            SAT[sect] = self.SID_USED_BY_MSAT
            sect += 1

        while sect < book_sect_count + MSAT_sect_count + SAT_sect_count:
            self.SAT_sect.append(sect)
            SAT[sect] = self.SID_USED_BY_SAT
            sect += 1

        while sect < book_sect_count + MSAT_sect_count + SAT_sect_count + dir_sect_count - 1:
            self.dir_stream_sect.append(sect)
            SAT[sect] = sect + 1
            sect += 1

        self.dir_stream_sect.append(sect)
        SAT[sect] = self.SID_END_OF_CHAIN
        sect += 1
        self.packed_SAT = struct.pack(('<%dl' % (SAT_sect_count * 128)), *SAT)
        MSAT_1st = [
         self.SID_FREE_SECTOR] * 109
        for (i, SAT_sect_num) in zip(range(0, 109), self.SAT_sect):
            MSAT_1st[i] = SAT_sect_num

        self.packed_MSAT_1st = struct.pack('<109l', *MSAT_1st)
        MSAT_2nd = [
         self.SID_FREE_SECTOR] * 128 * MSAT_sect_count
        if MSAT_sect_count > 0:
            MSAT_2nd[-1] = self.SID_END_OF_CHAIN
        i = 109
        msat_sect = 0
        sid_num = 0
        while i < SAT_sect_count:
            if (sid_num + 1) % 128 == 0:
                msat_sect += 1
                if msat_sect < len(self.MSAT_sect_2nd):
                    MSAT_2nd[sid_num] = self.MSAT_sect_2nd[msat_sect]
            else:
                MSAT_2nd[sid_num] = self.SAT_sect[i]
                i += 1
            sid_num += 1

        self.packed_MSAT_2nd = struct.pack(('<%dl' % (MSAT_sect_count * 128)), *MSAT_2nd)

    def __build_header(self):
        doc_magic = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
        file_uid = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        rev_num = '>\x00'
        ver_num = '\x03\x00'
        byte_order = b'\xfe\xff'
        log_sect_size = struct.pack('<H', 9)
        log_short_sect_size = struct.pack('<H', 6)
        not_used0 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        total_sat_sectors = struct.pack('<L', len(self.SAT_sect))
        dir_start_sid = struct.pack('<l', self.dir_stream_sect[0])
        not_used1 = '\x00\x00\x00\x00'
        min_stream_size = struct.pack('<L', 4096)
        ssat_start_sid = struct.pack('<l', -2)
        total_ssat_sectors = struct.pack('<L', 0)
        if len(self.MSAT_sect_2nd) == 0:
            msat_start_sid = struct.pack('<l', -2)
        else:
            msat_start_sid = struct.pack('<l', self.MSAT_sect_2nd[0])
        total_msat_sectors = struct.pack('<L', len(self.MSAT_sect_2nd))
        self.header = ('').join([doc_magic,
         file_uid,
         rev_num,
         ver_num,
         byte_order,
         log_sect_size,
         log_short_sect_size,
         not_used0,
         total_sat_sectors,
         dir_start_sid,
         not_used1,
         min_stream_size,
         ssat_start_sid,
         total_ssat_sectors,
         msat_start_sid,
         total_msat_sectors])

    def save(self, filename, stream):
        padding = '\x00' * (4096 - len(stream) % 4096)
        self.book_stream_len = len(stream) + len(padding)
        self.__build_directory()
        self.__build_sat()
        self.__build_header()
        f = file(filename, 'wb')
        f.write(self.header)
        f.write(self.packed_MSAT_1st)
        f.write(stream)
        f.write(padding)
        f.write(self.packed_MSAT_2nd)
        f.write(self.packed_SAT)
        f.write(self.dir_stream)
        f.close()


if __name__ == '__main__':
    d = XlsDoc()
    d.save('a.aaa', 'b' * 17000)