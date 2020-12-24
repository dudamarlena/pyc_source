# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sogubaby/anaconda3/envs/tbb/lib/python3.8/site-packages/scrapy_redis_bloomfilter/scheduler.py
# Compiled at: 2019-11-26 21:39:54
# Size of source mod 2**32: 6460 bytes
import importlib, six
from scrapy.utils.misc import load_object
from . import connection, defaults
from .defaults import BLOOMFILTER_BIT, BLOOMFILTER_HASH_NUMBER

class Scheduler(object):
    __doc__ = 'Redis-based scheduler\n\n    Settings\n    --------\n    SCHEDULER_PERSIST : bool (default: False)\n        Whether to persist or clear redis queue.\n    SCHEDULER_FLUSH_ON_START : bool (default: False)\n        Whether to flush redis queue on start.\n    SCHEDULER_IDLE_BEFORE_CLOSE : int (default: 0)\n        How many seconds to wait before closing if no message is received.\n    SCHEDULER_QUEUE_KEY : str\n        Scheduler redis key.\n    SCHEDULER_QUEUE_CLASS : str\n        Scheduler queue class.\n    SCHEDULER_DUPEFILTER_KEY : str\n        Scheduler dupefilter redis key.\n    SCHEDULER_DUPEFILTER_CLASS : str\n        Scheduler dupefilter class.\n    SCHEDULER_SERIALIZER : str\n        Scheduler serializer.\n\n    '

    def __init__(self, server, persist=False, flush_on_start=False, queue_key=defaults.SCHEDULER_QUEUE_KEY, queue_cls=defaults.SCHEDULER_QUEUE_CLASS, dupefilter_key=defaults.SCHEDULER_DUPEFILTER_KEY, dupefilter_cls=defaults.SCHEDULER_DUPEFILTER_CLASS, idle_before_close=0, serializer=None):
        """Initialize scheduler.

        Parameters
        ----------
        server : Redis
            The redis server instance.
        persist : bool
            Whether to flush requests when closing. Default is False.
        flush_on_start : bool
            Whether to flush requests on start. Default is False.
        queue_key : str
            Requests queue key.
        queue_cls : str
            Importable path to the queue class.
        dupefilter_key : str
            Duplicates filter key.
        dupefilter_cls : str
            Importable path to the dupefilter class.
        idle_before_close : int
            Timeout before giving up.

        """
        if idle_before_close < 0:
            raise TypeError('idle_before_close cannot be negative')
        self.server = server
        self.persist = persist
        self.flush_on_start = flush_on_start
        self.queue_key = queue_key
        self.queue_cls = queue_cls
        self.dupefilter_cls = dupefilter_cls
        self.dupefilter_key = dupefilter_key
        self.idle_before_close = idle_before_close
        self.serializer = serializer
        self.stats = None

    def __len__(self):
        return len(self.queue)

    @classmethod
    def from_settings(cls, settings):
        kwargs = {'persist':settings.getbool('SCHEDULER_PERSIST'), 
         'flush_on_start':settings.getbool('SCHEDULER_FLUSH_ON_START'), 
         'idle_before_close':settings.getint('SCHEDULER_IDLE_BEFORE_CLOSE')}
        optional = {'queue_key':'SCHEDULER_QUEUE_KEY', 
         'queue_cls':'SCHEDULER_QUEUE_CLASS', 
         'dupefilter_key':'SCHEDULER_DUPEFILTER_KEY', 
         'dupefilter_cls':'DUPEFILTER_CLASS', 
         'serializer':'SCHEDULER_SERIALIZER'}
        for name, setting_name in optional.items():
            val = settings.get(setting_name)
            if val:
                kwargs[name] = val
            if isinstance(kwargs.get('serializer'), six.string_types):
                kwargs['serializer'] = importlib.import_module(kwargs['serializer'])
            server = connection.from_settings(settings)
            server.ping()
            return cls(server=server, **kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        instance = cls.from_settings(crawler.settings)
        instance.stats = crawler.stats
        return instance

    def open(self, spider):
        self.spider = spider
        try:
            self.queue = load_object(self.queue_cls)(server=(self.server),
              spider=spider,
              key=(self.queue_key % {'spider': spider.name}),
              serializer=(self.serializer))
        except TypeError as e:
            try:
                raise ValueError("Failed to instantiate queue class '%s': %s", self.queue_cls, e)
            finally:
                e = None
                del e

        else:
            try:
                self.df = load_object(self.dupefilter_cls)(server=(self.server),
                  key=(self.dupefilter_key % {'spider': spider.name}),
                  debug=(spider.settings.getbool('DUPEFILTER_DEBUG')),
                  bit=(spider.settings.getint('BLOOMFILTER_BIT', BLOOMFILTER_BIT)),
                  hash_number=(spider.settings.getint('BLOOMFILTER_HASH_NUMBER', BLOOMFILTER_HASH_NUMBER)))
            except TypeError as e:
                try:
                    raise ValueError("Failed to instantiate dupefilter class '%s': %s", self.dupefilter_cls, e)
                finally:
                    e = None
                    del e

            else:
                if self.flush_on_start:
                    self.flush()
                if len(self.queue):
                    spider.log('Resuming crawl (%d requests scheduled)' % len(self.queue))

    def close(self, reason):
        if not self.persist:
            self.flush()

    def flush(self):
        self.df.clear()
        self.queue.clear()

    def enqueue_request(self, request):
        if not request.dont_filter:
            if self.df.request_seen(request):
                self.df.log(request, self.spider)
                return False
        if self.stats:
            self.stats.inc_value('scheduler/enqueued/redis', spider=(self.spider))
        self.queue.push(request)
        return True

    def next_request(self):
        block_pop_timeout = self.idle_before_close
        request = self.queue.pop(block_pop_timeout)
        if request:
            if self.stats:
                self.stats.inc_value('scheduler/dequeued/redis', spider=(self.spider))
        return request

    def has_pending_requests(self):
        return len(self) > 0