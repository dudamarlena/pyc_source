# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/lib/validator.py
# Compiled at: 2017-11-16 20:28:41
from sets import Set

def validate_dictionary(dictionary, supported_keys, required_fields):
    validation_errors = {}
    missing_fields = find_missing_fields(dictionary, required_fields)
    unsupported_keys = find_unsupported_keys(dictionary, supported_keys)
    if missing_fields:
        validation_errors['missing-fields'] = missing_fields
    if unsupported_keys:
        validation_errors['unsupported-keys'] = unsupported_keys
    return validation_errors


def find_unsupported_keys(dictionary, supported_keys):
    key_ustring_list = dictionary.keys()
    key_string_list = []
    for key_ustring in key_ustring_list:
        key_string_list = key_string_list + [str(key_ustring)]

    unsupported_keys = list(Set(key_string_list) - Set(supported_keys))
    return unsupported_keys


def find_missing_fields(dictionary, required_fields):
    missing_fields = []
    for i, field_path in enumerate(required_fields):
        path_parts = field_path.split('.')
        path_len = len(path_parts)
        if path_len == 1 and path_parts[0] not in dictionary:
            missing_fields = missing_fields + [required_fields[i]]
        elif path_len == 2 and (path_parts[0] not in dictionary or path_parts[1] not in dictionary[path_parts[0]]):
            missing_fields = missing_fields + [required_fields[i]]
        elif path_len == 3 and (path_parts[0] not in dictionary or path_parts[1] not in dictionary[path_parts[0]] or path_parts[2] not in dictionary[path_parts[0]][path_parts[1]]):
            missing_fields = missing_fields + [required_fields[i]]
        elif path_len == 4 and (path_parts[0] not in dictionary or path_parts[1] not in dictionary[path_parts[0]] or path_parts[2] not in dictionary[path_parts[0]][path_parts[1]] or path_parts[3] not in dictionary[path_parts[0]][path_parts[1]][path_parts[2]]):
            missing_fields = missing_fields + [required_fields[i]]

    return missing_fields