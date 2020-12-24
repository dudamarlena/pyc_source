# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/local/lambdafn/config.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 2229 bytes
"""
Lambda Function configuration data required by the runtime
"""
from samcli.commands.local.cli_common.user_exceptions import InvalidSamTemplateException
from .env_vars import EnvironmentVariables

class FunctionConfig:
    __doc__ = '\n    Data class to store function configuration. This class is a flavor of function configuration passed to\n    AWS Lambda APIs on the cloud. It is limited to properties that make sense in a local testing environment.\n    '
    _DEFAULT_TIMEOUT_SECONDS = 3
    _DEFAULT_MEMORY = 128

    def __init__(self, name, runtime, handler, code_abs_path, layers, memory=None, timeout=None, env_vars=None):
        """
        Initialize the class.

        Parameters
        ----------
        name str
            Name of the function
        runtime str
            Runtime of function
        handler str
            Handler method
        code_abs_path str
            Absolute path to the code
        layers list(str)
            List of Layers
        memory int
            Function memory limit in MB
        timeout int
            Function timeout in seconds
        env_vars samcli.local.lambdafn.env_vars.EnvironmentVariables
            Optional, Environment variables.
            If it not provided, this class will generate one for you based on the function properties
        """
        self.name = name
        self.runtime = runtime
        self.handler = handler
        self.code_abs_path = code_abs_path
        self.layers = layers
        self.memory = memory or self._DEFAULT_MEMORY
        self.timeout = timeout or self._DEFAULT_TIMEOUT_SECONDS
        if not isinstance(self.timeout, int):
            try:
                self.timeout = int(self.timeout)
            except (ValueError, TypeError):
                raise InvalidSamTemplateException('Invalid Number for Timeout: {}'.format(self.timeout))

        if not env_vars:
            env_vars = EnvironmentVariables(self.memory, self.timeout, self.handler)
        self.env_vars = env_vars
        self.env_vars.handler = self.handler
        self.env_vars.memory = self.memory
        self.env_vars.timeout = self.timeout