# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vagoth/scheduler/sync.py
# Compiled at: 2013-12-29 04:18:59
"""
This scheduler is suitable for small installations and frontend tools where
making synchronous calls to the hypervisor driver is appropriate.

For example, a command line VM management tool.
"""
from .. import exceptions

class SyncJobScheduler(object):
    """
    A synchronous job "scheduler"
    """

    def __init__(self, manager, config):
        self.manager = manager
        self.config = config

    def action(self, queue_name, action, **kwargs):
        """
        This calls self.manager.action() to run the action
        in the current thread.
        """
        self.manager.action(action, **kwargs)

    def cleanup(self):
        pass