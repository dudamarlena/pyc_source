# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/exceptions.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3299 bytes


class AirflowException(Exception):
    __doc__ = "\n    Base class for all Airflow's errors.\n    Each custom exception should be derived from this class\n    "
    status_code = 500


class AirflowBadRequest(AirflowException):
    __doc__ = 'Raise when the application or server cannot handle the request'
    status_code = 400


class AirflowNotFoundException(AirflowException):
    __doc__ = 'Raise when the requested object/resource is not available in the system'
    status_code = 404


class AirflowConfigException(AirflowException):
    pass


class AirflowSensorTimeout(AirflowException):
    pass


class AirflowRescheduleException(AirflowException):
    __doc__ = '\n    Raise when the task should be re-scheduled at a later time.\n\n    :param reschedule_date: The date when the task should be rescheduled\n    :type reschedule: datetime.datetime\n    '

    def __init__(self, reschedule_date):
        self.reschedule_date = reschedule_date


class AirflowTaskTimeout(AirflowException):
    pass


class AirflowWebServerTimeout(AirflowException):
    pass


class AirflowSkipException(AirflowException):
    pass


class AirflowDagCycleException(AirflowException):
    pass


class DagNotFound(AirflowNotFoundException):
    __doc__ = 'Raise when a DAG is not available in the system'


class DagRunNotFound(AirflowNotFoundException):
    __doc__ = 'Raise when a DAG Run is not available in the system'


class DagRunAlreadyExists(AirflowBadRequest):
    __doc__ = 'Raise when creating a DAG run for DAG which already has DAG run entry'


class DagFileExists(AirflowBadRequest):
    __doc__ = 'Raise when a DAG ID is still in DagBag i.e., DAG file is in DAG folder'


class TaskNotFound(AirflowNotFoundException):
    __doc__ = 'Raise when a Task is not available in the system'


class TaskInstanceNotFound(AirflowNotFoundException):
    __doc__ = 'Raise when a Task Instance is not available in the system'


class PoolNotFound(AirflowNotFoundException):
    __doc__ = 'Raise when a Pool is not available in the system'


class NoAvailablePoolSlot(AirflowException):
    __doc__ = 'Raise when there is not enough slots in pool'


class DagConcurrencyLimitReached(AirflowException):
    __doc__ = 'Raise when DAG concurrency limit is reached'


class TaskConcurrencyLimitReached(AirflowException):
    __doc__ = 'Raise when task concurrency limit is reached'