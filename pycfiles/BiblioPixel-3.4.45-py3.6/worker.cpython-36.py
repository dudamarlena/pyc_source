# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/threads/worker.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1913 bytes
import os, time, traceback, multiprocessing as mp
from .. import log
DEFAULT_COUNT = 4

class Worker(mp.Process):

    def __init__(self, queue, counter):
        super().__init__()
        self.time = time.time()
        self.queue = queue
        self.counter = counter

    def run(self):
        for command, *args in iter(self.queue.get, None):
            try:
                command(*args)
            except Exception as e:
                name = getattr(command, '__name__', str(command))
                log.printer('ERROR on command', name, args, e)
                traceback.print_exc()
            else:
                counter = self._increment_counter()
                self._log(command, args, counter)

    def _increment_counter(self):
        with self.counter.get_lock():
            self.counter.value += 1
            return self.counter.value

    def _log(self, command, args, counter):
        delta_t = time.time() - self.time
        average = delta_t / counter
        command = getattr(command, '__name__', str(command))
        msg = '{command}{args} -> {counter} ({average})'
        log.debug((msg.format)(**locals()))


class Workers:

    def __init__(self, count=DEFAULT_COUNT):
        self.queue = mp.Queue()
        self.counter = mp.Value('i')
        self.workers = [Worker(self.queue, self.counter) for i in range(count)]

    def __enter__(self):
        for w in self.workers:
            w.start()

        return self

    def __exit__(self, type, value, traceback):
        for w in self.workers:
            self.queue.put(None)

    def run(self, *args):
        self.queue.put(args)


def work_on(function, items, count=DEFAULT_COUNT):
    with Workers(count) as (workers):
        for item in items:
            (workers.run)(function, *item)