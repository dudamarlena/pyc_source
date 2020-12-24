# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twisting/progress_base.py
# Compiled at: 2009-03-30 16:53:59
"""Useful window for  progress task boxes display and management.
"""
from twisted.internet import reactor, threads
from zope.interface import implements
from twisting import IProgress
from twisting.messages import Stop
import logging
log = logging.getLogger()
__all__ = [
 'ProgressException', 'NotInitializeError', 'ProgressBase']

class ProgressException(Exception):
    pass


class NotInitializeError(ProgressException):
    pass


class ProgressBase(object):
    """Specific manager for tasks for the base worker API.
    """
    implements(IProgress)

    def __init__(self, all_finish_callback=None):
        """Instantiate a new singleton that can be call everywhere after.

        @param title: title of the manager, default: 'Progression manager'
        @type title: str

        @param all_finish_callback: specific callback for all tasks ending
        @type all_finish_callback: function
        """
        self.initialized = True
        self.task_dict = dict()
        self.all_finish_callback = all_finish_callback

    def add_task(self, id_, pretty_name):
        """Add a new task box into the progress window and init the twisted
        *deferToThread* callbacks for work, error, and result.

        @param id_: id of the task to create
        @type id_: str

        @param pretty_name: pretty name of the task to display in the box
        @type pretty_name: str
        """
        NotImplementedError('You must implement parse method')

    def start_task(self, id_, worker_callback, end_callback=None, error_callback=None, param=None):
        """Start a specific task.

        @param id_: id of the task to start
        @type id_: str

        @param worker_callback: worker function to manage
        @type worker_callback: function

        @param end_callback: function to call at the end
        @type end_callback: function

        @param error_callback: function to call in case of error
        @type error_callback: function

        @param param: simple way to add specific parameter when the task will be
        executed.
        @type param: obj
        """
        if not hasattr(self, 'initialized'):
            msg = 'You should initialize the progress window before using it'
            raise NotInitializeError(msg)
        if not self.task_dict.has_key(id_):
            return False
        if not worker_callback:
            return False
        task = self.task_dict[id_]
        if param:
            defered_thread = threads.deferToThread(worker_callback, task, param)
        else:
            defered_thread = threads.deferToThread(worker_callback, task)
        if end_callback:
            defered_thread.addCallback(end_callback)
        if error_callback:
            defered_thread.addErrback(error_callback)
        return True

    def stop_task(self, id_):
        """Stop a specific task using queue.

        @param id_: id of the task to remove
        @type id_: str
        """
        if not hasattr(self, 'initialized'):
            msg = 'You should initialize the progress window before using it'
            raise NotInitializeError(msg)
        if not self.task_dict.has_key(id_):
            return
        task = self.task_dict[id_]
        task.task_event_queue.put(Stop(id_))

    def stop_all_tasks(self):
        """Stop all the tasks.
        """
        if not hasattr(self, 'initialized'):
            msg = 'You should initialize the progress window before using it'
            raise NotInitializeError(msg)
        for key in self.task_dict.keys():
            self.stop_task(key)

    def remove_task(self, id_):
        """Remove a task box and the corresponding separator (pure esthetic
        problem, no functional need).

        @param id_: id of the task to remove
        @type id_: str
        """
        if not hasattr(self, 'initialized'):
            msg = 'You should initialize the progress window before using it'
            raise NotInitializeError(msg)
        if not self.task_dict.has_key(id_):
            return
        self.task_dict.pop(id_)

    def remove_all_tasks(self):
        """Remove all the tasks for next works.
        """
        if not hasattr(self, 'initialized'):
            msg = 'You should initialize the progress window before using it'
            raise NotInitializeError(msg)
        for key in self.task_dict.keys():
            self.remove_task(key)

    def quit(self):
        """Stop and remove all.
        """
        self.stop_all_tasks()
        self.remove_all_tasks()

    def pulse(self, id_):
        """update a task box progress pulse status.

        @param id_: id of the task to update
        @type id_: str
        """
        if not hasattr(self, 'initialized'):
            msg = 'You should initialize the progress window before using it'
            raise NotInitializeError(msg)
        if not self.task_dict.has_key(id_):
            return
        reactor.callFromThread(self.task_dict[id_].pulse)

    def task_finish(self, id_):
        """Set the final status for a specific method and check if all tasks
        are finished. If all task are ended call the all_task_finished callback
        from the parent window.

        @param id_: id of the task that was just ended
        @type id_: str
        """
        number_of_finished_tasks = 0
        for key in self.task_dict.keys():
            if self.task_dict[key].is_finished:
                number_of_finished_tasks += 1

        if number_of_finished_tasks == len(self.task_dict) and number_of_finished_tasks > 0:
            self.all_finish_callback()