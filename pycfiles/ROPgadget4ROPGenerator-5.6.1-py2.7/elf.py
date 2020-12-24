# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ropgadget/loaders/elf.py
# Compiled at: 2018-03-17 16:59:29
from capstone import *
from ctypes import *
from struct import unpack

class ELFFlags(object):
    ELFCLASS32 = 1
    ELFCLASS64 = 2
    EI_CLASS = 4
    EI_DATA = 5
    ELFDATA2LSB = 1
    ELFDATA2MSB = 2
    EM_386 = 3
    EM_X86_64 = 62
    EM_ARM = 40
    EM_MIPS = 8
    EM_SPARCv8p = 18
    EM_PowerPC = 20
    EM_ARM64 = 183


class Elf32_Ehdr_LSB(LittleEndianStructure):
    _fields_ = [
     (
      'e_ident', c_ubyte * 16),
     (
      'e_type', c_ushort),
     (
      'e_machine', c_ushort),
     (
      'e_version', c_uint),
     (
      'e_entry', c_uint),
     (
      'e_phoff', c_uint),
     (
      'e_shoff', c_uint),
     (
      'e_flags', c_uint),
     (
      'e_ehsize', c_ushort),
     (
      'e_phentsize', c_ushort),
     (
      'e_phnum', c_ushort),
     (
      'e_shentsize', c_ushort),
     (
      'e_shnum', c_ushort),
     (
      'e_shstrndx', c_ushort)]


class Elf64_Ehdr_LSB(LittleEndianStructure):
    _fields_ = [
     (
      'e_ident', c_ubyte * 16),
     (
      'e_type', c_ushort),
     (
      'e_machine', c_ushort),
     (
      'e_version', c_uint),
     (
      'e_entry', c_ulonglong),
     (
      'e_phoff', c_ulonglong),
     (
      'e_shoff', c_ulonglong),
     (
      'e_flags', c_uint),
     (
      'e_ehsize', c_ushort),
     (
      'e_phentsize', c_ushort),
     (
      'e_phnum', c_ushort),
     (
      'e_shentsize', c_ushort),
     (
      'e_shnum', c_ushort),
     (
      'e_shstrndx', c_ushort)]


class Elf32_Phdr_LSB(LittleEndianStructure):
    _fields_ = [
     (
      'p_type', c_uint),
     (
      'p_offset', c_uint),
     (
      'p_vaddr', c_uint),
     (
      'p_paddr', c_uint),
     (
      'p_filesz', c_uint),
     (
      'p_memsz', c_uint),
     (
      'p_flags', c_uint),
     (
      'p_align', c_uint)]


class Elf64_Phdr_LSB(LittleEndianStructure):
    _fields_ = [
     (
      'p_type', c_uint),
     (
      'p_flags', c_uint),
     (
      'p_offset', c_ulonglong),
     (
      'p_vaddr', c_ulonglong),
     (
      'p_paddr', c_ulonglong),
     (
      'p_filesz', c_ulonglong),
     (
      'p_memsz', c_ulonglong),
     (
      'p_align', c_ulonglong)]


class Elf32_Shdr_LSB(LittleEndianStructure):
    _fields_ = [
     (
      'sh_name', c_uint),
     (
      'sh_type', c_uint),
     (
      'sh_flags', c_uint),
     (
      'sh_addr', c_uint),
     (
      'sh_offset', c_uint),
     (
      'sh_size', c_uint),
     (
      'sh_link', c_uint),
     (
      'sh_info', c_uint),
     (
      'sh_addralign', c_uint),
     (
      'sh_entsize', c_uint)]


class Elf64_Shdr_LSB(LittleEndianStructure):
    _fields_ = [
     (
      'sh_name', c_uint),
     (
      'sh_type', c_uint),
     (
      'sh_flags', c_ulonglong),
     (
      'sh_addr', c_ulonglong),
     (
      'sh_offset', c_ulonglong),
     (
      'sh_size', c_ulonglong),
     (
      'sh_link', c_uint),
     (
      'sh_info', c_uint),
     (
      'sh_addralign', c_ulonglong),
     (
      'sh_entsize', c_ulonglong)]


class Elf32_Ehdr_MSB(BigEndianStructure):
    _fields_ = [
     (
      'e_ident', c_ubyte * 16),
     (
      'e_type', c_ushort),
     (
      'e_machine', c_ushort),
     (
      'e_version', c_uint),
     (
      'e_entry', c_uint),
     (
      'e_phoff', c_uint),
     (
      'e_shoff', c_uint),
     (
      'e_flags', c_uint),
     (
      'e_ehsize', c_ushort),
     (
      'e_phentsize', c_ushort),
     (
      'e_phnum', c_ushort),
     (
      'e_shentsize', c_ushort),
     (
      'e_shnum', c_ushort),
     (
      'e_shstrndx', c_ushort)]


