# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Support/TargetRegistry.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 4423 bytes
from binding import *
from src.namespace import llvm
llvm.includes.add('llvm/Support/TargetRegistry.h')
Target = llvm.Class()
TargetRegistry = llvm.Class()
from src.ADT.Triple import Triple
from src.ADT.StringRef import StringRef
from src.Target.TargetMachine import TargetMachine
from src.Target.TargetOptions import TargetOptions
from src.Support.CodeGen import Reloc, CodeModel, CodeGenOpt
if LLVM_VERSION >= (3, 4):
    from src.MC import MCSubtargetInfo
    from src.MC import MCDisassembler
    from src.MC import MCRegisterInfo
    from src.MC import MCAsmInfo
    from src.MC import MCInstrInfo
    from src.MC import MCInstrAnalysis
    from src.MC import MCInstPrinter

@Target
class Target:
    getNext = Method(const(ownedptr(Target)))
    getName = Method(cast(StdString, str))
    getShortDescription = Method(cast(StdString, str))

    def _has():
        return Method(cast(Bool, bool))

    hasJIT = _has()
    hasTargetMachine = _has()
    hasMCAsmBackend = _has()
    hasMCAsmParser = _has()
    hasAsmPrinter = _has()
    hasMCDisassembler = _has()
    hasMCInstPrinter = _has()
    hasMCCodeEmitter = _has()
    hasMCObjectStreamer = _has()
    hasAsmStreamer = _has()
    createTargetMachine = Method(ptr(TargetMachine), cast(str, StringRef), cast(str, StringRef), cast(str, StringRef), ref(TargetOptions), Reloc.Model, CodeModel.Model, CodeGenOpt.Level).require_only(4)
    if LLVM_VERSION >= (3, 4):
        createMCSubtargetInfo = Method(ptr(MCSubtargetInfo), cast(str, StringRef), cast(str, StringRef), cast(str, StringRef))
        createMCDisassembler = Method(ptr(MCDisassembler), ref(MCSubtargetInfo))
        createMCRegInfo = Method(ptr(MCRegisterInfo), cast(str, StringRef))
        createMCAsmInfo = Method(ptr(MCAsmInfo), const(ref(MCRegisterInfo)), cast(str, StringRef))
        createMCInstrInfo = Method(ptr(MCInstrInfo))
        createMCInstrAnalysis = Method(ptr(MCInstrAnalysis), const(ptr(MCInstrInfo)))
        createMCInstPrinter = Method(ptr(MCInstPrinter), cast(int, Unsigned), const(ref(MCAsmInfo)), const(ref(MCInstrInfo)), const(ref(MCRegisterInfo)), const(ref(MCSubtargetInfo)))


@TargetRegistry
class TargetRegistry:
    printRegisteredTargetsForVersion = StaticMethod()
    lookupTarget = CustomStaticMethod('TargetRegistry_lookupTarget', PyObjectPtr, cast(str, ConstCharPtr), PyObjectPtr)
    lookupTarget |= CustomStaticMethod('TargetRegistry_lookupTarget', PyObjectPtr, cast(str, ConstCharPtr), ref(Triple), PyObjectPtr)
    getClosestTargetForJIT = CustomStaticMethod('TargetRegistry_getClosestTargetForJIT', PyObjectPtr, PyObjectPtr)
    targetsList = CustomStaticMethod('TargetRegistry_targets_list', PyObjectPtr)