# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/watchers/psutils/decorators.py
# Compiled at: 2020-04-10 14:08:50
# Size of source mod 2**32: 2862 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from functools import wraps
from watchme.logger import bot
from watchme.tasks.decorators import ProcessRunner
from watchme import get_watcher

def monitor_resources(*args, **kwargs):
    """a decorator to monitor a function every 3 (or user specified) seconds. 
       We include one or more task names that include data we want to extract.
       we get the pid of the running function, and then use the
       monitor_pid_task from psutils to watch it. The functools "wraps"
       ensures that the (fargs, fkwargs) are passed from the calling function
       despite the wrapper. The following parameters can be provided to
       "monitor resources"

       Parameters
       ==========
       watcher: the watcher instance to use, used to save data to a "task"
                folder that starts with "decorator-<name<"
       seconds: how often to collect data during the run.
       only: ignore skip and include, only include this custom subset
       skip: Fields in the result to skip (list).
       include: Fields in the result to include back in (list).
       create: whether to create the watcher on the fly (default False, must
               exist)
       name: the suffix of the decorator-psutils-<name> folder. If not provided,
             defaults to the function name
    """

    def inner(func):

        @wraps(func)
        def wrapper(*fargs, **fkwargs):
            result = None
            if not args:
                bot.error('A watcher name is required for the psutils decorator.')
                return result
            watcher = get_watcher((args[0]), create=(kwargs.get('create', False)))
            runner = ProcessRunner(seconds=(kwargs.get('seconds', 3)),
              skip=(kwargs.get('skip', [])),
              include=(kwargs.get('include', [])),
              only=(kwargs.get('only', [])))
            (runner.run)(func, *fargs, **fkwargs)
            result = runner.wait('monitor_pid_task')
            name = kwargs.get('name', func.__name__)
            key = 'decorator-psutils-%s' % name
            results = {key: runner.timepoints}
            watcher.finish_runs(results)
            return result

        return wrapper

    return inner