# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/argos/Workspace/mamba-framework/mamba-server/mamba_server/context.py
# Compiled at: 2020-05-12 06:36:57
# Size of source mod 2**32: 884 bytes
"""Application context that is shared between components"""

class Context:
    __doc__ = 'Application context class'

    def __init__(self):
        self._memory = {}

    def get(self, parameter):
        """Returns the value of a context parameter, or None if it
        doesn´t exists.

        Args:
            parameter (str): String identifier of the parameter.

        Returns:
           The parameter value. None if parameter does not exists in context.
        """
        if parameter in self._memory:
            return self._memory[parameter]

    def set(self, parameter, value):
        """Set the value of a context parameter. If already exists, value is
        overwritten.

        Args:
            parameter (str): String identifier of the parameter.
            value: New parameter value.
        """
        self._memory[parameter] = value