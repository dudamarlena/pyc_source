# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/local/lambdafn/env_vars.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 8029 bytes
"""
Supplies the environment variables necessary to set up Local Lambda runtime
"""
import sys

class EnvironmentVariables:
    __doc__ = '\n    Use this class to get the environment variables necessary to run the Lambda function. It returns the AWS specific\n    variables (credentials, regions, etc) along with any environment variables configured on the function.\n\n    Customers define the name of the environment variables along with default values, if any, when creating the\n    function. In order to test the function with different scenarios, customers can override values for some of the\n    variables. This class supports three mechanisms of providing values to environment variables.\n    If a variable is given a value through all the three mechanisms, then the value from higher priority will be used:\n\n    Priority (Highest to Lowest):\n        - Override Values - User specified these\n        - Shell Environment Values - Came from the shell environment\n        - Default Values - Hard coded values\n\n    If a variable does *not* get a value from either of the above mechanisms, it is given a value of "" (empty string).\n    If the value of a variable is an intrinsic function dict/list, then it is given a value of "" (empty string).\n\n    If real AWS Credentials were supplied, this class will expose them through appropriate environment variables.\n    If not, this class will provide the following placeholder values to AWS Credentials:\n        region = "us-east-1"\n        key = "defaultkey"\n        secret = "defaultsecret"\n    '
    _BLANK_VALUE = ''
    _DEFAULT_AWS_CREDS = {'region':'us-east-1',  'key':'defaultkey',  'secret':'defaultsecret'}

    def __init__(self, function_memory=None, function_timeout=None, function_handler=None, variables=None, shell_env_values=None, override_values=None, aws_creds=None):
        """
        Initializes this class. It takes in two sets of properties:
            a) (Required) Function information
            b) (Optional) Environment variable configured on the function

        :param integer function_memory: Memory size of the function in megabytes
        :param integer function_timeout: Function's timeout in seconds
        :param string function_handler: Handler of the function
        :param dict variables: Optional. Dict whose key is the environment variable names and value is the default
            values for the variable.
        :param dict shell_env_values: Optional. Dict containing values for the variables grabbed from the shell's
            environment.
        :param dict override_values: Optional. Dict containing values for the variables that will override the values
            from ``default_values`` and ``shell_env_values``.
        :param dict aws_creds: Optional. Dictionary containing AWS credentials passed to the Lambda runtime through
            environment variables. It should contain "key", "secret", "region" and optional "sessiontoken" keys
        """
        self._function = {'memory':function_memory, 
         'timeout':function_timeout,  'handler':function_handler}
        self.variables = variables or {}
        self.shell_env_values = shell_env_values or {}
        self.override_values = override_values or {}
        self.aws_creds = aws_creds or {}

    def resolve(self):
        """
        Resolves the values from different sources and returns a dict of environment variables to use when running
        the function locally.

        :return dict: Dict where key is the variable name and value is the value of the variable. Both key and values
            are strings
        """
        result = self._get_aws_variables()
        for name, value in self.variables.items():
            if name in self.shell_env_values:
                value = self.shell_env_values[name]
            if name in self.override_values:
                value = self.override_values[name]
            result[name] = self._stringify_value(value)

        return result

    def add_lambda_event_body(self, value):
        """
        Adds the value of AWS_LAMBDA_EVENT_BODY environment variable.
        """
        self.variables['AWS_LAMBDA_EVENT_BODY'] = value

    @property
    def timeout(self):
        return self._function['timeout']

    @timeout.setter
    def timeout(self, value):
        self._function['timeout'] = value

    @property
    def memory(self):
        return self._function['memory']

    @memory.setter
    def memory(self, value):
        self._function['memory'] = value

    @property
    def handler(self):
        return self._function['handler']

    @handler.setter
    def handler(self, value):
        self._function['handler'] = value

    def _get_aws_variables(self):
        """
        Returns the AWS specific environment variables that should be available in the Lambda runtime.
        They are prefixed it "AWS_*".

        :return dict: Name and value of AWS environment variable
        """
        result = {'AWS_SAM_LOCAL':'true', 
         'AWS_LAMBDA_FUNCTION_MEMORY_SIZE':str(self.memory), 
         'AWS_LAMBDA_FUNCTION_TIMEOUT':str(self.timeout), 
         'AWS_LAMBDA_FUNCTION_HANDLER':str(self._function['handler']), 
         'AWS_REGION':self.aws_creds.get('region', self._DEFAULT_AWS_CREDS['region']), 
         'AWS_DEFAULT_REGION':self.aws_creds.get('region', self._DEFAULT_AWS_CREDS['region']), 
         'AWS_ACCESS_KEY_ID':self.aws_creds.get('key', self._DEFAULT_AWS_CREDS['key']), 
         'AWS_SECRET_ACCESS_KEY':self.aws_creds.get('secret', self._DEFAULT_AWS_CREDS['secret'])}
        if self.aws_creds.get('sessiontoken'):
            result['AWS_SESSION_TOKEN'] = self.aws_creds.get('sessiontoken')
        return result

    def _stringify_value(self, value):
        """
        This method stringifies values of environment variables. If the value of the method is a list or dictionary,
        then this method will replace it with empty string. Values of environment variables in Lambda must be a string.
        List or dictionary usually means they are intrinsic functions which have not been resolved.

        :param value: Value to stringify
        :return string: Stringified value
        """
        if isinstance(value, (dict, list, tuple)) or value is None:
            result = self._BLANK_VALUE
        else:
            if value is True:
                result = 'true'
            else:
                if value is False:
                    result = 'false'
                else:
                    if sys.version_info.major > 2:
                        result = str(value)
                    else:
                        if not isinstance(value, unicode):
                            result = str(value)
                        else:
                            result = value
        return result