# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nslocalizer/Finder/CodeFinder.py
# Compiled at: 2019-02-23 14:43:18
# Size of source mod 2**32: 2570 bytes
import Helpers.Logger as Logger
import xcodeproj.pbProj as pbProj
import xcodeproj.pbProj.PBXSourcesBuildPhase as PBXSourcesBuildPhase
from . import PathFinder

def getCodeFileList(project, target) -> list:
    Logger.write().info('Finding Code files for target "%s"...' % target[pbProj.PBX_Constants.kPBX_TARGET_name])
    build_phases = target.store[pbProj.PBX_Constants.kPBX_TARGET_buildPhases]
    source_phases = [build_phase for build_phase in build_phases if isinstance(build_phase, PBXSourcesBuildPhase)]
    all_build_files = list()
    for phase in source_phases:
        all_build_files.extend(phase.store[pbProj.PBX_Constants.kPBX_PHASE_files])

    all_file_refs = [PathFinder.resolveFilePathForReference(project, build_file.store[pbProj.PBX_Constants.kPBX_BUILDFILE_fileRef]) for build_file in all_build_files]
    return all_file_refs