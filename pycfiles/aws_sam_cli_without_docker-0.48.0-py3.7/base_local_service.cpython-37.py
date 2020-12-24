# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/local/services/base_local_service.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 7225 bytes
"""Base class for all Services that interact with Local Lambda"""
import json, logging, os
from flask import Response
LOG = logging.getLogger(__name__)

class BaseLocalService:

    def __init__(self, is_debugging, port, host):
        """
        Creates a BaseLocalService class

        Parameters
        ----------
        is_debugging bool
            Flag to run in debug mode or not
        port int
            Optional. port for the service to start listening on Defaults to 3000
        host str
            Optional. host to start the service on Defaults to '127.0.0.1
        """
        self.is_debugging = is_debugging
        self.port = port
        self.host = host
        self._app = None

    def create(self):
        """
        Creates a Flask Application that can be started.
        """
        raise NotImplementedError('Required method to implement')

    def run(self):
        """
        This starts up the (threaded) Local Server.
        Note: This is a **blocking call**

        Raises
        ------
        RuntimeError
            if the service was not created
        """
        if not self._app:
            raise RuntimeError('The application must be created before running')
        multi_threaded = not self.is_debugging
        LOG.debug('Localhost server is starting up. Multi-threading = %s', multi_threaded)
        os.environ['WERKZEUG_RUN_MAIN'] = 'true'
        self._app.run(threaded=multi_threaded, host=(self.host), port=(self.port))

    @staticmethod
    def service_response(body, headers, status_code):
        """
        Constructs a Flask Response from the body, headers, and status_code.

        :param str body: Response body as a string
        :param werkzeug.datastructures.Headers headers: headers for the response
        :param int status_code: status_code for response
        :return: Flask Response
        """
        response = Response(body)
        response.headers = headers
        response.status_code = status_code
        return response


class LambdaOutputParser:

    @staticmethod
    def get_lambda_output(stdout_stream):
        """
        This method will extract read the given stream and return the response from Lambda function separated out
        from any log statements it might have outputted. Logs end up in the stdout stream if the Lambda function
        wrote directly to stdout using System.out.println or equivalents.

        Parameters
        ----------
        stdout_stream : io.BaseIO
            Stream to fetch data from

        Returns
        -------
        str
            String data containing response from Lambda function
        str
            String data containng logs statements, if any.
        bool
            If the response is an error/exception from the container
        """
        stdout_data = stdout_stream.getvalue().rstrip(b'\n')
        lambda_response = stdout_data
        lambda_logs = None
        last_line_position = stdout_data.rfind(b'\n')
        if last_line_position >= 0:
            lambda_logs = stdout_data[:last_line_position]
            lambda_response = stdout_data[last_line_position:].strip()
        lambda_response = lambda_response.decode('utf-8')
        is_lambda_user_error_response = LambdaOutputParser.is_lambda_error_response(lambda_response)
        return (
         lambda_response, lambda_logs, is_lambda_user_error_response)

    @staticmethod
    def is_lambda_error_response(lambda_response):
        """
        Check to see if the output from the container is in the form of an Error/Exception from the Lambda invoke

        Parameters
        ----------
        lambda_response str
            The response the container returned

        Returns
        -------
        bool
            True if the output matches the Error/Exception Dictionary otherwise False
        """
        is_lambda_user_error_response = False
        try:
            lambda_response_dict = json.loads(lambda_response)
            if isinstance(lambda_response_dict, dict):
                if len(lambda_response_dict.keys() & {'errorMessage', 'errorType'}) == 2:
                    if len(lambda_response_dict.keys() & {'errorMessage', 'errorType', 'stackTrace', 'cause'}) == len(lambda_response_dict) or len(lambda_response_dict) == 3:
                        is_lambda_user_error_response = True
        except ValueError:
            pass

        return is_lambda_user_error_response