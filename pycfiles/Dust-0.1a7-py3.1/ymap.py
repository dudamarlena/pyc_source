# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/util/ymap.py
# Compiled at: 2010-06-01 17:17:21
import os, yaml

class YamlMap:

    def __init__(self, filename):
        self.filename = filename
        if os.path.exists(filename):
            f = open(self.filename, 'r')
            self.map = yaml.load(f)
            f.close()
        else:
            self.map = {}

    def getWithDefault(self, key, default):
        if key in self.map.keys():
            return self.map[key]
        else:
            return default

    def __getitem__(self, key):
        return self.map[key]

    def __setitem__(self, key, value):
        self.map[key] = value
        self.save()

    def keys(self):
        return self.map.keys()

    def values(self):
        return self.map.values()

    def save(self):
        f = open(self.filename, 'w')
        yaml.dump(self.map, f)
        f.close()