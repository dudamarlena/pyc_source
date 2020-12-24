# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/insight2/tornadoweb/config.py
# Compiled at: 2019-09-24 23:19:41
import six
if six.PY3:
    import builtins as __builtin__
else:
    import __builtin__
from os.path import exists
from types import ModuleType
from .utility import app_path, staticclass

@staticclass
class ConfigLoader(object):

    @staticmethod
    def load(config=None):
        if config:
            pys = map(app_path, (config,))
        else:
            pys = map(app_path, ('settings.py', ))
        dct = {}
        module = ModuleType('__conf__')
        for py in pys:
            scope = {}
            with open(py, 'r') as (f):
                body = f.read()
                exec body in scope
                for k, v in scope.items():
                    if k.startswith('__'):
                        continue
                    setattr(module, k, v)

        __builtin__.__conf__ = module