# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/utils/api.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 2170 bytes
import logging
from django.conf import settings
from django.utils.module_loading import import_string
logger = logging.getLogger(__name__)

def log_api_func(api, func):
    func_name = getattr(func, '__name__', str(func))
    if not func_name == '<lambda>':
        logger.debug('{}.{}'.format(api.__class__.__name__, func_name))


class Api(type):
    """Api"""

    def __getattr__(cls, attr):
        override_class_path = getattr(settings, cls.API_SETTING_NAME, cls.DEFAULT_CLASS_PATH)
        override_class = import_string(override_class_path)
        api_instance = override_class()
        func = getattr(api_instance, attr, lambda : None)
        log_api_func(api_instance, func)
        return func


class MatchingApi(metaclass=Api):
    API_SETTING_NAME = 'CALLISTO_MATCHING_API'
    DEFAULT_CLASS_PATH = 'callisto_core.reporting.api.CallistoCoreMatchingApi'


class NotificationApi(metaclass=Api):
    API_SETTING_NAME = 'CALLISTO_NOTIFICATION_API'
    DEFAULT_CLASS_PATH = 'callisto_core.notification.api.CallistoCoreNotificationApi'


class TenantApi(metaclass=Api):
    API_SETTING_NAME = 'CALLISTO_TENANT_API'
    DEFAULT_CLASS_PATH = 'callisto_core.utils.tenant_api.CallistoCoreTenantApi'