# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nazrul/www/python/Contributions/apps/hybrid-access-control-system/hacs/globals.py
# Compiled at: 2016-07-11 11:02:50
# Size of source mod 2**32: 1920 bytes
__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'
HACS_APP_NAME = 'hacs'
HACS_APP_LABEL = HACS_APP_NAME
HACS_GENERATED_FILENAME_PREFIX = 'hacs__generated_'
HACS_SERIALIZED_ROUTE_DIR_NAME = 'hacs_routes'
HTTP_METHOD_LIST = ('GET', 'POST', 'PUT', 'HEAD', 'PATCH', 'DELETE', 'OPTIONS')

class HACSSiteCache(object):
    __doc__ = " Obviously this class is not tread safe, infact we don't need to be. "

    def __init__(self):
        """
        :return:
        """
        self.__storage__ = dict()

    def get(self, key, default=None):
        """
        :param key:
        :param default:
        :return:
        """
        return self.__storage__.get(key, default)

    def set(self, key, value):
        """
        :param key:
        :param value:
        :return:
        """
        return self.__storage__.update({key: value})

    def clear(self):
        """
        :return:
        """
        del self.__storage__
        self.__storage__ = dict()

    def __getitem__(self, item):
        """
        :param item:
        :return:
        """
        return self.__storage__[item]

    def __setitem__(self, key, value):
        """
        :param key:
        :param value:
        :return:
        """
        self.__storage__[key] = value

    def __delitem__(self, key):
        """
        :param key:
        :return:
        """
        del self.__storage__[key]

    def __len__(self):
        """
        :return:
        """
        return len(self.__storage__)

    def __repr__(self):
        """
        :return:
        """
        return repr(self.__storage__)

    def __str__(self):
        """
        :return:
        """
        return str(self.__storage__)


HACS_SITE_CACHE = HACSSiteCache()