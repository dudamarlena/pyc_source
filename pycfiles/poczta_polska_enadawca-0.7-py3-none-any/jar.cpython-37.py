# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/helper/archieve/jar.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 1403 bytes
import os
from .zip import Zip

class Jar(Zip):

    def __init__(self, filename=''):
        Zip.__init__(self, filename)
        self.manifest = self.get_manifest()
        self.is_manifest_created = False

    def get_manifest(self, main_class='pocsuite.Payload'):
        manifest = 'Manifest-Version: 1.0\n'
        manifest += 'Main-Class: %s\n' % main_class
        manifest += 'Permissions: all-permissions\n\n'
        return manifest

    def add_file(self, name, content='', write_to_manifest=True):
        Zip.add_file(self, name, content)
        if write_to_manifest:
            self._Jar__add_file_to_manifest(name)

    def __add_file_to_manifest(self, filename):
        self.manifest += 'Name: {filename}\n\n'.format(filename=filename)

    def create_manifest(self):
        self.add_file('META-INF/MANIFEST.MF', (self.manifest), write_to_manifest=False)
        self.is_manifest_created = True

    def get_raw(self, remove_temp=False):
        if not self.is_manifest_created:
            self.create_manifest()
        if not self.name:
            print('You should create jar file before get raw content')
        with open(self.name, 'rb') as (f):
            content = f.read()
        if remove_temp:
            os.remove(self.name)
        return content

    def get_jar(self):
        if not self.is_manifest_created:
            self.create_manifest()
        return self.name