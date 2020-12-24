# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/program/exe.py
# Compiled at: 2009-09-07 17:44:28
"""
Microsoft Windows Portable Executable (PE) file parser.

Informations:
- Microsoft Portable Executable and Common Object File Format Specification:
  http://www.microsoft.com/whdc/system/platform/firmware/PECOFF.mspx

Author: Victor Stinner
Creation date: 2006-08-13
"""
from hachoir_parser import HachoirParser
from hachoir_core.endian import LITTLE_ENDIAN
from hachoir_core.field import FieldSet, RootSeekableFieldSet, UInt16, UInt32, String, RawBytes, PaddingBytes
from hachoir_core.text_handler import textHandler, hexadecimal
from hachoir_parser.program.exe_ne import NE_Header
from hachoir_parser.program.exe_pe import PE_Header, PE_OptHeader, SectionHeader
from hachoir_parser.program.exe_res import PE_Resource, NE_VersionInfoNode
MAX_NB_SECTION = 50

class MSDosHeader(FieldSet):
    __module__ = __name__
    static_size = 64 * 8

    def createFields(self):
        yield String(self, 'header', 2, 'File header (MZ)', charset='ASCII')
        yield UInt16(self, 'size_mod_512', 'File size in bytes modulo 512')
        yield UInt16(self, 'size_div_512', 'File size in bytes divide by 512')
        yield UInt16(self, 'reloc_entries', 'Number of relocation entries')
        yield UInt16(self, 'code_offset', 'Offset to the code in the file (divided by 16)')
        yield UInt16(self, 'needed_memory', 'Memory needed to run (divided by 16)')
        yield UInt16(self, 'max_memory', 'Maximum memory needed to run (divided by 16)')
        yield textHandler(UInt32(self, 'init_ss_sp', 'Initial value of SP:SS registers'), hexadecimal)
        yield UInt16(self, 'checksum', 'Checksum')
        yield textHandler(UInt32(self, 'init_cs_ip', 'Initial value of CS:IP registers'), hexadecimal)
        yield UInt16(self, 'reloc_offset', 'Offset in file to relocation table')
        yield UInt16(self, 'overlay_number', 'Overlay number')
        yield PaddingBytes(self, 'reserved[]', 8, 'Reserved')
        yield UInt16(self, 'oem_id', 'OEM id')
        yield UInt16(self, 'oem_info', 'OEM info')
        yield PaddingBytes(self, 'reserved[]', 20, 'Reserved')
        yield UInt32(self, 'next_offset', 'Offset to next header (PE or NE)')

    def isValid(self):
        if 512 <= self['size_mod_512'].value:
            return "Invalid field 'size_mod_512' value"
        if self['code_offset'].value < 4:
            return 'Invalid code offset'
        looks_pe = self['size_div_512'].value < 4
        if looks_pe:
            if self['checksum'].value != 0:
                return 'Invalid value of checksum'
            if not 80 <= self['next_offset'].value <= 1024:
                return 'Invalid value of next_offset'
        return ''


