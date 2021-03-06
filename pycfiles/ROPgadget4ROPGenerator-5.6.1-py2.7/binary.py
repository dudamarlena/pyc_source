# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ropgadget/binary.py
# Compiled at: 2018-03-17 16:59:29
from ropgadget.loaders.elf import *
from ropgadget.loaders.pe import *
from ropgadget.loaders.raw import *
from ropgadget.loaders.macho import *
from ropgadget.loaders.universal import *
from binascii import unhexlify

class Binary(object):

    def __init__(self, options):
        self.__fileName = options.binary
        self.__rawBinary = None
        self.__binary = None
        try:
            fd = open(self.__fileName, 'rb')
            self.__rawBinary = fd.read()
            fd.close()
        except:
            print "[Error] Can't open the binary or binary not found"
            return

        if options.rawArch and options.rawMode:
            self.__binary = Raw(self.__rawBinary, options.rawArch, options.rawMode)
        elif self.__rawBinary[:4] == unhexlify('7f454c46'):
            self.__binary = ELF(self.__rawBinary)
        elif self.__rawBinary[:2] == unhexlify('4d5a'):
            self.__binary = PE(self.__rawBinary)
        elif self.__rawBinary[:4] == unhexlify('cafebabe'):
            self.__binary = UNIVERSAL(self.__rawBinary)
        elif self.__rawBinary[:4] == unhexlify('cefaedfe') or self.__rawBinary[:4] == unhexlify('cffaedfe'):
            self.__binary = MACHO(self.__rawBinary)
        else:
            print '[Error] Binary format not supported'
            return
        return

    def getFileName(self):
        return self.__fileName

    def getRawBinary(self):
        return self.__rawBinary

    def getBinary(self):
        return self.__binary

    def getEntryPoint(self):
        return self.__binary.getEntryPoint()

    def getDataSections(self):
        return self.__binary.getDataSections()

    def getExecSections(self):
        return self.__binary.getExecSections()

    def getArch(self):
        return self.__binary.getArch()

    def getArchMode(self):
        return self.__binary.getArchMode()

    def getFormat(self):
        return self.__binary.getFormat()