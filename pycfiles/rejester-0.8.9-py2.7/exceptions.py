# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rejester/exceptions.py
# Compiled at: 2015-07-08 07:32:10
"""Exceptions raised in various places in rejester.

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.
"""

class RejesterException(Exception):
    """base exception for rejester package"""
    pass


class EnvironmentError(RejesterException):
    """indicates that the registry lost a lock or experienced a similar
failure that probably indicates a network or remote server failure"""
    pass


class LockError(RejesterException):
    """attempt to get a lock exceeded acquire time (atime)"""
    pass


class NoSuchWorkSpecError(RejesterException):
    """A `TaskMaster` function was called with a nonexistent work spec"""

    def __init__(self, work_spec_name, *args, **kwargs):
        super(NoSuchWorkSpecError, self).__init__(*args, **kwargs)
        self.work_spec_name = work_spec_name


class NoSuchWorkUnitError(RejesterException):
    """Valid work spec but invalid work unit.

    This occurs when a :class:`rejester.TaskMaster` function that
    manipulates existing work units is called with a valid work spec name
    but an invalid work unit name.

    """

    def __init__(self, work_unit_name, *args, **kwargs):
        super(NoSuchWorkUnitError, self).__init__(*args, **kwargs)
        self.work_unit_name = work_unit_name


class ProgrammerError(RejesterException):
    pass


class PriorityRangeEmpty(RejesterException):
    """
    given the priority_min/max, no item is available to be returned
    """
    pass


class LostLease(RejesterException):
    """worker waited too long between calls to update and another worker
got the WorkItem"""
    pass


class ItemInUseError(RejesterException):
    """tried to add an item to a queue that was already in use"""
    pass