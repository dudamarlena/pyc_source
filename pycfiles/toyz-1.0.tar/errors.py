# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/data-beta/users/fmooleka/git_projects/toyz/toyz/utils/errors.py
# Compiled at: 2015-06-30 23:44:06
"""
Error classes used in Toyz.
"""
import traceback

class Error(Exception):
    """
    Base class for custom errors related to the running of Toyz
    """
    pass


class ToyzError(Error):
    """
    Class for custom errors related to the running of Toyz.
    """

    def __init__(self, msg):
        self.msg = msg
        self.traceback = traceback.format_exc()

    def __str__(self):
        return self.traceback + '\n' + self.msg + '\n'


class ToyzDbError(ToyzError):
    """
    Class for errors initiating in the Toyz Database Interface
    """
    pass


class ToyzWebError(ToyzError):
    """
    Class for errors initiating in the Toyz Web Application
    """
    pass


class ToyzJobError(ToyzError):
    """
    Class for errors initiating in the Toyz Job Queue
    """
    pass


class ToyzIoError(ToyzError):
    """
    Class for I/O Errors
    """
    pass


class ToyzDataError(ToyzError):
    """
    Class for Toyz DataSource Errors
    """
    pass


class ToyzWarning:
    """
    Class for warnings
    """

    def __init__(self, msg):
        print ('Warning: {0}').format(msg)


toyz_errors = [
 ToyzError, ToyzDbError, ToyzWebError, ToyzJobError]