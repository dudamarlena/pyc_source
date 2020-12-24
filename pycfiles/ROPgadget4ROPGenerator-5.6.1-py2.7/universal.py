# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ropgadget/loaders/universal.py
# Compiled at: 2018-03-17 16:59:29
import sys
from capstone import *
from ctypes import *
from binascii import *
from ropgadget.loaders.macho import *

class FAT_HEADER(BigEndianStructure):
    _fields_ = [
     (
      'magic', c_uint),
     (
      'nfat_arch', c_uint)]


class FAT_ARC(BigEndianStructure):
    _fields_ = [
     (
      'cputype', c_uint),
     (
      'cpusubtype', c_uint),
     (
      'offset', c_uint),
     (
      'size', c_uint),
     (
      'align', c_uint)]


class MACHOFlags(object):
    CPU_TYPE_I386 = 7
    CPU_TYPE_X86_64 = CPU_TYPE_I386 | 16777216
    CPU_TYPE_MIPS = 8
    CPU_TYPE_ARM = 12
    CPU_TYPE_SPARC = 14
    CPU_TYPE_POWERPC = 18
    CPU_TYPE_POWERPC64 = CPU_TYPE_POWERPC | 16777216
    LC_SEGMENT = 1
    LC_SEGMENT_64 = 25
    S_ATTR_SOME_INSTRUCTIONS = 1024
    S_ATTR_PURE_INSTRUCTIONS = 2147483648


class UNIVERSAL(object):

    def __init__(self, binary):
        self.__binary = bytearray(binary)
        self.__machoBinaries = []
        self.__fatHeader = None
        self.__rawLoadCmd = None
        self.__sections_l = []
        self.__setHeader()
        self.__setBinaries()
        return

    def __setHeader(self):
        self.__fatHeader = FAT_HEADER.from_buffer_copy(self.__binary)

    def __setBinaries(self):
        offset = 8
        for i in xrange(self.__fatHeader.nfat_arch):
            header = FAT_ARC.from_buffer_copy(self.__binary[offset:])
            rawBinary = self.__binary[header.offset:header.offset + header.size]
            if rawBinary[:4] == unhexlify('cefaedfe') or rawBinary[:4] == unhexlify('cffaedfe'):
                self.__machoBinaries.append(MACHO(rawBinary))
            else:
                print '[Error] Binary #' + str(i + 1) + ' in Universal binary has an unsupported format'
            offset += sizeof(header)

    def getExecSections(self):
        ret = []
        for binary in self.__machoBinaries:
            ret += binary.getExecSections()

        return ret

    def getDataSections(self):
        ret = []
        for binary in self.__machoBinaries:
            ret += binary.getDataSections()

        return ret

    def getFormat(self):
        return 'Universal'

    def getEntryPoint(self):
        for binary in self.__machoBinaries:
            return binary.getEntryPoint()

    def getArch(self):
        for binary in self.__machoBinaries:
            return binary.getArch()

    def getArchMode(self):
        for binary in self.__machoBinaries:
            return binary.getArchMode()


if sys.version_info.major == 3:
    xrange = range