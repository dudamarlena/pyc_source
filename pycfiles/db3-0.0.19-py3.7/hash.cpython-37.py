# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ssdb/hash.py
# Compiled at: 2020-03-25 11:37:00
# Size of source mod 2**32: 4060 bytes
from ssdb.todo import *

class HashMap(Base):
    __doc__ = '出错则返回 false, 其它值表示正常.'

    def hset_list(self, name, key, value, unique=True) -> int:
        assert value, f"Value is EMPTY? ({value})"
        oo = self.hget(name, key)
        oo = oo if oo else []
        if unique:
            if value in oo:
                oo.remove(value)
        oo.append(value)
        value = oo
        return self.execute_command('hset', c(name, 1), c(key, 1), pickle_dumps(value))

    def hset(self, name, key, value) -> int:
        """
        :return: int (1:new 0:update)
        """
        return self.execute_command('hset', c(name, 1), c(key, 1), pickle_dumps(value))

    def hget(self, name, key):
        if c(key):
            return pickle_loads(self.execute_command('hget', c(name), c(key)))

    def hdel(self, name, key):
        """如果出错则返回 false, 其它值表示正常. 你无法通过返回值来判断被删除的 key 是否存在."""
        if key:
            return self.execute_command('hdel', c(name), c(key))

    def hincr(self, name, key, num: int=1):
        """返回新的值."""
        return self.execute_command('hincr', c(name), c(key), int(num))

    def hexists(self, name, key) -> int:
        """
        :return: exist: 1 / not:0
        """
        if key:
            return int(self.execute_command('hexists', c(name, 1), c(key, 1)))
        return 0

    def hsize(self, name) -> int:
        """
        :return: exist: 1 / not:0
        """
        return self.execute_command('hsize', c(name))

    def hlist(self, name_start=None, name_end=None, limit=None) -> list:
        """
        列出名字处于区间 (name_start, name_end] 的 hash map. ("", ""] 表示整个区间. (return name_list)
        """
        name_start, name_end = deal_start_end(name_start, name_end)
        name_end = name_end if name_end else '{}ÿ'.format(name_start)
        return bytes_to_str(self.execute_command('hlist', name_start, name_end, check_limit(limit)))

    def hrlist(self, name_start=None, name_end=None, limit=None) -> list:
        return self.hlist(name_start, name_end, limit)[::-1]

    def hkeys(self, name, key_start=None, key_end=None, limit=None):
        key_start, key_end = deal_start_end(key_start, key_end)
        return bytes_to_str(self.execute_command('hkeys', c(name), key_start, key_end, check_limit(limit)))

    def hgetall(self, name) -> dict:
        x = self.execute_command('hgetall', c(name))
        return list_to_dict(x)

    def hscan(self, name, key_start=None, key_end=None, limit=None, r='v'):
        """
        :param name:
        :param key_start:
        :param key_end:
        :param limit:
        :param r: v/d > value list/ kv dict
        :return:
        """
        key_start, key_end = deal_start_end(key_start, key_end)
        d = list_to_dict(self.execute_command('hscan', c(name), key_start, key_end, check_limit(limit)))
        if r == 'v':
            return list(d.values())
        return d

    def hrscan(self, name, key_start=None, key_end=None, limit=None, r='v'):
        key_start, key_end = deal_start_end(key_start, key_end, mode='z')
        d = list_to_dict(self.execute_command('hrscan', c(name), key_end, key_start, check_limit(limit)))
        if r == 'v':
            return list(d.values())
        return d

    def hclear(self, name) -> int:
        """
        :return: delete key number
        """
        return int(self.execute_command('hclear', c(name)))

    def multi_hset(self, name, kvs: dict):
        if kvs:
            return (self.execute_command)('multi_hset', c(name, 1), *dict_to_list(kvs))
        return 0

    def multi_hget(self, name, keys: list):
        if keys:
            return list_to_dict((self.execute_command)('multi_hget', c(name), *keys))
        return {}

    def multi_hdel(self, name, keys: list) -> int:
        if keys:
            return (self.execute_command)('multi_hdel', c(name), *keys)
        return 0

    hset_multi = multi_hset
    hget_multi = multi_hget
    hdel_multi = multi_hdel