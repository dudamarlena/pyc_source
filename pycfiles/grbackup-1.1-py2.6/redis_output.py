# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/grbackup/grb_plugins/redis_output.py
# Compiled at: 2013-06-08 16:30:53
from optparse import OptionGroup
import redis
plugin_type = 'redis'
support_threads = True
description = 'save items into Redis\noutput scheme:   redis://username:password@host[:port]/dbindex\noutput examples: redis://localhost:6379/3\n                 redis://user:password@localhost:6379/0\n'

def add_option_group(parser):
    redis_group = OptionGroup(parser, 'Redis Options')
    redis_group.add_option('--redis-scol-prefix', dest='redis_subs', default='subscription', type='str', help='subscriptions key prefix[default: %default]')
    redis_group.add_option('--redis-tcol-prefix', dest='redis_topics', default='topic', type='str', help='topics key prefix[default: %default]')
    redis_group.add_option('--redis-xcol-prefix', dest='redis_starred', default='starred', type='str', help='starred key prefix[default: %default]')
    parser.add_option_group(redis_group)


class WriteRedis(object):

    def __init__(self, uri, subs, topics, starred):
        self.uri = uri
        self.subs = subs
        self.topics = topics
        self.starred = starred
        self.conn = redis.StrictRedis.from_url(self.uri)

    def put_subscription(self, subscription):
        key = ('{subscription}:{0}').format(subscription['id'], subscription=self.subs)
        self.conn.hmset(key, subscription)

    def put_all(self, subscription, topic):
        self.put_subscription(subscription)
        subscription_url = subscription['id'][5:]
        self.put_topic(subscription_url, topic)

    def put_starred(self, topic):
        key = ('{starred}:{0}').format(topic['id'], starred=self.starred)
        self.conn.hmset(key, topic)

    def put_topic(self, subscription_url, topic):
        key = ('{topic}:{0}').format(topic['id'], topic=self.topics)
        self.conn.hmset(key, topic)


class writer(object):

    def __init__(self, opt):
        self._output = opt.output
        self._s = opt.redis_subs
        self._t = opt.redis_topics
        self._x = opt.redis_starred

    def __enter__(self):
        print (
         self._s, self._t, self._x)
        return WriteRedis(self._output, self._s, self._t, self._x)

    def __exit__(self, *exc_info):
        pass