# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nslocalizer/Executor/Executor.py
# Compiled at: 2019-02-23 14:43:18
# Size of source mod 2**32: 6742 bytes
import os, re, sys
import Helpers.Logger as Logger
import Helpers.FileOperations as FileOperations
from ..Language import Language
from ..Reporter import Reporter
import xcodeproj.xcodeproj as xcodeproj
import Finder.LanguageFinder as LanguageFinder
from ..Finder import CodeFinder

class Executor(object):
    base_language = None
    additional_languages = None

    @classmethod
    def run(cls, arguments) -> None:
        has_set_flag = arguments.find_missing or arguments.find_unused
        can_run = arguments.project and len(arguments.target) > 0 and has_set_flag
        xcodeproj_file = None
        desired_targets = list()
        if can_run:
            Logger.write().info('Loading project file...')
            project_file_path = os.path.normpath(arguments.project)
            xcodeproj_file = xcodeproj(project_file_path)
            Logger.write().info('Search for target "%s" in project "%s"' % (arguments.target, os.path.basename(project_file_path)))
            desired_targets = [target for target in xcodeproj_file.project_file.targets() if target['name'] in arguments.target]
        else:
            Logger.write().error('Please specify a project (--project) with a valid target (--target), and at least one search flag (--find-unused, --find-missing).')
        if xcodeproj is not None and len(desired_targets) == len(arguments.target):
            missing_strings = dict()
            unused_strings = dict()
            if arguments.find_missing:
                missing_strings = cls.findMissingStrings(xcodeproj_file, desired_targets)
                Reporter.logMissingStrings(missing_strings, arguments.ignore, arguments.error)
            if arguments.find_unused:
                unused_strings = cls.findUnusedStrings(xcodeproj_file, desired_targets)
                Reporter.logUnusedStrings(unused_strings, arguments.error)
        else:
            missing_targets = [target for target in arguments.target if target not in desired_targets]
            Logger.write().info('Could not find target "%s" in the specified project file.' % '", "'.join(missing_targets))

    @classmethod
    def findMissingStrings(cls, project, targets) -> dict:
        Logger.write().info('Finding strings that are missing from language files...')
        _ = targets
        base_language, additional_languages = cls.generateLanguages(project)
        missing_results = [string.processMapping(base_language, additional_languages) for string in base_language.strings]
        return dict(missing_results)

    @classmethod
    def findUnusedStrings(cls, project, targets) -> list:
        Logger.write().info('Finding strings that are unused but are in language files...')
        code_files = list()
        for target in targets:
            code_files.extend(CodeFinder.getCodeFileList(project.project_file, target))

        base_language, _ = cls.generateLanguages(project)
        known_strings = set()
        for source_code_file in code_files:
            data = FileOperations.getData(source_code_file)
            if data is None:
                continue
            matches = re.findall('NSLocalizedString\\(@?\\"(.*?)\\",', data)
            Logger.write().debug('%s: %i results' % (os.path.basename(source_code_file), len(matches)))
            known_strings.update(matches)

        unused_strings = [lstring for lstring in base_language.strings if lstring.string not in known_strings]
        for unused_string in unused_strings:
            unused_string.registerBase(base_language)

        return unused_strings

    @classmethod
    def generateLanguages(cls, project) -> (Language, {Language}):
        strings_files, stringsdict_files = LanguageFinder.getLocalizationFiles(project.project_file)
        languages = set([Language.Language(path) for path in strings_files])
        for language in languages:
            language.loadStringsDictFile(stringsdict_files)

        if cls.base_language is None:
            if cls.additional_languages is None:
                cls.additional_languages = set([language for language in languages if language.code != 'Base'])
                if len(cls.additional_languages) == len(languages):
                    Logger.write().info('Could not find a "Base" language, assuming "English"...')
                    cls.additional_languages = set([language for language in languages if language.code != 'en'])
                if len(cls.additional_languages) == len(languages):
                    Logger.write().error('Unable to locate the "Base" language, please assign one in the project file!')
                    sys.exit(1)
                other_languages = languages.difference(cls.additional_languages)
                cls.base_language = other_languages.pop()
                cls.base_language.findStrings()
        return (
         cls.base_language, cls.additional_languages)