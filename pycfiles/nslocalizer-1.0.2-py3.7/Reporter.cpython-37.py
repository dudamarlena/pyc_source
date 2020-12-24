# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nslocalizer/Reporter/Reporter.py
# Compiled at: 2019-02-23 14:43:18
# Size of source mod 2**32: 3337 bytes


def log(file_name, line_number, type_string, message_string) -> None:
    message = '%s:%s: %s: %s' % (file_name, line_number, type_string, message_string)
    ascii_message = message.encode('ascii', 'replace')
    display_message = ascii_message.decode('ascii', 'ignore')
    print(display_message)


def logError(file_name, line_number, message_string) -> None:
    log(file_name, line_number, 'error', message_string)


def logWarning(file_name, line_number, message_string) -> None:
    log(file_name, line_number, 'warning', message_string)


def logMissingStrings(warnings_dictionary, ignore_languages, is_error=False) -> None:
    keys = list(warnings_dictionary.keys())
    keys.sort(key=(lambda string: string.line_number))
    for key in keys:
        locale_names = [language.name for language in warnings_dictionary.get(key) if language.code not in ignore_languages]
        if len(locale_names):
            message = ', '.join(locale_names)
            message_string = 'String "%s" missing for: %s' % (key.string, message)
            if is_error is False:
                logWarning(key.base.strings_file, key.line_number, message_string)
            else:
                logError(key.base.strings_file, key.line_number, message_string)


def logUnusedStrings(unused_strings_list, is_error=False) -> None:
    unused_strings_list.sort(key=(lambda string: string.line_number))
    for unused_string in unused_strings_list:
        message = 'String "%s" is not used' % unused_string.string
        if is_error is False:
            logWarning(unused_string.base.strings_file, unused_string.line_number, message)
        else:
            logError(unused_string.base.strings_file, unused_string.line_number, message)