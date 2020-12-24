# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/project/datamaestro/registry.py
# Compiled at: 2020-02-25 07:34:23
# Size of source mod 2**32: 1409 bytes
from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile

class RegistryEntry:

    def __init__(self, registry, key):
        self.key = key
        self.dicts = []
        _key = ''
        for subkey in self.key.split('.'):
            _key = '%s.%s' % (_key, subkey) if _key else subkey
            if _key in registry.content:
                self.dicts.insert(0, registry.content[_key])

    def get(self, key, default):
        for d in self.dicts:
            if key in d:
                return d[key]

        return default

    def __getitem__(self, key):
        for d in self.dicts:
            if key in d:
                return d[key]

        raise KeyError(key)


class Registry:

    def __init__(self, path: Path):
        self.path = path
        self.dirty = False
        self.data = {}
        if path.is_file():
            with path.open('r') as (fp):
                for key, value in yaml.load(fp, Loader=(yaml.BaseLoader)).items():
                    self.data[key] = value

    def __getitem__(self, key):
        return RegistryEntry(self, key)

    def __setitem__(self, key, value):
        self.dirty = True
        self.data[key] = value

    def save(self):
        if self.dirty:
            with NamedTemporaryFile('w', delete=False) as (f):
                yaml.dump(self.data, f)
            shutil.move(f.name, self.path)
            self.dirty = False