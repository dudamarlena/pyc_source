# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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