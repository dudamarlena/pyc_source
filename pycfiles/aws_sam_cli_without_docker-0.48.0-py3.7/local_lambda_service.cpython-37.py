# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/commands/local/lib/local_lambda_service.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 2207 bytes
"""
Connects the CLI with Local Lambda Invoke Service.
"""
import logging
from samcli.local.lambda_service.local_lambda_invoke_service import LocalLambdaInvokeService
LOG = logging.getLogger(__name__)

class LocalLambdaService:
    __doc__ = '\n    Implementation of Local Lambda Invoke Service that is capable of serving the invoke path to your Lambda Functions\n    that are defined in a SAM file.\n    '

    def __init__(self, lambda_invoke_context, port, host):
        """
        Initialize the Local Lambda Invoke service.

        :param samcli.commands.local.cli_common.invoke_context.InvokeContext lambda_invoke_context: Context object
            that can help with Lambda invocation
        :param int port: Port to listen on
        :param string host: Local hostname or IP address to bind to
        """
        self.port = port
        self.host = host
        self.lambda_runner = lambda_invoke_context.local_lambda_runner
        self.stderr_stream = lambda_invoke_context.stderr

    def start(self):
        """
        Creates and starts the Local Lambda Invoke service. This method will block until the service is stopped
        manually using an interrupt. After the service is started, callers can make HTTP requests to the endpoint
        to invoke the Lambda function and receive a response.

        NOTE: This is a blocking call that will not return until the thread is interrupted with SIGINT/SIGTERM
        """
        service = LocalLambdaInvokeService(lambda_runner=(self.lambda_runner),
          port=(self.port),
          host=(self.host),
          stderr=(self.stderr_stream))
        service.create()
        LOG.info('Starting the Local Lambda Service. You can now invoke your Lambda Functions defined in your template through the endpoint.')
        service.run()