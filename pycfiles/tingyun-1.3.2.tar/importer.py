# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/packages/wrapt/importer.py
# Compiled at: 2016-06-30 06:13:10
"""This module implements a post import hook mechanism styled after what is
described in PEP-369. Note that it doesn't cope with modules being reloaded.

"""
import sys, threading
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    import importlib
from .decorators import synchronized
_post_import_hooks = {}
_post_import_hooks_init = False
_post_import_hooks_lock = threading.RLock()

@synchronized(_post_import_hooks_lock)
def register_post_import_hook(hook, name):
    global _post_import_hooks_init
    if not _post_import_hooks_init:
        _post_import_hooks_init = True
        sys.meta_path.insert(0, ImportHookFinder())
    hooks = _post_import_hooks.get(name, None)
    if hooks is None:
        module = sys.modules.get(name, None)
        if module is not None:
            _post_import_hooks[name] = []
            hook(module)
        else:
            _post_import_hooks[name] = [
             hook]
    elif hooks == []:
        hook(module)
    else:
        _post_import_hooks[name].append(hook)
    return


def discover_post_import_hooks(group):
    try:
        import pkg_resources
    except ImportError:
        return

    for entrypoint in pkg_resources.iter_entry_points(group=group):

        def proxy_post_import_hook(module):
            __import__(entrypoint.module_name)
            callback = sys.modules[entrypoint.module_name]
            for attr in entrypoints.attrs:
                callback = getattr(callback, attr)

            return callback(module)

        register_post_import_hook(proxy_post_import_hook, entrypoint.name)


@synchronized(_post_import_hooks_lock)
def notify_module_loaded(module):
    name = getattr(module, '__name__', None)
    hooks = _post_import_hooks.get(name, None)
    if hooks:
        _post_import_hooks[name] = []
        for hook in hooks:
            hook(module)

    return


class _ImportHookLoader:

    def load_module(self, fullname):
        module = sys.modules[fullname]
        notify_module_loaded(module)
        return module


class _ImportHookChainedLoader:

    def __init__(self, loader):
        self.loader = loader

    def load_module(self, fullname):
        module = self.loader.load_module(fullname)
        notify_module_loaded(module)
        return module


class ImportHookFinder:

    def __init__(self):
        self.in_progress = {}

    @synchronized(_post_import_hooks_lock)
    def find_module(self, fullname, path=None):
        if fullname not in _post_import_hooks:
            return
        else:
            if fullname in self.in_progress:
                return
            self.in_progress[fullname] = True
            try:
                if PY3:
                    loader = importlib.find_loader(fullname, path)
                    if loader:
                        return _ImportHookChainedLoader(loader)
                else:
                    __import__(fullname)
                    return _ImportHookLoader()
            finally:
                del self.in_progress[fullname]

            return


def when_imported(name):

    def register(hook):
        register_post_import_hook(hook, name)
        return hook

    return register