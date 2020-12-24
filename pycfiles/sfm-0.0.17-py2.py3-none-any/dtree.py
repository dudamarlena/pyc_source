# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/single_file_module-project/sfm/dtree.py
# Compiled at: 2019-04-22 00:16:32
"""
**中文文档**

DictTree是类似于xml的一种文档树结构的实现。

- set attributes 操作为DictTree添加metadata, 例如 ``DictTree.name = "John"``
- set item 操作为DictTree添加子树, 例如 ``DictTree["Sam"] = DictTree(name="Sam")``
- for 循环操作为遍历所有的子树的key, 同理有 keys(), values(), items() 方法可以对
  key, value或者两者进行循环遍历。
- keys_at(), values_at(), items_at() 可以根据树的深度进行遍历。深度为0返回母树本身。
- length_at() 返回在某个深度上子树的数量。
- stats(), stats_at() 返回树的基本信息统计情况。

注意: 本实现性能很一般, 若你对性能有需求, 请使用xml文档树。本实现是面向对象的
实现方式, 根据同样的思路, 还有一个函数式的实现 :mod:`~sfm.dict_tree`. 缺点是操作
比较不直观, 但是对于stats方法的性能有巨大的提升。这是因为在返回子树时候无需生成
子树对象。虽然生成子树对象实际上仅仅是将类的属性和字典进行绑定, 但是相对于在
循环中计数这一快速过程, 仍然是一笔不小的开销。
"""
from __future__ import print_function, unicode_literals
import json, pickle, collections
DATA = b'__data__'
META = b'__meta__'
KEY = b'__key__'
ROOT = b'__root__'

class DictTree(object):
    """
    Pure python xml doc tree implementation in dictionary.

    Usage::

        >>> dt = DictTree(name="USA")
        >>> dt["MD"] = DictTree(name="Maryland")
        >>> dt["VA"] = DictTree(name="Virginia")

        >>> dt["MD"]["Gaithersburg"] = DictTree(name="Gaithersburg", zipcode="20878")
        >>> dt["MD"]["College Park"] = DictTree(name="College Park", zipcode="20740")

        >>> dt["VA"]["Arlington"] = DictTree(name="Arlington", zipcode="22202")
        >>> dt["VA"]["Fairfax"] = DictTree(name="Fairfax", zipcode="20030")

        # visit tree metadata
        >>> dt.name
        USA
        >>> dt["MD"].name
        Maryland

        # visit node
        >>> dt["MD"]
        {
            "College Park": {
                "__key__": "College Park",
                "__meta__": {
                    "name": "College Park",
                    "zipcode": "20740"
                }
            },
            "Gaithersburg": {
                "__key__": "Gaithersburg",
                "__meta__": {
                    "name": "Gaithersburg",
                    "zipcode": "20878"
                }
            },
            "__key__": "MD",
            "__meta__": {
                "name": "Maryland"
            }
        }

        # visit key
        >>> dt_MD = dt["MD"]
        >>> dt_MD._key()
        MD

        >>> list(dt.keys_at(depth=1)) # or values_at(depth), items_at(depth)
        ['MD', 'VA']

        >>> list(dt.keys_at(depth=2))
        ['Gaithersburg', 'College Park', 'Arlington', 'Fairfax']

    **中文文档**

    internal data structure::

        {
            META: {key: value}, # parent tree attributes
            "child_key1": ... , # child tree's key, value pair.
            "child_key2": ... ,
            ...
        }

    对于根树而言, Key为 ``"root"``
    """
    __slots__ = [
     DATA]

    def __init__(self, __data__=None, **kwargs):
        if __data__ is None:
            object.__setattr__(self, DATA, {META: kwargs, KEY: ROOT})
        else:
            object.__setattr__(self, DATA, __data__)
        return

    def __str__(self):
        try:
            return json.dumps(self.__data__, sort_keys=True, indent=4)
        except:
            return str(self.__data__)

    def dump(self, path):
        """
        dump DictTree data to json files.
        """
        try:
            with open(path, b'wb') as (f):
                f.write(self.__str__().encode(b'utf-8'))
        except:
            pass

        with open(path, b'wb') as (f):
            pickle.dump(self.__data__, f)

    @classmethod
    def load(cls, path):
        """
        load DictTree from json files.
        """
        try:
            with open(path, b'rb') as (f):
                return cls(__data__=json.loads(f.read().decode(b'utf-8')))
        except:
            pass

        with open(path, b'rb') as (f):
            return cls(__data__=pickle.load(f))

    def __getattribute__(self, attr):
        try:
            return object.__getattribute__(self, DATA)[META][attr]
        except KeyError:
            return object.__getattribute__(self, attr)

    def __setattr__(self, attr, value):
        self.__data__[META][attr] = value

    def __setitem__(self, key, dict_tree):
        if key in (META, KEY):
            raise ValueError(b"'key' can't be '__meta__'!")
        if isinstance(dict_tree, DictTree):
            dict_tree.__data__[KEY] = key
            self.__data__[key] = dict_tree.__data__
        else:
            raise TypeError(b"attribute assignment only takes 'DictTree'.")

    def __getitem__(self, key):
        return DictTree(__data__=self.__data__[key])

    def __delitem__(self, key):
        if key in (META, KEY):
            raise ValueError(b"'key' can't be '__meta__'!")
        self.__data__[key][KEY] = ROOT
        del self.__data__[key]

    def __contains__(self, item):
        return item in self.__data__

    def __len__(self):
        u"""
        Return number of child trees.

        **中文文档**

        返回子树的数量。
        """
        return len(self.__data__) - 2

    def __iter__(self):
        for key in self.__data__:
            if key not in (META, KEY):
                yield key

    def _key(self):
        return self.__data__[KEY]

    def keys(self):
        """
        Iterate keys.
        """
        for key in self.__data__:
            if key not in (META, KEY):
                yield key

    def values(self):
        """
        Iterate values.
        """
        for key, value in self.__data__.items():
            if key not in (META, KEY):
                yield DictTree(__data__=value)

    def items(self):
        """
        Iterate items.
        :return:
        """
        for key, value in self.__data__.items():
            if key not in (META, KEY):
                yield (
                 key, DictTree(__data__=value))

    def keys_at(self, depth, counter=1):
        """
        Iterate keys at specified depth.
        """
        if depth < 1:
            yield ROOT
        elif counter == depth:
            for key in self.keys():
                yield key

        else:
            counter += 1
            for dict_tree in self.values():
                for key in dict_tree.keys_at(depth, counter):
                    yield key

    def values_at(self, depth):
        """
        Iterate values at specified depth.
        """
        if depth < 1:
            yield self
        else:
            for dict_tree in self.values():
                for value in dict_tree.values_at(depth - 1):
                    yield value

    def items_at(self, depth):
        """
        Iterate items at specified depth.
        """
        if depth < 1:
            yield (
             ROOT, self)
        elif depth == 1:
            for key, value in self.items():
                yield (
                 key, value)

        else:
            for dict_tree in self.values():
                for key, value in dict_tree.items_at(depth - 1):
                    yield (
                     key, value)

    def length_at(self, depth):
        """Get the number of nodes on specific depth.
        """
        if depth == 0:
            return 1
        counter = 0
        for dict_tree in self.values_at(depth - 1):
            counter += len(dict_tree)

        return counter

    def stats(self, result=None, counter=0):
        """
        Display the node stats info on specific depth in this dict.

        ::

            [
                {"depth": 0, "leaf": M0, "root": N0},
                {"depth": 1, "leaf": M1, "root": N1},
                ...
                {"depth": k, "leaf": Mk, "root": Nk},
            ]
        """
        if result is None:
            result = dict()
        if counter == 0:
            if len(self):
                result[0] = {b'depth': 0, b'leaf': 0, b'root': 1}
            else:
                result[0] = {b'depth': 0, b'leaf': 1, b'root': 0}
        counter += 1
        if len(self):
            result.setdefault(counter, {b'depth': counter, b'leaf': 0, b'root': 0})
            for dict_tree in self.values():
                if len(dict_tree):
                    result[counter][b'root'] += 1
                else:
                    result[counter][b'leaf'] += 1
                dict_tree.stats(result, counter)

        return [ collections.OrderedDict([(b'depth', info[b'depth']), (b'leaf', info[b'leaf']), (b'root', info[b'root'])]) for info in sorted(result.values(), key=lambda x: x[b'depth'])
               ]

    def stats_at(self, depth, display=False):
        root, leaf = (0, 0)
        for dict_tree in self.values_at(depth):
            if len(dict_tree):
                root += 1
            else:
                leaf += 1

        total = root + leaf
        if display:
            print(b'On depth %s, having %s root nodes, %s leaf nodes. %s nodes in total.' % (
             depth, root, leaf, total))
        return (
         root, leaf, total)


