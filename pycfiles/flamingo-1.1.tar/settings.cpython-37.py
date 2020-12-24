# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/settings/settings.py
# Compiled at: 2020-03-20 06:59:09
# Size of source mod 2**32: 1178 bytes
from copy import deepcopy
import importlib, runpy
from . import defaults
from flamingo.core.types import OverlayObject

class Settings(OverlayObject):

    def __init__(self):
        super().__init__()
        self.modules = []
        for name in dir(defaults):
            if name.startswith('_'):
                continue
            attr = getattr(defaults, name)
            try:
                attr_copy = deepcopy(attr)
            except Exception:
                pass

            self._attrs[name] = attr_copy

    def add(self, module):
        if not module.endswith('.py'):
            if not '/' in module:
                module = importlib.import_module(module).__file__
        attrs = runpy.run_path(module, init_globals=(self._attrs))
        self.modules.append(module)
        self._attrs = {k:v for k, v in attrs.items() if not k.startswith('_') if not k.startswith('_')}

    def get(self, *args):
        return getattr(self, *args)

    def __iter__(self):
        ignore = ('add', )
        for key in dir(self):
            if not key in ignore:
                if key.startswith('_'):
                    continue
                yield (
                 key, getattr(self, key))