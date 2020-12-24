# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pykzee/PluginLoaderPlugin.py
# Compiled at: 2018-12-26 06:11:30
# Size of source mod 2**32: 4334 bytes
import asyncio, functools, importlib, logging, sys, time, traceback
from pyimmutable import ImmutableDict
import pykzee.Plugin as Plugin
from pykzee.common import Undefined

class PluginLoaderPlugin(Plugin):

    def init(self, configPath, mountPath):
        self.lock = asyncio.Lock()
        self.configState = ImmutableDict()
        self.plugins = {}
        self.unsubscribe = self.subscribe(self.stateUpdate, configPath)
        self.mnt = self.mount(mountPath)

    def unloadModule(self, key):
        unload = self.plugins.pop(key, None)
        if unload is not None:
            unload()
        self.mnt.set((key,), Undefined)

    def loadModule(self, key, config):
        if key in self.plugins:
            self.unloadModule(key)
        info = {'time':time.time(), 
         'config':config}
        try:
            try:
                module = config.get('module', Undefined)
                class_ = config.get('class', Undefined)
                if module is Undefined or class_ is Undefined:
                    error(info, f"PluginLoaderPlugin: {key!r}: plugin description is missing module or class key")
                    return
                try:
                    sys.modules.pop(module, None)
                    mod = importlib.import_module(module)
                except Exception as ex:
                    try:
                        traceback.print_exc()
                        error(info, f"PluginLoaderPlugin: {key!r}: error importing module: {ex!r}")
                        return
                    finally:
                        ex = None
                        del ex

                try:
                    cls = getattr(mod, class_)
                except Exception as ex:
                    try:
                        error(info, f"PluginLoaderPlugin: {key!r}: error accessing class {class_!r} in module {module!r}: {ex!r}")
                        return
                    finally:
                        ex = None
                        del ex

                params = config.get('params', {})
                try:
                    remove_plugin = (self.addPlugin)(cls, **params)
                except Exception as ex:
                    try:
                        remove_plugin = noop
                        error(info, f"PluginLoaderPlugin: {key!r}: adding plugin failed: {ex!r}")
                    finally:
                        ex = None
                        del ex

                else:
                    p = ', '.join((f"{k}={v!r}" for k, v in params.items()))
                    logging.info(f"PluginLoaderPlugin: {key!r}: added plugin {module}:{class_}({p})")
                remove_command = self.mnt.registerCommand((
                 key,), 'reload', functools.partial(self.reloadModule, key), 'Reload this module')
                self.plugins[key] = lambda : (
                 remove_plugin(), remove_command())
            except Exception as ex:
                try:
                    info['exception'] = repr(ex)
                finally:
                    ex = None
                    del ex

        finally:
            self.mnt.set((key,), info)

    def reloadModule(self, key):
        try:
            self.loadModule(key, self.configState[key])
        except Exception:
            traceback.print_exc()
            raise

    async def stateUpdate(self, new_state):
        async with self.lock:
            if type(new_state) is not ImmutableDict:
                new_state = ImmutableDict()
            loaded_plugin_keys = set(self.configState)
            new_plugin_keys = set(new_state) - loaded_plugin_keys
            unload_plugin_keys = loaded_plugin_keys.difference(new_state)
            check_update_keys = loaded_plugin_keys.intersection(new_state)
            for key in sorted(unload_plugin_keys):
                logging.info(f"PluginLoaderPlugin: {key!r}: unloading")
                self.unloadModule(key)

            for key in sorted(check_update_keys):
                if new_state[key] is not self.configState[key]:
                    logging.info(f"PluginLoaderPlugin: {key!r}: unloading")
                    new_plugin_keys.add(key)
                    self.unloadModule(key)

            for key in sorted(new_plugin_keys):
                self.loadModule(key, new_state[key])

            self.configState = new_state


def error(info, message):
    info['error'] = message
    logging.error(message)


def noop():
    pass