# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-facebook-api/facebook_api/api.py
# Compiled at: 2016-03-30 12:49:23
"""
Copyright 2011-2015 ramusus
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from facebook import GraphAPI, GraphAPIError as FacebookError
from social_api.api import ApiAbstractBase, Singleton
__all__ = [
 'api_call', 'FacebookError']

@property
def code(self):
    try:
        return self.result['error']['code']
    except (KeyError, TypeError):
        return self.type


FacebookError.code = code

class FacebookApi(ApiAbstractBase):
    __metaclass__ = Singleton
    provider = 'facebook'
    error_class = FacebookError
    sleep_repeat_error_messages = ['An unexpected error has occurred. Please retry your request later']
    version = 2.3

    def call(self, method, methods_access_tag=None, *args, **kwargs):
        response = super(FacebookApi, self).call(method, methods_access_tag=methods_access_tag, *args, **kwargs)
        if getattr(response, 'error_code', None):
            error = 'Error %s: %s returned while executing method %s with params %s' % (
             response.error_code, response.error_msg, self.method, kwargs)
            self.logger.error(error)
            if self.recursion_count >= 3:
                raise Exception(error)
            return self.sleep_repeat_call(*args, **kwargs)
        else:
            return response

    def get_api(self, token):
        return GraphAPI(access_token=token, version=self.version)

    def get_api_response(self, *args, **kwargs):
        return self.api.get_object(self.method, *args, **kwargs)

    def handle_error_code_1(self, e, *args, **kwargs):
        if 'limit' in kwargs:
            self.logger.warning("Error 'An unknown error has occurred.', decrease limit. Method %s with params %s, recursion count: %d" % (
             self.method, kwargs, self.recursion_count))
            kwargs['limit'] /= 2
            return self.repeat_call(*args, **kwargs)
        else:
            return self.log_and_raise(e, *args, **kwargs)

    def handle_error_code_4(self, e, *args, **kwargs):
        self.logger.warning("Error 'Application request limit reached', wait for 600 secs. Method %s with params %s, recursion count: %d" % (
         self.method, kwargs, self.recursion_count))
        return self.sleep_repeat_call(seconds=600, *args, **kwargs)

    def handle_error_code_12(self, e, *args, **kwargs):
        return self.log_and_raise(e, *args, **kwargs)

    def handle_error_code_17(self, e, *args, **kwargs):
        self.logger.warning("Error 'User request limit reached', try access_token of another user. Method %s with params %s, recursion count: %d" % (
         self.method, kwargs, self.recursion_count))
        self.used_access_tokens += [self.api.access_token]
        return self.sleep_repeat_call(*args, **kwargs)

    def handle_error_code_190(self, e, *args, **kwargs):
        self.update_token()
        return self.repeat_call(*args, **kwargs)


def api_call(*args, **kwargs):
    api = FacebookApi()
    if 'version' in kwargs:
        api.version = kwargs.pop('version')
    return api.call(*args, **kwargs)