# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryosukekita/Desktop/PROJECTS/DSVISUALIZER/aefiles/scripts/load_funcs.py
# Compiled at: 2018-01-30 18:26:46
import json

def _byteify(data, ignore_dicts=False):
    """
    DESCRIPTION:
    - https://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-from-json

    """
    if isinstance(data, unicode):
        return data.encode('utf-8')
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    if isinstance(data, dict) and not ignore_dicts:
        return {_byteify(key, ignore_dicts=True):_byteify(value, ignore_dicts=True) for key, value in data.iteritems()}
    return data


def json_load_byteified(file_handle):
    return _byteify(json.load(file_handle, object_hook=_byteify), ignore_dicts=True)


def read_csv(file):
    with open(file) as (F):
        outArray = [ x.rstrip().split(',') for x in F.readlines() ]
    return outArray