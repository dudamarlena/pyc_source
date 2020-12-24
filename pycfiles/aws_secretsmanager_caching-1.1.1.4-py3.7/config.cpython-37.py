# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/aws_secretsmanager_caching/config.py
# Compiled at: 2019-05-13 16:05:47
# Size of source mod 2**32: 2714 bytes
"""Secret cache configuration object."""
from copy import deepcopy
from datetime import timedelta

class SecretCacheConfig:
    __doc__ = 'Advanced configuration for SecretCache clients.\n\n    :type max_cache_size: int\n    :param max_cache_size: The maximum number of secrets to cache.\n\n    :type exception_retry_delay_base: int\n    :param exception_retry_delay_base: The number of seconds to wait\n        after an exception is encountered and before retrying the request.\n\n    :type exception_retry_growth_factor: int\n    :param exception_retry_growth_factor: The growth factor to use for\n        calculating the wait time between retries of failed requests.\n\n    :type exception_retry_delay_max: int\n    :param exception_retry_delay_max: The maximum amount of time in\n        seconds to wait between failed requests.\n\n    :type default_version_stage: str\n    :param default_version_stage: The default version stage to request.\n\n    :type secret_refresh_interval: int\n    :param secret_refresh_interval: The number of seconds to wait between\n        refreshing cached secret information.\n\n    :type secret_cache_hook: SecretCacheHook\n    :param secret_cache_hook: An implementation of the SecretCacheHook abstract\n        class\n\n    '
    OPTION_DEFAULTS = {'max_cache_size':1024, 
     'exception_retry_delay_base':1, 
     'exception_retry_growth_factor':2, 
     'exception_retry_delay_max':3600, 
     'default_version_stage':'AWSCURRENT', 
     'secret_refresh_interval':timedelta(hours=1).total_seconds(), 
     'secret_cache_hook':None}

    def __init__(self, **kwargs):
        options = deepcopy(self.OPTION_DEFAULTS)
        if kwargs:
            for key, value in kwargs.items():
                if key in options:
                    options[key] = value
                else:
                    raise TypeError("Unexpected keyword argument '%s'" % key)

        for key, value in options.items():
            setattr(self, key, value)