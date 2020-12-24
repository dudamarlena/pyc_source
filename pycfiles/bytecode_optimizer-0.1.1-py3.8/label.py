# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bytecodehacks/label.py
# Compiled at: 2000-03-15 16:55:42
import struct

class Label:

    def __init__(self, byte=None):
        self.byte = byte
        self.__op = None
        self.absrefs = []
        self.relrefs = []
        return

    def resolve(self, code):
        self.__op = code.opcodes[code.byte2op[self.byte]].unflesh()

    def add_absref(self, byte):
        self.absrefs.append(byte)

    def add_relref(self, byte):
        self.relrefs.append(byte)

    def __setattr__(self, attr, value):
        if attr == 'op':
            self.__op = value.unflesh()
        else:
            self.__dict__[attr] = value

    def __getattr__(self, attr):
        if attr == 'op':
            return self.__op
        raise AttributeError, attr

    def write_refs(self, cs):
        address = self.__op.byte
        for byte in self.absrefs:
            cs.seek(byte + 1)
            cs.write(struct.pack('<h', address))

        for byte in self.relrefs:
            offset = address - byte - 3
            cs.seek(byte + 1)
            cs.write(struct.pack('<h', offset))