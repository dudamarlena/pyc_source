# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twisting/worker/task.py
# Compiled at: 2009-03-28 16:00:34
"""Gui box managed by the progress window for a task progress information
presentation.
"""
from Queue import Queue
from twisted.internet import reactor
from zope.interface import implements
from twisting import ITask, TaskBase
from twisting.messages import Pause, Play, Stop
__all__ = [
 'Task']

class Task(TaskBase):
    """Gtk event box to be added in the progress window for task progress view.
    """
    implements(ITask)

    def __init__(self, id_, pretty_name, remove_callback, finish_callback):
        """Init the task box variables and call init widget method to create
        and set an nice object for the progress representation of a specific
        task.

        @param id_: specific id of the task, common in all the twisting
        framework for separated management in the progress window
        @type id_: str

        @param pretty_name: much pretty name than the id for information
        displaying.
        @type pretty_name: str

        @param remove_callback: callback from the parent progress window
        to call on remove signal to ask for self removal when ask by the user
        @type remove_callback: function

        @param finish_callback: callback from the parent progress window
        to call at then end for main progress status update
        @type finish_callback: function
        """
        TaskBase.__init__(self, id_, pretty_name, remove_callback, finish_callback)
        self.__progression_title = self.pretty_name
        self.__progress_bar = 0
        self.__progression_label = ''

    def set_progress_end_state(self, label):
        """Common internal terminal method call from stop or finish state
        and finish flag update.

        @param label: specific label to display at the task end
        @type label: str
        """
        TaskBase.set_progress_end_state(self, label)
        self.__progress_bar = 1
        self.__progression_label = label

    def set_title(self, text):
        """Simple title label update. Can be used at the end somewhere
        else to pass a message to the user.
        """
        self.__progression_title = text

    def set_text(self, text):
        """Simple progress info label update. Can be used at the end somewhere
        else to pass a message to the user.
        """
        self.__progression_label = text