# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ssdb/kv.py
# Compiled at: 2020-03-25 11:37:00
# Size of source mod 2**32: 4939 bytes
from ssdb.todo import *

class KV(Base):
    __doc__ = '\n    ssdb python 3 client\n    '

    def set(self, key, value) -> int:
        """
        :return: int (1)
        """
        return self.execute_command('set', c(key, 1), pickle_dumps(value))

    def setx(self, key, value, ttl: int) -> int:
        """
        :return: int (1)
        """
        return self.execute_command('setx', c(key, 1), pickle_dumps(value), ttl)

    def setnx(self, key, value, ttl: int) -> int:
        """
        当 key 不存在时, 设置指定 key 的值内容. 如果已存在, 则不设置.
        :return: 1: value 已经设置, 0: key 已经存在, 不更新.
        """
        warnings.warn('This method is invalid, Please do not use...', DeprecationWarning)
        return int(self.execute_command('setnx', c(key, 1), pickle_dumps(value), ttl))

    def expire(self, key, ttl: int) -> int:
        """
        :return: 如果 key 存在并设置成功, 返回 1, 如果 key 不存在, 返回 0.
        """
        return int(self.execute_command('expire', c(key, 1), ttl))

    def ttl(self, key) -> int:
        """
        :return: ttl | -1: not ttl
        """
        return int(self.execute_command('ttl', c(key)))

    def get(self, key):
        """
        :return: None or Obj
        """
        d = self.execute_command('get', c(key))
        return pickle_loads(d)

    def getset(self, key, value):
        """
        :return: None or **Old Obj**
        """
        warnings.warn('This method is invalid, Please do not use...', DeprecationWarning)
        d = self.execute_command('getset', c(key, 1), pickle_dumps(value))
        return pickle_loads(d)

    def delete(self, key) -> int:
        """
        :return: ALL 1
        """
        return self.execute_command('del', c(key))

    def incr(self, key, num: int=1) -> int:
        """
        :param key:
        :param num: int, default = 1
        :return: int (new value)
        """
        return self.execute_command('incr', c(key, 1), int(num))

    def exists(self, key) -> int:
        """
        :return: exist: 1 / not: 0
        :rtype: int
        """
        return int(self.execute_command('exists', c(key)))

    def strlen(self, key) -> int:
        warnings.warn('This method is incorrect, Because [pickle.dumps], Please do not use...', DeprecationWarning)
        return int(self.execute_command('strlen', c(key)))

    def keys(self, key_start=None, key_end=None, limit=None) -> list:
        """
        keys('') >>>  ("", ""] 表示整个区间.
        warn: keys('0') >>> ['0_1', '0_2'] not include '0'
        """
        key_start = c(key_start, check_empty=False)
        key_end = key_end if key_end else '{}ÿ'.format(key_start)
        return bytes_to_str(self.execute_command('keys', key_start, key_end, check_limit(limit)))

    def rkeys(self, key_start=None, key_end=None, limit=None) -> list:
        return self.keys(key_start, key_end, limit)[::-1]

    def scan(self, key_start=None, key_end=None, limit=None, r='v'):
        """
        :param key_start:
        :param key_end:
        :param limit:
        :param r: v/d > value list/dict
        :return:
        """
        key_start = c(key_start, check_empty=False)
        key_end = key_end if key_end else '{}ÿ'.format(key_start)
        x = list_to_dict(self.execute_command('scan', key_start, key_end, check_limit(limit)))
        if r == 'v':
            return list(x.values())
        return x

    def rscan(self, key_start=None, key_end=None, limit=None, r='v') -> list:
        x = self.scan(key_start, key_end, limit, r)
        if r == 'v':
            return x[::-1]
        return x

    def multi_set(self, kvs):
        if kvs:
            return (self.execute_command)(*('multi_set', ), *dict_to_list(kvs))
        return 0

    def multi_get(self, keys, r='v'):
        x = list_to_dict((self.execute_command)(*('multi_get', ), *keys)) if keys else {}
        if r == 'v':
            return list(x.values())
        return x

    def multi_del(self, keys) -> int:
        if keys:
            return (self.execute_command)(*('multi_del', ), *keys)
        return 0