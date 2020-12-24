# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/command/create.py
# Compiled at: 2020-04-10 14:08:50
# Size of source mod 2**32: 2096 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from watchme.utils import run_command, mkdir_p
from watchme.defaults import WATCHME_WATCHER, WATCHME_BASE_DIR
from watchme.logger import bot
from watchme.config import generate_watcher_config
import os

def create_watcher(name=None, watcher_type=None, base=None):
    """create a watcher, meaning a folder with a configuration and
       initialized git repo.

       Parameters
       ==========
       name: the watcher to create, uses default or WATCHME_WATCHER
       watcher_type: the type of watcher to create. defaults to 
                     WATCHER_DEFAULT_TYPE
        base: The watcher base to use (defaults to $HOME/.watchme)
    """
    if name is None:
        name = WATCHME_WATCHER
    else:
        if base is None:
            base = WATCHME_BASE_DIR
        repo = os.path.join(base, name)
        os.path.exists(repo) or bot.info('Adding watcher %s...' % repo)
        mkdir_p(repo)
        run_command('git --git-dir=%s/.git init' % repo)
        run_command('git --git-dir=%s/.git config commit.gpgsign false' % repo)
        generate_watcher_config(repo, watcher_type)
        run_command('git -C %s add watchme.cfg' % repo)
        return repo
    bot.info('%s already exists: %s' % (name, repo))


def create_watcher_base(name=None, base=None):
    """create a watch base and default repo, if it doesn't already exist.

       Parameters
       ==========
       name: the watcher to create, uses default or WATCHME_WATCHER
       base: the watcher base, defaults to WATCHME_BASE_DIR
    """
    if base is None:
        base = WATCHME_BASE_DIR
    else:
        if name is None:
            name = WATCHME_WATCHER
        os.path.exists(base) or bot.info('Creating %s...' % base)
        mkdir_p(base)