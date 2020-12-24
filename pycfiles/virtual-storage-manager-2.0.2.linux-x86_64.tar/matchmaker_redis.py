# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/rpc/matchmaker_redis.py
# Compiled at: 2016-06-13 14:11:03
"""
The MatchMaker classes should accept a Topic or Fanout exchange key and
return keys for direct exchanges, per (approximate) AMQP parlance.
"""
from oslo.config import cfg
from vsm.openstack.common import importutils
from vsm.openstack.common import log as logging
from vsm.openstack.common.rpc import matchmaker as mm_common
redis = importutils.try_import('redis')
matchmaker_redis_opts = [
 cfg.StrOpt('host', default='127.0.0.1', help='Host to locate redis'),
 cfg.IntOpt('port', default=6379, help='Use this port to connect to redis host.'),
 cfg.StrOpt('password', default=None, help='Password for Redis server. (optional)')]
CONF = cfg.CONF
opt_group = cfg.OptGroup(name='matchmaker_redis', title='Options for Redis-based MatchMaker')
CONF.register_group(opt_group)
CONF.register_opts(matchmaker_redis_opts, opt_group)
LOG = logging.getLogger(__name__)

class RedisExchange(mm_common.Exchange):

    def __init__(self, matchmaker):
        self.matchmaker = matchmaker
        self.redis = matchmaker.redis
        super(RedisExchange, self).__init__()


class RedisTopicExchange(RedisExchange):
    """
    Exchange where all topic keys are split, sending to second half.
    i.e. "compute.host" sends a message to "compute" running on "host"
    """

    def run(self, topic):
        while True:
            member_name = self.redis.srandmember(topic)
            if not member_name:
                break
            if not self.matchmaker.is_alive(topic, member_name):
                continue
            host = member_name.split('.', 1)[1]
            return [(member_name, host)]

        return []


class RedisFanoutExchange(RedisExchange):
    """
    Return a list of all hosts.
    """

    def run(self, topic):
        topic = topic.split('~', 1)[1]
        hosts = self.redis.smembers(topic)
        good_hosts = filter(lambda host: self.matchmaker.is_alive(topic, host), hosts)
        return [ (x, x.split('.', 1)[1]) for x in good_hosts ]


class MatchMakerRedis(mm_common.HeartbeatMatchMakerBase):
    """
    MatchMaker registering and looking-up hosts with a Redis server.
    """

    def __init__(self):
        super(MatchMakerRedis, self).__init__()
        if not redis:
            raise ImportError('Failed to import module redis.')
        self.redis = redis.StrictRedis(host=CONF.matchmaker_redis.host, port=CONF.matchmaker_redis.port, password=CONF.matchmaker_redis.password)
        self.add_binding(mm_common.FanoutBinding(), RedisFanoutExchange(self))
        self.add_binding(mm_common.DirectBinding(), mm_common.DirectExchange())
        self.add_binding(mm_common.TopicBinding(), RedisTopicExchange(self))

    def ack_alive(self, key, host):
        topic = '%s.%s' % (key, host)
        if not self.redis.expire(topic, CONF.matchmaker_heartbeat_ttl):
            self.register(self.topic_host[host], host)

    def is_alive(self, topic, host):
        if self.redis.ttl(host) == -1:
            self.expire(topic, host)
            return False
        return True

    def expire(self, topic, host):
        with self.redis.pipeline() as (pipe):
            pipe.multi()
            pipe.delete(host)
            pipe.srem(topic, host)
            pipe.execute()

    def backend_register(self, key, key_host):
        with self.redis.pipeline() as (pipe):
            pipe.multi()
            pipe.sadd(key, key_host)
            pipe.set(key_host, '')
            pipe.execute()

    def backend_unregister(self, key, key_host):
        with self.redis.pipeline() as (pipe):
            pipe.multi()
            pipe.srem(key, key_host)
            pipe.delete(key_host)
            pipe.execute()