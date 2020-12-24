# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kyzima-spb/www/django-projects/mosginfo/adminlte_full/tasks.py
# Compiled at: 2016-04-14 15:36:33
# Size of source mod 2**32: 908 bytes
import django.dispatch

class Task(object):
    COLOR_AQUA = 'aqua'
    COLOR_GREEN = 'green'
    COLOR_RED = 'red'
    COLOR_YELLOW = 'yellow'

    def __init__(self, title, progress, color=None, uid=None):
        self._Task__uid = uid
        self.title = title
        self.progress = progress
        self.color = color or self.COLOR_AQUA

    @property
    def uid(self):
        return self._Task__uid


class TaskList(object):
    show_signal = django.dispatch.Signal()

    def __init__(self):
        self._TaskList__tasks = []

    def add_task(self, task):
        if isinstance(task, Task):
            self._TaskList__tasks.append(task)

    @property
    def tasks(self):
        return self._TaskList__tasks

    @tasks.setter
    def tasks(self, tasks):
        for task in tasks:
            self.add_task(task)

    @property
    def total(self):
        return len(self.tasks)