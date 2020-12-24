# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/aws_secretsmanager_caching/secret_cache.py
# Compiled at: 2019-05-13 21:26:38
# Size of source mod 2**32: 3562 bytes
"""High level AWS Secrets Manager caching client."""
from copy import deepcopy
import botocore.session
from pkg_resources import DistributionNotFound, get_distribution
from .cache import LRUCache, SecretCacheItem
from .config import SecretCacheConfig

class SecretCache:
    __doc__ = 'Secret Cache client for AWS Secrets Manager secrets'
    try:
        __version__ = get_distribution('aws_secretsmanager_caching').version
    except DistributionNotFound:
        __version__ = '0.0.0'

    def __init__(self, config=SecretCacheConfig(), client=None):
        """Construct a secret cache using the given configuration and
        AWS Secrets Manager boto client.

        :type config: aws_secretsmanager_caching.SecretCacheConfig
        :param config: Secret cache configuration

        :type client: botocore.client.BaseClient
        :param client: botocore 'secretsmanager' client
        """
        self._client = client
        self._config = deepcopy(config)
        self._cache = LRUCache(max_size=(self._config.max_cache_size))
        if self._client is None:
            self._client = botocore.session.get_session().create_client('secretsmanager')
        self._client.meta.config.user_agent_extra = 'AwsSecretCache/{}'.format(SecretCache.__version__)

    def _get_cached_secret(self, secret_id):
        """Get a cached secret for the given secret identifier.

        :type secret_id: str
        :param secret_id: The secret identifier

        :rtype: aws_secretsmanager_caching.cache.SecretCacheItem
        :return: The associated cached secret item
        """
        secret = self._cache.get(secret_id)
        if secret is not None:
            return secret
        self._cache.put_if_absent(secret_id, SecretCacheItem(config=(self._config), client=(self._client), secret_id=secret_id))
        return self._cache.get(secret_id)

    def get_secret_string(self, secret_id, version_stage=None):
        """Get the secret string value from the cache.

        :type secret_id: str
        :param secret_id: The secret identifier

        :type version_stage: str
        :param version_stage: The stage for the requested version.

        :rtype: str
        :return: The associated secret string value
        """
        secret = self._get_cached_secret(secret_id).get_secret_value(version_stage)
        if secret is None:
            return secret
        return secret.get('SecretString')

    def get_secret_binary(self, secret_id, version_stage=None):
        """Get the secret binary value from the cache.

        :type secret_id: str
        :param secret_id: The secret identifier

        :type version_stage: str
        :param version_stage: The stage for the requested version.

        :rtype: bytes
        :return: The associated secret binary value
        """
        secret = self._get_cached_secret(secret_id).get_secret_value(version_stage)
        if secret is None:
            return secret
        return secret.get('SecretBinary')