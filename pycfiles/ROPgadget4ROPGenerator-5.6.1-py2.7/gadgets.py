# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ropgadget/gadgets.py
# Compiled at: 2018-03-17 16:59:29
import re
from capstone import *

class Gadgets(object):

    def __init__(self, binary, options, offset):
        self.__binary = binary
        self.__options = options
        self.__offset = offset

    def __checkInstructionBlackListedX86(self, insts):
        bl = [
         'db', 'int3']
        for inst in insts:
            for b in bl:
                if inst.split(' ')[0] == b:
                    return True

        return False

    def __checkMultiBr(self, insts, br):
        count = 0
        for inst in insts:
            if inst.split()[0] in br:
                count += 1

        return count

    def __passCleanX86(self, gadgets, multibr=False):
        new = []
        br = ['ret', 'retf', 'int', 'sysenter', 'jmp', 'call', 'syscall']
        for gadget in gadgets:
            insts = gadget['gadget'].split(' ; ')
            if len(insts) == 1 and insts[0].split(' ')[0] not in br:
                continue
            if insts[(-1)].split(' ')[0] not in br:
                continue
            if self.__checkInstructionBlackListedX86(insts):
                continue
            if not multibr and self.__checkMultiBr(insts, br) > 1:
                continue
            if len([ m.start() for m in re.finditer('ret', gadget['gadget']) ]) > 1:
                continue
            new += [gadget]

        return new

    def __gadgetsFinding(self, section, gadgets, arch, mode):
        C_OP = 0
        C_SIZE = 1
        C_ALIGN = 2
        PREV_BYTES = 9
        ret = []
        md = Cs(arch, mode)
        for gad in gadgets:
            allRefRet = [ m.start() for m in re.finditer(gad[C_OP], section['opcodes']) ]
            for ref in allRefRet:
                for i in range(self.__options.depth):
                    if (section['vaddr'] + ref - i * gad[C_ALIGN]) % gad[C_ALIGN] == 0:
                        decodes = md.disasm(section['opcodes'][ref - i * gad[C_ALIGN]:ref + gad[C_SIZE]], section['vaddr'] + ref)
                        gadget = ''
                        for decode in decodes:
                            gadget += (decode.mnemonic + ' ' + decode.op_str + ' ; ').replace('  ', ' ')

                        if re.search(gad[C_OP], decode.bytes) is None:
                            continue
                        if len(gadget) > 0:
                            gadget = gadget[:-3]
                            off = self.__offset
                            vaddr = off + section['vaddr'] + ref - i * gad[C_ALIGN]
                            prevBytesAddr = max(section['vaddr'], vaddr - PREV_BYTES)
                            prevBytes = section['opcodes'][prevBytesAddr - section['vaddr']:vaddr - section['vaddr']]
                            ret += [{'vaddr': vaddr, 'gadget': gadget, 'decodes': decodes, 'bytes': section['opcodes'][ref - i * gad[C_ALIGN]:ref + gad[C_SIZE]], 'prev': prevBytes}]

        return ret

    def addROPGadgets(self, section):
        arch = self.__binary.getArch()
        arch_mode = self.__binary.getArchMode()
        if arch == CS_ARCH_X86:
            gadgets = [[b'\xc3', 1, 1],
             [
              b'\xc2[\x00-\xff]{2}', 3, 1],
             [
              b'\xcb', 1, 1],
             [
              b'\xca[\x00-\xff]{2}', 3, 1],
             [
              b'\xf2\xc3', 2, 1],
             [
              b'\xf2\xc2[\x00-\xff]{2}', 4, 1]]
        elif arch == CS_ARCH_MIPS:
            gadgets = []
        elif arch == CS_ARCH_PPC:
            gadgets = [[b'N\x80\x00 ', 4, 4]]
            arch_mode = arch_mode + CS_MODE_BIG_ENDIAN
        elif arch == CS_ARCH_SPARC:
            gadgets = [[b'\x81\xc3\xe0\x08', 4, 4],
             [
              b'\x81\xc7\xe0\x08', 4, 4],
             [
              b'\x81\xe8\x00\x00', 4, 4]]
            arch_mode = CS_MODE_BIG_ENDIAN
        elif arch == CS_ARCH_ARM:
            gadgets = []
        elif arch == CS_ARCH_ARM64:
            gadgets = [[b'\xc0\x03_\xd6', 4, 4]]
            arch_mode = CS_MODE_ARM
        else:
            print 'Gadgets().addROPGadgets() - Architecture not supported'
            return
        if len(gadgets) > 0:
            return self.__gadgetsFinding(section, gadgets, arch, arch_mode)
        else:
            return gadgets

    def addJOPGadgets(self, section):
        arch = self.__binary.getArch()
        arch_mode = self.__binary.getArchMode()
        if arch == CS_ARCH_X86:
            gadgets = [[b'\xff[ !"#&\']{1}', 2, 1],
             [
              b'\xff[\xe0\xe1\xe2\xe3\xe4\xe6\xe7]{1}', 2, 1],
             [
              b'\xff[\x10\x11\x12\x13\x16\x17]{1}', 2, 1],
             [
              b'\xff[\xd0\xd1\xd2\xd3\xd4\xd6\xd7]{1}', 2, 1],
             [
              b'\xf2\xff[ !"#&\']{1}', 3, 1],
             [
              b'\xf2\xff[\xe0\xe1\xe2\xe3\xe4\xe6\xe7]{1}', 3, 1],
             [
              b'\xf2\xff[\x10\x11\x12\x13\x16\x17]{1}', 3, 1],
             [
              b'\xf2\xff[\xd0\xd1\xd2\xd3\xd4\xd6\xd7]{1}', 3, 1]]
        elif arch == CS_ARCH_MIPS:
            gadgets = [[b'\t\xf8 \x03[\x00-\xff]{4}', 8, 4],
             [
              b'\x08\x00 \x03[\x00-\xff]{4}', 8, 4],
             [
              b'\x08\x00\xe0\x03[\x00-\xff]{4}', 8, 4]]
        elif arch == CS_ARCH_PPC:
            gadgets = []
        elif arch == CS_ARCH_SPARC:
            gadgets = [[b'\x81\xc0[\x00@\x80\xc0]{1}\x00', 4, 4]]
            arch_mode = CS_MODE_BIG_ENDIAN
        elif arch == CS_ARCH_ARM64:
            gadgets = [[b'[\x00 @`\x80\xa0\xc0\xe0]{1}[\x00-\x03]{1}[\x1f_]{1}\xd6', 4, 4],
             [
              b'[\x00 @`\x80\xa0\xc0\xe0]{1}[\x00-\x03]{1}\\?\xd6', 4, 4]]
            arch_mode = CS_MODE_ARM
        elif arch == CS_ARCH_ARM:
            if self.__options.thumb or self.__options.rawMode == 'thumb':
                gadgets = [['[\x00\x08\x10\x18 (08@Hp]{1}G', 2, 2],
                 [
                  b'[\x80\x88\x90\x98\xa0\xa8\xb0\xb8\xc0\xc8\xf0]{1}G', 2, 2],
                 [
                  b'[\x00-\xff]{1}\xbd', 2, 2]]
                arch_mode = CS_MODE_THUMB
            else:
                gadgets = [
                 [
                  b'[\x10-\x19\x1e]{1}\xff/\xe1', 4, 4],
                 [
                  b'[0-9>]{1}\xff/\xe1', 4, 4],
                 [
                  b'[\x00-\xff][\x80-\xff][\x10-\x1e0->P-^p-~\x90-\x9e\xb0-\xbe\xd0-\xde\xf0-\xfe][\xe8\xe9]', 4, 4]]
                arch_mode = CS_MODE_ARM
        else:
            print 'Gadgets().addJOPGadgets() - Architecture not supported'
            return
        if len(gadgets) > 0:
            return self.__gadgetsFinding(section, gadgets, arch, arch_mode)
        else:
            return gadgets

    def addSYSGadgets(self, section):
        arch = self.__binary.getArch()
        arch_mode = self.__binary.getArchMode()
        if arch == CS_ARCH_X86:
            gadgets = [['̀', 2, 1],
             [
              '\x0f4', 2, 1],
             [
              '\x0f\x05', 2, 1],
             [
              b'e\xff\x15\x10\x00\x00\x00', 7, 1],
             [
              b'\xcd\x80\xc3', 3, 1],
             [
              b'\x0f4\xc3', 3, 1],
             [
              b'\x0f\x05\xc3', 3, 1],
             [
              b'e\xff\x15\x10\x00\x00\x00\xc3', 8, 1]]
        elif arch == CS_ARCH_MIPS:
            gadgets = [['\x0c\x00\x00\x00', 4, 4]]
        elif arch == CS_ARCH_PPC:
            gadgets = []
        elif arch == CS_ARCH_SPARC:
            gadgets = []
        elif arch == CS_ARCH_ARM64:
            gadgets = []
        elif arch == CS_ARCH_ARM:
            if self.__options.thumb or self.__options.rawMode == 'thumb':
                gadgets = [[b'\x00-\xff]{1}\xef', 2, 2]]
                arch_mode = CS_MODE_THUMB
            else:
                gadgets = [
                 [
                  b'\x00-\xff]{3}\xef', 4, 4]]
                arch_mode = CS_MODE_ARM
        else:
            print 'Gadgets().addSYSGadgets() - Architecture not supported'
            return
        if len(gadgets) > 0:
            return self.__gadgetsFinding(section, gadgets, arch, arch_mode)
        else:
            return []

    def passClean(self, gadgets, multibr):
        arch = self.__binary.getArch()
        if arch == CS_ARCH_X86:
            return self.__passCleanX86(gadgets, multibr)
        else:
            if arch == CS_ARCH_MIPS:
                return gadgets
            else:
                if arch == CS_ARCH_PPC:
                    return gadgets
                if arch == CS_ARCH_SPARC:
                    return gadgets
                if arch == CS_ARCH_ARM:
                    return gadgets
                if arch == CS_ARCH_ARM64:
                    return gadgets
                print 'Gadgets().passClean() - Architecture not supported'
                return

            return