# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n8f5s77x/tzutil/tzutil/import_json.py
# Compiled at: 2018-12-04 01:36:04
# Size of source mod 2**32: 416 bytes
from os.path import join
from json import load, dump

class ImportJson:

    def __init__(self, root):
        self.root = root

    def __call__(self, path, data=None):
        fpath = join(self.root, path + '.json')
        if data is None:
            with open(fpath) as (f):
                r = load(f)
                return r
        else:
            with open(fpath, 'w') as (f):
                dump(data, f)