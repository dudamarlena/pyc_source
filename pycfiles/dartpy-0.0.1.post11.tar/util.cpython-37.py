# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/js/dev/prl/dart/pybind11/python/tests/util.py
# Compiled at: 2019-05-16 01:57:01
# Size of source mod 2**32: 472 bytes
import inspect, os, os.path

def get_path_to_this_file():
    return inspect.getfile(inspect.currentframe())


def get_asset_path(rel_path, check_existing=False):
    if rel_path.startswith('/'):
        full_path = rel_path
    else:
        full_path = os.path.join(os.path.dirname(__file__), '../../data/', rel_path)
    if check_existing:
        if not os.path.exists(full_path):
            raise IOError('File %s does not exist' % full_path)
    return full_path