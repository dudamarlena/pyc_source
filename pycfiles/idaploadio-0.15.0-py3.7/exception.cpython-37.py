# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/exception.py
# Compiled at: 2020-04-15 05:36:19
# Size of source mod 2**32: 1052 bytes


class LocustError(Exception):
    pass


class ResponseError(Exception):
    pass


class CatchResponseError(Exception):
    pass


class MissingWaitTimeError(LocustError):
    pass


class InterruptTaskSet(Exception):
    __doc__ = '\n    Exception that will interrupt a Locust when thrown inside a task\n    '

    def __init__(self, reschedule=True):
        """
        If *reschedule* is True and the InterruptTaskSet is raised inside a nested TaskSet,
        the parent TaskSet whould immediately reschedule another task.
        """
        self.reschedule = reschedule


class StopLocust(Exception):
    pass


class RescheduleTask(Exception):
    __doc__ = "\n    When raised in a task it's equivalent of a return statement.\n    \n    Used internally by TaskSet. When raised within the task control flow of a TaskSet, \n    but not inside a task, the execution should be handed over to the parent TaskSet.\n    "


class RescheduleTaskImmediately(Exception):
    __doc__ = '\n    When raised in a Locust task, another idapload task will be rescheduled immediately\n    '