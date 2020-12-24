# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/sheldon/storage.py
# Compiled at: 2015-11-23 23:22:39
# Size of source mod 2**32: 2345 bytes
"""
Interface to Redis-storage.

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: The MIT license

Copyright (C) 2015
"""
from sheldon.utils import logger
from redis import StrictRedis

class Storage:

    def __init__(self, bot):
        """
        Create new storage for bot

        :param bot: Bot object
        :return:
        """
        self.bot = bot
        self.redis = StrictRedis(host=bot.config.get('SHELDON_REDIS_HOST', 'localhost'), port=bot.config.get('SHELDON_REDIS_PORT', '6379'), db=bot.config.get('SHELDON_REDIS_DB', '0'))
        try:
            self.redis.client_list()
        except Exception as error:
            logger.error_message('Error while connecting Redis:')
            logger.error_message(str(error))
            self.redis = None

    def get(self, key, default_value=None):
        """
        Get value from redis storage

        :param key: string, redis key for needed value
        :param default_value: string, value that returns if
                              key not found or redis isn't
                              connected to this bot
        :return: value with that key or default value
        """
        if not self.redis:
            logger.warning_message('Redis not available for {} key'.format(key))
            return default_value
        else:
            value = self.redis.get(key)
            if value is not None:
                return value
            return default_value

    def set(self, key, value):
        """
        Set key to value in redis storage

        :param key: string
        :param value: string
        :return:
        """
        if not self.redis:
            logger.warning_message("{} key didn't save in storage".format(key))
            return
        return self.redis.set(key, value)