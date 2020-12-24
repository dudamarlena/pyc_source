# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Metadata.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 1808 bytes
from binding import *
from .namespace import llvm
from .Value import Value, MDNode, MDString
from .LLVMContext import LLVMContext
from .ADT.StringRef import StringRef
from .Module import Module
from .Function import Function
from .Support.raw_ostream import raw_ostream
from .Assembly.AssemblyAnnotationWriter import AssemblyAnnotationWriter

@MDNode
class MDNode:
    _downcast_ = Value
    replaceOperandWith = Method(Void, cast(int, Unsigned), ptr(Value))
    getOperand = Method(ptr(Value), cast(int, Unsigned))
    getNumOperands = Method(cast(Unsigned, int))
    isFunctionLocal = Method(cast(Bool, bool))
    getFunction = Method(const(ptr(Function)))
    get = CustomStaticMethod('MDNode_get', PyObjectPtr, ref(LLVMContext), PyObjectPtr)


@MDString
class MDString:
    _downcast_ = Value
    get = StaticMethod(ptr(MDString), ref(LLVMContext), cast(str, StringRef))
    getString = Method(cast(StringRef, str))
    getLength = Method(cast(int, Unsigned))


@llvm.Class()
class NamedMDNode:
    eraseFromParent = Method()
    eraseFromParent.disowning = True
    dropAllReferences = Method()
    getParent = Method(ptr(Module))
    getOperand = Method(ptr(MDNode), cast(int, Unsigned))
    getNumOperands = Method(cast(Unsigned, int))
    getName = Method(cast(StringRef, str))
    addOperand = Method(Void, ptr(MDNode))
    print_ = Method(Void, ref(raw_ostream), ptr(AssemblyAnnotationWriter))
    print_.realname = 'print'
    dump = Method()

    @CustomPythonMethod
    def __str__(self):
        from llvmpy import extra
        os = extra.make_raw_ostream_for_printing()
        self.print_(os, None)
        return os.str()