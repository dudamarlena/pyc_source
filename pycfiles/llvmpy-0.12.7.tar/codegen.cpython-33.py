# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Support/CodeGen.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 567 bytes
from binding import *
from ..namespace import llvm
Reloc = llvm.Namespace('Reloc')
Reloc.Enum('Model', 'Default', 'Static', 'PIC_', 'DynamicNoPIC')
CodeModel = llvm.Namespace('CodeModel')
CodeModel.Enum('Model', 'Default', 'JITDefault', 'Small', 'Kernel', 'Medium', 'Large')
TLSModel = llvm.Namespace('TLSModel')
TLSModel.Enum('Model', 'GeneralDynamic', 'LocalDynamic', 'InitialExec', 'LocalExec')
CodeGenOpt = llvm.Namespace('CodeGenOpt')
CodeGenOpt.Enum('Level', 'None', 'Less', 'Default', 'Aggressive')