# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lems/base/errors.py
# Compiled at: 2015-11-16 08:17:20
"""
Error classes.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

class LEMSError(Exception):
    """
    Base exception class.
    """

    def __init__(self, message, *params, **key_params):
        """
        Constructor

        @param message: Error message.
        @type message: string

        @param params: Optional arguments for formatting.
        @type params: list

        @param key_params: Named arguments for formatting.
        @type key_params: dict
        """
        self.message = None
        if params:
            if key_params:
                self.message = message.format(*params, **key_params)
            else:
                self.message = message.format(*params)
        elif key_params:
            self.message = message(**key_params)
        else:
            self.message = message
        return

    def __str__(self):
        """
        Returns the error message string.

        @return: The error message
        @rtype: string
        """
        return self.message


class StackError(LEMSError):
    """
    Exception class to signal errors in the Stack class.
    """
    pass


class ParseError(LEMSError):
    """
    Exception class to signal errors found during parsing.
    """
    pass


class ModelError(LEMSError):
    """
    Exception class to signal errors in creating the model.
    """
    pass


class SimBuildError(LEMSError):
    """
    Exception class to signal errors in building the simulation.
    """
    pass


class SimError(LEMSError):
    """
    Exception class to signal errors in simulation.
    """
    pass