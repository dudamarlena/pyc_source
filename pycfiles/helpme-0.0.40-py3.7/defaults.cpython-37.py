# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpme/defaults.py
# Compiled at: 2019-12-18 16:18:07
# Size of source mod 2**32: 2016 bytes
"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from helpme.utils import get_userhome
import tempfile, os, sys

def convert2boolean(arg):
    """
    convert2boolean is used for environmental variables
    that must be returned as boolean
    """
    if not isinstance(arg, bool):
        return arg.lower() in ('yes', 'true', 't', '1', 'y')
    return arg


def getenv(variable_key, default=None, required=False, silent=True):
    """
    getenv will attempt to get an environment variable. If the variable
    is not found, None is returned.

    :param variable_key: the variable name
    :param required: exit with error if not found
    :param silent: Do not print debugging information for variable
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
HELPME_CLIENT = getenv('HELPME_CLIENT', 'github')
HELPME_WORKERS = int(getenv('HELPME_PYTHON_THREADS', 9))
_config = os.path.join(USERHOME, '.helpme')
HELPME_CONFIG_DIR = getenv('HELPME_CONFIG_DIR', _config)
_secrets = os.path.join(HELPME_CONFIG_DIR, 'helpme.cfg')
HELPME_CLIENT_SECRETS = getenv('HELPME_CLIENT_SECRETS', _secrets)
HELPME_HELPERS = ['github', 'uservoice', 'discourse']