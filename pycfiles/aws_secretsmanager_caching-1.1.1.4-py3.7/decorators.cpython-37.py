# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/aws_secretsmanager_caching/decorators.py
# Compiled at: 2019-05-13 16:05:47
# Size of source mod 2**32: 3557 bytes
"""Decorators for use with caching library """
import json

class InjectSecretString:
    __doc__ = 'Decorator implementing high-level Secrets Manager caching client'

    def __init__(self, secret_id, cache):
        """
        Constructs a decorator to inject a single non-keyworded argument from a cached secret for a given function.

        :type secret_id: str
        :param secret_id: The secret identifier

        :type cache: aws_secretsmanager_caching.SecretCache
        :param cache: Secret cache
        """
        self.cache = cache
        self.secret_id = secret_id

    def __call__(self, func):
        """
        Return a function with cached secret injected as first argument.

        :type func: object
        :param func: The function for injecting a single non-keyworded argument too.
        :return The function with the injected argument.
        """
        secret = self.cache.get_secret_string(secret_id=(self.secret_id))

        def _wrapped_func(*args, **kwargs):
            func(secret, *args, **kwargs)

        return _wrapped_func


class InjectKeywordedSecretString:
    __doc__ = 'Decorator implementing high-level Secrets Manager caching client using JSON-based secrets'

    def __init__(self, secret_id, cache, **kwargs):
        """
        Construct a decorator to inject a variable list of keyword arguments to a given function with resolved values
        from a cached secret.

        :type kwargs: dict
        :param kwargs: dictionary mapping original keyword argument of wrapped function to JSON-encoded secret key

        :type secret_id: str
        :param secret_id: The secret identifier

        :type cache: aws_secretsmanager_caching.SecretCache
        :param cache: Secret cache
        """
        self.cache = cache
        self.kwarg_map = kwargs
        self.secret_id = secret_id

    def __call__(self, func):
        """
        Return a function with injected keyword arguments from a cached secret.

        :type func: object
        :param func: function for injecting keyword arguments.
        :return The original function with injected keyword arguments
        """
        try:
            secret = json.loads(self.cache.get_secret_string(secret_id=(self.secret_id)))
        except json.decoder.JSONDecodeError:
            raise RuntimeError('Cached secret is not valid JSON')

        resolved_kwargs = dict()
        for orig_kwarg in self.kwarg_map:
            secret_key = self.kwarg_map[orig_kwarg]
            try:
                resolved_kwargs[orig_kwarg] = secret[secret_key]
            except KeyError:
                raise RuntimeError('Cached secret does not contain key {0}'.format(secret_key))

        def _wrapped_func(*args, **kwargs):
            func(args, **resolved_kwargs, **kwargs)

        return _wrapped_func