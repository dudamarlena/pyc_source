# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/jlogin/utils/jlib.py
# Compiled at: 2019-09-10 14:41:11
# Size of source mod 2**32: 868 bytes
from os.path import isfile
from json import dump, load

class JsonManager:

    def create_json(self, filepath, dirdata, *args):
        from os import mkdir
        try:
            mkdir(dirdata)
        except OSError:
            pass

        data = {'username':'', 
         'password':''}
        if args:
            data = {'username':f"{args[0]}", 
             'password':f"{args[1]}"}
        with open(filepath, 'w') as (f):
            dump(data, f, indent=2, separators=(',', ': '))

    def read_json(self, filepath):
        if isfile(filepath):
            with open(filepath) as (f):
                data = load(f)
            return data
        return False

    def update_json(self, filepath, data):
        with open(filepath, 'w') as (f):
            dump(data, f, indent=2, separators=(',', ': '))