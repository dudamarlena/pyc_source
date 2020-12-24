# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-api/vkontakte_api/api.py
# Compiled at: 2016-03-14 10:47:40
from django.conf import settings
from social_api.api import ApiAbstractBase, Singleton
from vkontakte import VKError as VkontakteError, API
__all__ = [
 'api_call', 'VkontakteError']

class VkontakteApi(ApiAbstractBase):
    __metaclass__ = Singleton
    provider = 'vkontakte'
    provider_social_auth = 'vk-oauth2'
    error_class = VkontakteError
    request_timeout = getattr(settings, 'VKONTAKTE_API_REQUEST_TIMEOUT', 1)

    def get_consistent_token(self):
        return getattr(settings, 'VKONTAKTE_API_ACCESS_TOKEN', None)

    def get_api(self, token):
        return API(token=token)

    def get_api_response(self, *args, **kwargs):
        return self.api.get(self.method, timeout=self.request_timeout, *args, **kwargs)

    def handle_error_code_5(self, e, *args, **kwargs):
        self.used_access_tokens += [self.api.token]
        return self.repeat_call(*args, **kwargs)

    def handle_error_code_6(self, e, *args, **kwargs):
        self.logger.info("Vkontakte error 'Too many requests per second' on method: %s, recursion count: %d" % (
         self.method, self.recursion_count))
        return self.repeat_call(*args, **kwargs)

    def handle_error_code_9(self, e, *args, **kwargs):
        self.logger.warning('Vkontakte flood control registered while executing method %s with params %s,             recursion count: %d' % (self.method, kwargs, self.recursion_count))
        self.used_access_tokens += [self.api.token]
        return self.sleep_repeat_call(*args, **kwargs)

    def handle_error_code_10(self, e, *args, **kwargs):
        self.logger.warning('Internal server error: Database problems, try later. Error registered while executing             method %s with params %s, recursion count: %d' % (self.method, kwargs, self.recursion_count))
        return self.sleep_repeat_call(*args, **kwargs)

    def handle_error_code_17(self, e, *args, **kwargs):
        self.used_access_tokens += [self.api.token]
        return self.repeat_call(*args, **kwargs)

    def handle_error_code_500(self, e, *args, **kwargs):
        return self.sleep_repeat_call(*args, **kwargs)

    def handle_error_code_501(self, e, *args, **kwargs):
        return self.sleep_repeat_call(*args, **kwargs)

    def handle_error_code_502(self, e, *args, **kwargs):
        return self.sleep_repeat_call(*args, **kwargs)

    def handle_error_code_504(self, e, *args, **kwargs):
        return self.sleep_repeat_call(*args, **kwargs)


def api_call(*args, **kwargs):
    api = VkontakteApi()
    return api.call(*args, **kwargs)