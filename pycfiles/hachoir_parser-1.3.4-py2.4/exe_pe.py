# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/program/exe_pe.py
# Compiled at: 2009-09-07 17:44:28
from hachoir_core.field import FieldSet, ParserError, Bit, UInt8, UInt16, UInt32, TimestampUnix32, Bytes, String, Enum, PaddingBytes, PaddingBits, NullBytes, NullBits
from hachoir_core.text_handler import textHandler, hexadecimal, filesizeHandler
from hachoir_core.error import HACHOIR_ERRORS

class SectionHeader(FieldSet):
    __module__ = __name__
    static_size = 40 * 8

    def createFields(self):
        yield String(self, 'name', 8, charset='ASCII', strip='\x00 ')
        yield filesizeHandler(UInt32(self, 'mem_size', 'Size in memory'))
        yield textHandler(UInt32(self, 'rva', 'RVA (location) in memory'), hexadecimal)
        yield filesizeHandler(UInt32(self, 'phys_size', 'Physical size (on disk)'))
        yield filesizeHandler(UInt32(self, 'phys_off', 'Physical location (on disk)'))
        yield PaddingBytes(self, 'reserved', 12)
        yield NullBits(self, 'reserved[]', 4)
        yield NullBits(self, 'reserved[]', 1)
        yield Bit(self, 'has_code', 'Contains code')
        yield Bit(self, 'has_init_data', 'Contains initialized data')
        yield Bit(self, 'has_uninit_data', 'Contains uninitialized data')
        yield NullBits(self, 'reserved[]', 1)
        yield Bit(self, 'has_comment', 'Contains comments?')
        yield NullBits(self, 'reserved[]', 1)
        yield Bit(self, 'remove', 'Contents will not become part of image')
        yield Bit(self, 'has_comdata', 'Contains comdat?')
        yield NullBits(self, 'reserved[]', 1)
        yield Bit(self, 'no_defer_spec_exc', 'Reset speculative exceptions handling bits in the TLB entries')
        yield Bit(self, 'gp_rel', 'Content can be accessed relative to GP')
        yield NullBits(self, 'reserved[]', 4)
        yield NullBits(self, 'reserved[]', 4)
        yield Bit(self, 'ext_reloc', 'Contains extended relocations?')
        yield Bit(self, 'discarded', 'Can be discarded?')
        yield Bit(self, 'is_not_cached', 'Is not cachable?')
        yield Bit(self, 'is_not_paged', 'Is not pageable?')
        yield Bit(self, 'is_shareable', 'Is shareable?')
        yield Bit(self, 'is_executable', 'Is executable?')
        yield Bit(self, 'is_readable', 'Is readable?')
        yield Bit(self, 'is_writable', 'Is writable?')

    def rva2file(self, rva):
        return self['phys_off'].value + (rva - self['rva'].value)

    def createDescription(self):
        rva = self['rva'].value
        size = self['mem_size'].value
        info = ['rva=0x%08x..0x%08x' % (rva, rva + size), 'size=%s' % self['mem_size'].display]
        if self['is_executable'].value:
            info.append('exec')
        if self['is_readable'].value:
            info.append('read')
        if self['is_writable'].value:
            info.append('write')
        return 'Section "%s": %s' % (self['name'].value, (', ').join(info))

    def createSectionName(self):
        try:
            name = str(self['name'].value.strip('.'))
            if name:
                return 'section_%s' % name
        except HACHOIR_ERRORS, err:
            self.warning(unicode(err))
            return 'section[]'


