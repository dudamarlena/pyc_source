# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/somewheve/PycharmProjects/ctpbee/ctpbee/looper/data.py
# Compiled at: 2019-12-29 20:22:54
# Size of source mod 2**32: 2878 bytes
__doc__ = '\n回测数据模块\n\n数据应该是需要被特殊处理的， 这样才可以达到最佳访问速度\n\n\ntodo: 优化数据访问速度\n--------- >\n'
from datetime import datetime
from itertools import chain

class Bumblebee(dict):
    """Bumblebee"""
    __slots__ = [
     'last_price', 'datetime', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'type']
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
    """VessData"""

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