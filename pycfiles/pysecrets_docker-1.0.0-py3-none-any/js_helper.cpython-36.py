# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pysecret-project/pysecret/js_helper.py
# Compiled at: 2019-04-10 20:34:51
# Size of source mod 2**32: 800 bytes
import os

def create_json_if_not_exists(path):
    if not os.path.exists(path):
        with open(path, 'wb') as (f):
            f.write('{}'.encode('utf-8'))


def set_value(data, json_path, value):
    paths = json_path.split('.')
    path_length = len(paths)
    for ind, key in enumerate(paths):
        if ind == path_length - 1:
            data[key] = value
        else:
            data.setdefault(key, {})
            data = data[key]

    return data


def get_value(data, json_path):
    paths = json_path.split('.')
    value = data
    for key in paths:
        value = value[key]

    return value


def del_key(data, json_path):
    paths = json_path.split('.')
    for key in paths[:-1]:
        data = data[key]

    del data[paths[(-1)]]