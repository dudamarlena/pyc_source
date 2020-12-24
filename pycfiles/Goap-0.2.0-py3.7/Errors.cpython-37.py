# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Goap/Errors.py
# Compiled at: 2019-07-05 11:36:04
# Size of source mod 2**32: 919 bytes
from __future__ import absolute_import
from __future__ import unicode_literals

class OperationFailedError(Exception):

    def __init__(self, reason):
        self.msg = reason


class SensorError(Exception):
    __doc__ = " Sensor's Error base class "


class SensorMultipleTypeError(SensorError):
    __doc__ = ' Sensor can not be two type at once '


class SensorDoesNotExistError(SensorError):
    __doc__ = ' Sensor do not exist '


class SensorAlreadyInCollectionError(SensorError):
    __doc__ = ' Sensor do not exist '


class PlanError(Exception):
    pass


class PlanFailed(PlanError):
    pass


class ActionError(Exception):
    __doc__ = " Action's Error base class "


class ActionMultipleTypeError(ActionError):
    __doc__ = ' Action cannot be two types at once '


class ActionAlreadyInCollectionError(ActionError):
    __doc__ = ' Action with same name already in collection '