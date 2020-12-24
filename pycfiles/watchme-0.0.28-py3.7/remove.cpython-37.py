# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/client/remove.py
# Compiled at: 2020-04-10 14:08:50
# Size of source mod 2**32: 935 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from watchme import get_watcher
from watchme.logger import bot

def main(args, extra):
    """activate one or more watchers
    """
    name = args.watcher[0]
    watcher = get_watcher(name, base=(args.base), create=False)
    if args.delete:
        watcher.delete()
    else:
        if extra is None:
            bot.exit('Provide tasks to remove, or --delete for entire watcher.')
        for task in extra:
            watcher.remove_task(task)