# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Linker.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 2212 bytes
from binding import *
from .namespace import llvm
from .ADT.StringRef import StringRef
from .Module import Module
from .LLVMContext import LLVMContext
llvm.includes.add('llvm/Linker.h')
Linker = llvm.Class()

@Linker
class Linker:
    LinkerMode = Enum('DestroySource, PreserveSource')
    if LLVM_VERSION >= (3, 3):
        new = Constructor(ptr(Module))
    else:
        _new_w_empty = Constructor(cast(str, StringRef), cast(str, StringRef), ref(LLVMContext), cast(int, Unsigned)).require_only(3)
        _new_w_existing = Constructor(cast(str, StringRef), ptr(Module), cast(int, Unsigned)).require_only(2)

        @CustomPythonStaticMethod
        def new(progname, module_or_name, *args):
            if isinstance(module_or_name, Module):
                return _new_w_existing(progname, module_or_name, *args)
            else:
                return _new_w_empty(progname, module_or_name, *args)

    delete = Destructor()
    getModule = Method(ptr(Module))
    LinkInModule = CustomMethod('Linker_LinkInModule', PyObjectPtr, ptr(Module), PyObjectPtr)
    _LinkModules = CustomStaticMethod('Linker_LinkModules', PyObjectPtr, ptr(Module), ptr(Module), LinkerMode, PyObjectPtr)

    @CustomPythonStaticMethod
    def LinkModules(module, other, mode, errmsg):
        failed = Linker._LinkModules(module, other, mode, errmsg)
        if not failed:
            if mode != Linker.LinkerMode.PreserveSource:
                capsule.release_ownership(other._ptr)
        return failed