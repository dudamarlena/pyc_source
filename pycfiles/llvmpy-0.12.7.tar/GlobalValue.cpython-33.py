# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/GlobalValue.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 1783 bytes
from binding import *
from .namespace import llvm
from .Value import GlobalValue
from .Module import Module
from .ADT.StringRef import StringRef

@GlobalValue
class GlobalValue:
    if LLVM_VERSION >= (3, 3):
        _include_ = 'llvm/IR/GlobalValue.h'
    else:
        _include_ = 'llvm/GlobalValue.h'
    LinkageTypes = Enum('\n        ExternalLinkage, AvailableExternallyLinkage, LinkOnceAnyLinkage,\n        LinkOnceODRLinkage, LinkOnceODRAutoHideLinkage, WeakAnyLinkage,\n        WeakODRLinkage, AppendingLinkage, InternalLinkage, PrivateLinkage,\n        LinkerPrivateLinkage, LinkerPrivateWeakLinkage, DLLImportLinkage,\n        DLLExportLinkage, ExternalWeakLinkage, CommonLinkage\n        ')
    VisibilityTypes = Enum('DefaultVisibility,\n                              HiddenVisibility,\n                              ProtectedVisibility')
    setLinkage = Method(Void, LinkageTypes)
    getLinkage = Method(LinkageTypes)
    setVisibility = Method(Void, VisibilityTypes)
    getVisibility = Method(VisibilityTypes)
    setLinkage = Method(Void, LinkageTypes)
    getLinkage = Method(LinkageTypes)
    getAlignment = Method(cast(Unsigned, int))
    setAlignment = Method(Void, cast(int, Unsigned))
    hasSection = Method(cast(Bool, bool))
    getSection = Method(cast(ConstStdString, str))
    setSection = Method(Void, cast(str, StringRef))
    isDiscardableIfUnused = Method(cast(Bool, bool))
    mayBeOverridden = Method(cast(Bool, bool))
    isWeakForLinker = Method(cast(Bool, bool))
    copyAttributesFrom = Method(Void, ptr(GlobalValue))
    destroyConstant = Method()
    isDeclaration = Method(cast(Bool, bool))
    removeFromParent = Method()
    eraseFromParent = Method()
    eraseFromParent.disowning = True
    getParent = Method(ownedptr(Module))