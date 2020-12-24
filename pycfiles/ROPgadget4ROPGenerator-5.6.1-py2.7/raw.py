# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ropgadget/loaders/raw.py
# Compiled at: 2018-03-17 16:59:29
from capstone import *

class Raw(object):

    def __init__(self, binary, arch, mode):
        self.__binary = bytearray(binary)
        self.__arch = arch
        self.__mode = mode

    def getEntryPoint(self):
        return 0

    def getExecSections(self):
        return [{'name': 'raw', 'offset': 0, 'size': len(self.__binary), 'vaddr': 0, 'opcodes': bytes(self.__binary)}]

    def getDataSections(self):
        return []

    def getArch(self):
        arch = {'x86': CS_ARCH_X86, 
           'arm': CS_ARCH_ARM, 
           'arm64': CS_ARCH_ARM64, 
           'sparc': CS_ARCH_SPARC, 
           'mips': CS_ARCH_MIPS, 
           'ppc': CS_ARCH_PPC}
        try:
            ret = arch[self.__arch]
        except:
            print '[Error] Raw.getArch() - Architecture not supported. Only supported: x86 arm arm64 sparc mips ppc'
            return

        return ret

    def getArchMode(self):
        mode = {'32': CS_MODE_32, 
           '64': CS_MODE_64, 
           'arm': CS_MODE_ARM, 
           'thumb': CS_MODE_THUMB}
        try:
            ret = mode[self.__mode]
        except:
            print '[Error] Raw.getArchMode() - Mode not supported. Only supported: 32 64 arm thumb'
            return

        return ret

    def getFormat(self):
        return 'Raw'