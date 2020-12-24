# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatpy\binder.py
# Compiled at: 2015-01-11 14:47:47
from six.moves.urllib.parse import quote
import time, re, requests
from chatpy.error import ChatpyError
from chatpy.models import Model
from chatpy.utils import convert_to_utf8_str
re_path_template = re.compile('{\\w+}')

def bind_api(**config):

    class APIMethod(object):
        path = config['path']
        payload_type = config.get('payload_type', None)
        payload_list = config.get('payload_list', False)
        allowed_param = config.get('allowed_param', [])
        method = config.get('method', 'GET')
        require_auth = config.get('require_auth', True)
        use_cache = config.get('use_cache', True)

        def __init__(self, api, args, kargs):
            if self.require_auth and not api.auth:
                raise ChatpyError('Authentication required!')
            self.api = api
            self.post_data = kargs.pop('post_data', None)
            self.retry_count = kargs.pop('retry_count', api.retry_count)
            self.retry_delay = kargs.pop('retry_delay', api.retry_delay)
            self.retry_errors = kargs.pop('retry_errors', api.retry_errors)
            self.headers = kargs.pop('headers', {})
            self.build_parameters(args, kargs)
            self.api_root = api.api_root
            self.build_path()
            if api.secure:
                self.scheme = 'https://'
            else:
                self.scheme = 'http://'
            self.host = api.host
            self.headers['Host'] = self.host
            return

        def build_parameters(self, args, kargs):
            self.parameters = {}
            for idx, arg in enumerate(args):
                if arg is None:
                    continue
                try:
                    self.parameters[self.allowed_param[idx]] = convert_to_utf8_str(arg)
                except IndexError:
                    raise ChatpyError('Too many parameters supplied!')

            for k, arg in kargs.items():
                if arg is None:
                    continue
                if k in self.parameters:
                    raise ChatpyError('Multiple values for parameter %s supplied!' % k)
                self.parameters[k] = convert_to_utf8_str(arg)

            return

        def build_path(self):
            for variable in re_path_template.findall(self.path):
                name = variable.strip('{}')
                if name == 'user' and 'user' not in self.parameters and self.api.auth:
                    value = self.api.auth.get_username()
                else:
                    try:
                        value = quote(self.parameters[name])
                    except KeyError:
                        raise ChatpyError('No parameter value found for path variable: %s' % name)

                    del self.parameters[name]
                self.path = self.path.replace(variable, value)

        def execute(self):
            url = self.scheme + self.host + self.api_root + self.path
            if self.use_cache and self.api.cache and self.method == 'GET':
                cache_result = self.api.cache.get(url)
                if cache_result:
                    if isinstance(cache_result, list):
                        for result in cache_result:
                            if isinstance(result, Model):
                                result._api = self.api

                    elif isinstance(cache_result, Model):
                        cache_result._api = self.api
                    return cache_result
            retries_performed = 0
            while retries_performed < self.retry_count + 1:
                if self.api.auth:
                    self.api.auth.apply_auth(self.scheme + self.host + url, self.method, self.headers, self.parameters)
                if self.api.compression:
                    self.headers['Accept-encoding'] = 'gzip'
                options = {'timeout': self.api.timeout, 
                   'headers': self.headers, 
                   'data': self.post_data, 
                   'params': self.parameters}
                try:
                    resp = requests.request(self.method, url, **options)
                except Exception as e:
                    raise ChatpyError('Failed to send request: %s' % e)

                if self.retry_errors:
                    if resp.status_code not in self.retry_errors:
                        break
                elif resp.status_code in (200, 204):
                    break
                time.sleep(self.retry_delay)
                retries_performed += 1

            self.api.last_response = resp
            if resp.status_code not in (200, 204):
                try:
                    error_msg = self.api.parser.parse_error(resp.read())
                except Exception:
                    error_msg = 'Chatwork error response: status code = %s' % resp.status_code

                raise ChatpyError(error_msg, resp)
            text = resp.text
            if resp.status_code == 204:
                text = '{}'
            result = self.api.parser.parse(self, text)
            if self.use_cache and self.api.cache and self.method == 'GET' and result:
                self.api.cache.store(url, result)
            return result

    def _call(api, *args, **kargs):
        method = APIMethod(api, args, kargs)
        return method.execute()

    if 'cursor' in APIMethod.allowed_param:
        _call.pagination_mode = 'cursor'
    elif 'max_id' in APIMethod.allowed_param and 'since_id' in APIMethod.allowed_param:
        _call.pagination_mode = 'id'
    elif 'page' in APIMethod.allowed_param:
        _call.pagination_mode = 'page'
    return _call