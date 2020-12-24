# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sogubaby/anaconda3/envs/tbb/lib/python3.8/site-packages/scrapy_redis_bloomfilter/defaults.py
# Compiled at: 2019-11-26 21:39:54
# Size of source mod 2**32: 704 bytes
import redis
DUPEFILTER_KEY = 'dupefilter:%(timestamp)s'
PIPELINE_KEY = '%(spider)s:items'
BLOOMFILTER_HASH_NUMBER = 6
BLOOMFILTER_BIT = 30
DUPEFILTER_DEBUG = False
REDIS_CLS = redis.StrictRedis
REDIS_ENCODING = 'utf-8'
REDIS_PARAMS = {'socket_timeout':30, 
 'socket_connect_timeout':30, 
 'retry_on_timeout':True, 
 'encoding':REDIS_ENCODING}
SCHEDULER_QUEUE_KEY = '%(spider)s:requests'
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'
SCHEDULER_DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
START_URLS_KEY = '%(name)s:start_urls'
START_URLS_AS_SET = False