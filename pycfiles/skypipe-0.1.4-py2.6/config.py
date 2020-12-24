# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/dotcloud/ui/config.py
# Compiled at: 2012-09-19 14:56:08
import os, json
CLIENT_KEY = '9b8d4bc07a4a60f7536cafd46ec492'
CLIENT_SECRET = '2fa7e44a09e3c9b7d63de7ffb97112'

class GlobalConfig(object):

    def __init__(self):
        self.dir = os.path.expanduser('~/.dotcloud_cli')
        self.path = self.path_to('config')
        self.key = self.path_to('dotcloud.key')
        self.load()

    def path_to(self, name):
        path = os.path.join(self.dir, name)
        if os.environ.get('SETTINGS_FLAVOR'):
            path = path + '.' + os.environ.get('SETTINGS_FLAVOR')
        return path

    def load(self):
        try:
            self.data = json.load(file(self.path))
            self.loaded = True
        except (IOError, ValueError):
            self.loaded = False

    def save(self):
        if not os.path.exists(self.dir):
            os.mkdir(self.dir, 448)
        try:
            f = open(self.path, 'w+')
            json.dump(self.data, f, indent=4)
        except:
            raise

    def get(self, *args):
        if not self.loaded:
            return None
        else:
            return self.data.get(*args)

    def save_key(self, key):
        f = open(self.key, 'w')
        f.write(key)
        try:
            os.fchmod(f.fileno(), 384)
        except:
            pass

        f.close()