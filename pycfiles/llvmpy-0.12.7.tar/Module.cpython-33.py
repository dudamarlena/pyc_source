# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Module.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 3212 bytes
from binding import *
from .namespace import llvm
Module = llvm.Class()
from .LLVMContext import LLVMContext
from .ADT.StringRef import StringRef
from .Constant import Constant
from .GlobalVariable import GlobalVariable
from .Function import Function
from .DerivedTypes import FunctionType
from .Support.raw_ostream import raw_ostream
from .Assembly.AssemblyAnnotationWriter import AssemblyAnnotationWriter
from .Type import Type, StructType
from .Metadata import NamedMDNode

@Module
class Module:
    if LLVM_VERSION >= (3, 3):
        _include_ = 'llvm/IR/Module.h'
    else:
        _include_ = 'llvm/Module.h'
    Endianness = Enum('AnyEndianness', 'LittleEndian', 'BigEndian')
    PointerSize = Enum('AnyPointerSize', 'Pointer32', 'Pointer64')
    new = Constructor(cast(str, StringRef), ref(LLVMContext))
    delete = Destructor()
    getModuleIdentifier = Method(cast(ConstStdString, str))
    getDataLayout = Method(cast(ConstStdString, str))
    getTargetTriple = Method(cast(ConstStdString, str))
    getEndianness = Method(Endianness)
    getPointerSize = Method(PointerSize)
    getContext = Method(ref(LLVMContext))
    getModuleInlineAsm = Method(cast(ConstStdString, str))
    setModuleIdentifier = Method(Void, cast(str, StringRef))
    setDataLayout = Method(Void, cast(str, StringRef))
    setTargetTriple = Method(Void, cast(str, StringRef))
    setModuleInlineAsm = Method(Void, cast(str, StringRef))
    appendModuleInlineAsm = Method(Void, cast(str, StringRef))
    getOrInsertFunction = Method(ptr(Constant), cast(str, StringRef), ptr(FunctionType))
    getFunction = Method(ptr(Function), cast(str, StringRef))
    list_functions = CustomMethod('Module_list_functions', PyObjectPtr)
    getGlobalVariable = Method(ptr(GlobalVariable), cast(str, StringRef), cast(bool, Bool)).require_only(1)
    getNamedGlobal = Method(ptr(GlobalVariable), cast(str, StringRef))
    getOrInsertGlobal = Method(ptr(Constant), cast(str, StringRef), ptr(Type))
    list_globals = CustomMethod('Module_list_globals', PyObjectPtr)
    getNamedMetadata = Method(ptr(NamedMDNode), cast(str, StringRef))
    getOrInsertNamedMetadata = Method(ptr(NamedMDNode), cast(str, StringRef))
    eraseNamedMetadata = Method(Void, ptr(NamedMDNode))
    list_named_metadata = CustomMethod('Module_list_named_metadata', PyObjectPtr)
    dump = Method(Void)
    print_ = Method(Void, ref(raw_ostream), ptr(AssemblyAnnotationWriter))
    print_.realname = 'print'

    @CustomPythonMethod
    def __str__(self):
        from llvmpy import extra
        os = extra.make_raw_ostream_for_printing()
        self.print_(os, None)
        return os.str()

    dropAllReferences = Method()
    getTypeByName = Method(ptr(StructType), cast(str, StringRef))