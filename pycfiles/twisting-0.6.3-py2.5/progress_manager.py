# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twisting/progress_manager.py
# Compiled at: 2009-03-28 16:00:34
from zinspect import conforms
from twisting import IProgress, ITask, ProgressBase, TaskBase

class ProgressManager(object):
    state_machine = None
    instance = None

    def __new__(klass, title='Progression dialog', all_finish_callback=None, ui=False):
        """
        """
        if klass.instance is None:
            if ui:
                from twisting.gui_worker import ProgressWindow, TaskBox
                conforms(ProgressBase, IProgress)
                conforms(TaskBase, ITask)
                instance_ = ProgressWindow(title=title, all_finish_callback=all_finish_callback)
            else:
                from twisting.worker import Progress, Task
                conforms(ProgressBase, IProgress)
                conforms(TaskBase, ITask)
                instance_ = Progress(all_finish_callback=all_finish_callback)
            klass.instance = instance_
        return klass.instance