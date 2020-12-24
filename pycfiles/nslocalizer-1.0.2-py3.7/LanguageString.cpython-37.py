# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nslocalizer/Language/LanguageString.py
# Compiled at: 2019-02-23 14:43:18
# Size of source mod 2**32: 2624 bytes


def HasStringForLanguage(string, language) -> bool:
    result = False
    for lang_string in language.strings:
        result = string == lang_string.string
        if result is True:
            break

    return result


class LanguageString(object):

    def __init__(self, string_key, string_value):
        self.line_number = 0
        self.string = string_key
        self.value = string_value
        self.base = None
        self.mapping = dict()

    def __repr__(self) -> str:
        return str(self.string)

    def registerBase(self, base_language):
        self.base = base_language

    def processMapping(self, base_language, additional_languages) -> (
 object, list):
        self.registerBase(base_language)
        results = [(language, HasStringForLanguage(self.string, language)) for language in additional_languages]
        self.mapping = dict(results)
        missing_keys = [key for key in self.mapping if self.mapping[key] is False]
        return (self, missing_keys)