class Elf64_Ehdr_MSB(BigEndianStructure):
    _fields_ = [
     (
      'e_ident', c_ubyte * 16),
     (
      'e_type', c_ushort),
     (
      'e_machine', c_ushort),
     (
      'e_version', c_uint),
     (
      'e_entry', c_ulonglong),
     (
      'e_phoff', c_ulonglong),
     (
      'e_shoff', c_ulonglong),
     (
      'e_flags', c_uint),
     (
      'e_ehsize', c_ushort),
     (
      'e_phentsize', c_ushort),
     (
      'e_phnum', c_ushort),
     (
      'e_shentsize', c_ushort),
     (
      'e_shnum', c_ushort),
     (
      'e_shstrndx', c_ushort)]


class Elf32_Phdr_MSB(BigEndianStructure):
    _fields_ = [
     (
      'p_type', c_uint),
     (
      'p_offset', c_uint),
     (
      'p_vaddr', c_uint),
     (
      'p_paddr', c_uint),
     (
      'p_filesz', c_uint),
     (
      'p_memsz', c_uint),
     (
      'p_flags', c_uint),
     (
      'p_align', c_uint)]


class Elf64_Phdr_MSB(BigEndianStructure):
    _fields_ = [
     (
      'p_type', c_uint),
     (
      'p_flags', c_uint),
     (
      'p_offset', c_ulonglong),
     (
      'p_vaddr', c_ulonglong),
     (
      'p_paddr', c_ulonglong),
     (
      'p_filesz', c_ulonglong),
     (
      'p_memsz', c_ulonglong),
     (
      'p_align', c_ulonglong)]


class Elf32_Shdr_MSB(BigEndianStructure):
    _fields_ = [
     (
      'sh_name', c_uint),
     (
      'sh_type', c_uint),
     (
      'sh_flags', c_uint),
     (
      'sh_addr', c_uint),
     (
      'sh_offset', c_uint),
     (
      'sh_size', c_uint),
     (
      'sh_link', c_uint),
     (
      'sh_info', c_uint),
     (
      'sh_addralign', c_uint),
     (
      'sh_entsize', c_uint)]


class Elf64_Shdr_MSB(BigEndianStructure):
    _fields_ = [
     (
      'sh_name', c_uint),
     (
      'sh_type', c_uint),
     (
      'sh_flags', c_ulonglong),
     (
      'sh_addr', c_ulonglong),
     (
      'sh_offset', c_ulonglong),
     (
      'sh_size', c_ulonglong),
     (
      'sh_link', c_uint),
     (
      'sh_info', c_uint),
     (
      'sh_addralign', c_ulonglong),
     (
      'sh_entsize', c_ulonglong)]


