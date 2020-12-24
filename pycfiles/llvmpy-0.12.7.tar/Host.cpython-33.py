# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Support/Host.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 1387 bytes
from binding import *
from src.namespace import sys
getDefaultTargetTriple = sys.Function('getDefaultTargetTriple', cast(ConstStdString, str))
if LLVM_VERSION >= (3, 3):
    getProcessTriple = sys.Function('getProcessTriple', cast(ConstStdString, str))
    isLittleEndianHost = sys.CustomFunction('isLittleEndianHost', 'llvm_sys_isLittleEndianHost', cast(Bool, bool))
    isBigEndianHost = sys.CustomFunction('isBigEndianHost', 'llvm_sys_isBigEndianHost', cast(Bool, bool))
else:
    isLittleEndianHost = sys.Function('isLittleEndianHost', cast(Bool, bool))
    isBigEndianHost = sys.Function('isBigEndianHost', cast(Bool, bool))
getHostCPUName = sys.Function('getHostCPUName', cast(ConstStdString, str))
getHostCPUFeatures = sys.CustomFunction('getHostCPUFeatures', 'llvm_sys_getHostCPUFeatures', PyObjectPtr, PyObjectPtr)