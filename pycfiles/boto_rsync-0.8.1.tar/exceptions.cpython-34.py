# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/swf/exceptions.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 958 bytes
__doc__ = '\nExceptions that are specific to the swf module.\n\nThis module subclasses the base SWF response exception, \nboto.exceptions.SWFResponseError, for some of the SWF specific faults.\n'
from boto.exception import SWFResponseError

class SWFDomainAlreadyExistsError(SWFResponseError):
    """SWFDomainAlreadyExistsError"""
    pass


class SWFLimitExceededError(SWFResponseError):
    """SWFLimitExceededError"""
    pass


class SWFOperationNotPermittedError(SWFResponseError):
    """SWFOperationNotPermittedError"""
    pass


class SWFTypeAlreadyExistsError(SWFResponseError):
    """SWFTypeAlreadyExistsError"""
    pass


class SWFWorkflowExecutionAlreadyStartedError(SWFResponseError):
    """SWFWorkflowExecutionAlreadyStartedError"""
    pass