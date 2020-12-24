# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rd/.envs/bb/lib/python3.6/site-packages/edgy/event/event.py
# Compiled at: 2016-12-28 09:48:30
# Size of source mod 2**32: 192 bytes
from __future__ import absolute_import

class Event(object):
    propagation_stopped = False

    def stop_propagation(self):
        self.propagation_stopped = True