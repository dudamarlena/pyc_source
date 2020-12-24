# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/op_imports.py
# Compiled at: 2020-04-26 21:30:06
"""Facilitates importing opmaps for the a given Python version"""
import sys
from xdis import IS_PYPY
from xdis.magics import canonic_python_version
from xdis.opcodes import opcode_10
from xdis.opcodes import opcode_11
from xdis.opcodes import opcode_13
from xdis.opcodes import opcode_14
from xdis.opcodes import opcode_15
from xdis.opcodes import opcode_16
from xdis.opcodes import opcode_20
from xdis.opcodes import opcode_21
from xdis.opcodes import opcode_22
from xdis.opcodes import opcode_23
from xdis.opcodes import opcode_24
from xdis.opcodes import opcode_25
from xdis.opcodes import opcode_26
from xdis.opcodes import opcode_27
from xdis.opcodes import opcode_30
from xdis.opcodes import opcode_31
from xdis.opcodes import opcode_32
from xdis.opcodes import opcode_33
from xdis.opcodes import opcode_34
from xdis.opcodes import opcode_35
from xdis.opcodes import opcode_36
from xdis.opcodes import opcode_37
from xdis.opcodes import opcode_38
from xdis.opcodes import opcode_39
from xdis.opcodes import opcode_26pypy
from xdis.opcodes import opcode_27pypy
from xdis.opcodes import opcode_32pypy
from xdis.opcodes import opcode_33pypy
from xdis.opcodes import opcode_35pypy
from xdis.opcodes import opcode_36pypy
op_imports = {1.0: opcode_10, '1.0': opcode_10, 1.1: opcode_11, '1.1': opcode_11, 1.2: opcode_11, '1.2': opcode_11, 1.3: opcode_13, '1.3': opcode_13, 1.4: opcode_14, '1.4': opcode_14, 1.5: opcode_15, '1.5': opcode_15, 1.6: opcode_16, '1.6': opcode_16, '2.0': opcode_20, 2.0: opcode_20, '2.1': opcode_21, 2.1: opcode_21, '2.2': opcode_22, 2.2: opcode_22, '2.3a0': opcode_23, 2.3: opcode_23, '2.4b1': opcode_24, 2.4: opcode_24, '2.5c2': opcode_25, 2.5: opcode_25, '2.6a1': opcode_26, 2.6: opcode_26, '2.7': opcode_27, 2.7: opcode_27, '3.0': opcode_30, 3.0: opcode_30, '3.0a5': opcode_30, '3.1': opcode_31, '3.1a0+': opcode_31, 3.1: opcode_31, '3.2': opcode_32, '3.2a2': opcode_32, 3.2: opcode_32, '3.3a4': opcode_33, 3.3: opcode_33, '3.4': opcode_34, '3.4rc2': opcode_34, 3.4: opcode_34, '3.5': opcode_35, '3.5.1': opcode_35, '3.5.2': opcode_35, '3.5.3': opcode_35, '3.5.4': opcode_35, 3.5: opcode_35, '3.6rc1': opcode_36, '3.6rc1': opcode_36, 3.6: opcode_36, '3.7.0beta3': opcode_37, '3.7.0.beta3': opcode_37, '3.7.0': opcode_37, 3.7: opcode_37, '3.8.0alpha0': opcode_38, '3.8.0a0': opcode_38, '3.8.0a3+': opcode_38, '3.8.0alpha3': opcode_38, '3.8.0beta2': opcode_38, '3.8.0rc1+': opcode_38, '3.8.0candidate1': opcode_38, '3.8': opcode_38, '3.9.0alpha1': opcode_39, '3.9.0alpha2': opcode_39, '3.9': opcode_39, '2.6pypy': opcode_26pypy, '2.7pypy': opcode_27pypy, '3.2pypy': opcode_32pypy, '3.3pypy': opcode_33pypy, '3.5pypy': opcode_35pypy, '3.6pypy': opcode_36pypy, '3.6.1pypy': opcode_36pypy}
for (k, v) in canonic_python_version.items():
    if v in op_imports:
        op_imports[k] = op_imports[v]

def get_opcode_module(version_info=None, variant=None):
    if version_info is None:
        version_info = sys.version_info
        if variant is None and IS_PYPY:
            variant = 'pypy'
    vers_str = ('.').join([ str(v) for v in version_info[0:3] ])
    if len(version_info) >= 3 and version_info[3] != 'final':
        vers_str += ('').join([ str(v) for v in version_info[3:] ])
    if variant is None:
        try:
            import platform
            variant = platform.python_implementation()
            if platform in ('Jython', 'Pyston'):
                vers_str += variant
        except:
            pass

    else:
        vers_str += variant
    return op_imports[canonic_python_version[vers_str]]


if __name__ == '__main__':
    print get_opcode_module()