# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nslocalizer/Finder/LanguageFinder.py
# Compiled at: 2019-02-23 14:43:18
# Size of source mod 2**32: 4310 bytes
import Helpers.Logger as Logger
import xcodeproj.pbProj as pbProj
import xcodeproj.pbProj.PBXVariantGroup as PBXVariantGroup
from . import PathFinder

def FilterByName(items, name) -> PBXVariantGroup:
    matched_items = [item for item in items if item.store[pbProj.PBX_Constants.kPBX_REFERENCE_name] == name]
    if len(matched_items):
        matched_items = matched_items[0]
    else:
        matched_items = None
    return matched_items


class LanguageFinder(object):
    localizable_strings = None
    localizable_stringsdict = None
    strings_file_refs = list()
    stringsdict_file_refs = list()

    @classmethod
    def getLocalizationFiles(cls, project) -> (dict, dict):
        if cls.localizable_strings is None or cls.localizable_stringsdict is None:
            variant_groups = [pbx_object for pbx_object in project.pbx_objects if isinstance(pbx_object, PBXVariantGroup)]
            if cls.localizable_strings is None:
                Logger.write().info('Filtering for Localizable.strings files...')
                cls.localizable_strings = FilterByName(variant_groups, 'Localizable.strings')
            if cls.localizable_stringsdict is None:
                Logger.write().info('Filtering for Localizable.stringsdict files...')
                cls.localizable_stringsdict = FilterByName(variant_groups, 'Localizable.stringsdict')
        if len(cls.strings_file_refs) == 0 or len(cls.stringsdict_file_refs) == 0:
            Logger.write().info('Resolving language-specific file paths...')
            if len(cls.strings_file_refs) == 0 and cls.localizable_strings is not None:
                languages = cls.localizable_strings.store[pbProj.PBX_Constants.kPBX_REFERENCE_children]
                cls.strings_file_refs = [PathFinder.resolveFilePathForReference(project, language_file) for language_file in languages]
            else:
                Logger.write().info('Could not find any Localizable.strings files, continuing...')
            if len(cls.stringsdict_file_refs) == 0 and cls.localizable_stringsdict is not None:
                language_dicts = cls.localizable_stringsdict.store[pbProj.PBX_Constants.kPBX_REFERENCE_children]
                cls.stringsdict_file_refs = [PathFinder.resolveFilePathForReference(project, language_file_dict) for language_file_dict in language_dicts]
        else:
            Logger.write().info('Could not find any Localizable.stringsdict files, continuing...')
        return (cls.strings_file_refs, cls.stringsdict_file_refs)