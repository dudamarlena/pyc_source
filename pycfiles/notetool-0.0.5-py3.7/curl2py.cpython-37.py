# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notetool/convert/curl2py.py
# Compiled at: 2020-03-18 05:54:05
# Size of source mod 2**32: 3271 bytes
import argparse, json, re, shlex
from collections import OrderedDict, namedtuple
import six.moves as Cookie
parser = argparse.ArgumentParser()
parser.add_argument('command')
parser.add_argument('url')
parser.add_argument('-d', '--data')
parser.add_argument('-b', '--data-binary', default=None)
parser.add_argument('-X', default='')
parser.add_argument('-H', '--header', action='append', default=[])
parser.add_argument('--compressed', action='store_true')
parser.add_argument('--insecure', action='store_true')
BASE_INDENT = '    '
ParsedContext = namedtuple('ParsedContext', ['method', 'url', 'data', 'headers', 'cookies', 'verify'])

def parse_context(curl_command):
    method = 'get'
    tokens = shlex.split(curl_command)
    parsed_args = parser.parse_args(tokens)
    post_data = parsed_args.data or parsed_args.data_binary
    if post_data:
        method = 'post'
    if parsed_args.X:
        method = parsed_args.X.lower()
    cookie_dict = OrderedDict()
    quoted_headers = OrderedDict()
    for curl_header in parsed_args.header:
        if curl_header.startswith(':'):
            occurrence = [m.start() for m in re.finditer(':', curl_header)]
            header_key, header_value = curl_header[:occurrence[1]], curl_header[occurrence[1] + 1:]
        else:
            header_key, header_value = curl_header.split(':', 1)
        if header_key.lower() == 'cookie':
            cookie = Cookie.SimpleCookie(header_value)
            for key in cookie:
                cookie_dict[key] = cookie[key].value

        else:
            quoted_headers[header_key] = header_value.strip()

    return ParsedContext(method=method,
      url=(parsed_args.url),
      data=post_data,
      headers=quoted_headers,
      cookies=cookie_dict,
      verify=(parsed_args.insecure))


def parse(curl_command):
    parsed_context = parse_context(curl_command)
    data_token = ''
    if parsed_context.data:
        data_token = "{}data='{}',\n".format(BASE_INDENT, parsed_context.data)
    verify_token = ''
    if parsed_context.verify:
        verify_token = '\n{}verify=False'.format(BASE_INDENT)
    formatter = {'method':parsed_context.method, 
     'url':parsed_context.url, 
     'data_token':data_token, 
     'headers_token':'{}headers={}'.format(BASE_INDENT, dict_to_pretty_string(parsed_context.headers)), 
     'cookies_token':'{}cookies={}'.format(BASE_INDENT, dict_to_pretty_string(parsed_context.cookies)), 
     'security_token':verify_token}
    res = [
     'url = "{}"'.format(parsed_context.url),
     'headers = {}'.format(dict_to_pretty_string((parsed_context.headers), indent=2)),
     'cookies = {}'.format(dict_to_pretty_string((parsed_context.cookies), indent=2)),
     ('response = requests.{method}(url,{data_token} headers=headers, cookies=cookies, {security_token})'.format)(**formatter)]
    res = '\n'.join(res)
    return res


def dict_to_pretty_string(the_dict, indent=4):
    if not the_dict:
        return '{}'
    return ('\n' + ' ' * indent).join(json.dumps(the_dict, sort_keys=True, indent=indent, separators=(',',
                                                                                                      ': ')).splitlines())