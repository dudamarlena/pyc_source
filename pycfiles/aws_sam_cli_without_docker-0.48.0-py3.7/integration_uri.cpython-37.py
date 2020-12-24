# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/commands/local/lib/swagger/integration_uri.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 10773 bytes
"""
Handles parsing of Swagger Integration data. This contains the arn of the Lambda function it connects to,
integration type, response template etc.
"""
import re, logging
from enum import Enum
from six import string_types
LOG = logging.getLogger(__name__)

class LambdaUri:
    __doc__ = '\n    Purely static class that helps you parse Lambda Function Integration URI ARN\n    '
    _FN_SUB = 'Fn::Sub'
    _REGEX_GET_FUNCTION_ARN = '.*/functions/(.*)/invocations'
    _REGEX_GET_FUNCTION_NAME = '.*:function:([^:]*)'
    _REGEX_STAGE_VARIABLE = '\\$\\{stageVariables\\..+\\}'
    _REGEX_VALID_FUNCTION_NAME = '([a-zA-Z0-9-_]+)'
    _REGEX_SUB_FUNCTION_ARN = '\\$\\{([A-Za-z0-9]+)\\.(Arn|Alias)\\}'

    @staticmethod
    def get_function_name(integration_uri):
        """
        Gets the name of the function from the Integration URI ARN. This is a best effort service which returns None
        if function name could not be parsed. This can happen when the ARN is an intrinsic function which is too
        complex or the ARN is not a Lambda integration.

        Parameters
        ----------
        integration_uri : basestring or dict
            Integration URI data extracted from Swagger dictionary. This could be a string of the ARN or an intrinsic
            function that will resolve to the ARN

        Returns
        -------
        basestring or None
            If the function name could be parsed out of the Integration URI ARN. None, otherwise
        """
        arn = LambdaUri._get_function_arn(integration_uri)
        LOG.debug('Extracted Function ARN: %s', arn)
        return LambdaUri._get_function_name_from_arn(arn)

    @staticmethod
    def _get_function_arn(uri_data):
        """
        Integration URI can be expressed in various shapes and forms. This method normalizes the Integration URI ARN
        and returns the Lambda Function ARN. Here are the different forms of Integration URI ARN:

        - String:
            - Fully resolved ARN
            - ARN with Stage Variables:
              Ex: arn:aws:apigateway:ap-southeast-2:lambda:path/2015-03-31/functions/arn:aws:lambda:ap-southeast-2:123456789012:function:${stageVariables.PostFunctionName}/invocations  # NOQA

        - Dictionary: Usually contains intrinsic functions

            - Fn::Sub:
              Example:
              {
                "Fn::Sub":
                  "arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${LambdaFunction.Arn}/invocations"
              }

            - Fn::Join: **Unsupported**. It is very hard to combine the joins into one string especially when
              certain properties are resolved only at runtime.

            - Ref, Fn::GetAtt: **Unsupported**. Impossible to use these intrinsics with integration URI. CFN doesn't
              support this functionality.

        Note
        ~~~~
        This method supports only a very restricted subset of intrinsic functions with Swagger document. This is the
        best we can do without implementing a full blown intrinsic function resolution module.

        Parameters
        ----------
        uri_data : string or dict
            Value of Integration URI. It can either be a string or an intrinsic function that resolves to a string

        Returns
        -------
        basestring or None
            Lambda Function ARN extracted from Integration URI. None, if it cannot get function Arn
        """
        if not uri_data:
            return
        else:
            if LambdaUri._is_sub_intrinsic(uri_data):
                uri_data = LambdaUri._resolve_fn_sub(uri_data)
                LOG.debug('Resolved Sub intrinsic function: %s', uri_data)
            else:
                isinstance(uri_data, string_types) or LOG.debug('This Integration URI format is not supported: %s', uri_data)
                return
            matches = re.match(LambdaUri._REGEX_GET_FUNCTION_ARN, uri_data)
            matches and matches.groups() or LOG.debug('Ignoring Integration URI because it is not a Lambda Function integration: %s', uri_data)
            return
        groups = matches.groups()
        return groups[0]

    @staticmethod
    def _get_function_name_from_arn(function_arn):
        """
        Given the integration ARN, extract the Lambda function name from the ARN. If there
        are stage variables, or other unsupported formats, this function will return None.

        Parameters
        ----------
        function_arn : basestring or None
            Function ARN from the swagger document

        Returns
        -------
        basestring or None
            Function name of this integration. None if the ARN is not parsable
        """
        if not function_arn:
            return
        else:
            matches = re.match(LambdaUri._REGEX_GET_FUNCTION_NAME, function_arn)
            matches and matches.groups() or LOG.debug('No Lambda function ARN defined for integration containing ARN %s', function_arn)
            return
        groups = matches.groups()
        maybe_function_name = groups[0]
        if re.match(LambdaUri._REGEX_STAGE_VARIABLE, maybe_function_name):
            LOG.debug('Stage variables are not supported. Ignoring integration with function ARN %s', function_arn)
            return
        if re.match(LambdaUri._REGEX_VALID_FUNCTION_NAME, maybe_function_name):
            return maybe_function_name
        LOG.debug('Ignoring integration ARN. Unable to parse Function Name from function arn %s', function_arn)

    @staticmethod
    def _resolve_fn_sub(uri_data):
        """
        Tries to resolve an Integration URI which contains Fn::Sub intrinsic function. This method tries to resolve
        and produce a string output.

        Example:
        {
          "Fn::Sub":
            "arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${LambdaFunction.Arn}/invocations"
        }

        Fn::Sub Processing:
        ~~~~~~~~~~~~~~~~~~

        If this is a Fn::Sub, resolve as following:
            1. Get the ARN String:
                - If Sub is using the array syntax, then use element which is a string.
                - If Sub is using string syntax, then just use the string.
            2. If there is a ${XXX.Arn} then replace it with a dummy ARN
            3. Otherwise skip it

        .. code:
            Input:
            {
              "Fn::Sub":
                "arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${LambdaFunction.Arn}/invocations"
            }

            Output: "arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:LambdaFunction/invocations"  # NOQA

        Note
        ~~~~
        This method supports only a very restricted subset of intrinsic functions with Swagger document. This is the
        best we can do without implementing a full blown intrinsic function resolution module.

        Parameters
        ----------
        uri_data : string or dict
            Value of Integration URI. It can either be a string or an intrinsic function that resolves to a string

        Returns
        -------
        string
            Integration URI as a string, if we were able to resolve the Sub intrinsic
        dict
            Input data is returned unmodified if we are unable to resolve the intrinsic
        """
        arn = uri_data[LambdaUri._FN_SUB]
        if isinstance(arn, list):
            arn = arn[0]
        if not isinstance(arn, string_types):
            LOG.debug('Unable to resolve Fn::Sub value for integration URI: %s', uri_data)
            return uri_data
        lambda_function_arn_template = 'arn:aws:lambda:${AWS::Region}:123456789012:function:\\1'
        return re.sub(LambdaUri._REGEX_SUB_FUNCTION_ARN, lambda_function_arn_template, arn)

    @staticmethod
    def _is_sub_intrinsic(data):
        """
        Is this input data a Fn::Sub intrinsic function

        Parameters
        ----------
        data
            Data to check

        Returns
        -------
        bool
            True if the data Fn::Sub intrinsic function
        """
        return isinstance(data, dict) and len(data) == 1 and LambdaUri._FN_SUB in data


class IntegrationType(Enum):
    aws_proxy = 'aws_proxy'
    mock = 'mock'