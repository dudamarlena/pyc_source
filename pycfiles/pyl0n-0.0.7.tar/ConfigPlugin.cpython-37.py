# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pykzee/ConfigPlugin.py
# Compiled at: 2018-12-26 06:11:30
# Size of source mod 2**32: 4074 bytes
import asyncio, json, logging, os, stat, aiofiles, aionotify
import pykzee.Plugin as Plugin
from pykzee.common import print_exception_task_callback
directory_watch_flags = aionotify.Flags.MODIFY | aionotify.Flags.CREATE | aionotify.Flags.DELETE | aionotify.Flags.MOVED_FROM | aionotify.Flags.MOVED_TO

class ConfigPlugin(Plugin):

    async def init(self, path, directory, delay=2):
        self._ConfigPlugin__directory = directory
        self._ConfigPlugin__delay = delay
        mount = self.mount(path)
        self._ConfigPlugin__set = mount.set
        self._ConfigPlugin__set((), await load_json_tree(directory))
        self._ConfigPlugin__rereadEvent = asyncio.Event()
        watcher = self._ConfigPlugin__watcher = aionotify.Watcher()
        await watcher.setup(asyncio.get_event_loop())
        self._ConfigPlugin__watchTask = asyncio.create_task(self._ConfigPlugin__watchTaskImpl())
        self._ConfigPlugin__watchTask.add_done_callback(print_exception_task_callback)
        self._ConfigPlugin__rereadTask = asyncio.create_task(self._ConfigPlugin__rereadTaskImpl())
        self._ConfigPlugin__rereadTask.add_done_callback(print_exception_task_callback)
        dirs = [
         directory]
        watched_dirs = self._ConfigPlugin__watched_dirs = set()
        while dirs:
            d = dirs.pop()
            print(d)
            watcher.watch(d, directory_watch_flags)
            watched_dirs.add(d)
            dirs.extend((path for path in (os.path.join(d, fn) for fn in os.listdir(d)) if os.path.isdir(path)))

    async def shutdown(self):
        self._ConfigPlugin__watchTask.cancel()
        self._ConfigPlugin__rereadTaskImpl.cancel()

    async def __watchTaskImpl(self):
        while True:
            event = await self._ConfigPlugin__watcher.get_event()
            logging.debug(f"read fs event: flags={hex(event.flags)} name={event.name!r} alias={event.alias!r}")
            if event.flags & aionotify.Flags.ISDIR:
                d = os.path.join(event.alias, event.name)
                if event.flags & aionotify.Flags.CREATE:
                    if d not in self._ConfigPlugin__watched_dirs:
                        try:
                            self._ConfigPlugin__watcher.watch(d, directory_watch_flags)
                        except Exception as ex:
                            try:
                                logging.warning(f"Exception caught installing watch {d!r}: {ex!r}")
                            finally:
                                ex = None
                                del ex

                        else:
                            self._ConfigPlugin__watched_dirs.add(d)
                elif event.flags & aionotify.Flags.DELETE:
                    if d in self._ConfigPlugin__watched_dirs:
                        self._ConfigPlugin__watched_dirs.remove(d)
                        try:
                            self._ConfigPlugin__watcher.unwatch(d)
                        except Exception as ex:
                            try:
                                logging.warning(f"Exception caught uninstalling watch {d!r}: {ex!r}")
                            finally:
                                ex = None
                                del ex

            self._ConfigPlugin__rereadEvent.set()

    async def __rereadTaskImpl(self):
        while True:
            await self._ConfigPlugin__rereadEvent.wait()
            await asyncio.sleep(self._ConfigPlugin__delay)
            self._ConfigPlugin__rereadEvent.clear()
            try:
                new_state = await load_json_tree(self._ConfigPlugin__directory)
            except Exception as ex:
                try:
                    logging.warning(f"Error reading configuration: {ex!r}")
                    continue
                finally:
                    ex = None
                    del ex

            self._ConfigPlugin__set((), new_state)


async def load_json_tree(fspath):
    mode = os.stat(fspath).st_mode
    if stat.S_ISREG(mode):
        async with aiofiles.open(fspath) as f:
            return json.loads(await f.read())
    else:
        if stat.S_ISDIR(mode):
            result = {}
            for filename in os.listdir(fspath):
                if filename.endswith('~'):
                    continue
                result[filename] = await load_json_tree(os.path.join(fspath, filename))

            return result
        logging.warning(f"ConfigPlugin: ignoring non-regular file f{fspath}")