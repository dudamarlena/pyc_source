# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/somewheve/PycharmProjects/ctpbee/ctpbee/looper/report.py
# Compiled at: 2019-12-10 01:06:48
# Size of source mod 2**32: 1971 bytes
__doc__ = '\n此模块是用来帮助ctpbee的回测来生成指定的策略报告，UI本身采用\n\n'
import os, webbrowser
from jinja2 import Environment, PackageLoader, select_autoescape
from ctpbee import get_ctpbee_path
from datetime import datetime
from ctpbee.func import join_path
env = Environment(loader=(PackageLoader('ctpbee', 'looper/templates')),
  autoescape=(select_autoescape(['html', 'xml'])))
main_template = env.get_template('looper.html')
trade_template = env.get_template('trade_record.html')

def render_result--- This code section failed: ---

 L.  28         0  LOAD_GLOBAL              str
                2  LOAD_FAST                'datetimed'
                4  LOAD_METHOD              strftime
                6  LOAD_STR                 '%Y-%m-%d_%H_%M_%S'
                8  CALL_METHOD_1         1  ''
               10  CALL_FUNCTION_1       1  ''
               12  STORE_FAST               'datetimed'

 L.  29        14  LOAD_GLOBAL              main_template
               16  LOAD_ATTR                render
               18  LOAD_FAST                'result'
               20  LOAD_FAST                'strategy'

 L.  30        22  LOAD_FAST                'account_data'

 L.  31        24  LOAD_FAST                'net_pnl'

 L.  31        26  LOAD_FAST                'cost_time'

 L.  32        28  LOAD_FAST                'datetimed'

 L.  29        30  LOAD_CONST               ('result', 'strategy', 'account_data', 'net_pnl', 'cost_time', 'datetime')
               32  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
               34  STORE_FAST               'code_string'

 L.  33        36  LOAD_GLOBAL              trade_template
               38  LOAD_ATTR                render
               40  LOAD_FAST                'trade_data'
               42  LOAD_CONST               ('trade_data',)
               44  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               46  STORE_FAST               'trade_code_string'

 L.  36        48  LOAD_FAST                'kwargs'
               50  LOAD_METHOD              get
               52  LOAD_STR                 'file_path'
               54  LOAD_CONST               None
               56  CALL_METHOD_2         2  ''
               58  STORE_FAST               'file_path'

 L.  39        60  LOAD_FAST                'kwargs'
               62  LOAD_METHOD              get
               64  LOAD_STR                 'trade_file_path'
               66  LOAD_CONST               None
               68  CALL_METHOD_2         2  ''
               70  STORE_FAST               'trade_path'

 L.  42        72  LOAD_GLOBAL              join_path
               74  LOAD_GLOBAL              get_ctpbee_path
               76  CALL_FUNCTION_0       0  ''
               78  LOAD_STR                 'looper'
               80  CALL_FUNCTION_2       2  ''
               82  STORE_FAST               'path'

 L.  43        84  LOAD_FAST                'file_path'
               86  POP_JUMP_IF_TRUE    124  'to 124'

 L.  44        88  LOAD_GLOBAL              os
               90  LOAD_ATTR                path
               92  LOAD_METHOD              isdir
               94  LOAD_FAST                'path'
               96  CALL_METHOD_1         1  ''
               98  POP_JUMP_IF_TRUE    110  'to 110'

 L.  45       100  LOAD_GLOBAL              os
              102  LOAD_METHOD              mkdir
              104  LOAD_FAST                'path'
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          
            110_0  COME_FROM            98  '98'

 L.  47       110  LOAD_GLOBAL              join_path
              112  LOAD_FAST                'path'
              114  LOAD_FAST                'datetimed'
              116  LOAD_STR                 '.html'
              118  BINARY_ADD       
              120  CALL_FUNCTION_2       2  ''
              122  STORE_FAST               'file_path'
            124_0  COME_FROM            86  '86'

 L.  49       124  LOAD_FAST                'trade_path'
              126  POP_JUMP_IF_TRUE    142  'to 142'

 L.  50       128  LOAD_GLOBAL              join_path
              130  LOAD_FAST                'path'
              132  LOAD_FAST                'datetimed'
              134  LOAD_STR                 '-trade.html'
              136  BINARY_ADD       
              138  CALL_FUNCTION_2       2  ''
              140  STORE_FAST               'trade_path'
            142_0  COME_FROM           126  '126'

 L.  51       142  LOAD_GLOBAL              open
              144  LOAD_FAST                'file_path'
              146  LOAD_STR                 'w'
              148  LOAD_STR                 'utf8'
              150  LOAD_CONST               ('encoding',)
              152  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              154  SETUP_WITH          172  'to 172'
              156  STORE_FAST               'f'

 L.  52       158  LOAD_FAST                'f'
              160  LOAD_METHOD              write
              162  LOAD_FAST                'code_string'
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          
              168  POP_BLOCK        
              170  BEGIN_FINALLY    
            172_0  COME_FROM_WITH      154  '154'
              172  WITH_CLEANUP_START
              174  WITH_CLEANUP_FINISH
              176  END_FINALLY      

 L.  53       178  LOAD_GLOBAL              open
              180  LOAD_FAST                'trade_path'
              182  LOAD_STR                 'w'
              184  LOAD_STR                 'utf8'
              186  LOAD_CONST               ('encoding',)
              188  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              190  SETUP_WITH          208  'to 208'
              192  STORE_FAST               'f'

 L.  54       194  LOAD_FAST                'f'
              196  LOAD_METHOD              write
              198  LOAD_FAST                'trade_code_string'
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          
              204  POP_BLOCK        
              206  BEGIN_FINALLY    
            208_0  COME_FROM_WITH      190  '190'
              208  WITH_CLEANUP_START
              210  WITH_CLEANUP_FINISH
              212  END_FINALLY      

 L.  55       214  LOAD_FAST                'kwargs'
              216  LOAD_METHOD              get
              218  LOAD_STR                 'auto_open'
              220  LOAD_CONST               None
              222  CALL_METHOD_2         2  ''
              224  POP_JUMP_IF_FALSE   236  'to 236'

 L.  56       226  LOAD_GLOBAL              webbrowser
              228  LOAD_METHOD              open
              230  LOAD_FAST                'file_path'
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          
            236_0  COME_FROM           224  '224'

 L.  57       236  LOAD_FAST                'file_path'
              238  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 170