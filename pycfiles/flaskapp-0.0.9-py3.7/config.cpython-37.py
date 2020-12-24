# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/flaskapp/config.py
# Compiled at: 2019-07-24 05:34:04
# Size of source mod 2**32: 293 bytes
from pathlib import Path
p = Path(__file__)
ROOT_DIR = p.parent.resolve()
BASE_DIR = ROOT_DIR.joinpath('base')
TEMP_DIR = ROOT_DIR.joinpath('temp')
if __name__ == '__main__':
    _locals = dict(locals())
    for k, v in _locals.items():
        if '_DIR' in k:
            print(k, ':', v)