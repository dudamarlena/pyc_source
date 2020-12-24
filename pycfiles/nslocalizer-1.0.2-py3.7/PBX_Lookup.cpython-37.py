# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nslocalizer/xcodeproj/pbProj/PBX_Lookup.py
# Compiled at: 2019-02-23 14:43:19
# Size of source mod 2**32: 5501 bytes
from . import PBX_Constants
from . import PBXItem
from . import PBXAggregateTarget
from . import PBXAppleScriptBuildPhase
from . import PBXApplicationReference
from . import PBXApplicationTarget
from . import PBXBuildFile
from . import PBXBuildRule
from . import PBXBundleReference
from . import PBXBundleTarget
from . import PBXContainerItemProxy
from . import PBXCopyFilesBuildPhase
from . import PBXExecutableFileReference
from . import PBXFileReference
from . import PBXFrameworkReference
from . import PBXFrameworksBuildPhase
from . import PBXFrameworkTarget
from . import PBXGroup
from . import PBXHeadersBuildPhase
from . import PBXJavaArchiveBuildPhase
from . import PBXLegacyTarget
from . import PBXLibraryReference
from . import PBXLibraryTarget
from . import PBXNativeTarget
from . import PBXProject
from . import PBXReferenceProxy
from . import PBXResourcesBuildPhase
from . import PBXRezBuildPhase
from . import PBXShellScriptBuildPhase
from . import PBXSourcesBuildPhase
from . import PBXStandAloneTarget
from . import PBXTargetDependency
from . import PBXToolTarget
from . import PBXVariantGroup
from . import PBXZipArchiveReference
from . import XCBuildConfiguration
from . import XCConfigurationList
from . import XCVersionGroup
PBX_TYPE_TABLE = {'PBXAggregateTarget':PBXAggregateTarget.PBXAggregateTarget, 
 'PBXAppleScriptBuildPhase':PBXAppleScriptBuildPhase.PBXAppleScriptBuildPhase, 
 'PBXApplicationReference':PBXApplicationReference.PBXApplicationReference, 
 'PBXApplicationTarget':PBXApplicationTarget.PBXApplicationTarget, 
 'PBXBuildFile':PBXBuildFile.PBXBuildFile, 
 'PBXBuildRule':PBXBuildRule.PBXBuildRule, 
 'PBXBundleReference':PBXBundleReference.PBXBundleReference, 
 'PBXBundleTarget':PBXBundleTarget.PBXBundleTarget, 
 'PBXContainerItemProxy':PBXContainerItemProxy.PBXContainerItemProxy, 
 'PBXCopyFilesBuildPhase':PBXCopyFilesBuildPhase.PBXCopyFilesBuildPhase, 
 'PBXExecutableFileReference':PBXExecutableFileReference.PBXExecutableFileReference, 
 'PBXFileReference':PBXFileReference.PBXFileReference, 
 'PBXFrameworkReference':PBXFrameworkReference.PBXFrameworkReference, 
 'PBXFrameworksBuildPhase':PBXFrameworksBuildPhase.PBXFrameworksBuildPhase, 
 'PBXFrameworkTarget':PBXFrameworkTarget.PBXFrameworkTarget, 
 'PBXGroup':PBXGroup.PBXGroup, 
 'PBXHeadersBuildPhase':PBXHeadersBuildPhase.PBXHeadersBuildPhase, 
 'PBXJavaArchiveBuildPhase':PBXJavaArchiveBuildPhase.PBXJavaArchiveBuildPhase, 
 'PBXLegacyTarget':PBXLegacyTarget.PBXLegacyTarget, 
 'PBXLibraryReference':PBXLibraryReference.PBXLibraryReference, 
 'PBXLibraryTarget':PBXLibraryTarget.PBXLibraryTarget, 
 'PBXNativeTarget':PBXNativeTarget.PBXNativeTarget, 
 'PBXProject':PBXProject.PBXProject, 
 'PBXReferenceProxy':PBXReferenceProxy.PBXReferenceProxy, 
 'PBXResourcesBuildPhase':PBXResourcesBuildPhase.PBXResourcesBuildPhase, 
 'PBXRezBuildPhase':PBXRezBuildPhase.PBXRezBuildPhase, 
 'PBXShellScriptBuildPhase':PBXShellScriptBuildPhase.PBXShellScriptBuildPhase, 
 'PBXSourcesBuildPhase':PBXSourcesBuildPhase.PBXSourcesBuildPhase, 
 'PBXStandAloneTarget':PBXStandAloneTarget.PBXStandAloneTarget, 
 'PBXTargetDependency':PBXTargetDependency.PBXTargetDependency, 
 'PBXToolTarget':PBXToolTarget.PBXToolTarget, 
 'PBXVariantGroup':PBXVariantGroup.PBXVariantGroup, 
 'PBXZipArchiveReference':PBXZipArchiveReference.PBXZipArchiveReference, 
 'XCBuildConfiguration':XCBuildConfiguration.XCBuildConfiguration, 
 'XCConfigurationList':XCConfigurationList.XCConfigurationList, 
 'XCVersionGroup':XCVersionGroup.XCVersionGroup}

def PBX_Type_Resolver(identifier, dictionary):
    object_type = dictionary.get(PBX_Constants.kPBX_isa, None)
    result = None
    if object_type:
        result = PBX_TYPE_TABLE.get(object_type, PBXItem.PBXItem)(identifier, dictionary)
    return result