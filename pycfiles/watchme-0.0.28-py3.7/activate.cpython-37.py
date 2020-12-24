# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/client/activate.py
# Compiled at: 2020-04-10 14:08:49
# Size of source mod 2**32: 643 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from watchme import get_watcher

def main(args, extra):
    """activate one or more watchers
    """
    watcher = args.watcher[0]
    watcher = get_watcher(watcher, base=(args.base))
    if extra is None:
        watcher.activate()
    else:
        for name in extra:
            watcher.activate(name)