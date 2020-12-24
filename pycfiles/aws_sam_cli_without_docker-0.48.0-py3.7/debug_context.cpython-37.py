# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/commands/local/lib/debug_context.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 755 bytes
"""
Information and debug options for a specific runtime.
"""

class DebugContext:

    def __init__(self, debug_ports=None, debugger_path=None, debug_args=None):
        """
        Initialize the Debug Context with Lambda debugger options

        :param tuple(int) debug_ports: Collection of debugger ports to be exposed from a docker container
        :param Path debugger_path: Path to a debugger to be launched
        :param string debug_args: Additional arguments to be passed to the debugger
        """
        self.debug_ports = debug_ports
        self.debugger_path = debugger_path
        self.debug_args = debug_args

    def __bool__(self):
        return bool(self.debug_ports)

    def __nonzero__(self):
        return self.__bool__()