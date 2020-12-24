# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gridtest/main/expand.py
# Compiled at: 2020-05-09 20:18:22
# Size of source mod 2**32: 2685 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from gridtest.logger import bot
from gridtest.defaults import GRIDTEST_GRIDEXPANDERS
import os

def custom_range(start, stop, by=1.0, precision=2):
    """the range function only accepts integers, and user's will likely
       want to provide float. Thus we use custom_range to provide this

       Arguments:
        - start (int or float) : the starting value
        - stop (int or float) : go up to this value
        - by (float or int) : increment by this value (default 1.0)
        - precision (int) : decimals to round to (default 2)
    """
    start = float(start)
    count = 0
    values = []
    while True:
        value = round(float(start + count * by), precision)
        if by > 0 and value >= stop:
            break
        else:
            if by < 0:
                if value <= stop:
                    break
        values.append(value)
        count += 1

    return values


def expand_args(args):
    """Given a grid of arguments, expand special cases into longer lists
       of arguments.
       E.g., convert an entry with these keys:
 

       into:

       In the case that a grid has a string identifier to point to a key
       in the lookup, we use that listing of values instead that should
       already be calculated.
    """
    for param, settings in args.items():
        if isinstance(settings, dict):
            if set(settings.keys()).difference(GRIDTEST_GRIDEXPANDERS):
                if param != 'self':
                    bot.exit(f"Invalid key in grid settings {settings}")
            values = []
            if 'min' in settings and 'max' in settings and 'by' in settings:
                values += custom_range(settings['min'], settings['max'], settings['by'])
            else:
                if 'min' in settings and 'max' in settings:
                    values += custom_range(settings['min'], settings['max'])
                else:
                    if 'list' in settings:
                        values += settings['list']
                    else:
                        if param == 'self':
                            values = settings
            args[param] = values
        else:
            args[param] = settings

    return args