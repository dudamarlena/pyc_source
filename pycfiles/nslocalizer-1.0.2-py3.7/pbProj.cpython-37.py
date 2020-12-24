# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nslocalizer/xcodeproj/pbProj/pbProj.py
# Compiled at: 2019-02-23 14:43:19
# Size of source mod 2**32: 5561 bytes
import pbPlist
from . import PBX_Constants
from . import PBX_Lookup

class PBXProj(object):

    def __init__(self, file_path):
        plist = pbPlist.pbPlist.PBPlist(file_path)
        contents = plist.root.nativeType()
        self.pbx_objects = set()
        self.pbx_identifier = None
        self.pbx_root_object = None
        self.pbx_object_version = 0
        self.pbx_archive_version = 0
        if contents is not None:
            self.pbx_file_path = plist.file_path
            self.pbx_identifier = contents.get(PBX_Constants.kPBX_rootObject, None)
            archive_version = contents.get(PBX_Constants.kPBX_archiveVersion, None)
            if archive_version:
                self.pbx_archive_version = int(archive_version)
            object_version = contents.get(PBX_Constants.kPBX_objectVersion, None)
            if object_version:
                self.pbx_object_version = int(object_version)
            self.pbx_classes = contents.get(PBX_Constants.kPBX_classes, None)
            objects_dict = contents.get(PBX_Constants.kPBX_objects, None)
            self.pbx_objects = [PBX_Lookup.PBX_Type_Resolver(entry, value) for entry, value in list(objects_dict.items())]
            self.pbx_root_object = self.objectForIdentifier(self.pbx_identifier)
            self.pbx_root_object.resolveGraph(self)

    def __repr__(self):
        rep_string = '<%s : INVALID OBJECT>' % self.__class__.__name__
        if self.isValid():
            rep_string = '<%s : %s : %s>' % (self.__class__.__name__, self.pbx_identifier, self.pbx_file_path)
        return rep_string

    def __attrs(self):
        return (
         self.pbx_identifier, self.pbx_file_path)

    def __eq__(self, other):
        return isinstance(other, PBXProj) and self.pbx_identifier == other.pbx_identifier and self.pbx_file_path == other.pbx_file_path

    def __hash__(self):
        return hash(self._PBXProj__attrs())

    def isValid(self):
        return self.pbx_identifier is not None

    def objectForIdentifier(self, identifier):
        """
        Returns the parsed object from the project file for matching identifier, if no matching object is found it will return None.
        """
        result = None
        if self.isValid():
            filter_results = [pbx_object for pbx_object in self.pbx_objects if pbx_object.identifier == identifier]
            if len(filter_results):
                result = filter_results[0]
        return result

    def projects(self):
        """
        This method returns a set of 'xcodeproj' objects that represents any referenced
        xcodeproj files in this project.
        """
        subprojects = set()
        if self.isValid():
            subprojects = [path for path in self._PBXProj__subproject_paths()]
        return subprojects

    def __subproject_paths(self):
        """
        This method is for returning a list of paths to referenced project files in this
        xcodeproj file.
        """
        paths = list()
        if self.isValid():
            project_references = self.pbx_root_object.get(PBX_Constants.kPBX_PROJECT_projectReferences, None)
            if project_references:
                paths = [project_dict[PBX_Constants.kPBX_PROJECTREF_ProjectRef] for project_dict in project_references]
        return paths

    def targets(self):
        """
        This method will return a list of build targets that are associated with this xcodeproj.
        """
        targets = list()
        if self.isValid():
            target_list = self.pbx_root_object.get(PBX_Constants.kPBX_PROJECT_targets, None)
            if target_list:
                targets.extend(target_list)
        return targets