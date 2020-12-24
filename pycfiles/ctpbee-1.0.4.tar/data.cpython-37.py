# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/somewheve/PycharmProjects/ctpbee/ctpbee/looper/data.py
# Compiled at: 2019-12-29 20:22:54
# Size of source mod 2**32: 2878 bytes
"""
回测数据模块

数据应该是需要被特殊处理的， 这样才可以达到最佳访问速度

todo: 优化数据访问速度
--------- >
"""
from datetime import datetime
from itertools import chain

class Bumblebee(dict):
    __doc__ = '  '
    __slots__ = ['last_price', 'datetime', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'type']
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    __getattribute__ = dict.get
    datetime_type = 'datetime'

    def __init__(self, **kwargs):
        if 'last_price' in kwargs:
            self['type'] = 'tick'
        else:
            self['type'] = 'bar'
        (super().__init__)(**kwargs)
        self.datetime = Bumblebee.covert_datetime(self.datetime)

    @staticmethod
    def covert_datetime(datetime_data):
        """
        此函数接受三种格式的数据转换过程
        :param datetime_data  str/int
        """
        if isinstance(datetime_data, datetime):
            return datetime_data
        if isinstance(datetime_data, str):
            try:
                return datetime.strptime(datetime_data, '%Y-%m-%d %H:%M:%S')
            except Exception:
                return datetime.strptime(datetime_data, '%Y-%m-%d %H:%M:%S.%f')

        if isinstance(datetime_data, int):
            return datetime.fromtimestamp(datetime_data)


class VessData:
    __doc__ = '\n        本类存在的意义就是整合各家数据， 提供数据统一的解决方案 ^_^ hope you will relax it\n        如果数据想接进来, 请提交pr\n\n    '

    def __init__(self, data):
        self.init_flag = False
        self.data = data
        self.data_provider = 'ctpbee'
        self.product_type = 'future'
        self.data_type = Bumblebee(**data[0]).type
        try:
            self.inner_data = chain(map(lambda x: Bumblebee(**x), data))
            self.init_flag = True
        except Exception:
            pass

        self.slice = 0

    def __next__(self):
        """ 实现生成器协议使得这个类可以被next函数不断调用 """
        result = next(self.inner_data)
        return result

    def __iter__(self):
        return iter(self.inner_data)

    @property
    def length(self):
        return len(self.data)

    @property
    def type(self):
        """ 数据类型 """
        return self.data_type

    @property
    def product(self):
        """ 产品类型 """
        return self.product_type