# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pypitestjson\pypitestjson.py
# Compiled at: 2020-03-10 06:36:13
# Size of source mod 2**32: 336 bytes
import os, sys, json

def load_dict(self, filename):
    with open(filename, 'r') as (json_file):
        dic = json.load(json_file)
    return dic


def save_dict(self, filename, dic):
    with open(filename, 'w') as (json_file):
        json.dump(dic, json_file)