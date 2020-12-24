# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/catchbot/message/content/static.py
# Compiled at: 2018-06-23 13:58:03
# Size of source mod 2**32: 843 bytes


def _get_value_by_path(json_obj, path):
    value = json_obj
    for path_key in path.split('.'):
        value = value[path_key]

    return value


def _get_value_by_variants(json_obj, path_with_variants):
    variants = path_with_variants.split('|')
    value = None
    for variant in variants:
        try:
            value = _get_value_by_path(json_obj, variant)
        except KeyError:
            continue

    if not value:
        value = '!' + path_with_variants
    return value


def get_static_msg_content(mapping, json_obj):
    result = {}
    for key, value_obj in mapping.items():
        if not isinstance(value_obj, str):
            result[key] = get_static_msg_content(value_obj, json_obj)
        else:
            path = value_obj
            result[key] = _get_value_by_variants(json_obj, path)

    return result