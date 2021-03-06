# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/wait_time.py
# Compiled at: 2020-04-13 02:37:12
# Size of source mod 2**32: 1886 bytes
import random
from time import time

def between(min_wait, max_wait):
    """
    Returns a function that will return a random number between min_wait and max_wait.
    
    Example::
    
        class User(Locust):
            # wait between 3.0 and 10.5 seconds after each task
            wait_time = between(3.0, 10.5)
    """
    return lambda instance: min_wait + random.random() * (max_wait - min_wait)


def constant(wait_time):
    """
    Returns a function that just returns the number specified by the wait_time argument
    
    Example::
    
        class User(Locust):
            wait_time = constant(3)
    """
    return lambda instance: wait_time


def constant_pacing(wait_time):
    """
    Returns a function that will track the run time of the tasks, and for each time it's 
    called it will return a wait time that will try to make the total time between task 
    execution equal to the time specified by the wait_time argument. 
    
    In the following example the task will always be executed once every second, no matter 
    the task execution time::
    
        class User(Locust):
            wait_time = constant_pacing(1)
            class task_set(TaskSet):
                @task
                def my_task(self):
                    time.sleep(random.random())
    
    If a task execution exceeds the specified wait_time, the wait will be 0 before starting 
    the next task.
    """

    def wait_time_func(self):
        if not hasattr(self, '_cp_last_run'):
            self._cp_last_wait_time = wait_time
            self._cp_last_run = time()
            return wait_time
        run_time = time() - self._cp_last_run - self._cp_last_wait_time
        self._cp_last_wait_time = max(0, wait_time - run_time)
        self._cp_last_run = time()
        return self._cp_last_wait_time

    return wait_time_func