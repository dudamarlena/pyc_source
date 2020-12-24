# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/lems/base/errors.py
# Compiled at: 2015-11-16 08:17:20
__doc__ = '\nError classes.\n\n@author: Gautham Ganapathy\n@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)\n@contact: gautham@lisphacker.org\n'

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


class ParseError(LEMSError):
    """
    Exception class to signal errors found during parsing.
    """


class ModelError(LEMSError):
    """
    Exception class to signal errors in creating the model.
    """


class SimBuildError(LEMSError):
    """
    Exception class to signal errors in building the simulation.
    """


class SimError(LEMSError):
    """
    Exception class to signal errors in simulation.
    """