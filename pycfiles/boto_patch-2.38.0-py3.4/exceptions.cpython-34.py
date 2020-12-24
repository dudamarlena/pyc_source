# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/swf/exceptions.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 958 bytes
"""
Exceptions that are specific to the swf module.

This module subclasses the base SWF response exception, 
boto.exceptions.SWFResponseError, for some of the SWF specific faults.
"""
from boto.exception import SWFResponseError

class SWFDomainAlreadyExistsError(SWFResponseError):
    __doc__ = '\n    Raised when when the domain already exists.\n    '


class SWFLimitExceededError(SWFResponseError):
    __doc__ = '\n    Raised when when a system imposed limitation has been reached.\n    '


class SWFOperationNotPermittedError(SWFResponseError):
    __doc__ = '\n    Raised when (reserved for future use).\n    '


class SWFTypeAlreadyExistsError(SWFResponseError):
    __doc__ = '\n    Raised when when the workflow type or activity type already exists.\n    '


class SWFWorkflowExecutionAlreadyStartedError(SWFResponseError):
    __doc__ = '\n    Raised when an open execution with the same workflow_id is already running\n    in the specified domain.\n    '