# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/defaults.py
# Compiled at: 2020-04-10 14:08:50
# Size of source mod 2**32: 2011 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

The watcher is actually a connection to crontab. This is what helps to schedule
the watched to check for changes at some frequency, and update the files.

"""
from watchme.logger import bot
from watchme.utils import get_userhome
import os, sys

def getenv(variable_key, default=None, required=False, silent=True):
    """ attempt to get an environment variable. If the variable
        is not found, None is returned.

        Parameters
        ==========
        variable_key: the variable name
        required: exit with error if not found
        silent: Do not print debugging information for variable
    """
    variable = os.environ.get(variable_key, default)
    if variable is None:
        if required:
            bot.error('Cannot find environment variable %s, exiting.' % variable_key)
            sys.exit(1)
    if not silent:
        if variable is not None:
            bot.verbose('%s found as %s' % (variable_key, variable))
    return variable


USERHOME = get_userhome()
WATCHME_WATCHER = getenv('WATCHME_WATCHER', 'watcher')
_config = os.path.join(USERHOME, '.watchme')
WATCHME_BASE_DIR = getenv('WATCHME_BASE_DIR', _config)
WATCHME_WORKERS = int(getenv('WATCHME_WORKERS', 9))
WATCHME_TASK_TYPES = [
 'urls', 'url', 'gpu', 'psutils', 'results']
WATCHME_DEFAULT_TYPE = 'urls'
WATCHME_NOTALLOWED_PARAMS = [
 'type', 'active']