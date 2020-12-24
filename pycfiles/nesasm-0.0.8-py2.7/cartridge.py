# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nesasm/cartridge.py
# Compiled at: 2017-01-04 16:34:21
NES_ID = [
 78, 69, 83, 26]

class Cartridge(object):

    def __init__(self):
        self.banks = {}
        self.bank_id = 0
        self.pc = 0
        self.inespgr = 1
        self.ineschr = 1
        self.inesmap = 1
        self.inesmir = 1
        self.rs = 0
        self.path = ''

    def nes_get_header(self):
        unused = [
         0, 0, 0, 0, 0, 0, 0, 0]
        header = []
        header.extend(NES_ID)
        header.append(self.inespgr)
        header.append(self.ineschr)
        header.append(self.inesmir)
        header.append(self.inesmap)
        header.extend(unused)
        return header

    def set_iNES_prg(self, inespgr):
        self.inespgr = inespgr

    def set_iNES_chr(self, ineschr):
        self.ineschr = ineschr

    def set_iNES_map(self, inesmap):
        self.inesmap = inesmap

    def set_iNES_mir(self, inesmir):
        self.inesmir = inesmir

    def set_bank_id(self, _id):
        if _id not in self.banks:
            self.banks[_id] = dict(code=[], start=None, size=8192)
        self.bank_id = _id
        return

    def set_org(self, org):
        if self.bank_id not in self.banks:
            self.set_bank_id(self.bank_id)
        if not self.banks[self.bank_id]['start']:
            self.banks[self.bank_id]['start'] = org
            self.pc = org
        else:
            while self.pc < org:
                self.append_code([255])

            self.pc = org

    def append_code(self, code):
        if self.bank_id not in self.banks:
            self.set_bank_id(self.bank_id)
        for c in code:
            assert c <= 255

        self.banks[self.bank_id]['code'].extend(code)
        self.pc += len(code)

    def get_code(self):
        if self.bank_id not in self.banks:
            self.set_bank_id(self.bank_id)
        return self.banks[self.bank_id]['code']

    def get_ines_code(self):
        if self.bank_id not in self.banks:
            self.set_bank_id(self.bank_id)
        opcodes = []
        nes_header = self.nes_get_header()
        opcodes.extend(nes_header)
        try:
            _values = self.banks.itervalues
        except AttributeError:
            _values = self.banks.values

        for bank in _values():
            for _ in range(len(bank['code']), bank['size']):
                bank['code'].append(255)

            opcodes.extend(bank['code'])

        return opcodes