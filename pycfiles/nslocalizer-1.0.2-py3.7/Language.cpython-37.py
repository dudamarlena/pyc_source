# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nslocalizer/Language/Language.py
# Compiled at: 2019-02-23 14:43:18
# Size of source mod 2**32: 3921 bytes
import os, langcodes
from pbPlist import pbPlist
from .LanguageString import LanguageString
import Helpers.Logger as Logger
import Helpers.FileOperations as FileOperations

def GetLanguageCodeFromPath(path) -> str:
    dirname = os.path.dirname(path)
    basename = os.path.basename(dirname)
    locale, _ = os.path.splitext(basename)
    return locale


def FindLineIndex(data, string) -> int:
    line_index = 0
    localized_string_entry = '"' + str(string) + '"'
    if data is not None:
        position = data.find(localized_string_entry)
        line_index = data[:position].count('\n') + 1
    return line_index


def LoadStrings(file_path) -> list:
    strings_file_contents = pbPlist.PBPlist(file_path)
    results = [LanguageString(localized_string_key, strings_file_contents.root[localized_string_key]) for localized_string_key in list(strings_file_contents.root.keys())]
    return results


class Language(object):

    def __init__(self, strings_file_path):
        self.code = GetLanguageCodeFromPath(strings_file_path)
        self.name = langcodes.LanguageData(language=(self.code)).language_name()
        self.strings_file = strings_file_path
        self.stringsdict_file = None
        self.stringsdict = None
        self.strings = LoadStrings(self.strings_file)

    def findStrings(self) -> None:
        strings_missing_line_numbers = [lstring for lstring in self.strings if lstring.line_number == 0]
        if len(strings_missing_line_numbers):
            Logger.write().info('Resolving line numbers...')
            data = FileOperations.getData(self.strings_file)
            for lstring in strings_missing_line_numbers:
                lstring.line_number = FindLineIndex(data, lstring.string)

    def loadStringsDictFile(self, stringsdict_file_array) -> None:
        for stringsdict_file in stringsdict_file_array:
            dict_locale = GetLanguageCodeFromPath(stringsdict_file)
            if self.code == dict_locale:
                self.stringsdict_file = stringsdict_file
                break

        if self.stringsdict_file is not None:
            self.stringsdict = LoadStrings(self.stringsdict_file)

    def __repr__(self) -> str:
        return '<%s : %s>' % (type(self).__name__, self.name)