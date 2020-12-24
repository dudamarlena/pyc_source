# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/client/init.py
# Compiled at: 2020-04-10 14:08:49
# Size of source mod 2**32: 606 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from watchme.command.create import create_watcher_base, create_watcher

def main(args, extra):
    """init means creating the watcher base, and the first (default) watcher.
    """
    create_watcher_base(args.watcher, args.base)
    if not args.create_empty:
        create_watcher(args.watcher)