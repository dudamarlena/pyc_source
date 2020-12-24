# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/CallingConv.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 425 bytes
from binding import *
from .namespace import llvm
ccs = '\n    C, Fast, Cold, GHC, FirstTargetCC, X86_StdCall, X86_FastCall,\n    ARM_APCS, ARM_AAPCS, ARM_AAPCS_VFP, MSP430_INTR, X86_ThisCall,\n    PTX_Kernel, PTX_Device,\n'
if LLVM_VERSION <= (3, 3):
    ccs += 'MBLAZE_INTR, MBLAZE_SVOL,'
ccs += 'SPIR_FUNC, SPIR_KERNEL, Intel_OCL_BI'
CallingConv = llvm.Namespace('CallingConv')
ID = CallingConv.Enum('ID', ccs)