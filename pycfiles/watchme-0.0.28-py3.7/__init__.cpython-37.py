# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/__init__.py
# Compiled at: 2020-04-10 14:08:49
# Size of source mod 2**32: 1148 bytes
"""

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from watchme.version import __version__

def get_watcher(name='watcher', base=None, create=False, quiet=True, **kwargs):
    """
       get the correct watcher depending on the environment variable
       WATCHME_WATCHER or default to "watcher"

       Parameters
       ==========
       name: the name of the watcher, will be made all lowercase
       base: the watcher base, if not defined, will use WATCHER_BASE_DIR envar
       create: if the watcher folder doesn't exist, create it (default False)
               for all interactions with a watcher other than create, we should
               exit if the watcher the user wants doesn't exist.
       quiet: if True, suppress most output about the client (e.g. speak)
    """
    from watchme.watchers import Watcher
    Watcher.name = name.lower()
    Watcher.quiet = quiet
    return Watcher(create=create, base=base)