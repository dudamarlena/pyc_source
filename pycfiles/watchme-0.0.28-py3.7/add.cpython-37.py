# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/client/add.py
# Compiled at: 2020-04-10 14:08:49
# Size of source mod 2**32: 1418 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from watchme import get_watcher
from watchme.logger import bot

def main(args, extra):
    """add a task for a watcher
    """
    name = args.watcher[0]
    task = args.task[0]
    if not task.startswith('task'):
        example = 'watchme add-task watcher task-cpu func@cpu_task type@psutils'
        bot.exit('Task name must start with "task", e.g., %s' % example)
    if extra is None:
        bot.exit('Please provide parameters to add to your watcher (key@value)')
    watcher_type = args.watcher_type
    params = []
    for param in extra:
        if param.startswith('type@'):
            watcher_type = param.replace('type@', '')
        else:
            params.append(param)

    watcher = get_watcher(name, base=(args.base), create=False)
    watcher.add_task(task=task,
      task_type=watcher_type,
      params=params,
      force=(args.force),
      active=(args.active))