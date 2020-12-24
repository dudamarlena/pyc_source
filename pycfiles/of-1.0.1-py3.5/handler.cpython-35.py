# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/of/common/queue/handler.py
# Compiled at: 2016-09-15 19:50:18
# Size of source mod 2**32: 2071 bytes
"""
The handler module implements the Handler class.

Created on Jan 22, 2016

@author: Nicklas Boerjesson
"""
import os
from of.common.logging import write_to_log, EC_COMMUNICATION, SEV_DEBUG, EC_NOTIFICATION
__author__ = 'Nicklas Borjesson'

class Handler(object):
    __doc__ = '\n    Handler is the base class for all queue item handlers.\n    '
    log_prefix = None
    process_id = None
    _last_message_id = None

    def __init__(self, _process_id):
        self.process_id = _process_id
        self.log_prefix = str(os.getpid()) + '-' + self.__class__.__name__ + ': '

    def on_monitor_init(self, _monitor):
        """
        Override this to make something happen after the monitor has been initialized.

        :param _monitor: The monitor
        """
        pass

    def write_dbg_info(self, _data):
        """
        Shortcut to writing debug information
        :param _message: The message
        :param _severity: The severity of the log information, a constant defined in the built-in logging module
        """
        write_to_log(self.log_prefix + _data, _category=EC_NOTIFICATION, _severity=SEV_DEBUG, _process_id=self.process_id)

    def handle(self, _item):
        """
        This function is implemented by subclasses and is called when the monitor detects that an item has been queued.
        It is imperative that it doesn't contain synchronous code that might not return or otherwise hang in any way.
        Hint: Only use async I/0 and avoid complex library calls.

        :param _item: The item from the queue
        """
        raise Exception(self.log_prefix + 'The required call handler method is not implemented.')

    def shut_down(self, _user_id):
        """
        Called by the monitor when shutting down. Override to provide own actions

        :param _user_id: The Optimal BPM user id

        """
        pass