# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/polical/MateriaClass.py
# Compiled at: 2020-05-12 16:47:43
# Size of source mod 2**32: 203 bytes


class Materia:

    def __init__(self, name, codigo, id=''):
        self.id = id
        self.name = name
        self.codigo = codigo

    def print(self):
        print(self.id, self.name, self.codigo)