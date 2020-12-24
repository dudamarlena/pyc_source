# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/b3ql/.virtualenvs/SSD/lib/python3.7/site-packages/ssd/utils/registry.py
# Compiled at: 2019-10-28 14:34:58
# Size of source mod 2**32: 1309 bytes


def _register_generic(module_dict, module_name, module):
    assert module_name not in module_dict
    module_dict[module_name] = module


class Registry(dict):
    __doc__ = '\n    A helper class for managing registering modules, it extends a dictionary\n    and provides a register functions.\n    Eg. creating a registry:\n        some_registry = Registry({"default": default_module})\n    There\'re two ways of registering new modules:\n    1): normal way is just calling register function:\n        def foo():\n            ...\n        some_registry.register("foo_module", foo)\n    2): used as decorator when declaring the module:\n        @some_registry.register("foo_module")\n        @some_registry.register("foo_module_nickname")\n        def foo():\n            ...\n    Access of module is just like using a dictionary, eg:\n        f = some_registry["foo_module"]\n    '

    def __init__(self, *args, **kwargs):
        (super(Registry, self).__init__)(*args, **kwargs)

    def register(self, module_name, module=None):
        if module is not None:
            _register_generic(self, module_name, module)
            return

        def register_fn(fn):
            _register_generic(self, module_name, fn)
            return fn

        return register_fn