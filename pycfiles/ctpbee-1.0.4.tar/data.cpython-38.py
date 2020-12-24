# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/somewheve/PycharmProjects/ctpbee/ctpbee/looper/data.py
# Compiled at: 2019-12-19 00:19:34
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
    def covert_datetime--- This code section failed: ---

 L.  39         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'datetime_data'
                4  LOAD_GLOBAL              datetime
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L.  40        10  LOAD_FAST                'datetime_data'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.  41        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'datetime_data'
               18  LOAD_GLOBAL              str
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_FALSE    72  'to 72'

 L.  43        24  SETUP_FINALLY        40  'to 40'

 L.  44        26  LOAD_GLOBAL              datetime
               28  LOAD_METHOD              strptime
               30  LOAD_FAST                'datetime_data'
               32  LOAD_STR                 '%Y-%m-%d %H:%M:%S'
               34  CALL_METHOD_2         2  ''
               36  POP_BLOCK        
               38  RETURN_VALUE     
             40_0  COME_FROM_FINALLY    24  '24'

 L.  45        40  DUP_TOP          
               42  LOAD_GLOBAL              Exception
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    70  'to 70'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L.  46        54  LOAD_GLOBAL              datetime
               56  LOAD_METHOD              strptime
               58  LOAD_FAST                'datetime_data'
               60  LOAD_STR                 '%Y-%m-%d %H:%M:%S.%f'
               62  CALL_METHOD_2         2  ''
               64  ROT_FOUR         
               66  POP_EXCEPT       
               68  RETURN_VALUE     
             70_0  COME_FROM            46  '46'
               70  END_FINALLY      
             72_0  COME_FROM            22  '22'

 L.  47        72  LOAD_GLOBAL              isinstance
               74  LOAD_FAST                'datetime_data'
               76  LOAD_GLOBAL              int
               78  CALL_FUNCTION_2       2  ''
               80  POP_JUMP_IF_FALSE    92  'to 92'

 L.  51        82  LOAD_GLOBAL              datetime
               84  LOAD_METHOD              fromtimestamp
               86  LOAD_FAST                'datetime_data'
               88  CALL_METHOD_1         1  ''
               90  RETURN_VALUE     
             92_0  COME_FROM            80  '80'

Parse error at or near `POP_TOP' instruction at offset 50


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
        else:
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