class ELF(object):

    def __init__(self, binary):
        self.__binary = bytearray(binary)
        self.__ElfHeader = None
        self.__shdr_l = []
        self.__phdr_l = []
        self.__setHeaderElf()
        self.__setShdr()
        self.__setPhdr()
        return

    def __setHeaderElf(self):
        e_ident = self.__binary[:15]
        ei_class = e_ident[ELFFlags.EI_CLASS]
        ei_data = e_ident[ELFFlags.EI_DATA]
        if ei_class != ELFFlags.ELFCLASS32 and ei_class != ELFFlags.ELFCLASS64:
            print '[Error] ELF.__setHeaderElf() - Bad Arch size'
            return
        else:
            if ei_data != ELFFlags.ELFDATA2LSB and ei_data != ELFFlags.ELFDATA2MSB:
                print '[Error] ELF.__setHeaderElf() - Bad architecture endian'
                return
            if ei_class == ELFFlags.ELFCLASS32:
                if ei_data == ELFFlags.ELFDATA2LSB:
                    self.__ElfHeader = Elf32_Ehdr_LSB.from_buffer_copy(self.__binary)
                elif ei_data == ELFFlags.ELFDATA2MSB:
                    self.__ElfHeader = Elf32_Ehdr_MSB.from_buffer_copy(self.__binary)
            elif ei_class == ELFFlags.ELFCLASS64:
                if ei_data == ELFFlags.ELFDATA2LSB:
                    self.__ElfHeader = Elf64_Ehdr_LSB.from_buffer_copy(self.__binary)
                elif ei_data == ELFFlags.ELFDATA2MSB:
                    self.__ElfHeader = Elf64_Ehdr_MSB.from_buffer_copy(self.__binary)
            self.getArch()
            return

    def __setShdr(self):
        shdr_num = self.__ElfHeader.e_shnum
        base = self.__binary[self.__ElfHeader.e_shoff:]
        shdr_l = []
        e_ident = self.__binary[:15]
        ei_data = e_ident[ELFFlags.EI_DATA]
        for i in range(shdr_num):
            if self.getArchMode() == CS_MODE_32:
                if ei_data == ELFFlags.ELFDATA2LSB:
                    shdr = Elf32_Shdr_LSB.from_buffer_copy(base)
                elif ei_data == ELFFlags.ELFDATA2MSB:
                    shdr = Elf32_Shdr_MSB.from_buffer_copy(base)
            elif self.getArchMode() == CS_MODE_64:
                if ei_data == ELFFlags.ELFDATA2LSB:
                    shdr = Elf64_Shdr_LSB.from_buffer_copy(base)
                elif ei_data == ELFFlags.ELFDATA2MSB:
                    shdr = Elf64_Shdr_MSB.from_buffer_copy(base)
            self.__shdr_l.append(shdr)
            base = base[self.__ElfHeader.e_shentsize:]

        if self.__ElfHeader.e_shstrndx != 0:
            string_table = str(self.__binary[self.__shdr_l[self.__ElfHeader.e_shstrndx].sh_offset:])
            for i in range(shdr_num):
                self.__shdr_l[i].str_name = string_table[self.__shdr_l[i].sh_name:].split('\x00')[0]

    def __setPhdr(self):
        pdhr_num = self.__ElfHeader.e_phnum
        base = self.__binary[self.__ElfHeader.e_phoff:]
        phdr_l = []
        e_ident = self.__binary[:15]
        ei_data = e_ident[ELFFlags.EI_DATA]
        for i in range(pdhr_num):
            if self.getArchMode() == CS_MODE_32:
                if ei_data == ELFFlags.ELFDATA2LSB:
                    phdr = Elf32_Phdr_LSB.from_buffer_copy(base)
                elif ei_data == ELFFlags.ELFDATA2MSB:
                    phdr = Elf32_Phdr_MSB.from_buffer_copy(base)
            elif self.getArchMode() == CS_MODE_64:
                if ei_data == ELFFlags.ELFDATA2LSB:
                    phdr = Elf64_Phdr_LSB.from_buffer_copy(base)
                elif ei_data == ELFFlags.ELFDATA2MSB:
                    phdr = Elf64_Phdr_MSB.from_buffer_copy(base)
            self.__phdr_l.append(phdr)
            base = base[self.__ElfHeader.e_phentsize:]

    def getEntryPoint(self):
        return self.__e_entry

    def getExecSections(self):
        ret = []
        for segment in self.__phdr_l:
            if segment.p_flags & 1:
                ret += [
                 {'offset': segment.p_offset, 
                    'size': segment.p_memsz, 
                    'vaddr': segment.p_vaddr, 
                    'opcodes': bytes(self.__binary[segment.p_offset:segment.p_offset + segment.p_memsz])}]

        return ret

    def getDataSections(self):
        ret = []
        for section in self.__shdr_l:
            if not section.sh_flags & 4 and section.sh_flags & 2:
                ret += [
                 {'name': section.str_name, 
                    'offset': section.sh_offset, 
                    'size': section.sh_size, 
                    'vaddr': section.sh_addr, 
                    'opcodes': str(self.__binary[section.sh_offset:section.sh_offset + section.sh_size])}]

        return ret

    def getArch(self):
        if self.__ElfHeader.e_machine == ELFFlags.EM_386 or self.__ElfHeader.e_machine == ELFFlags.EM_X86_64:
            return CS_ARCH_X86
        if self.__ElfHeader.e_machine == ELFFlags.EM_ARM:
            return CS_ARCH_ARM
        else:
            if self.__ElfHeader.e_machine == ELFFlags.EM_ARM64:
                return CS_ARCH_ARM64
            else:
                if self.__ElfHeader.e_machine == ELFFlags.EM_MIPS:
                    return CS_ARCH_MIPS
                if self.__ElfHeader.e_machine == ELFFlags.EM_PowerPC:
                    return CS_ARCH_PPC
                if self.__ElfHeader.e_machine == ELFFlags.EM_SPARCv8p:
                    return CS_ARCH_SPARC
                print '[Error] ELF.getArch() - Architecture not supported'
                return

            return

    def getArchMode(self):
        if self.__ElfHeader.e_ident[ELFFlags.EI_CLASS] == ELFFlags.ELFCLASS32:
            return CS_MODE_32
        else:
            if self.__ElfHeader.e_ident[ELFFlags.EI_CLASS] == ELFFlags.ELFCLASS64:
                return CS_MODE_64
            else:
                print '[Error] ELF.getArchMode() - Bad Arch size'
                return

            return

    def getFormat(self):
        return 'ELF'