if __name__ == b'__main__':
    import os, time, string, random
    from pprint import pprint

    def rand_str(length):
        return (b'').join([ random.choice(string.ascii_letters) for _ in range(length) ])


    def benchmark():
        """
        ....creating elapse 27.871160
        dumping elapse 23.268375
        loading elapse 3.634183
        [OrderedDict([('depth', 0), ('leaf', 0), ('root', 1)]),
         OrderedDict([('depth', 1), ('leaf', 0), ('root', 10)]),
         OrderedDict([('depth', 2), ('leaf', 0), ('root', 100)]),
         OrderedDict([('depth', 3), ('leaf', 0), ('root', 1000)]),
         OrderedDict([('depth', 4), ('leaf', 0), ('root', 10000)]),
         OrderedDict([('depth', 5), ('leaf', 0), ('root', 100000)]),
         OrderedDict([('depth', 6), ('leaf', 1000000), ('root', 0)])]
        analyze elapse 86.070060
        ...
        """
        path = b'test.json'
        st = time.clock()
        d = DictTree(name=rand_str(8))
        for depth in range(6):
            for dict_tree in d.values_at(depth):
                for _ in range(10):
                    dict_tree[rand_str(8)] = DictTree(name=rand_str(8))

        print(b'creating elapse %.6f' % (time.clock() - st,))
        st = time.clock()
        d.dump(path)
        print(b'dumping elapse %.6f' % (time.clock() - st,))
        st = time.clock()
        d = DictTree.load(path)
        print(b'loading elapse %.6f' % (time.clock() - st,))
        st = time.clock()
        pprint(d.stats())
        print(b'analyze elapse %.6f' % (time.clock() - st,))
        st = time.clock()
        for depth in range(7):
            d.stats_at(depth)

        print(b'analyze elapse %.6f' % (time.clock() - st,))
        os.remove(path)