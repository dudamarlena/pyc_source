# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\upxer\StringPytxer.py
# Compiled at: 2018-01-11 18:32:47
# Size of source mod 2**32: 1332 bytes
import re
regex_first_letter_lowercase = re.compile('(^[^A-Z])|\\w([A-Z])')
regex_capitalize_name = re.compile('\\b[^\\s^A-Z]')
regex_abbreviate_name = re.compile('\\s(\\w{1})\\w+')

def is_uncapitalize(text):
    return bool(regex_first_letter_lowercase.search(text))


def is_uncapitalize_name(name):
    return bool(regex_capitalize_name.search(name))


def capitalize(text):
    if is_uncapitalize(text):
        return text[:1].upper() + text[1:].lower()
    else:
        return text


def capitalize_list_of_strings(list_strings):
    return [capitalize(word) for word in list_strings]


def list_to_string(list):
    return ' '.join(str(x) for x in list)


def capitalize_name(name):
    if is_uncapitalize_name(name):
        list_of_substrings = name.split()
        list_of_substrings_capitalize = [capitalize(word) for word in list_of_substrings]
        return list_to_string(list_of_substrings_capitalize)
    else:
        return name


def abbreviate_name(name, max_len=12):
    if len(name) > max_len:
        string_abbreviate_name = regex_abbreviate_name.sub(' \\1.', name)
        string_splitted = string_abbreviate_name.lower().split()
        return list_to_string(capitalize_list_of_strings(string_splitted))
    else:
        return name