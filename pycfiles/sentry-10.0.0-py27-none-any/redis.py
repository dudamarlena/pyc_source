# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/redis.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import functools, logging, posixpath, six
from threading import Lock
import rb
from django.utils.functional import SimpleLazyObject
from pkg_resources import resource_string
from redis.client import Script
from redis.connection import ConnectionPool
from redis.exceptions import ConnectionError, BusyLoadingError
from rediscluster import StrictRedisCluster
from sentry import options
from sentry.exceptions import InvalidConfiguration
from sentry.utils import warnings
from sentry.utils.warnings import DeprecatedSettingWarning
from sentry.utils.versioning import Version, check_versions
logger = logging.getLogger(__name__)
_pool_cache = {}
_pool_lock = Lock()

def _shared_pool(**opts):
    if 'host' in opts:
        key = '%s:%s/%s' % (opts['host'], opts['port'], opts['db'])
    else:
        key = '%s/%s' % (opts['path'], opts['db'])
    pool = _pool_cache.get(key)
    if pool is not None:
        return pool
    else:
        with _pool_lock:
            pool = _pool_cache.get(key)
            if pool is not None:
                return pool
            pool = ConnectionPool(**opts)
            _pool_cache[key] = pool
            return pool
        return


_make_rb_cluster = functools.partial(rb.Cluster, pool_cls=_shared_pool)

def make_rb_cluster(*args, **kwargs):
    import warnings
    warnings.warn('Direct Redis cluster construction is deprecated, please use named clusters. Direct cluster construction will be removed in Sentry 8.5.', DeprecationWarning)
    return _make_rb_cluster(*args, **kwargs)


class _RBCluster(object):

    def supports(self, config):
        return not config.get('is_redis_cluster', False)

    def factory(self, **config):
        hosts = config['hosts']
        hosts = {k:v for k, v in enumerate(hosts)} if isinstance(hosts, list) else hosts
        config['hosts'] = hosts
        return _make_rb_cluster(**config)

    def __str__(self):
        return 'Redis Blaster Cluster'


class RetryingStrictRedisCluster(StrictRedisCluster):
    """
    Execute a command with cluster reinitialization retry logic.

    Should a cluster respond with a ConnectionError or BusyLoadingError the
    cluster nodes list will be reinitialized and the command will be executed
    again with the most up to date view of the world.
    """

    def execute_command(self, *args, **kwargs):
        try:
            return super(self.__class__, self).execute_command(*args, **kwargs)
        except (ConnectionError,
         BusyLoadingError,
         KeyError):
            self.connection_pool.nodes.reset()
            return super(self.__class__, self).execute_command(*args, **kwargs)


class _RedisCluster(object):

    def supports(self, config):
        return config.get('is_redis_cluster', False)

    def factory(self, **config):
        hosts = config.get('hosts')
        hosts = hosts.values() if isinstance(hosts, dict) else hosts

        def cluster_factory():
            return RetryingStrictRedisCluster(startup_nodes=hosts, decode_responses=True, skip_full_coverage_check=True)

        return SimpleLazyObject(cluster_factory)

    def __str__(self):
        return 'Redis Cluster'


class ClusterManager(object):

    def __init__(self, options_manager, cluster_type=_RBCluster):
        self.__clusters = {}
        self.__options_manager = options_manager
        self.__cluster_type = cluster_type()

    def get(self, key):
        cluster = self.__clusters.get(key)
        if cluster:
            return cluster
        else:
            configuration = self.__options_manager.get('redis.clusters').get(key)
            if configuration is None:
                raise KeyError(('Invalid cluster name: {}').format(key))
            if not self.__cluster_type.supports(configuration):
                raise KeyError(('Invalid cluster type, expected: {}').format(self.__cluster_type))
            cluster = self.__clusters[key] = self.__cluster_type.factory(**configuration)
            return cluster


clusters = ClusterManager(options.default_manager)
redis_clusters = ClusterManager(options.default_manager, _RedisCluster)

def get_cluster_from_options(setting, options, cluster_manager=clusters):
    cluster_option_name = 'cluster'
    default_cluster_name = 'default'
    cluster_constructor_option_names = frozenset(('hosts', ))
    options = options.copy()
    cluster_options = {key:options.pop(key) for key in set(options.keys()).intersection(cluster_constructor_option_names)}
    if cluster_options:
        if cluster_option_name in options:
            raise InvalidConfiguration(('Cannot provide both named cluster ({!r}) and cluster configuration ({}) options.').format(cluster_option_name, (', ').join(map(repr, cluster_constructor_option_names))))
        else:
            warnings.warn(DeprecatedSettingWarning(('{} parameter of {}').format((', ').join(map(repr, cluster_constructor_option_names)), setting), ('{}["{}"]').format(setting, cluster_option_name), removed_in_version='8.5'), stacklevel=2)
        cluster = rb.Cluster(pool_cls=_shared_pool, **cluster_options)
    else:
        cluster = cluster_manager.get(options.pop(cluster_option_name, default_cluster_name))
    return (cluster, options)


def check_cluster_versions(cluster, required, recommended=None, label=None):
    try:
        with cluster.all() as (client):
            results = client.info()
    except Exception as e:
        raise InvalidConfiguration(six.text_type(e))

    versions = {}
    for id, info in results.value.items():
        host = cluster.hosts[id]
        key = ('{host}:{port}').format(host=host.host, port=host.port)
        versions[key] = Version(map(int, info['redis_version'].split('.', 3)))

    check_versions('Redis' if label is None else 'Redis (%s)' % (label,), versions, required, recommended)
    return


def load_script(path):
    script = Script(None, resource_string('sentry', posixpath.join('scripts', path)))

    def call_script(client, keys, args):
        ('\n        Executes {!r} as a Lua script on a Redis server.\n\n        Takes the client to execute the script on as the first argument,\n        followed by the values that will be provided as ``KEYS`` and ``ARGV``\n        to the script as two sequence arguments.\n        ').format(path)
        return script(keys, args, client)

    return call_script