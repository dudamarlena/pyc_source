# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gridtest/defaults.py
# Compiled at: 2020-05-03 16:38:15
# Size of source mod 2**32: 1356 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
import multiprocessing, os, sys

def getenv(variable_key, default=None, required=False, silent=True):
    """ attempt to get an environment variable. If the variable
        is not found, None is returned.

        Arguments:

         - variable_key (str) : the variable name
         - required (bool) : exit with error if not found
         - silent (bool) : Do not print debugging information
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


GRIDTEST_NPROC = multiprocessing.cpu_count()
GRIDTEST_WORKERS = int(getenv('GRIDTEST_WORKERS', GRIDTEST_NPROC * 2 + 1))
GRIDTEST_SHELL = getenv('GRIDTEST_SHELL', 'ipython')
GRIDTEST_RETURNTYPES = ['raises', 'returns', 'exists', 'istrue', 'isfalse']
GRIDTEST_GRIDEXPANDERS = ['min', 'max', 'by', 'list']
GRIDTEST_FUNCS = [
 'tmp_dir', 'tmp_path']