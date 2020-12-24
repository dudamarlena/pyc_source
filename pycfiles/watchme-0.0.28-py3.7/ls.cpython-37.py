# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/client/ls.py
# Compiled at: 2020-04-10 14:08:49
# Size of source mod 2**32: 1028 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from watchme.command import get_watchers, list_task, list_watcher, list_watcher_types
from watchme.logger import bot

def main(args, extra):
    """list installed watchers
    """
    if args.watchers is True:
        list_watcher_types()
    else:
        if extra is None:
            get_watchers(args.base)
        else:
            if len(extra) == 1:
                list_watcher(extra[0], args.base)
            else:
                if len(extra) == 2:
                    list_task(extra[0], extra[1], args.base)
                else:
                    bot.exit('Please provide none or all of <watcher> <task> to list.')