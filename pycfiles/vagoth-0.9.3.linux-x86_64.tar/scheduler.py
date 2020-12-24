# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vagoth/interfaces/scheduler.py
# Compiled at: 2013-12-29 04:14:58
import zope.interface as ZI

class IScheduler(ZI.Interface):
    """
    Scheduler's are called to schedule the background execution of actions.
    Vagoth's default schedulers are quite basic, but you can implement your
    own so long as it matches the IScheduler interface.
    """

    def __init__(manager, config):
        """
        Instantiated with an instance of Manager and a configuration dict
        """
        pass

    def action(self, queue_name, action, **kwargs):
        """
        Schedule the given action with kwargs.

        Actions in the same queue_name should be executed in sequence.
        """
        pass

    def cleanup(self):
        """
        Called by Manager.cleanup() at shutdown time.
        It could be used to close DB connections, cleanup threads or
        child processes, etc.
        """
        pass