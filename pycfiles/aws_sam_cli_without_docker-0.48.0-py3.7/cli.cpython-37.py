# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/commands/local/start_lambda/cli.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 5383 bytes
"""
CLI command for "local start-lambda" command
"""
import logging, click
from samcli.cli.main import pass_context, common_options as cli_framework_options, aws_creds_options
from samcli.commands.local.cli_common.options import invoke_common_options, service_common_options
from samcli.lib.telemetry.metrics import track_command
from samcli.cli.cli_config_file import configuration_option, TomlProvider
LOG = logging.getLogger(__name__)
HELP_TEXT = '\nYou can use this command to programmatically invoke your Lambda function locally using the AWS CLI or SDKs.\nThis command starts a local endpoint that emulates the AWS Lambda service, and you can run your automated\ntests against this local Lambda endpoint. When you send an invoke to this endpoint using the AWS CLI or\nSDK, it will locally execute the Lambda function specified in the request.\n\n\x08\nSETUP\n------\nStart the local Lambda endpoint by running this command in the directory that contains your AWS SAM template.\n$ sam local start-lambda\n\n\x08\nUSING AWS CLI\n-------------\nThen, you can invoke your Lambda function locally using the AWS CLI\n$ aws lambda invoke --function-name "HelloWorldFunction" --endpoint-url "http://127.0.0.1:3001" --no-verify-ssl out.txt\n\n\n\x08\nUSING AWS SDK\n-------------\nYou can also use the AWS SDK in your automated tests to invoke your functions programatically.\nHere is a Python example:\n    self.lambda_client = boto3.client(\'lambda\',\n                                  endpoint_url="http://127.0.0.1:3001",\n                                  use_ssl=False,\n                                  verify=False,\n                                  config=Config(signature_version=UNSIGNED,\n                                                read_timeout=0,\n                                                retries={\'max_attempts\': 0}))\n    self.lambda_client.invoke(FunctionName="HelloWorldFunction")\n'

@click.command('start-lambda',
  help=HELP_TEXT,
  short_help='Starts a local endpoint you can use to invoke your local Lambda functions.')
@configuration_option(provider=TomlProvider(section='parameters'))
@service_common_options(3001)
@invoke_common_options
@cli_framework_options
@aws_creds_options
@pass_context
@track_command
def cli(ctx, host, port, template_file, env_vars, debug_port, debug_args, debugger_path, docker_volume_basedir, docker_network, log_file, layer_cache_basedir, skip_pull_image, force_image_build, parameter_overrides):
    do_cli(ctx, host, port, template_file, env_vars, debug_port, debug_args, debugger_path, docker_volume_basedir, docker_network, log_file, layer_cache_basedir, skip_pull_image, force_image_build, parameter_overrides)


def do_cli(ctx, host, port, template, env_vars, debug_port, debug_args, debugger_path, docker_volume_basedir, docker_network, log_file, layer_cache_basedir, skip_pull_image, force_image_build, parameter_overrides):
    """
    Implementation of the ``cli`` method, just separated out for unit testing purposes
    """
    from samcli.commands.local.cli_common.invoke_context import InvokeContext
    from samcli.commands.local.cli_common.user_exceptions import UserException
    from samcli.lib.providers.exceptions import InvalidLayerReference
    from samcli.commands.local.lib.local_lambda_service import LocalLambdaService
    from samcli.commands.validate.lib.exceptions import InvalidSamDocumentException
    from samcli.commands.local.lib.exceptions import OverridesNotWellDefinedError
    from samcli.local.docker.lambda_debug_settings import DebuggingNotSupported
    LOG.debug('local start_lambda command is called')
    try:
        with InvokeContext(template_file=template,
          function_identifier=None,
          env_vars_file=env_vars,
          docker_volume_basedir=docker_volume_basedir,
          docker_network=docker_network,
          log_file=log_file,
          skip_pull_image=skip_pull_image,
          debug_ports=debug_port,
          debug_args=debug_args,
          debugger_path=debugger_path,
          parameter_overrides=parameter_overrides,
          layer_cache_basedir=layer_cache_basedir,
          force_image_build=force_image_build,
          aws_region=(ctx.region),
          aws_profile=(ctx.profile)) as (invoke_context):
            service = LocalLambdaService(lambda_invoke_context=invoke_context, port=port, host=host)
            service.start()
    except (InvalidSamDocumentException,
     OverridesNotWellDefinedError,
     InvalidLayerReference,
     DebuggingNotSupported) as ex:
        try:
            raise UserException((str(ex)), wrapped_from=(ex.__class__.__name__))
        finally:
            ex = None
            del ex