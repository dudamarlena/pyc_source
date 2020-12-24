# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nslocalizer/xcodeproj/pbProj/PBXProject.py
# Compiled at: 2019-02-23 14:43:19
# Size of source mod 2**32: 3256 bytes
from . import PBX_Constants
from .PBXItem import PBXItem

class PBXProject_ProjectReference(PBXItem):

    def __init__(self, identifier, dictionary):
        super(self.__class__, self).__init__(identifier, dictionary)

    def __repr__(self):
        return self.store.__repr__()

    def resolveGraph(self, project):
        super(self.__class__, self).resolveGraph(project)
        self.resolveGraphNodeForKey(PBX_Constants.kPBX_PROJECTREF_ProjectRef, project)
        self.resolveGraphNodeForKey(PBX_Constants.kPBX_PROJECTREF_ProductGroup, project)


class PBXProject(PBXItem):

    def __init__(self, identifier, dictionary):
        super(self.__class__, self).__init__(identifier, dictionary)

    def resolveGraph(self, project):
        super(self.__class__, self).resolveGraph(project)
        self.resolveGraphNodeForKey(PBX_Constants.kPBX_TARGET_buildConfigurationList, project)
        self.resolveGraphNodeForKey(PBX_Constants.kPBX_PROJECT_mainGroup, project)
        self.resolveGraphNodeForKey(PBX_Constants.kPBX_PROJECT_productRefGroup, project)
        self.resolveGraphNodesForArray(PBX_Constants.kPBX_PROJECT_targets, project)
        project_references = self.get(PBX_Constants.kPBX_PROJECT_projectReferences, None)
        if project_references:
            resolved_references = list()
            for reference in project_references:
                project_reference = PBXProject_ProjectReference(None, reference)
                project_reference.resolveGraph(project)
                resolved_references.append(project_reference)

            self[PBX_Constants.kPBX_PROJECT_projectReferences] = resolved_references