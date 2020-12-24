# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/client/edit.py
# Compiled at: 2020-04-10 14:08:49
# Size of source mod 2**32: 1027 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from watchme import get_watcher
from watchme.logger import bot

def main(args, extra):
    """edit the configuration for a watcher task
    """
    name = args.watcher[0]
    action = args.action[0]
    task = args.task[0]
    watcher = get_watcher(name, base=(args.base))
    if extra is None:
        bot.exit('Please provide one or more items to %s' % action)
    key = extra[0]
    value = None
    if action in ('add', 'update'):
        if len(extra) != 2:
            bot.exit('You must do watchme <watcher> add <key> <value>')
        value = extra[1]
    watcher.edit_task(task, action, key, value)