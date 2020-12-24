# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/commands/local/lib/local_lambda.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 10043 bytes
"""
Implementation of Local Lambda runner
"""
import os, logging, boto3
from samcli.lib.utils.codeuri import resolve_code_path
from samcli.local.lambdafn.env_vars import EnvironmentVariables
from samcli.local.lambdafn.config import FunctionConfig
from samcli.local.lambdafn.exceptions import FunctionNotFound
from samcli.commands.local.lib.exceptions import OverridesNotWellDefinedError
LOG = logging.getLogger(__name__)

class LocalLambdaRunner:
    __doc__ = '\n    Runs Lambda functions locally. This class is a wrapper around the `samcli.local` library which takes care\n    of actually running the function on a Docker container.\n    '
    MAX_DEBUG_TIMEOUT = 36000

    def __init__(self, local_runtime, function_provider, cwd, aws_profile=None, aws_region=None, env_vars_values=None, debug_context=None):
        """
        Initializes the class

        :param samcli.local.lambdafn.runtime.LambdaRuntime local_runtime: Lambda runtime capable of running a function
        :param samcli.commands.local.lib.provider.FunctionProvider function_provider: Provider that can return a
            Lambda function
        :param string cwd: Current working directory. We will resolve all function CodeURIs relative to this directory.
        :param string aws_profile: Optional. Name of the profile to fetch AWS credentials from.
        :param string aws_region: Optional. AWS Region to use.
        :param dict env_vars_values: Optional. Dictionary containing values of environment variables.
        :param DebugContext debug_context: Optional. Debug context for the function (includes port, args, and path).
        """
        self.local_runtime = local_runtime
        self.provider = function_provider
        self.cwd = cwd
        self.aws_profile = aws_profile
        self.aws_region = aws_region
        self.env_vars_values = env_vars_values or {}
        self.debug_context = debug_context
        self._boto3_session_creds = None
        self._boto3_region = None

    def invoke(self, function_name, event, stdout=None, stderr=None):
        """
        Find the Lambda function with given name and invoke it. Pass the given event to the function and return
        response through the given streams.

        This function will block until either the function completes or times out.

        Parameters
        ----------
        function_name str
            Name of the Lambda function to invoke
        event str
            Event data passed to the function. Must be a valid JSON String.
        stdout samcli.lib.utils.stream_writer.StreamWriter
            Stream writer to write the output of the Lambda function to.
        stderr samcli.lib.utils.stream_writer.StreamWriter
            Stream writer to write the Lambda runtime logs to.

        Raises
        ------
        FunctionNotfound
            When we cannot find a function with the given name
        """
        function = self.provider.get(function_name)
        if not function:
            all_functions = [f.functionname for f in self.provider.get_all()]
            available_function_message = '{} not found. Possible options in your template: {}'.format(function_name, all_functions)
            LOG.info(available_function_message)
            raise FunctionNotFound("Unable to find a Function with name '{}'".format(function_name))
        LOG.debug("Found one Lambda function with name '%s'", function_name)
        LOG.info('Invoking %s (%s)', function.handler, function.runtime)
        config = self._get_invoke_config(function)
        self.local_runtime.invoke(config, event, debug_context=(self.debug_context), stdout=stdout, stderr=stderr)

    def is_debugging(self):
        """
        Are we debugging the invoke?

        Returns
        -------
        bool
            True, if we are debugging the invoke ie. the Docker container will break into the debugger and wait for
            attach
        """
        return bool(self.debug_context)

    def _get_invoke_config(self, function):
        """
        Returns invoke configuration to pass to Lambda Runtime to invoke the given function

        :param samcli.commands.local.lib.provider.Function function: Lambda function to generate the configuration for
        :return samcli.local.lambdafn.config.FunctionConfig: Function configuration to pass to Lambda runtime
        """
        env_vars = self._make_env_vars(function)
        code_abs_path = resolve_code_path(self.cwd, function.codeuri)
        LOG.debug('Resolved absolute path to code is %s', code_abs_path)
        function_timeout = function.timeout
        if self.is_debugging():
            function_timeout = self.MAX_DEBUG_TIMEOUT
        return FunctionConfig(name=(function.functionname),
          runtime=(function.runtime),
          handler=(function.handler),
          code_abs_path=code_abs_path,
          layers=(function.layers),
          memory=(function.memory),
          timeout=function_timeout,
          env_vars=env_vars)

    def _make_env_vars(self, function):
        """Returns the environment variables configuration for this function

        Parameters
        ----------
        function : samcli.commands.local.lib.provider.Function
            Lambda function to generate the configuration for

        Returns
        -------
        samcli.local.lambdafn.env_vars.EnvironmentVariables
            Environment variable configuration for this function

        Raises
        ------
        samcli.commands.local.lib.exceptions.OverridesNotWellDefinedError
            If the environment dict is in the wrong format to process environment vars

        """
        name = function.functionname
        variables = None
        if function.environment and isinstance(function.environment, dict) and 'Variables' in function.environment:
            variables = function.environment['Variables']
        else:
            LOG.debug("No environment variables found for function '%s'", name)
        for env_var_value in self.env_vars_values.values():
            if not isinstance(env_var_value, dict):
                reason = '\n                            Environment variables must be in either CloudFormation parameter file\n                            format or in {FunctionName: {key:value}} JSON pairs\n                            '
                LOG.debug(reason)
                raise OverridesNotWellDefinedError(reason)

        if 'Parameters' in self.env_vars_values:
            LOG.debug('Environment variables overrides data is in CloudFormation parameter file format')
            overrides = self.env_vars_values['Parameters']
        else:
            LOG.debug('Environment variables overrides data is standard format')
            overrides = self.env_vars_values.get(name, None)
        shell_env = os.environ
        aws_creds = self.get_aws_creds()
        return EnvironmentVariables((function.memory),
          (function.timeout),
          (function.handler),
          variables=variables,
          shell_env_values=shell_env,
          override_values=overrides,
          aws_creds=aws_creds)

    def _get_session_creds(self):
        if self._boto3_session_creds is None:
            LOG.debug("Loading AWS credentials from session with profile '%s'", self.aws_profile)
            session = boto3.session.Session(profile_name=(self.aws_profile), region_name=(self.aws_region))
            if hasattr(session, 'region_name'):
                if session.region_name:
                    self._boto3_region = session.region_name
            if session:
                self._boto3_session_creds = session.get_credentials()
        return self._boto3_session_creds

    def get_aws_creds(self):
        """
        Returns AWS credentials obtained from the shell environment or given profile

        :return dict: A dictionary containing credentials. This dict has the structure
             {"region": "", "key": "", "secret": "", "sessiontoken": ""}. If credentials could not be resolved,
             this returns None
        """
        result = {}
        creds = self._get_session_creds()
        if self._boto3_region:
            result['region'] = self._boto3_region
        else:
            return creds or result
        if hasattr(creds, 'access_key'):
            if creds.access_key:
                result['key'] = creds.access_key
        if hasattr(creds, 'secret_key'):
            if creds.secret_key:
                result['secret'] = creds.secret_key
        if hasattr(creds, 'token'):
            if creds.token:
                result['sessiontoken'] = creds.token
        return result