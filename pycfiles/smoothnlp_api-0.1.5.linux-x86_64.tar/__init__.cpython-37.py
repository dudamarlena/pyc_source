# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/conda/lib/python3.7/site-packages/smoothnlp_api/__init__.py
# Compiled at: 2019-09-17 09:18:30
# Size of source mod 2**32: 1650 bytes
"""
    Investment

    投资事件(主要来源ITjuzi)  * 默认域名： service-m5j3awiv-1259459016.ap-shanghai.apigateway.myqcloud.com/release * 自定义域名： data.service.invest.smoothnlp.com/   # noqa: E501
"""
from __future__ import absolute_import
import logging, hmac, base64, datetime, hashlib
logger = logging.getLogger('data_service_logger')

def getSimpleSign--- This code section failed: ---

 L.  27         0  LOAD_STR                 '%a, %d %b %Y %H:%M:%S GMT'
                2  STORE_FAST               'GMT_FORMAT'

 L.  28         4  LOAD_FAST                'SecretId'
                6  LOAD_STR                 ''
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_TRUE     36  'to 36'
               12  LOAD_FAST                'SecretKey'
               14  LOAD_STR                 ''
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_TRUE     36  'to 36'
               20  LOAD_FAST                'SecretKey'
               22  LOAD_CONST               None
               24  COMPARE_OP               is
               26  POP_JUMP_IF_TRUE     36  'to 36'
               28  LOAD_FAST                'SecretId'
               30  LOAD_CONST               None
               32  COMPARE_OP               is
               34  POP_JUMP_IF_FALSE    54  'to 54'
             36_0  COME_FROM            26  '26'
             36_1  COME_FROM            18  '18'
             36_2  COME_FROM            10  '10'

 L.  29        36  LOAD_GLOBAL              logger
               38  LOAD_METHOD              fatal
               40  LOAD_STR                 '请先设置 SecretId/SecretKey 对，再计算签名'
               42  CALL_METHOD_1         1  '1 positional argument'
               44  POP_TOP          

 L.  30        46  LOAD_GLOBAL              ConnectionError
               48  LOAD_STR                 ' Invalid Secret ID or Key '
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            34  '34'

 L.  31        54  LOAD_GLOBAL              datetime
               56  LOAD_ATTR                datetime
               58  LOAD_METHOD              utcnow
               60  CALL_METHOD_0         0  '0 positional arguments'
               62  LOAD_METHOD              strftime
               64  LOAD_FAST                'GMT_FORMAT'
               66  CALL_METHOD_1         1  '1 positional argument'
               68  STORE_FAST               'dateTime'

 L.  32        70  LOAD_STR                 'hmac id="'
               72  LOAD_FAST                'SecretId'
               74  BINARY_ADD       
               76  LOAD_STR                 '", algorithm="hmac-sha1", headers="date source", signature="'
               78  BINARY_ADD       
               80  STORE_FAST               'auth'

 L.  33        82  LOAD_STR                 'date: '
               84  LOAD_FAST                'dateTime'
               86  BINARY_ADD       
               88  LOAD_STR                 '\n'
               90  BINARY_ADD       
               92  LOAD_STR                 'source: '
               94  BINARY_ADD       
               96  LOAD_FAST                'source'
               98  BINARY_ADD       
              100  STORE_FAST               'signStr'

 L.  35       102  LOAD_GLOBAL              hmac
              104  LOAD_METHOD              new
              106  LOAD_FAST                'SecretKey'
              108  LOAD_METHOD              encode
              110  LOAD_STR                 'utf-8'
              112  CALL_METHOD_1         1  '1 positional argument'
              114  LOAD_FAST                'signStr'
              116  LOAD_METHOD              encode
              118  LOAD_STR                 'utf-8'
              120  CALL_METHOD_1         1  '1 positional argument'
              122  LOAD_GLOBAL              hashlib
              124  LOAD_ATTR                sha1
              126  CALL_METHOD_3         3  '3 positional arguments'
              128  LOAD_METHOD              digest
              130  CALL_METHOD_0         0  '0 positional arguments'
              132  STORE_FAST               'sign'

 L.  36       134  LOAD_GLOBAL              base64
              136  LOAD_METHOD              b64encode
              138  LOAD_FAST                'sign'
              140  CALL_METHOD_1         1  '1 positional argument'
              142  STORE_FAST               'sign'

 L.  37       144  LOAD_FAST                'sign'
              146  LOAD_METHOD              decode
              148  LOAD_STR                 'utf-8'
              150  CALL_METHOD_1         1  '1 positional argument'
              152  STORE_FAST               'sign'

 L.  38       154  LOAD_FAST                'auth'
              156  LOAD_FAST                'sign'
              158  BINARY_ADD       
              160  LOAD_STR                 '"'
              162  BINARY_ADD       
              164  STORE_FAST               'sign'

 L.  40       166  LOAD_FAST                'sign'
              168  LOAD_FAST                'dateTime'
              170  BUILD_TUPLE_2         2 
              172  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 54_0


from smoothnlp_api.api.investment_api import InvestmentApi
from smoothnlp_api.api.news_api import NewsApi
from smoothnlp_api.api.company_api import CompanyApi
from smoothnlp_api.api_client import ApiClient
from smoothnlp_api.configuration import Configuration
config = Configuration()