# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winpwn\asm.py
# Compiled at: 2020-04-17 05:15:28
from .context import context
from .misc import Latin1_encode, Latin1_decode

def disasm(machine_code, addr=0, arch=None):
    import capstone
    machine_code = Latin1_encode(machine_code)
    if arch is None:
        arch = context.arch
    if arch == 'i386':
        disasmer = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    else:
        if arch == 'amd64':
            disasmer = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        l = ''
        for i in disasmer.disasm(machine_code, addr):
            l += ('{:8s} {};\n').format(i.mnemonic, i.op_str)

    return Latin1_decode(Latin1_encode(l.strip('\n')))


def asm(asm_code, addr=0, arch=None):
    import keystone
    asm_code = Latin1_encode(asm_code)
    if arch is None:
        arch = context.arch
    if arch == 'i386':
        asmer = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_32)
    else:
        if arch == 'amd64':
            asmer = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
        l = ''
        for i in asmer.asm(asm_code, addr)[0]:
            l += chr(i)

    return Latin1_decode(Latin1_encode(l.strip('\n')))