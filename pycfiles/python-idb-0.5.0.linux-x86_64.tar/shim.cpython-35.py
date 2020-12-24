# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/env/lib/python3.5/site-packages/idb/shim.py
# Compiled at: 2018-07-30 13:00:24
# Size of source mod 2**32: 3292 bytes
import sys
if sys.version_info[0] == 2:
    import imp, sys, logging, idb
    logger = logging.getLogger(__name__)

    class HookedImporter(object):

        def __init__(self, hooks=None):
            super(HookedImporter, self).__init__()
            self.hooks = hooks

        def find_module(self, fullname, path=None):
            logger.info('find_module: fullname: %s, path=%s', fullname, path)
            if fullname not in self.hooks:
                return
            return self

        def load_module(self, fullname):
            logger.info('load_module: fullname: %s', fullname)
            mod = self.hooks[fullname]
            newmod = sys.modules.setdefault(fullname, imp.new_module(fullname))
            newmod.__file__ = sys.modules[mod.__module__].__file__
            newmod.__loader__ = self
            newmod.__package__ = ''
            for attr in dir(mod):
                if attr.startswith('__'):
                    pass
                else:
                    newmod.__dict__[attr] = getattr(mod, attr)

            return newmod

        def install(self):
            sys.meta_path.insert(0, self)


elif sys.version_info[0] == 3:
    import sys, types, logging, importlib.abc, importlib.util, idb
    logger = logging.getLogger(__name__)

    class HookedImporter(importlib.abc.MetaPathFinder, importlib.abc.Loader):

        def __init__(self, hooks=None):
            self.hooks = hooks

        def find_spec(self, name, path, target=None):
            if name not in self.hooks:
                return
            spec = importlib.util.spec_from_loader(name, self)
            return spec

        def create_module(self, spec):
            logger.info('hooking import: %s', spec.name)
            module = types.ModuleType(spec.name)
            module.__loader__ = self
            module.__package__ = ''
            mod = self.hooks[spec.name]
            for attr in dir(mod):
                if attr.startswith('__'):
                    pass
                else:
                    module.__dict__[attr] = getattr(mod, attr)

            return module

        def exec_module(self, module):
            pass

        def install(self):
            sys.meta_path.insert(0, self)


def install(db, ScreenEA=None):
    if ScreenEA is None:
        ScreenEA = list(sorted(idb.analysis.Segments(db).segments.keys()))[0]
    api = idb.IDAPython(db, ScreenEA=ScreenEA)
    hooks = {'idc': api.idc, 
     'idaapi': api.idaapi, 
     'idautils': api.idautils, 
     'ida_funcs': api.ida_funcs, 
     'ida_bytes': api.ida_bytes, 
     'ida_netnode': api.ida_netnode, 
     'ida_nalt': api.ida_nalt, 
     'ida_name': api.ida_name, 
     'ida_entry': api.ida_entry}
    importer = HookedImporter(hooks=hooks)
    importer.install()
    return hooks