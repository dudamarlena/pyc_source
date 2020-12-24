# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/christian/Documents/workspace/Yeti/yeti/engine.py
# Compiled at: 2016-02-18 19:58:42
# Size of source mod 2**32: 9452 bytes
import threading, importlib, inspect, pyclbr, asyncio, logging, sys, os, yaml
_engine_instances = dict()

def set_engine(engine):
    """
    Sets the context for the current thread.

    :param context: An instance of Engine to be saved
    """
    _engine_instances[threading.current_thread()] = engine


def get_engine():
    """
    :returns: the engine set for the current thread.
    """
    return _engine_instances[threading.current_thread()]


class Engine:
    __doc__ = '\n    This hosts an asyncio event loop in a thread, and contains mechanisms for loading and running modules.\n    '
    event_loop = None
    _thread = None

    def __init__(self, loop_class=None):
        self.loaded_modules = {}
        self.running_modules = {}
        self.failed_modules = []
        self.module_sets = {}
        self.enabled_modules = []
        self.embedded_modules = []
        if loop_class is None:
            self.event_loop = asyncio.get_event_loop()
        else:
            self.event_loop = loop_class()
        asyncio.set_event_loop(self.event_loop)
        asyncio.run_coroutine_threadsafe(self._start(), self.event_loop)
        self.logger = logging.getLogger(name='yeti.' + self.__class__.__name__)

    def thread_coroutine(self, coroutine, logger=None):
        """
        Schedules coroutine to be run in the engine's event loop.
        This function is thread-safe.

        :param coroutine: The coroutine to schedule
        """
        if logger is None:
            logger = self.logger
        asyncio.run_coroutine_threadsafe(self._error_net(coroutine, logger), self.event_loop)

    async def _error_net(self, coro, log):
        try:
            await coro
        except Exception as e:
            self.logger.exception(e)

    def spawn_thread(self):
        """Spawns a new thread and runs :meth:`.run_forever` in it."""
        if self._thread is None:
            self._thread = threading.Thread(target=self.run_forever)
            self._thread.start()

    def run_forever(self):
        """
        Sets the engine for the current thread, and runs the engine's event loop forever.
        """
        set_engine(self)
        asyncio.set_event_loop(self.event_loop)
        self.event_loop.run_forever()

    def run_for(self, time):
        """
        Sets the engine for the current thread, and runs the engine's event loop for the specified duration.

        :param time: The time in seconds to run the event loop for.
        """
        set_engine(self)
        asyncio.set_event_loop(self.event_loop)
        self.event_loop.run_until_complete(asyncio.sleep(time))

    async def _start(self):
        for mod_id in self.enabled_modules:
            try:
                await self.start_module(mod_id)
            except Exception as e:
                self.logger.exception(e)

    def stop(self):
        """
        Schedules :meth:`._stop_coroutine` to be run in the engine's event loop.
        This method is thread-safe.
        """
        self.thread_coroutine(self._stop_coroutine())

    async def _stop_coroutine(self):
        """
        Unloads all modules and stops the event loop.
        This method is a coroutine.
        """
        for modname in self.loaded_modules:
            await self.stop_module(modname)

        self.event_loop.stop()

    def load_config(self, filename):
        file = open(filename)
        data = yaml.load(file)
        file.close()
        self.module_sets.update(data.get('module_sets', {}))
        self.enabled_modules.extend(data.get('enabled', []))
        self.embedded_modules.extend(data.get('embedded', []))
        for module_dir in data.get('module_dirs', []):
            sys.path.append(os.path.join(os.path.dirname(filename), module_dir))

    async def reload_module(self, module, retry_failed=False):
        """
        Reload the given yeti module

        :param module: The module to restart (either a module object, module path, or module set id)
        :param retry_failed: If true, then clear any failures before reloading.
        """
        if retry_failed:
            if module in self.failed_modules:
                self.failed_modules.remove(module)
            if module in self.module_sets:
                for m in self.module_sets[module]:
                    if m in self.failed_modules:
                        self.failed_modules.remove(m)

            mod_path = module
        else:
            mod_path, _ = self._get_module(module)
            await self.stop_module(mod_path)
        await self.start_module(mod_path)

    async def start_module(self, mod_id, mod_class=None, mod_object=None):
        """
        Creates a module object and adds it to running_modules
        """
        if mod_id in self.running_modules:
            return
        mod_set = [
         mod_id]
        if mod_id in self.module_sets:
            mod_set = self.module_sets[mod_id]
        for mod_path in mod_set:
            if mod_path not in self.failed_modules:
                break
        else:
            raise RuntimeError('Cannot import {}, all candidates have failed.'.format(mod_id))

        try:
            if mod_object is None:
                if mod_class is None:
                    try:
                        scanned_objects = pyclbr.readmodule(mod_path)
                    except AttributeError as e:
                        raise ImportError('Failed to find module {}.'.format(mod_path))

                    for class_name in scanned_objects:
                        if hasattr(scanned_objects[class_name], 'methods') and 'module_init' in scanned_objects[class_name].methods:
                            break
                    else:
                        raise ImportError('Failed to find appropriate module type.')

                    if mod_path in sys.modules:
                        importlib.reload(sys.modules[mod_path])
                        pymod = sys.modules[mod_path]
                    else:
                        pymod = importlib.import_module(mod_path)
                    mod_class = getattr(pymod, class_name)
                mod_object = mod_class(self)
            self.running_modules[mod_path] = mod_object
            mod_object.start()
            return
        except Exception as e:
            self.logger.exception(e)

        await self.fail_module(mod_id)

    async def stop_module(self, module):
        mod_path, mod_object = self._get_module(module)
        await mod_object.stop()
        if mod_path in self.running_modules:
            del self.running_modules[mod_path]

    async def fail_module(self, module):
        mod_path, mod_object = self._get_module(module)
        await self.stop_module(mod_path)
        self.failed_modules.append(mod_path)
        for mod_set in self.module_sets:
            if mod_path in self.module_sets[mod_set]:
                await self.start_module(mod_set)

    def get_tagged_methods(self, tag):
        tags = []
        for mod in self.running_modules:
            tags.extend(self.running_modules[mod].get_tagged_methods(tag))

        return tags

    async def run_tagged_methods(self, tag, *args, **kwargs):
        for mod in self.running_modules:
            mod_obj = self.running_modules[mod]
            for method in mod_obj.get_tagged_methods(tag):
                if asyncio.iscoroutinefunction(method):
                    mod_obj.start_coroutine(method(*args, **kwargs))
                else:
                    method(*args, **kwargs)

    def get_module(self, mod_id):
        return GhostModule(self, mod_id)

    def _get_module(self, module):
        if isinstance(module, str):
            mod_id = module
            if mod_id in self.module_sets:
                for mod_path in self.module_sets[mod_id]:
                    if mod_path in self.running_modules:
                        break
                else:
                    raise ValueError('No running modules in module_set {}'.format(mod_id))

            else:
                mod_path = mod_id
            mod_object = self.running_modules[mod_path]
        else:
            mod_object = module
            for mod_path in self.running_modules:
                if self.running_modules[mod_path] is mod_object:
                    break
            else:
                raise ValueError('{} not in running modules'.format(mod_object))

        return (
         mod_path, mod_object)


class GhostModule:

    def __init__(self, engine, mod_id):
        self.mod_id = mod_id
        self.engine = engine
        self.mod_obj = None

    def __getattr__(self, item):
        if self.mod_obj is None or not self.mod_obj.alive:
            _, self.mod_obj = self.engine._get_module(self.mod_id)
        return getattr(self.mod_obj, item)