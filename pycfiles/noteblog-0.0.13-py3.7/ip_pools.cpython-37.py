# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/ip_pools.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 4871 bytes
from requests import get
import gc
from pickle import dumps
from random import randint
from .sql_utils import BaseRedisCli
from .safe_utils import get_uuid3
from data.pickle_utils import deserializate_pickle_object
from .common_utils import json_2_dict
from .time_utils import *
__all__ = [
 'MyIpPools',
 'IpPools']
ip_proxy_pool = 'IPProxyPool'
fz_ip_pool = 'fz_ip_pool'
sesame_ip_pool = 'sesame_ip_pool'
tri_ip_pool = 'tri_ip_pool'

class MyIpPools(object):

    def __init__(self, type=ip_proxy_pool, high_conceal=False):
        """
        :param type: 所使用ip池类型
        :param high_conceal: 是否初始化为高匿代理
        """
        super(MyIpPools, self).__init__()
        self.high_conceal = high_conceal
        self.type = type
        self.redis_cli = BaseRedisCli() if (self.type == fz_ip_pool or self.type == sesame_ip_pool) else None
        if self.type == fz_ip_pool:
            self.h_key = get_uuid3('h_proxy_list')
        else:
            if self.type == sesame_ip_pool:
                self.h_key = get_uuid3('sesame_ip_pool')
            else:
                self.h_key = None

    def get_proxy_ip_from_ip_pool(self):
        """
        从代理ip池中获取到对应ip
        :return: dict类型 {'http': ['http://183.136.218.253:80', ...]}
        """
        proxy_list = []
        if self.type == ip_proxy_pool:
            if self.high_conceal:
                base_url = 'http://127.0.0.1:8000/?types=0'
            else:
                base_url = 'http://127.0.0.1:8000'
            try:
                result = get(base_url).json()
            except Exception as e:
                try:
                    print(e)
                    return {'http': None}
                finally:
                    e = None
                    del e

            for item in result:
                if item[2] > 7:
                    tmp_url = 'http://{}:{}'.format(item[0], item[1])
                    proxy_list.append(tmp_url)
                else:
                    delete_url = 'http://127.0.0.1:8000/delete?ip='
                    delete_info = get(delete_url + item[0])

        else:
            if self.type == fz_ip_pool:
                base_url = 'http://127.0.0.1:8002/get_all'
                try:
                    res = get(base_url).json()
                    assert res != [], 'res为空list!'
                except Exception as e:
                    try:
                        print(e)
                        return {'https': None}
                    finally:
                        e = None
                        del e

                proxy_list = ['http://{}:{}'.format(item['ip'], item['port']) for item in res]
            else:
                if self.type == sesame_ip_pool:
                    _ = json_2_dict((self.redis_cli.get(name=(self.h_key)) or dumps([])), default_res=[])
                    proxy_list = []
                    for i in _:
                        if datetime_to_timestamp(string_to_datetime(i.get('expire_time', ''))) > datetime_to_timestamp(get_shanghai_time()) + 15:
                            proxy_list.append('http://{}:{}'.format(i.get('ip', ''), i.get('port', '')))

                else:
                    if self.type == tri_ip_pool:
                        base_url = 'http://127.0.0.1:8001/get_all'
                        try:
                            res = get(base_url).json()
                            assert res != [], 'res为空list!'
                        except Exception as e:
                            try:
                                print(e)
                                return {'https': None}
                            finally:
                                e = None
                                del e

                        proxy_list = ['http://{}:{}'.format(item['ip'], item['port']) for item in res]
                        return {'https': proxy_list}
                    raise ValueError('type值异常, 请检查!')
        return {'http': proxy_list}

    def _get_random_proxy_ip(self):
        """
        随机获取一个代理ip: 格式 'http://175.6.2.174:8088'
        :return:
        """
        _ = self.get_proxy_ip_from_ip_pool()
        ip_list = _.get('http') if _.get('http') is not None else _.get('https')
        try:
            if isinstance(ip_list, list):
                proxy_ip = ip_list[randint(0, len(ip_list) - 1)]
            else:
                raise TypeError
        except Exception:
            print('从ip池获取随机ip失败...正在使用本机ip进行爬取!')
            proxy_ip = False

        return proxy_ip

    def _empty_ip_pools--- This code section failed: ---

 L. 129         0  LOAD_FAST                'self'
                2  LOAD_ATTR                type
                4  LOAD_GLOBAL              ip_proxy_pool
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    84  'to 84'

 L. 130        10  LOAD_STR                 'http://127.0.0.1:8000'
               12  STORE_FAST               'base_url'

 L. 131        14  LOAD_GLOBAL              get
               16  LOAD_FAST                'base_url'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_METHOD              json
               22  CALL_METHOD_0         0  '0 positional arguments'
               24  STORE_FAST               'result'

 L. 132        26  LOAD_STR                 'http://127.0.0.1:8000/delete?ip='
               28  STORE_FAST               'delete_url'

 L. 134        30  SETUP_LOOP          120  'to 120'
               32  LOAD_FAST                'result'
               34  GET_ITER         
             36_0  COME_FROM            50  '50'
               36  FOR_ITER             80  'to 80'
               38  STORE_FAST               'item'

 L. 135        40  LOAD_FAST                'item'
               42  LOAD_CONST               2
               44  BINARY_SUBSCR    
               46  LOAD_CONST               11
               48  COMPARE_OP               <
               50  POP_JUMP_IF_FALSE    36  'to 36'

 L. 136        52  LOAD_GLOBAL              get
               54  LOAD_FAST                'delete_url'
               56  LOAD_FAST                'item'
               58  LOAD_CONST               0
               60  BINARY_SUBSCR    
               62  BINARY_ADD       
               64  CALL_FUNCTION_1       1  '1 positional argument'
               66  STORE_FAST               'delete_info'

 L. 137        68  LOAD_GLOBAL              print
               70  LOAD_FAST                'delete_info'
               72  LOAD_ATTR                text
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  POP_TOP          
               78  JUMP_BACK            36  'to 36'
               80  POP_BLOCK        
               82  JUMP_FORWARD        120  'to 120'
             84_0  COME_FROM             8  '8'

 L. 138        84  LOAD_FAST                'self'
               86  LOAD_ATTR                type
               88  LOAD_GLOBAL              fz_ip_pool
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_TRUE    104  'to 104'
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                type
               98  LOAD_GLOBAL              sesame_ip_pool
              100  COMPARE_OP               ==
              102  POP_JUMP_IF_FALSE   120  'to 120'
            104_0  COME_FROM            92  '92'

 L. 139       104  LOAD_FAST                'self'
              106  LOAD_ATTR                redis_cli
              108  LOAD_METHOD              set
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                h_key
              114  LOAD_STR                 ''
              116  CALL_METHOD_2         2  '2 positional arguments'
              118  POP_TOP          
            120_0  COME_FROM           102  '102'
            120_1  COME_FROM            82  '82'
            120_2  COME_FROM_LOOP       30  '30'

Parse error at or near `COME_FROM' instruction at offset 120_1

    def __del__(self):
        try:
            del self.redis_cli
        except:
            pass

        gc.collect()


class IpPools(MyIpPools):
    pass