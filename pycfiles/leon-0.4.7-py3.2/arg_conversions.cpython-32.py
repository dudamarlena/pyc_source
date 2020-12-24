# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/leon/arg_conversions.py
# Compiled at: 2013-05-03 04:46:44
NOT_OPTIONAL_MARKER = object()

class list_of:

    def __init__(self, member_type):
        self.member_type = member_type

    def convert_list(self, alist):
        return [convert_to_type(i, self.member_type) for i in alist]


def convert_to_type(value, default_value_or_type):
    if type(default_value_or_type) is type:
        target_type = default_value_or_type
    else:
        target_type = type(default_value_or_type)
    if target_type is int:
        return int(value)
    if target_type is bool:
        val = value.lower().strip()
        if val in ('true', 'on', 'yes', '1'):
            return True
        if val in ('false', 'off', 'no', '0'):
            return False
        raise Exception('The string "%s" can not be converted to a bool value. Supported values are: true/false, on/off, 1/0, yes/no' % value)
    if target_type is list and type(value) != list:
        return list(value)
    if isinstance(default_value_or_type, list_of):
        value = value if isinstance(value, list) else [value]
        return default_value_or_type.convert_list(value)
    return value