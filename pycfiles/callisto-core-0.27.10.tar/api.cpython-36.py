# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = '\n        Used to create overrideable calls\n\n        See CallistoCoreNotificationApi and SiteAwareNotificationApi\n        for example implementations\n\n        By default, calls to (ex) NotificationApi will be routed to\n        CallistoCoreNotificationApi. So...\n\n            NotificationApi.example_call()\n\n        resolves to...\n\n            CallistoCoreNotificationApi.example_call()\n\n        The purposes of the Api classes are to allow implementors to define\n        custom functionality. So you can create an ProjectExampleApi that\n        is a subclass of CallistoCoreNotificationApi and redefines all of\n        its functions. You can also disable a function by overriding it and\n        making it return None.\n\n        You can also disable an api entirely by setting DEFAULT_CLASS to\n        a ProjectExampleApi that defines no functions. This is useful if you\n        want to disable an entire app (ex callisto_core.notification)\n    '

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