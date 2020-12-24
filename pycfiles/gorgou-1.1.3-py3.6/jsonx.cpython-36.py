# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/gorgou/x/jsonx.py
# Compiled at: 2018-02-02 23:22:40
# Size of source mod 2**32: 340 bytes
import json

def load_json(_file):
    return load_file_to_obj(_file)


def load_file_to_obj(_file):
    f = file(_file)
    jsonobj = json.load(f)
    return jsonobj


def load_str_to_obj(str):
    return json.loads(str)


def dump_to_str(obj):
    return json.dumps(obj, ensure_ascii=False)