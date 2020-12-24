# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/exceptions.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3299 bytes


class AirflowException(Exception):
    """AirflowException"""
    status_code = 500


class AirflowBadRequest(AirflowException):
    """AirflowBadRequest"""
    status_code = 400


class AirflowNotFoundException(AirflowException):
    """AirflowNotFoundException"""
    status_code = 404


class AirflowConfigException(AirflowException):
    pass


class AirflowSensorTimeout(AirflowException):
    pass


class AirflowRescheduleException(AirflowException):
    """AirflowRescheduleException"""

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
    """DagNotFound"""
    pass


class DagRunNotFound(AirflowNotFoundException):
    """DagRunNotFound"""
    pass


class DagRunAlreadyExists(AirflowBadRequest):
    """DagRunAlreadyExists"""
    pass


class DagFileExists(AirflowBadRequest):
    """DagFileExists"""
    pass


class TaskNotFound(AirflowNotFoundException):
    """TaskNotFound"""
    pass


class TaskInstanceNotFound(AirflowNotFoundException):
    """TaskInstanceNotFound"""
    pass


class PoolNotFound(AirflowNotFoundException):
    """PoolNotFound"""
    pass


class NoAvailablePoolSlot(AirflowException):
    """NoAvailablePoolSlot"""
    pass


class DagConcurrencyLimitReached(AirflowException):
    """DagConcurrencyLimitReached"""
    pass


class TaskConcurrencyLimitReached(AirflowException):
    """TaskConcurrencyLimitReached"""
    pass