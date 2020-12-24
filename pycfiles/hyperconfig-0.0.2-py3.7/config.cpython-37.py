# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/hyperconfig/config.py
# Compiled at: 2018-10-24 05:32:37
# Size of source mod 2**32: 242 bytes
import json

class Config(object):

    def __init__(self, dict):
        vars(self).update(dict)


def loadconfig(json_file):
    with open(json_file, 'r') as (j):
        json_str = j.read()
    return json.loads(json_str, object_hook=Config)