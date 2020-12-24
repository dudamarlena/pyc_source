# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Target/TargetMachine.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 2607 bytes
from binding import *
from src.namespace import llvm
TargetMachine = llvm.Class()
from src.Support.TargetRegistry import Target
from src.ADT.StringRef import StringRef
from src.Support.CodeGen import CodeModel, TLSModel, CodeGenOpt, Reloc
from src.GlobalValue import GlobalValue
from src.DataLayout import DataLayout
if LLVM_VERSION >= (3, 4):
    from src.MC import MCAsmInfo, TargetInstrInfo, TargetSubtargetInfo, TargetRegisterInfo
if LLVM_VERSION < (3, 3):
    from src.TargetTransformInfo import ScalarTargetTransformInfo, VectorTargetTransformInfo
from src.PassManager import PassManagerBase
from src.Support.FormattedStream import formatted_raw_ostream

@TargetMachine
class TargetMachine:
    _include_ = 'llvm/Target/TargetMachine.h'
    CodeGenFileType = Enum('\n                           CGFT_AssemblyFile\n                           CGFT_ObjectFile\n                           CGFT_Null')
    delete = Destructor()
    getTarget = Method(const(ref(Target)))
    getTargetTriple = Method(cast(StringRef, str))
    getTargetCPU = Method(cast(StringRef, str))
    getTargetFeatureString = Method(cast(StringRef, str))
    getRelocationModel = Method(Reloc.Model)
    getCodeModel = Method(CodeModel.Model)
    getTLSModel = Method(TLSModel.Model, ptr(GlobalValue))
    getOptLevel = Method(CodeGenOpt.Level)
    hasMCUseDwarfDirectory = Method(cast(Bool, bool))
    setMCUseDwarfDirectory = Method(Void, cast(bool, Bool))
    getDataLayout = Method(const(ownedptr(DataLayout)))
    if LLVM_VERSION < (3, 3):
        getScalarTargetTransformInfo = Method(const(ownedptr(ScalarTargetTransformInfo)))
        getVectorTargetTransformInfo = Method(const(ownedptr(VectorTargetTransformInfo)))
    else:
        addAnalysisPasses = Method(Void, ref(PassManagerBase))
    addPassesToEmitFile = Method(cast(bool, Bool), ref(PassManagerBase), ref(formatted_raw_ostream), CodeGenFileType, cast(bool, Bool)).require_only(3)
    if LLVM_VERSION >= (3, 4):
        getSubtargetImpl = Method(const(ownedptr(TargetSubtargetInfo)))
        getMCAsmInfo = Method(const(ownedptr(MCAsmInfo)))
        getInstrInfo = Method(const(ownedptr(TargetInstrInfo)))
        getRegisterInfo = Method(const(ownedptr(TargetRegisterInfo)))