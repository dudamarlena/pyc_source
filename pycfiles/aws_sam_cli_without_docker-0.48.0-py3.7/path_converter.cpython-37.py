# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/local/apigw/path_converter.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 2737 bytes
"""
Converter class that handles the conversion of paths from Api Gateway to Flask and back.
"""
import re
PROXY_PATH_PARAMS_ESCAPED = '(.*/){(.*)\\+}'
FLASK_CAPTURE_ALL_PATH = '\\g<1><path:\\g<2>>'
PROXY_PATH_PARAMS = '/{\\g<1>+}'
FLASK_CAPTURE_ALL_PATH_REGEX = '/<path:(.*)>'
LEFT_BRACKET = '{'
RIGHT_BRACKET = '}'
LEFT_ANGLE_BRACKET = '<'
RIGHT_ANGLE_BRACKET = '>'
APIGW_TO_FLASK_REGEX = re.compile(PROXY_PATH_PARAMS_ESCAPED)
FLASK_TO_APIGW_REGEX = re.compile(FLASK_CAPTURE_ALL_PATH_REGEX)

class PathConverter:

    @staticmethod
    def convert_path_to_flask(path):
        """
        Converts a Path from an Api Gateway defined path to one that is accepted by Flask

        Examples:

        '/id/{id}' => '/id/<id>'
        '/{proxy+}' => '/<path:proxy>'

        :param str path: Path to convert to Flask defined path
        :return str: Path representing a Flask path
        """
        proxy_sub_path = APIGW_TO_FLASK_REGEX.sub(FLASK_CAPTURE_ALL_PATH, path)
        return proxy_sub_path.replace(LEFT_BRACKET, LEFT_ANGLE_BRACKET).replace(RIGHT_BRACKET, RIGHT_ANGLE_BRACKET)

    @staticmethod
    def convert_path_to_api_gateway(path):
        """
        Converts a Path from a Flask defined path to one that is accepted by Api Gateway

        Examples:

        '/id/<id>' => '/id/{id}'
        '/<path:proxy>' => '/{proxy+}'

        :param str path: Path to convert to Api Gateway defined path
        :return str: Path representing an Api Gateway path
        """
        proxy_sub_path = FLASK_TO_APIGW_REGEX.sub(PROXY_PATH_PARAMS, path)
        return proxy_sub_path.replace(LEFT_ANGLE_BRACKET, LEFT_BRACKET).replace(RIGHT_ANGLE_BRACKET, RIGHT_BRACKET)