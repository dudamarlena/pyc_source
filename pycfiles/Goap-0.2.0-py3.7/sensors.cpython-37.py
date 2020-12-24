# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Goap/utils/os/sensors.py
# Compiled at: 2019-07-05 11:36:04
# Size of source mod 2**32: 3070 bytes
from os import listdir
from os.path import isdir, isfile, exists
from lvm2py import *
from Goap.Sensor import *

class OSFilePath(Sensor):

    def __init__(self, binding, name, path):
        self.path = path
        super(Sensor).__init__(binding=binding, name=name)

    def exists(self):
        return exists(self.path)

    def is_dir(self):
        if self.exists():
            return isdir(self.path)
        return False

    def is_file(self):
        if self.exists():
            return isfile(self.path)
        return False

    def content(self):
        if self.exists():
            return ''.join((str(i + '\n') for i in listdir(self.path)))
        return 'not_exist'


class DirectoryExist(OSFilePath):

    def __init__(self, binding, name, path):
        super(Sensor).__init__(binding=binding, name=name, path=path)

    def exec(self):
        return self.is_dir()


class FileExist(OSFilePath):

    def __init__(self, binding, name, path):
        super(Sensor).__init__(binding=binding, name=name, path=path)

    def exec(self):
        return self.is_file()


class FileIsOlderThan(OSFilePath):

    def __init__(self, binding, name, path):
        super(Sensor).__init__(binding=binding, name=name, path=path)

    def is_older(self, days: str):
        pass


class FileNamePattern(OSFilePath):

    def __init__(self, binding, name, path):
        super(Sensor).__init__(binding=binding, name=name, path=path)

    def has_name_pattern(self):
        pass


class FileHasExtension(OSFilePath):

    def __init__(self, binding, name, path):
        super(Sensor).__init__(binding=binding, name=name, path=path)

    def has_extension(self, extension: str):
        pass


class LVM(Sensor):

    def __init__(self, **kwargs):
        self.lvm = LVM()
        self.binding = kwargs.get('binding', None)
        self.binding = kwargs.get('name', None)
        self.vg_name = kwargs.get('vg_name', None)
        self.lv_name = kwargs.get('lv_name', None)
        super(Sensor).__init__(binding=(self.binding), name=(self.name))

    def vg_exists(self):
        try:
            if self.lvm.get_vg(self.vg_name):
                return 'exist'
            return 'not_exist'
        except LookupError as e:
            try:
                raise '{}'.format(e)
            finally:
                e = None
                del e

    def vg_size(self):
        pass

    def vg_available_space(self):
        pass

    def lv_exists(self):
        pass

    def lv_size(self):
        pass


class VGExists(LVM):

    def __init__(self, binding, vg_name):
        super(Sensor).__init__(binding=binding, vg_name=vg_name)

    def exec(self):
        return self.vg_exists()


if __name__ == '__main__':
    pass