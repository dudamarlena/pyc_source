# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/helper/archieve/zip.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 1126 bytes
import zipfile

class Zip:

    def __init__(self, filename=''):
        self.name = filename
        self.files = set()
        if filename:
            self.create_archieve(filename)

    def create_archieve(self, filename):
        if not self.name:
            self.name = filename
        zf = zipfile.ZipFile(filename, 'w')
        zf.close()

    def add_file(self, name, content=''):
        if not self.is_valid(name):
            return
        else:
            zf = zipfile.ZipFile(self.name, 'a')
            if content:
                zf.writestr(name, content)
            else:
                zf.write(name)
        zf.close()
        self.files.add(name)

    def is_valid(self, filename=''):
        if not self.name:
            raise Exception('Error. Zip archieve is not created.')
            return False
        else:
            assert zipfile.is_zipfile(self.name), 'Error. File {name} is not zip archieve.'.format(name=(self.name))
            return False
        if filename:
            if filename in self.files:
                raise Exception('Error. There is file with the same name.')
                return False
        return True