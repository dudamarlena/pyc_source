# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pifx/util.py
# Compiled at: 2018-04-25 18:34:44
import json, re, six
from pifx.constants import A_ERROR_HTTP_CODES, A_OK_HTTP_CODES

def generate_auth_header(api_key):
    headers = {'Authorization': ('Bearer {}').format(api_key)}
    return headers


def arg_tup_to_dict(argument_tuples):
    """Given a set of argument tuples, set their value in a data dictionary if not blank"""
    data = dict()
    for arg_name, arg_val in argument_tuples:
        if arg_val is not None:
            if arg_val is True:
                arg_val = 'true'
            elif arg_val is False:
                arg_val = 'false'
            data[arg_name] = arg_val

    return data


def parse_data(parsed_data):
    """Given parsed response, return correct return values"""
    return parsed_data['results']


def parse_response(response):
    """Parse JSON API response, return object."""
    parsed_response = json.loads(response.text)
    return parsed_response


def handle_error(response):
    """Raise appropriate exceptions if necessary."""
    status_code = response.status_code
    if status_code not in A_OK_HTTP_CODES:
        error_explanation = A_ERROR_HTTP_CODES.get(status_code)
        raise_error = ('{}: {}').format(status_code, error_explanation)
        raise Exception(raise_error)
    else:
        return True


def encode_url_path(url):
    """Encodes the path url string replacing special characters with properly escaped sequences.
    Not intended for use with query string parameters. """
    return six.moves.urllib.parse.quote(url)


def encode_url_arg(self, url_arg):
    arg_regex = '(\\w+):(.*)'
    if ':' not in url_arg:
        return encode_url_path(url_arg)
    else:
        url_arg_matches = re.match(arg_regex, url_arg)
        identifier_name = url_arg_matches.group(1)
        argument_content = url_arg_matches.group(2)
        encoded_arg = encode_url_path(argument_content)
        return identifier_name + ':' + encoded_arg