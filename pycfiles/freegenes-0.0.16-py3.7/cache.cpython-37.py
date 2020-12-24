# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/freegenes/main/cache.py
# Compiled at: 2019-09-28 11:05:55
# Size of source mod 2**32: 670 bytes
"""

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from freegenes.logger import bot
import requests, os, re

def cache_parts(self):
    """cache the parts for the client
    """
    if 'parts' not in self.cache:
        bot.info('Caching parts for future requests...')
        parts_listing = self.get_parts()
        parts = {}
        for part in parts_listing:
            parts[part['uuid']] = self.get_parts(uuid=(part['uuid']))

        self.cache['parts'] = parts