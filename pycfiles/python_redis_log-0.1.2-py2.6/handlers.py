# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/redislog/handlers.py
# Compiled at: 2011-06-02 12:01:51
import logging, redis, simplejson as json

class RedisFormatter(logging.Formatter):

    def format(self, record):
        """
        JSON-encode a record for serializing through redis.

        Convert date to iso format, and stringify any exceptions.
        """
        data = record._raw.copy()
        data['time'] = data['time'].isoformat()
        if data.get('traceback'):
            data['traceback'] = self.formatException(data['traceback'])
        return json.dumps(data)


class RedisHandler(logging.Handler):
    """
    Publish messages to redis channel.

    As a convenience, the classmethod to() can be used as a 
    constructor, just as in Andrei Savu's mongodb-log handler.
    """

    @classmethod
    def to(cklass, channel, host='localhost', port=6379, level=logging.NOTSET):
        return cklass(channel, redis.Redis(host=host, port=port), level=level)

    def __init__(self, channel, redis_client, level=logging.NOTSET):
        """
        Create a new logger for the given channel and redis_client.
        """
        logging.Handler.__init__(self, level)
        self.channel = channel
        self.redis_client = redis_client
        self.formatter = RedisFormatter()

    def emit(self, record):
        """
        Publish record to redis logging channel
        """
        self.redis_client.publish(self.channel, self.format(record))