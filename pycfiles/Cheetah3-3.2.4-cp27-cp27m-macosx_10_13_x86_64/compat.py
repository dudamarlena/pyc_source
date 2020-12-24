# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/compat.py
# Compiled at: 2019-09-22 10:12:27
import os, sys, types
PY2 = sys.version_info[0] < 3
if PY2:
    string_type = basestring
    unicode = unicode
else:
    string_type = str
    unicode = str
try:
    RecursionError = RecursionError
except NameError:
    RecursionError = RuntimeError

if PY2:
    import imp

    def load_module_from_file(base_name, module_name, filename):
        fp, pathname, description = imp.find_module(base_name, [os.path.dirname(filename)])
        try:
            module = imp.load_module(module_name, fp, pathname, description)
        finally:
            fp.close()

        return module


    new_module = imp.new_module
    get_suffixes = imp.get_suffixes
else:
    import importlib.machinery, importlib.util

    def load_module_from_file(base_name, module_name, filename):
        specs = importlib.util.spec_from_file_location(module_name, filename)
        return specs.loader.load_module()


    new_module = types.ModuleType

    def get_suffixes():
        extensions = [ (s, 'rb', 3) for s in importlib.machinery.EXTENSION_SUFFIXES ]
        source = [ (s, 'rU', 1) for s in importlib.machinery.SOURCE_SUFFIXES ]
        bytecode = [ (s, 'rb', 2) for s in importlib.machinery.BYTECODE_SUFFIXES ]
        return extensions + source + bytecode