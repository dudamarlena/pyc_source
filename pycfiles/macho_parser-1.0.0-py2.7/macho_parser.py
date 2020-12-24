# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/macho_parser/macho_parser.py
# Compiled at: 2017-05-19 00:15:23
from collections import namedtuple
from struct import Struct
import mmap
mach_header = namedtuple('mach_header', 'magic cputype cpusubtype filetype ncmds sizeofcmds flags')
mach_header_struct = Struct('IiiIIII')
mh_magic = 4277009102
mh_cigam = 3472551422
mach_header_64 = namedtuple('mach_header_64', 'magic cputype cpusubtype filetype ncmds sizeofcmds flags reserved')
mach_header_64_struct = Struct('IiiIIIII')
mh_magic_64 = 4277009103
mh_cigam_64 = 3489328638
load_command = namedtuple('load_command', 'cmd cmdsize')
load_command_struct = Struct('II')
LC_SEGMENT = 1
LC_SEGMENT_64 = 25
segment_command = namedtuple('segment_command', 'cmd cmdsize segname vmaddr vmsize fileoff filesize maxprot initprot nsects flags')
segment_command_struct = Struct('II16sIIIIiiII')
segment_command_64 = namedtuple('segment_command_64', 'cmd cmdsize segname vmaddr vmsize fileoff filesize maxprot initprot nsects flags')
segment_command_64_struct = Struct('II16sQQQQiiII')
section = namedtuple('section', 'sectname segname addr size offset align reloff nreloc flags reserved1 reserved2')
section_struct = Struct('16s16sIIIIIIIII')
section_64 = namedtuple('section_64', 'sectname segname addr size offset align reloff nreloc flags reserved1 reserved2 reserved3')
section_64_struct = Struct('16s16sQQIIIIIIII')

class MachO(object):

    def __init__(self, filename):
        self._filename = filename
        self._rf = None
        self._mm = None
        return

    def __enter__(self):
        self._rf = open(self._filename, 'rb')
        self._mm = mmap.mmap(self._rf.fileno(), 0, mmap.MAP_PRIVATE, mmap.PROT_READ)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is not None:
            pass
        self._mm.close()
        self._rf.close()
        return

    def _get_header(self):
        """return a 3-tuple (begin_pos, end_pos, header)."""
        header = mach_header._make(mach_header_struct.unpack(self._mm[:mach_header_struct.size]))
        if header.magic == mh_magic_64 or header.magic == mh_cigam_64:
            return (0, mach_header_64_struct.size, mach_header_64._make(mach_header_64_struct.unpack(self._mm[:mach_header_64_struct.size])))
        else:
            return (
             0, mach_header_struct.size, header)

    def get_header(self):
        return self._get_header()[2]

    def _get_load_commands(self):
        """return a 3-tuple (begin_pos, end_pos, load_command)."""
        _, cur_pos, header = self._get_header()
        for i in xrange(header.ncmds):
            lc = load_command._make(load_command_struct.unpack(self._mm[cur_pos:cur_pos + load_command_struct.size]))
            yield (cur_pos, cur_pos + load_command_struct.size, lc)
            cur_pos += lc.cmdsize

    def get_load_commands(self):
        for _, _, lc in self._get_load_commands():
            yield lc

    def _get_segments(self):
        """return a 3-tuple (begin_pos, end_pos, segment)."""
        for pos, _, lc in self._get_load_commands():
            if lc.cmd == LC_SEGMENT_64:
                seg = segment_command_64._make(segment_command_64_struct.unpack(self._mm[pos:pos + segment_command_64_struct.size]))
                yield (pos, pos + segment_command_64_struct.size, seg)
            elif lc.cmd == LC_SEGMENT:
                seg = segment_command._make(segment_command_struct.unpack(self._mm[pos:pos + segment_command_struct.size]))
                yield (pos, pos + segment_command_struct.size, seg)

    def get_segments(self):
        for _, _, seg in self._get_segments():
            yield seg

    def _get_sections(self):
        """return a 3-tuple (begin_pos, end_pos, section)."""
        for pos, sect_pos, seg in self._get_segments():
            for i in xrange(seg.nsects):
                if seg.cmd == LC_SEGMENT_64:
                    sect = section_64._make(section_64_struct.unpack(self._mm[sect_pos:sect_pos + section_64_struct.size]))
                    yield (sect_pos, sect_pos + section_64_struct.size, sect)
                    sect_pos += section_64_struct.size
                else:
                    sect = section._make(section_struct.unpack(self._mm[sect_pos:sect_pos + section_struct.size]))
                    yield (sect_pos, sect_pos + section_struct.size, sect)
                    sect_pos += section_struct.size

    def get_sections(self):
        for _, _, sect in self._get_sections():
            yield sect

    def _get_data(self, offset, length):
        return self._mm[offset:offset + length]

    def get_section_data(self, segname, sectname):
        for sect in self.get_sections():
            if sect.segname.rstrip('\x00') == segname and sect.sectname.rstrip('\x00') == sectname:
                return self._get_data(sect.offset, sect.size).rstrip('\x00')

        return