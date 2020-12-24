# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Attributes.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 2756 bytes
from binding import *
from .namespace import llvm
from .LLVMContext import LLVMContext
if LLVM_VERSION >= (3, 3):
    llvm.includes.add('llvm/IR/Attributes.h')
else:
    llvm.includes.add('llvm/Attributes.h')
AttrBuilder = llvm.Class()
if LLVM_VERSION >= (3, 3):
    Attribute = llvm.Class()
    AttributeSet = llvm.Class()
else:
    Attributes = llvm.Class()
if LLVM_VERSION >= (3, 3):

    @Attribute
    class Attribute:
        AttrKind = Enum('None, Alignment, AlwaysInline,\n                  ByVal, InlineHint, InReg,\n                  MinSize, Naked, Nest, NoAlias,\n                  NoBuiltin, NoCapture, NoDuplicate, NoImplicitFloat,\n                  NoInline, NonLazyBind, NoRedZone, NoReturn,\n                  NoUnwind, OptimizeForSize, ReadNone, ReadOnly,\n                  Returned, ReturnsTwice, SExt, StackAlignment,\n                  StackProtect, StackProtectReq, StackProtectStrong, StructRet,\n                  SanitizeAddress, SanitizeThread, SanitizeMemory, UWTable,\n                  ZExt, EndAttrKinds')
        delete = Destructor()
        get = StaticMethod(Attribute, ref(LLVMContext), AttrKind, cast(int, Uint64)).require_only(2)


    @AttrBuilder
    class AttrBuilder:
        new = Constructor()
        delete = Destructor()
        clear = Method()
        addAttribute = Method(ref(AttrBuilder), Attribute.AttrKind)
        removeAttribute = Method(ref(AttrBuilder), Attribute.AttrKind)
        addAlignmentAttr = Method(ref(AttrBuilder), cast(int, Unsigned))


    @AttributeSet
    class AttributeSet:
        delete = Destructor()
        get = StaticMethod(AttributeSet, ref(LLVMContext), cast(int, Unsigned), ref(AttrBuilder))


else:

    @Attributes
    class Attributes:
        AttrVal = Enum('None, AddressSafety, Alignment, AlwaysInline,\n            ByVal, InlineHint, InReg, MinSize,\n            Naked, Nest, NoAlias, NoCapture,\n            NoImplicitFloat, NoInline, NonLazyBind, NoRedZone,\n            NoReturn, NoUnwind, OptimizeForSize, ReadNone,\n            ReadOnly, ReturnsTwice, SExt, StackAlignment,\n            StackProtect, StackProtectReq, StructRet, UWTable, ZExt')
        delete = Destructor()
        get = StaticMethod(Attributes, ref(LLVMContext), ref(AttrBuilder))


    @AttrBuilder
    class AttrBuilder:
        new = Constructor()
        delete = Destructor()
        clear = Method()
        addAttribute = Method(ref(AttrBuilder), Attributes.AttrVal)
        removeAttribute = Method(ref(AttrBuilder), Attributes.AttrVal)
        addAlignmentAttr = Method(ref(AttrBuilder), cast(int, Unsigned))