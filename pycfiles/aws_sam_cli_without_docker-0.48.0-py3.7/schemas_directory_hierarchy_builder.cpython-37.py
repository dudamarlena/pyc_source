# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/schemas/schemas_directory_hierarchy_builder.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 1028 bytes
""" Responsible for building schema code directory hierarchy based on schema name """
import re
CHARACTER_TO_SANITIZE = '[^a-zA-Z0-9_@]'
POTENTIAL_PACKAGE_SEPARATOR = '[@]'

def get_package_hierarchy(schema_name):
    path = 'schema'
    if schema_name.startswith('aws.partner-'):
        path = path + '.aws.partner'
        tail = schema_name[len('aws.partner-'):]
        path = path + '.' + sanitize_name(tail)
        return path.lower()
    if schema_name.startswith('aws.'):
        parts = schema_name.split('.')
        for part in parts:
            path = path + '.'
            path = path + sanitize_name(part)

        return path.lower()
    return f"{path}.{sanitize_name(schema_name)}".lower()


def sanitize_name(name):
    name = re.sub(CHARACTER_TO_SANITIZE, '_', name)
    return re.sub(POTENTIAL_PACKAGE_SEPARATOR, '.', name)