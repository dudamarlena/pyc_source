# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jack/code/pain/pain/scaffolds.py
# Compiled at: 2013-04-29 05:42:53
import os, string
from .files import *

class Scaffold(object):

    def __init__(self, name, **config):
        self.config = config
        self.config.update(name=name)
        self.config.update(is_package=True)
        self.files = {}

    def add_file(self, path, f):
        if path not in self.files:
            self.files[path] = []
        self.files[path].append(f)

    def write(self, root_dir):
        if self.config.get('is_package'):
            root_dir = os.path.join(root_dir, self.config.get('name'))
        for path, files in self.files.iteritems():
            for f in files:
                write_path = '%s%s' % (root_dir, os.path.join(string.Template(path).safe_substitute(**self.config), f.name))
                if not os.path.exists(os.path.dirname(write_path)):
                    os.makedirs(os.path.dirname(write_path))
                text = f.template(self.config)
                with open(write_path, 'w+') as (f):
                    f.write(text)


class Default(Scaffold):

    def __init__(self, name, **config):
        super(Default, self).__init__(name, **config)
        self.files = {'/': [
               SetupPy(), SetupCfg(), Requirements(), TODO(), README(), MANIFEST(), TravisYaml(), GitIgnore(), Env()], 
           '/$name': [
                    Init()], 
           '/$name/tests': [
                          Init()]}