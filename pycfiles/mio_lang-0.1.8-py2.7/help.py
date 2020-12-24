# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fabfile/help.py
# Compiled at: 2013-12-08 17:19:04
"""Help Tasks"""
from __future__ import print_function
from fabric import state
from fabric.api import task
from fabric.tasks import Task
from fabric.task_utils import crawl

@task(default=True)
def help(name=None):
    """Display help for a given task

    Options:
        name    - The task to display help on.

    To display a list of available tasks type:

        $ fab -l

    To display help on a specific task type:

        $ fab help:<name>
    """
    if name is None:
        name = 'help'
    task = crawl(name, state.commands)
    if isinstance(task, Task):
        doc = getattr(task, '__doc__', None)
        if doc is not None:
            print(('Help on {0:s}:').format(name))
            print()
            print(doc)
        else:
            print(('No help available for {0;s}').format(name))
    else:
        print(('No such task {0:s}').format(name))
        print('For a list of tasks type: fab -l')
    return