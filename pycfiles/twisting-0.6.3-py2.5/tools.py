# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twisting/tools.py
# Compiled at: 2009-03-28 16:00:34
"""Little tools package form relative packaged resource path retrieval.
"""
import pkg_resources
from twisted.internet import reactor
from twisting.messages import Pause, Play, Stop
from twisting import ProgressManager
__ALL__ = [
 'check', 'get_filepath', 'pulse', 'state_machine']

def get_filepath(class_path, file_name):
    """return the relative static path to a file

    @param class_path: must be call with __name__
    @type class_path: str

    @param file_name: name of the expected file
    @type file_name: str
    """
    if pkg_resources.resource_exists(class_path, file_name):
        return pkg_resources.resource_filename(class_path, file_name)
    else:
        return
    return


def pulse(task):
    ProgressManager().pulse(task.id_)


def check(task):
    """Check the current progress state of a specific task.

    @param task: task to be checked
    @type task: twisting.base_worker.Task

    @return: boolean info:
        - True: when a stop message from the task is catched
        - False: no message catched, the worker can continue
    """
    while not task.task_event_queue.empty():
        event = task.task_event_queue.get()
        if isinstance(event, Stop):
            reactor.callFromThread(task.stop)
            return True
        if isinstance(event, Pause):
            event_pause = task.task_event_queue.get(block=True)
            if isinstance(event_pause, Play):
                pass
            elif isinstance(event_pause, Stop):
                reactor.callFromThread(task.stop)
                return True

    return False


def state_machine(task):
    """Sate machine method call by the worker to up update a task and the
    progress window, or be paused or stopped. Must be call in the worker loop
    otherwhise no progress status or info will be updated.

    @param task: task to be checked
    @type task: twisting.base_worker.Task

    @return: boolean info:
        - True: when a stop message from the task is catched
        - False: no message catched, the worker can continue
    """
    pulse(task)
    return check(task)