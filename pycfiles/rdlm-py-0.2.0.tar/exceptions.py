# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fab/Documents/rdlm-py/rdlmpy/exceptions.py
# Compiled at: 2013-06-06 16:19:47


class RDLMException(Exception):
    """
    Abstract class to represent a generic RDLM exception
    """
    pass


class RDLMLockWaitExceededException(RDLMException):
    """
    Exception: the lock is not acquired after wait timeout
    """
    pass


class RDLMLockDeletedException(RDLMException):
    """
    Exception: the lock has been deleted by an delete request
    """
    pass


class RDLMServerException(RDLMException):
    """
    Unknown exception from the RDLM server
    """
    pass


class RDLMClientException(RDLMException):
    """
    Unknown exception from the client
    """
    pass