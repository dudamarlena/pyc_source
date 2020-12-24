# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/locking/manager.py
# Compiled at: 2019-08-16 12:27:43
from __future__ import absolute_import
from sentry.utils.locking.lock import Lock

class LockManager(object):

    def __init__(self, backend):
        self.backend = backend

    def get(self, key, duration, routing_key=None):
        """
        Retrieve a ``Lock`` instance.
        """
        return Lock(self.backend, key, duration, routing_key)