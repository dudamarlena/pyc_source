# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/parameter_handler.py
# Compiled at: 2013-04-04 15:36:36
"""Defines an interface implemented by classes capable of handling
external parameters."""
from muntjac.terminal.terminal import IErrorEvent as ITerminalErrorEvent

class IParameterHandler(object):
    """C{IParameterHandler} is implemented by classes capable of handling
    external parameters.

    What parameters are provided depend on what the L{Terminal} provides
    and if the application is deployed as a servlet. URL GET
    parameters are typically provided to the L{handleParameters}
    method.

    A C{IParameterHandler} must be registered to a C{Window} using
    L{Window.addParameterHandler} to be called when parameters are available.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def handleParameters(self, parameters):
        """Handles the given parameters. All parameters names are of type
        string and the values are string arrays.

        @param parameters:
                   an unmodifiable map which contains the parameter names
                   and values
        """
        raise NotImplementedError


class IErrorEvent(ITerminalErrorEvent):
    """An IErrorEvent implementation for IParameterHandler."""

    def getParameterHandler(self):
        """Gets the IParameterHandler that caused the error.

        @return: the IParameterHandler that caused the error
        """
        raise NotImplementedError