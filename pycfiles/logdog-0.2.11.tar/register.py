# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miph/Development/logdog/python-logdog/logdog/core/register.py
# Compiled at: 2015-04-04 17:37:36
from __future__ import absolute_import, unicode_literals
import anydbm, json, os
from logdog.core.path import Path

class Register(object):

    def __init__(self, index_file, reset=False):
        self._index_file = os.path.expandvars(os.path.expanduser(index_file))
        if not os.path.exists(os.path.dirname(self._index_file)):
            os.makedirs(os.path.dirname(self._index_file))
        self._reg = anydbm.open(self._index_file, b'c')
        if reset:
            self._reg.clear()

    def set(self, key, val):
        self._reg[str(key)] = str(val)

    def get(self, key):
        return self._reg[key]

    def __getitem__(self, item):
        return self._reg[item]

    def get_path(self, name):
        path = Path(b'', 0, None)
        path.__setstate__(json.loads(self.get(name)))
        return path

    def set_path(self, path_obj):
        self.set(path_obj.name, json.dumps(path_obj.__getstate__()))