# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/state.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 3179 bytes
from __future__ import unicode_literals
from builtins import object

class State(object):
    """State"""
    NONE = None
    REMOVED = 'removed'
    SCHEDULED = 'scheduled'
    QUEUED = 'queued'
    RUNNING = 'running'
    SUCCESS = 'success'
    SHUTDOWN = 'shutdown'
    FAILED = 'failed'
    UP_FOR_RETRY = 'up_for_retry'
    UP_FOR_RESCHEDULE = 'up_for_reschedule'
    UPSTREAM_FAILED = 'upstream_failed'
    SKIPPED = 'skipped'
    task_states = (
     SUCCESS,
     RUNNING,
     FAILED,
     UPSTREAM_FAILED,
     SKIPPED,
     UP_FOR_RETRY,
     UP_FOR_RESCHEDULE,
     QUEUED,
     NONE,
     SCHEDULED)
    dag_states = (
     SUCCESS,
     RUNNING,
     FAILED)
    state_color = {QUEUED: 'gray', 
     RUNNING: 'lime', 
     SUCCESS: 'green', 
     SHUTDOWN: 'blue', 
     FAILED: 'red', 
     UP_FOR_RETRY: 'gold', 
     UP_FOR_RESCHEDULE: 'turquoise', 
     UPSTREAM_FAILED: 'orange', 
     SKIPPED: 'pink', 
     REMOVED: 'lightgrey', 
     SCHEDULED: 'tan', 
     NONE: 'lightblue'}

    @classmethod
    def color(cls, state):
        return cls.state_color.get(state, 'white')

    @classmethod
    def color_fg(cls, state):
        color = cls.color(state)
        if color in ('green', 'red'):
            return 'white'
        else:
            return 'black'

    @classmethod
    def finished(cls):
        """
        A list of states indicating that a task started and completed a
        run attempt. Note that the attempt could have resulted in failure or
        have been interrupted; in any case, it is no longer running.
        """
        return [
         cls.SUCCESS,
         cls.FAILED,
         cls.SKIPPED]

    @classmethod
    def unfinished(cls):
        """
        A list of states indicating that a task either has not completed
        a run or has not even started.
        """
        return [
         cls.NONE,
         cls.SCHEDULED,
         cls.QUEUED,
         cls.RUNNING,
         cls.SHUTDOWN,
         cls.UP_FOR_RETRY,
         cls.UP_FOR_RESCHEDULE]