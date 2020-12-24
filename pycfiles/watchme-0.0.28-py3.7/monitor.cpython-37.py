# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/client/monitor.py
# Compiled at: 2020-04-10 14:08:50
# Size of source mod 2**32: 1798 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from watchme.command import get_watchers
from watchme import get_watcher
from watchme.tasks.decorators import TerminalRunner
import json

def main(args, extra):
    """monitor a task (from the command line), meaning wrapping it with
       multiprocessing, getting the id, and returning a result (command line 
       or written to file)
    """
    watcher = args.watcher
    command = extra
    if watcher not in get_watchers((args.base), quiet=True):
        command = [
         watcher] + command
        watcher = None
    else:
        watcher = get_watcher(watcher, base=(args.base), create=False)
    command = ' '.join(command)
    runner = TerminalRunner(command,
      skip=(args.skip),
      include=(args.include),
      only=(args.only),
      seconds=(args.seconds))
    runner.run()
    timepoints = runner.wait(args.func)
    prefix = 'decorator-psutils'
    if args.func == 'gpu_task':
        prefix = 'decorator-gpu'
    elif watcher is None or args.test is True:
        print(json.dumps(timepoints))
    else:
        name = args.name
        if name is None:
            name = command.replace(' ', '-')
        name = '%s-%s' % (prefix, name)
        watcher.finish_runs({name: timepoints})