class ExeFile(HachoirParser, RootSeekableFieldSet):
    __module__ = __name__
    PARSER_TAGS = {'id': 'exe', 'category': 'program', 'file_ext': ('exe', 'dll', 'ocx'), 'mime': ('application/x-dosexec', ), 'min_size': 64 * 8, 'magic_regex': (('MZ.[\x00\x01].{4}[^\x00\x01\x02\x03]', 0), ), 'description': 'Microsoft Windows Portable Executable'}
    endian = LITTLE_ENDIAN

    def __init__(self, stream, **args):
        RootSeekableFieldSet.__init__(self, None, 'root', stream, None, stream.askSize(self))
        HachoirParser.__init__(self, stream, **args)
        return

    def validate(self):
        if self.stream.readBytes(0, 2) != 'MZ':
            return 'Wrong header'
        err = self['msdos'].isValid()
        if err:
            return 'Invalid MSDOS header: ' + err
        if self.isPE():
            if MAX_NB_SECTION < self['pe_header/nb_section'].value:
                return 'Invalid number of section (%s)' % self['pe_header/nb_section'].value
        return True

    def createFields(self):
        yield MSDosHeader(self, 'msdos', 'MS-DOS program header')
        if self.isPE() or self.isNE():
            offset = self['msdos/next_offset'].value
            self.seekByte(offset, relative=False)
        if self.isPE():
            for field in self.parsePortableExecutable():
                yield field

        elif self.isNE():
            for field in self.parseNE_Executable():
                yield field

        else:
            offset = self['msdos/code_offset'].value * 16
            self.seekByte(offset, relative=False)

    def parseNE_Executable(self):
        yield NE_Header(self, 'ne_header')
        start = self.current_size
        addr = self.stream.searchBytes('VS_VERSION_INFO', start)
        if addr:
            self.seekBit(addr - 32)
            yield NE_VersionInfoNode(self, 'info')

    def parsePortableExecutable(self):
        yield PE_Header(self, 'pe_header')
        size = self['pe_header/opt_hdr_size'].value
        rsrc_rva = None
        if size:
            yield PE_OptHeader(self, 'pe_opt_header', size=size * 8)
            if 'pe_opt_header/resource/rva' in self:
                rsrc_rva = self['pe_opt_header/resource/rva'].value
        sections = []
        for index in xrange(self['pe_header/nb_section'].value):
            section = SectionHeader(self, 'section_hdr[]')
            yield section
            if section['phys_size'].value:
                sections.append(section)

        sections.sort(key=lambda field: field['phys_off'].value)
        for section in sections:
            self.seekByte(section['phys_off'].value)
            size = section['phys_size'].value
            if size:
                name = section.createSectionName()
                if rsrc_rva is not None and section['rva'].value == rsrc_rva:
                    yield PE_Resource(self, name, section, size=size * 8)
                else:
                    yield RawBytes(self, name, size)

        return

    def isPE(self):
        if not hasattr(self, '_is_pe'):
            self._is_pe = False
            offset = self['msdos/next_offset'].value * 8
            if 2 * 8 <= offset and offset + PE_Header.static_size <= self.size and self.stream.readBytes(offset, 4) == 'PE\x00\x00':
                self._is_pe = True
        return self._is_pe

    def isNE(self):
        if not hasattr(self, '_is_ne'):
            self._is_ne = False
            offset = self['msdos/next_offset'].value * 8
            if 64 * 8 <= offset and offset + NE_Header.static_size <= self.size and self.stream.readBytes(offset, 2) == 'NE':
                self._is_ne = True
        return self._is_ne

    def getResource(self):
        if not self.isPE():
            return
        if 'pe_opt_header/resource/size' in self:
            if not self['pe_opt_header/resource/size'].value:
                return
        if 'section_rsrc' in self:
            return self['section_rsrc']
        return

    def createDescription(self):
        if self.isPE():
            if self['pe_header/is_dll'].value:
                text = 'Microsoft Windows DLL'
            else:
                text = 'Microsoft Windows Portable Executable'
            info = [
             self['pe_header/cpu'].display]
            if 'pe_opt_header' in self:
                hdr = self['pe_opt_header']
                info.append(hdr['subsystem'].display)
            if self['pe_header/is_stripped'].value:
                info.append('stripped')
            return '%s: %s' % (text, (', ').join(info))
        elif self.isNE():
            return 'New-style Executable (NE) for Microsoft MS Windows 3.x'
        else:
            return 'MS-DOS executable'

    def createContentSize(self):
        if self.isPE():
            size = 0
            for index in xrange(self['pe_header/nb_section'].value):
                section = self[('section_hdr[%u]' % index)]
                section_size = section['phys_size'].value
                if not section_size:
                    continue
                section_size = (section_size + section['phys_off'].value) * 8
                if size:
                    size = max(size, section_size)
                else:
                    size = section_size

            if size:
                return size
            else:
                return
        elif self.isNE():
            return
        else:
            size = self['msdos/size_mod_512'].value + (self['msdos/size_div_512'].value - 1) * 512
            if size < 0:
                return
        return size * 8