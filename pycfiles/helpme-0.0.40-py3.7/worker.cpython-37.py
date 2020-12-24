# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpme/main/workers/worker.py
# Compiled at: 2019-12-09 18:49:03
# Size of source mod 2**32: 3939 bytes
"""

Copyright (C) 2018-2020 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
from helpme.logger import bot
from helpme.defaults import HELPME_WORKERS
import multiprocessing, itertools, time, signal, sys, re, os

class Workers(object):

    def __init__(self, workers=None):
        if workers is None:
            workers = HELPME_WORKERS
        self.workers = workers
        bot.debug('Using %s workers for multiprocess.' % self.workers)

    def start(self):
        bot.debug('Starting multiprocess')
        self.start_time = time.time()

    def end(self):
        self.end_time = time.time()
        self.runtime = self.runtime = self.end_time - self.start_time
        bot.debug('Ending multiprocess, runtime: %s sec' % self.runtime)

    def run(self, func, tasks, func2=None):
        """run will send a list of tasks,
        a tuple with arguments, through a function.
        the arguments should be ordered correctly.
        :param func: the function to run with multiprocessing.pool
        :param tasks: a list of tasks, each a tuple
                      of arguments to process
        :param func2: filter function to run result
                      from func through (optional)
        """
        progress = 1
        total = len(tasks)
        if len(tasks) == 0:
            return
        if func2 is not None:
            total = total * 2
        finished = []
        level1 = []
        results = []
        try:
            prefix = '[%s/%s]' % (progress, total)
            bot.show_progress(0, total, length=35, prefix=prefix)
            pool = multiprocessing.Pool(self.workers, init_worker)
            self.start()
            for task in tasks:
                result = pool.apply_async(multi_wrapper, multi_package(func, [task]))
                results.append(result)
                level1.append(result._job)

            while len(results) > 0:
                result = results.pop()
                result.wait()
                bot.show_progress(progress, total, length=35, prefix=prefix)
                progress += 1
                prefix = '[%s/%s]' % (progress, total)
                if func2 is not None and result._job in level1:
                    result = pool.apply_async(multi_wrapper, multi_package(func2, [(result.get(),)]))
                    results.append(result)
                else:
                    finished.append(result.get())

            self.end()
            pool.close()
            pool.join()
        except (KeyboardInterrupt, SystemExit):
            bot.error('Keyboard interrupt detected, terminating workers!')
            pool.terminate()
            sys.exit(1)
        except Exception as e:
            try:
                bot.error(e)
            finally:
                e = None
                del e

        return finished


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def multi_wrapper(func_args):
    function, args = func_args
    return function(*args)


def multi_package(func, args):
    return zip(itertools.repeat(func), args)