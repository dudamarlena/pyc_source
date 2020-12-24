# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/uniborg/storage.py
# Compiled at: 2019-05-07 16:28:53
import json
from pathlib import Path
FILE_NAME = 'data.json'

class Storage:

    class _Guard:

        def __init__(self, storage):
            self._storage = storage

        def __enter__(self):
            self._storage._autosave = False

        def __exit__(self, *args):
            self._storage._autosave = True
            self._storage._save()

    def __init__(self, root):
        self._root = Path(root)
        self._autosave = True
        self._guard = self._Guard(self)
        if (self._root / FILE_NAME).is_file():
            with open(self._root / FILE_NAME) as (fp):
                self._data = json.load(fp)
        else:
            self._data = {}

    def bulk_save(self):
        return self._guard

    def __getattr__(self, name):
        if name.startswith('_'):
            raise ValueError('You can only access existing private members')
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            self.__dict__[name] = value
        else:
            self._data[name] = value
            if self._autosave:
                self._save()

    def _save(self):
        if not self._root.is_dir():
            self._root(parents=True, exist_ok=True)
        with open(self._root / FILE_NAME, 'w') as (fp):
            json.dump(self._data, fp)