class DataDirectory(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield textHandler(UInt32(self, 'rva', 'Virtual address'), hexadecimal)
        yield filesizeHandler(UInt32(self, 'size'))

    def createDescription(self):
        if self['size'].value:
            return 'Directory at %s (%s)' % (self['rva'].display, self['size'].display)
        else:
            return '(empty directory)'


class PE_Header(FieldSet):
    __module__ = __name__
    static_size = 24 * 8
    cpu_name = {388: 'Alpha AXP', 448: 'ARM', 332: 'Intel 80386', 333: 'Intel 80486', 334: 'Intel Pentium', 512: 'Intel IA64', 616: 'Motorola 68000', 614: 'MIPS', 644: 'Alpha AXP 64 bits', 870: 'MIPS with FPU', 1126: 'MIPS16 with FPU', 496: 'PowerPC little endian', 354: 'R3000', 358: 'MIPS little endian (R4000)', 360: 'R10000', 418: 'Hitachi SH3', 422: 'Hitachi SH4', 352: 'R3000 (MIPS), big endian', 354: 'R3000 (MIPS), little endian', 358: 'R4000 (MIPS), little endian', 360: 'R10000 (MIPS), little endian', 388: 'DEC Alpha AXP', 496: 'IBM Power PC, little endian'}

    def createFields(self):
        yield Bytes(self, 'header', 4, 'PE header signature (PE\\0\\0)')
        if self['header'].value != 'PE\x00\x00':
            raise ParserError('Invalid PE header signature')
        yield Enum(UInt16(self, 'cpu', 'CPU type'), self.cpu_name)
        yield UInt16(self, 'nb_section', 'Number of sections')
        yield TimestampUnix32(self, 'creation_date', 'Creation date')
        yield UInt32(self, 'ptr_to_sym', 'Pointer to symbol table')
        yield UInt32(self, 'nb_symbols', 'Number of symbols')
        yield UInt16(self, 'opt_hdr_size', 'Optional header size')
        yield Bit(self, 'reloc_stripped', "If true, don't contain base relocations.")
        yield Bit(self, 'exec_image', 'Executable image?')
        yield Bit(self, 'line_nb_stripped', 'COFF line numbers stripped?')
        yield Bit(self, 'local_sym_stripped', 'COFF symbol table entries stripped?')
        yield Bit(self, 'aggr_ws', 'Aggressively trim working set')
        yield Bit(self, 'large_addr', 'Application can handle addresses greater than 2 GB')
        yield NullBits(self, 'reserved', 1)
        yield Bit(self, 'reverse_lo', 'Little endian: LSB precedes MSB in memory')
        yield Bit(self, '32bit', 'Machine based on 32-bit-word architecture')
        yield Bit(self, 'is_stripped', 'Debugging information removed?')
        yield Bit(self, 'swap', 'If image is on removable media, copy and run from swap file')
        yield PaddingBits(self, 'reserved2', 1)
        yield Bit(self, 'is_system', "It's a system file")
        yield Bit(self, 'is_dll', "It's a dynamic-link library (DLL)")
        yield Bit(self, 'up', 'File should be run only on a UP machine')
        yield Bit(self, 'reverse_hi', 'Big endian: MSB precedes LSB in memory')


class PE_OptHeader(FieldSet):
    __module__ = __name__
    SUBSYSTEM_NAME = {1: 'Native', 2: 'Windows GUI', 3: 'Windows CUI', 5: 'OS/2 CUI', 7: 'POSIX CUI', 8: 'Native Windows', 9: 'Windows CE GUI', 10: 'EFI application', 11: 'EFI boot service driver', 12: 'EFI runtime driver', 13: 'EFI ROM', 14: 'XBOX', 16: 'Windows boot application'}
    DIRECTORY_NAME = {0: 'export', 1: 'import', 2: 'resource', 3: 'exception', 4: 'certificate', 5: 'relocation', 6: 'debug', 7: 'description', 8: 'global_ptr', 9: 'tls', 10: 'load_config', 11: 'bound_import', 12: 'import_address'}

    def createFields(self):
        yield UInt16(self, 'signature', 'PE optional header signature (0x010b)')
        if self['signature'].value != 267:
            raise ParserError('Invalid PE optional header signature')
        yield UInt8(self, 'maj_lnk_ver', 'Major linker version')
        yield UInt8(self, 'min_lnk_ver', 'Minor linker version')
        yield filesizeHandler(UInt32(self, 'size_code', 'Size of code'))
        yield filesizeHandler(UInt32(self, 'size_init_data', 'Size of initialized data'))
        yield filesizeHandler(UInt32(self, 'size_uninit_data', 'Size of uninitialized data'))
        yield textHandler(UInt32(self, 'entry_point', 'Address (RVA) of the code entry point'), hexadecimal)
        yield textHandler(UInt32(self, 'base_code', 'Base (RVA) of code'), hexadecimal)
        yield textHandler(UInt32(self, 'base_data', 'Base (RVA) of data'), hexadecimal)
        yield textHandler(UInt32(self, 'image_base', 'Image base (RVA)'), hexadecimal)
        yield filesizeHandler(UInt32(self, 'sect_align', 'Section alignment'))
        yield filesizeHandler(UInt32(self, 'file_align', 'File alignment'))
        yield UInt16(self, 'maj_os_ver', 'Major OS version')
        yield UInt16(self, 'min_os_ver', 'Minor OS version')
        yield UInt16(self, 'maj_img_ver', 'Major image version')
        yield UInt16(self, 'min_img_ver', 'Minor image version')
        yield UInt16(self, 'maj_subsys_ver', 'Major subsystem version')
        yield UInt16(self, 'min_subsys_ver', 'Minor subsystem version')
        yield NullBytes(self, 'reserved', 4)
        yield filesizeHandler(UInt32(self, 'size_img', 'Size of image'))
        yield filesizeHandler(UInt32(self, 'size_hdr', 'Size of headers'))
        yield textHandler(UInt32(self, 'checksum'), hexadecimal)
        yield Enum(UInt16(self, 'subsystem'), self.SUBSYSTEM_NAME)
        yield UInt16(self, 'dll_flags')
        yield filesizeHandler(UInt32(self, 'size_stack_reserve'))
        yield filesizeHandler(UInt32(self, 'size_stack_commit'))
        yield filesizeHandler(UInt32(self, 'size_heap_reserve'))
        yield filesizeHandler(UInt32(self, 'size_heap_commit'))
        yield UInt32(self, 'loader_flags')
        yield UInt32(self, 'nb_directory', 'Number of RVA and sizes')
        for index in xrange(self['nb_directory'].value):
            try:
                name = self.DIRECTORY_NAME[index]
            except KeyError:
                name = 'data_dir[%u]' % index

            yield DataDirectory(self, name)

    def createDescription(self):
        return 'PE optional header: %s, entry point %s' % (self['subsystem'].display, self['entry_point'].display)