# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/of/common/queue/monitor.py
# Compiled at: 2016-09-15 19:50:33
# Size of source mod 2**32: 4715 bytes
"""
The monitor module implements the Monitor and MonitorThread classes.

Created on Jan 22, 2016

@author: Nicklas Boerjesson
"""
import os, traceback, threading
from queue import Empty, Queue
from of.common.logging import write_to_log, EC_UNCATEGORIZED, SEV_DEBUG, SEV_ERROR, EC_INTERNAL
from of.schemas.constants import zero_object_id
__author__ = 'Nicklas Boerjesson'

class MonitorThread(threading.Thread):
    terminated = None

    def __init__(self, _monitor):
        self.terminated = False
        super(MonitorThread, self).__init__(target=_monitor.monitor, name=_monitor.__class__.__name__ + '_queue monitor thread')


class Monitor(object):
    __doc__ = '\n    The monitor class monitors a given queue for new items and calls a handler when new items appear on the queue.\n    '
    queue = None
    handler = None
    process_id = None
    before_get_queue = None
    log_prefix = None
    monitor_thread = None

    def __init__(self, _handler, _queue=None):
        self.log_prefix = self.__class__.__name__ + '(' + str(_handler.__class__.__name__) + '): '
        if _queue:
            self.queue = _queue
        else:
            self.queue = Queue()
        self.handler = _handler
        self.handler.on_monitor_init(self)
        if self.queue:
            self.start()

    def write_dbg_info(self, _data):
        write_to_log(self.log_prefix + _data, _category=EC_UNCATEGORIZED, _severity=SEV_DEBUG, _process_id=self.process_id)

    def after_get_queue(self):
        """
        Implement this for something to happen immidiately after a each queue check has happened.
        """
        pass

    def monitor(self):
        """
        Monitors the queue. Stops when the queue-threads' terminated attribute is set to True
        """
        self.write_dbg_info('In monitor thread monitoring queue.')
        while not self.monitor_thread.terminated:
            try:
                _item = self.queue.get(True, 0.1)
                try:
                    self.handler.handle(_item)
                except Exception as e:
                    write_to_log(self.log_prefix + 'Error handling item:' + str(e) + '\nData:\n' + str(_item) + '\nTraceback:' + traceback.format_exc(), _category=EC_INTERNAL, _severity=SEV_ERROR)

            except Empty:
                pass
            except Exception as e:
                self.monitor_thread.terminated = True
                raise Exception(write_to_log(self.log_prefix + 'Terminating, error accessing own queue:' + str(e), _category=EC_INTERNAL, _severity=SEV_ERROR))

            self.after_get_queue()

        self.write_dbg_info('Monitor thread stopped.')

    def stop(self, _user_id=zero_object_id, _reverse_order=None):
        """
        Stops the monitor and tells the handler to shut down

        :param _user_id: The Optimal BPM user Id that is stopping the monitor
        :param _reverse_order: If true, the monitor is kept running while the handler is shut down.
        """
        if not _reverse_order:
            self.write_dbg_info('Told to stop, ceasing monitoring.')
            self.monitor_thread.terminated = True
        self.write_dbg_info('Shutting down handler(' + str(self.handler.__class__.__name__) + ').')
        self.handler.shut_down(_user_id)
        self.write_dbg_info('Handler shut down.')
        if _reverse_order:
            self.write_dbg_info('Told to stop, ceasing monitoring.')
            self.monitor_thread.terminated = True

    def start(self):
        """
        Start monitoring the queue
        """
        if self.monitor_thread and not self.monitor_thread.terminated:
            raise Exception(write_to_log(self.log_prefix + 'The queue monitor is already running.', _category=EC_INTERNAL, _severity=SEV_ERROR))
        self.monitor_thread = MonitorThread(_monitor=self)
        self.monitor_thread.terminated = False
        self.monitor_thread.start()
        self.write_dbg_info('Running, monitoring thread: ' + str(self.monitor_thread.name))