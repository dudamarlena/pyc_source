# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/ADT/Triple.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 1612 bytes
from binding import *
from ..namespace import llvm
from .StringRef import StringRef
Triple = llvm.Class()

@Triple
class Triple:
    _include_ = 'llvm/ADT/Triple.h'
    new = Constructor()
    new |= Constructor(cast(str, StringRef))
    new |= Constructor(cast(str, StringRef), cast(str, StringRef), cast(str, StringRef))

    def _return_str():
        return Method(cast(StringRef, str))

    getTriple = _return_str()
    getArchName = _return_str()
    getVendorName = _return_str()
    getOSName = _return_str()
    getEnvironmentName = _return_str()
    getOSAndEnvironmentName = _return_str()

    @CustomPythonMethod
    def __str__(self):
        return self.getTriple()

    def _return_bool(*args):
        return Method(cast(bool, Bool), *args)

    isArch64Bit = _return_bool()
    isArch32Bit = _return_bool()
    isArch16Bit = _return_bool()
    isOSVersionLT = _return_bool(cast(int, Unsigned), cast(int, Unsigned), cast(int, Unsigned)).require_only(1)
    isMacOSXVersionLT = _return_bool(cast(int, Unsigned), cast(int, Unsigned), cast(int, Unsigned)).require_only(1)
    isMacOSX = _return_bool()
    isOSDarwin = _return_bool()
    isOSCygMing = _return_bool()
    isOSWindows = _return_bool()
    isOSBinFormatELF = _return_bool()
    isOSBinFormatCOFF = _return_bool()
    isEnvironmentMachO = _return_bool()
    get32BitArchVariant = Method(Triple)
    get64BitArchVariant = Method(Triple)