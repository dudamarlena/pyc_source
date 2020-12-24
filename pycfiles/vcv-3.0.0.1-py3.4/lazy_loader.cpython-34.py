# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/util/lazy_loader.py
# Compiled at: 2018-06-15 01:22:48
# Size of source mod 2**32: 2006 bytes
"""A LazyLoader class."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import importlib, types

class LazyLoader(types.ModuleType):
    __doc__ = 'Lazily import a module, mainly to avoid pulling in large dependencies.\n\n  `contrib`, and `ffmpeg` are examples of modules that are large and not always\n  needed, and this allows them to only be loaded when they are used.\n  '

    def __init__(self, local_name, parent_module_globals, name):
        self._local_name = local_name
        self._parent_module_globals = parent_module_globals
        super(LazyLoader, self).__init__(name)

    def _load(self):
        module = importlib.import_module(self.__name__)
        self._parent_module_globals[self._local_name] = module
        self.__dict__.update(module.__dict__)
        return module

    def __getattr__(self, item):
        module = self._load()
        return getattr(module, item)

    def __dir__(self):
        module = self._load()
        return dir(module)