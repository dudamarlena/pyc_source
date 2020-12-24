# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/step/Workspace/pypack/pypack.importer/pypack/importer/Importer.py
# Compiled at: 2018-02-14 15:19:13
# Size of source mod 2**32: 640 bytes
import importlib

class Importer:

    @staticmethod
    def get(module=None, name=None):
        if not isinstance(module, str):
            raise TypeError('cannot import module', module)
        if not isinstance(name, str):
            raise TypeError('cannot import function', name)
        return getattr(importlib.import_module(module), name)

    @staticmethod
    def path(path=None, name=None):
        if not isinstance(path, str):
            raise TypeError('cannot import module', path)
        if not isinstance(name, str):
            raise TypeError('cannot import function', name)
        return importlib.machinery.SourceFileLoader(name, path).load_module()