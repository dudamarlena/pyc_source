# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/DIBuilder.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 17706 bytes
from binding import *
from .namespace import llvm
DIBuilder = llvm.Class()
from .Module import Module
from .Value import Value, MDNode, Function, BasicBlock
from .Instruction import Instruction
from .DebugInfo import DIFile, DIEnumerator, DIType, DIBasicType, DIDerivedType, DICompositeType
from .DebugInfo import DIDescriptor, DIArray, DISubrange, DIGlobalVariable
from .DebugInfo import DIVariable, DISubprogram, DINameSpace, DILexicalBlockFile
from .DebugInfo import DILexicalBlock
from .ADT.SmallVector import SmallVector_Value
from .ADT.StringRef import StringRef
unsigned_arg = cast(int, Unsigned)
stringref_arg = cast(str, StringRef)
bool_arg = cast(bool, Bool)
uint64_arg = cast(int, Uint64)
int64_arg = cast(int, Int64)

@DIBuilder
class DIBuilder:
    _include_ = 'llvm/DIBuilder.h'
    new = Constructor(ref(Module))
    delete = Destructor()
    if LLVM_VERSION <= (3, 3):
        getCU = Method(const(ptr(MDNode)))
    finalize = Method()
    createCompileUnit = Method(Void, unsigned_arg, stringref_arg, stringref_arg, stringref_arg, bool_arg, stringref_arg, unsigned_arg)
    createFile = Method(DIFile, stringref_arg, stringref_arg)
    createEnumerator = Method(DIEnumerator, stringref_arg, uint64_arg if LLVM_VERSION <= (3,
                                                                                          3) else int64_arg)
    if LLVM_VERSION <= (3, 3):
        createNullPtrType = Method(DIType, stringref_arg)
    else:
        createNullPtrType = Method(DIBasicType)
    createBasicType = Method(DIType, stringref_arg, uint64_arg, uint64_arg, unsigned_arg)
    createQualifiedType = Method(DIType, unsigned_arg, ref(DIType))
    createPointerType = Method(DIType, ref(DIType), uint64_arg, uint64_arg, stringref_arg).require_only(2)
    createReferenceType = Method(DIType, unsigned_arg, ref(DIType))
    createTypedef = Method(DIType, ref(DIType), stringref_arg, ref(DIFile), unsigned_arg, ref(DIDescriptor))
    createFriend = Method(DIType if LLVM_VERSION <= (3, 3) else DIDerivedType, ref(DIType), ref(DIType))
    createInheritance = Method(DIType, ref(DIType), ref(DIType), uint64_arg, unsigned_arg)
    createMemberType = Method(DIType, ref(DIDescriptor), stringref_arg, ref(DIFile), unsigned_arg, uint64_arg, uint64_arg, uint64_arg, unsigned_arg, ref(DIType))
    createClassType = Method(DIType, ref(DIDescriptor), stringref_arg, ref(DIFile), unsigned_arg, uint64_arg, uint64_arg, uint64_arg, unsigned_arg, ref(DIType), ref(DIArray), ptr(MDNode), ptr(MDNode)).require_only(10)
    if LLVM_VERSION >= (3, 3):
        createStructType = Method(DIType, ref(DIDescriptor), stringref_arg, ref(DIFile), unsigned_arg, uint64_arg, uint64_arg, unsigned_arg, ref(DIType), ref(DIArray), unsigned_arg).require_only(9)
    else:
        createStructType = Method(DIType, ref(DIDescriptor), stringref_arg, ref(DIFile), unsigned_arg, uint64_arg, uint64_arg, unsigned_arg, ref(DIArray), unsigned_arg).require_only(8)
    createUnionType = Method(DIType, ref(DIDescriptor), stringref_arg, ref(DIFile), unsigned_arg, uint64_arg, uint64_arg, unsigned_arg, ref(DIArray), unsigned_arg).require_only(8)
    createArrayType = Method(DIType, uint64_arg, uint64_arg, ref(DIType), ref(DIArray))
    createVectorType = Method(DIType if LLVM_VERSION <= (3, 3) else DICompositeType, uint64_arg, uint64_arg, ref(DIType), ref(DIArray))
    createEnumerationType = Method(DIType, ref(DIDescriptor), stringref_arg, ref(DIFile), unsigned_arg, uint64_arg, uint64_arg, ref(DIArray), ref(DIType))
    createSubroutineType = Method(DIType, ref(DIFile), ref(DIArray))
    createArtificialType = Method(DIType, ref(DIType))
    createObjectPointerType = Method(DIType, ref(DIType))
    createForwardDecl = Method(DIType, unsigned_arg, stringref_arg, ref(DIDescriptor), ref(DIFile), unsigned_arg, unsigned_arg, uint64_arg, uint64_arg).require_only(5)
    retainType = Method(Void, ref(DIType))
    createUnspecifiedParameter = Method(DIDescriptor)
    getOrCreateArray = Method(DIArray, ref(SmallVector_Value))
    getOrCreateSubrange = Method(DISubrange, int64_arg, int64_arg)
    createGlobalVariable = Method(DIGlobalVariable, stringref_arg, ref(DIFile), unsigned_arg, ref(DIType), bool_arg, ptr(Value))
    createStaticVariable = Method(DIGlobalVariable, ref(DIDescriptor), stringref_arg, stringref_arg, ref(DIFile), unsigned_arg, ref(DIType), bool_arg, ptr(Value))
    createLocalVariable = Method(DIVariable, unsigned_arg, ref(DIDescriptor), stringref_arg, ref(DIFile), unsigned_arg, ref(DIType), bool_arg, unsigned_arg, unsigned_arg).require_only(6)
    createComplexVariable = Method(DIVariable, unsigned_arg, ref(DIDescriptor), stringref_arg, ref(DIFile), unsigned_arg, ref(DIType), ref(SmallVector_Value), unsigned_arg).require_only(7)
    createFunction = Method(DISubprogram, ref(DIDescriptor), stringref_arg, stringref_arg, ref(DIFile), unsigned_arg, ref(DIType if LLVM_VERSION <= (3,
                                                                                                                                                     3) else DICompositeType), bool_arg, bool_arg, unsigned_arg, unsigned_arg, bool_arg, ptr(Function), ptr(MDNode), ptr(MDNode)).require_only(9)
    createMethod = Method(DISubprogram, ref(DIDescriptor), stringref_arg, stringref_arg, ref(DIFile), unsigned_arg, ref(DIType if LLVM_VERSION <= (3,
                                                                                                                                                   3) else DICompositeType), bool_arg, bool_arg, unsigned_arg, unsigned_arg, ptr(MDNode), unsigned_arg, bool_arg, ptr(Function), ptr(MDNode)).require_only(8)
    createNameSpace = Method(DINameSpace, ref(DIDescriptor), stringref_arg, ref(DIFile), unsigned_arg)
    createLexicalBlockFile = Method(DILexicalBlockFile, ref(DIDescriptor), ref(DIFile))
    createLexicalBlock = Method(DILexicalBlock, ref(DIDescriptor), ref(DIFile), unsigned_arg, unsigned_arg)
    _insertDeclare_1 = Method(ptr(Instruction), ptr(Value), ref(DIVariable), ptr(BasicBlock))
    _insertDeclare_1.realname = 'insertDeclare'
    _insertDeclare_2 = Method(ptr(Instruction), ptr(Value), ref(DIVariable), ptr(Instruction))
    _insertDeclare_2.realname = 'insertDeclare'

    @CustomPythonMethod
    def insertDeclare(self, storage, varinfo, insertpt):
        if isinstance(insertbefore, _api.llvm.Instruction):
            return self._insertDeclare_2(storage, varinfo, insertpt)
        else:
            return self._insertDeclare_1(storage, varinfo, insertpt)

    _insertDbgValueIntrinsic_1 = Method(ptr(Instruction), ptr(Value), uint64_arg, ref(DIVariable), ptr(BasicBlock))
    _insertDbgValueIntrinsic_1.realname = 'insertDbgValueIntrinsic'
    _insertDbgValueIntrinsic_2 = Method(ptr(Instruction), ptr(Value), uint64_arg, ref(DIVariable), ptr(Instruction))
    _insertDbgValueIntrinsic_2.realname = 'insertDbgValueIntrinsic'

    @CustomPythonMethod
    def insertDbgValueIntrinsic(self, storage, varinfo, insertpt):
        if isinstance(insertbefore, _api.llvm.Instruction):
            return self._insertDbgValueIntrinsic_2(storage, varinfo, insertpt)
        else:
            return self._insertDbgValueIntrinsic_1(storage, varinfo, insertpt)