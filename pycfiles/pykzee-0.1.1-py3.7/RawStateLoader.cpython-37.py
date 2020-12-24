# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pykzee/core/RawStateLoader.py
# Compiled at: 2019-11-01 11:57:33
# Size of source mod 2**32: 2689 bytes
import asyncio, json, logging, os, stat, traceback, aiofiles
from pyimmutable import ImmutableDict
import watchdog.events, watchdog.observers
from pykzee.core.common import print_exception_task_callback

class RawStateLoader:

    def __init__(self, set_raw_state):
        self._RawStateLoader__setRawState = set_raw_state
        self._RawStateLoader__shutdown = asyncio.Future()
        self._RawStateLoader__reread_tree_event = asyncio.Event()
        asyncio.create_task(self._RawStateLoader__rereadTaskImpl()).add_done_callback(print_exception_task_callback)
        observer = self._RawStateLoader__observer = watchdog.observers.Observer()
        loop = asyncio.get_event_loop()
        observer.schedule((WatchdogEventHandler(lambda : loop.call_soon_threadsafe(self._RawStateLoader__reread_tree_event.set))),
          '.',
          recursive=True)
        observer.start()

    def __del__(self):
        self._RawStateLoader__observer.stop()
        self._RawStateLoader__observer.join()

    async def readStateFromDisk(self):
        self._RawStateLoader__reread_tree_event.clear()
        self._RawStateLoader__setRawState(ImmutableDict([x async for x in load_state_tree('.')]))

    async def run(self):
        return await self._RawStateLoader__shutdown

    async def __rereadTaskImpl(self):
        while 1:
            await self._RawStateLoader__reread_tree_event.wait()
            await asyncio.sleep(2)
            if self._RawStateLoader__reread_tree_event.is_set():
                try:
                    await self.readStateFromDisk()
                except Exception:
                    traceback.print_exc()


class WatchdogEventHandler(watchdog.events.FileSystemEventHandler):

    def __init__(self, callback):
        self._WatchdogEventHandler__callback = callback

    def on_any_event(self, event):
        self._WatchdogEventHandler__callback()


async def load_state_tree(dirpath):
    for filename in sorted(os.listdir(dirpath)):
        if not filename.startswith('.'):
            if filename.endswith('~'):
                continue
            key = filename
            fspath = os.path.join(dirpath, filename)
            mode = os.stat(fspath).st_mode
            if stat.S_ISDIR(mode):
                yield (
                 key,
                 ImmutableDict([x async for x in load_state_tree(fspath)]))
            elif stat.S_ISREG(mode):
                async with aiofiles.open(fspath) as f:
                    content = await f.read()
                if key.endswith('.json'):
                    key = key[:-5]
                    content = json.loads(content)
                else:
                    if key.endswith('.txt'):
                        key = key[:-4]
                yield (
                 key, content)
            else:
                logging.warning(f"ConfigPlugin: ignoring non-regular file f{fspath}")