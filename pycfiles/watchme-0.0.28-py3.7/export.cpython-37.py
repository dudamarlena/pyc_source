# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/client/export.py
# Compiled at: 2020-04-10 14:08:49
# Size of source mod 2**32: 1493 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from watchme import get_watcher
from watchme.utils import write_json
from watchme.logger import bot
import json, os

def main(args, extra):
    """export temporal data for a watcher
    """
    name = args.watcher[0]
    task = args.task[0]
    filename = args.filename[0]
    if not task.startswith('task'):
        if not task.startswith('decorator'):
            example = 'watchme export watcher task-reddit result.txt'
            bot.exit('Task name must start with "task" or "decorator": %s' % example)
    out = args.out
    watcher = get_watcher(name, base=(args.base), create=False)
    if out is not None:
        if os.path.exists(out):
            if args.force is False:
                bot.exit('%s exists! Use --force to overwrite.' % out)
    else:
        result = watcher.export_dict(task=task,
          filename=filename,
          name=name,
          export_json=(args.json),
          base=(args.base))
        if result is not None:
            if out is None:
                print(json.dumps(result, indent=4))
            else:
                write_json(result, out)
                bot.info('Result written to %s' % out)