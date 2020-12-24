# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpme/client/list.py
# Compiled at: 2019-12-18 16:19:19
# Size of source mod 2**32: 593 bytes
"""

Copyright (C) 2018-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from helpme.logger import bot
from helpme.defaults import HELPME_HELPERS
import sys, pwd, os

def main(args, extra):
    """print the listing of helpers installed, defined by the HELPME_HELPERS
       variable in the default settings flie, and then exit.
    """
    bot.info('Helpers Installed:')
    print('\n'.join(HELPME_HELPERS))