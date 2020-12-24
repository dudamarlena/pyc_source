# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twisting/worker/progress.py
# Compiled at: 2009-03-28 16:00:34
"""Useful window for  progress task boxes display and management.
"""
from zope.interface import implements
from twisting import IProgress, ProgressBase, NotInitializeError
from twisting.worker import Task
import logging
log = logging.getLogger()
__all__ = [
 'Progress']

class Progress(ProgressBase):
    """Specific manager for tasks for the base worker API.
    """

    def add_task(self, id_, pretty_name):
        """Add a new task box into the progress window and init the twisted
        *deferToThread* callbacks for work, error, and result.

        @param id_: id of the task to create
        @type id_: str

        @param pretty_name: pretty name of the task to display in the box
        @type pretty_name: str
        """
        if not hasattr(self, 'initialized'):
            msg = 'You should initialize the progress window before using it'
            raise NotInitializeError(msg)
        if self.task_dict.has_key(id_):
            return True
        task = Task(id_, pretty_name, self.remove_task, self.task_finish)
        self.task_dict[id_] = task
        return False