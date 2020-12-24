# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\atapibasiclib\mysqllib.py
# Compiled at: 2019-12-25 04:05:58
# Size of source mod 2**32: 5376 bytes
__doc__ = '\n此模块包含数据库操作相关的函数，如查询，增删改\n'
import atApiBasicLibrary.log as logger
import pymysql

def queryonefrommysql--- This code section failed: ---

 L.  14         0  LOAD_FAST                'conn'
                2  LOAD_METHOD              cursor
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'cursor'

 L.  15      8_10  SETUP_FINALLY       346  'to 346'
            12_14  SETUP_FINALLY       270  'to 270'

 L.  16        16  LOAD_GLOBAL              logger
               18  LOAD_ATTR                info
               20  LOAD_STR                 '\n数据库执行SQL: '
               22  LOAD_FAST                'sql'
               24  BINARY_ADD       
               26  LOAD_CONST               True
               28  LOAD_CONST               True
               30  LOAD_CONST               ('html', 'also_console')
               32  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               34  POP_TOP          

 L.  17        36  LOAD_FAST                'cursor'
               38  LOAD_METHOD              execute
               40  LOAD_FAST                'sql'
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'count'

 L.  18        46  LOAD_GLOBAL              logger
               48  LOAD_ATTR                info
               50  LOAD_STR                 'count=%s'
               52  LOAD_FAST                'count'
               54  BINARY_MODULO    
               56  LOAD_CONST               True
               58  LOAD_CONST               True
               60  LOAD_CONST               ('html', 'also_console')
               62  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               64  POP_TOP          

 L.  20        66  LOAD_FAST                'cursor'
               68  LOAD_METHOD              fetchall
               70  CALL_METHOD_0         0  ''
               72  STORE_FAST               'result'

 L.  21        74  BUILD_LIST_0          0 
               76  STORE_FAST               'fields_list'

 L.  22        78  LOAD_FAST                'cursor'
               80  LOAD_ATTR                description
               82  GET_ITER         
               84  FOR_ITER            104  'to 104'
               86  STORE_FAST               'field'

 L.  24        88  LOAD_FAST                'fields_list'
               90  LOAD_METHOD              append
               92  LOAD_FAST                'field'
               94  LOAD_CONST               0
               96  BINARY_SUBSCR    
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          
              102  JUMP_BACK            84  'to 84'

 L.  25       104  LOAD_FAST                'conn'
              106  LOAD_METHOD              commit
              108  CALL_METHOD_0         0  ''
              110  POP_TOP          

 L.  26       112  LOAD_FAST                'result'
              114  LOAD_CONST               None
              116  COMPARE_OP               is
              118  POP_JUMP_IF_TRUE    132  'to 132'
              120  LOAD_GLOBAL              len
              122  LOAD_FAST                'result'
              124  CALL_FUNCTION_1       1  ''
              126  LOAD_CONST               0
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   158  'to 158'
            132_0  COME_FROM           118  '118'

 L.  27       132  LOAD_GLOBAL              logger
              134  LOAD_ATTR                info
              136  LOAD_STR                 '数据库返回结果: None'
              138  LOAD_CONST               True
              140  LOAD_CONST               True
              142  LOAD_CONST               ('html', 'also_console')
              144  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              146  POP_TOP          

 L.  28       148  POP_BLOCK        
              150  POP_BLOCK        
              152  CALL_FINALLY        346  'to 346'
              154  LOAD_CONST               None
              156  RETURN_VALUE     
            158_0  COME_FROM           130  '130'

 L.  29       158  BUILD_LIST_0          0 
              160  STORE_FAST               'result_list'

 L.  30       162  LOAD_GLOBAL              range
              164  LOAD_GLOBAL              len
              166  LOAD_FAST                'result'
              168  CALL_FUNCTION_1       1  ''
              170  CALL_FUNCTION_1       1  ''
              172  GET_ITER         
              174  FOR_ITER            236  'to 236'
              176  STORE_FAST               'i'

 L.  31       178  BUILD_MAP_0           0 
              180  STORE_FAST               'row_dict'

 L.  32       182  LOAD_FAST                'result'
              184  LOAD_FAST                'i'
              186  BINARY_SUBSCR    
              188  STORE_FAST               'row'

 L.  33       190  LOAD_GLOBAL              range
              192  LOAD_GLOBAL              len
              194  LOAD_FAST                'row'
              196  CALL_FUNCTION_1       1  ''
              198  CALL_FUNCTION_1       1  ''
              200  GET_ITER         
              202  FOR_ITER            224  'to 224'
              204  STORE_FAST               'j'

 L.  34       206  LOAD_FAST                'row'
              208  LOAD_FAST                'j'
              210  BINARY_SUBSCR    
              212  LOAD_FAST                'row_dict'
              214  LOAD_FAST                'fields_list'
              216  LOAD_FAST                'j'
              218  BINARY_SUBSCR    
              220  STORE_SUBSCR     
              222  JUMP_BACK           202  'to 202'

 L.  35       224  LOAD_FAST                'result_list'
              226  LOAD_METHOD              append
              228  LOAD_FAST                'row_dict'
              230  CALL_METHOD_1         1  ''
              232  POP_TOP          
              234  JUMP_BACK           174  'to 174'

 L.  36       236  LOAD_GLOBAL              logger
              238  LOAD_ATTR                info
              240  LOAD_STR                 '数据库返回结果: '
              242  LOAD_GLOBAL              str
              244  LOAD_FAST                'result_list'
              246  CALL_FUNCTION_1       1  ''
              248  BINARY_ADD       
              250  LOAD_CONST               True
              252  LOAD_CONST               True
              254  LOAD_CONST               ('html', 'also_console')
              256  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              258  POP_TOP          

 L.  37       260  LOAD_FAST                'result_list'
              262  POP_BLOCK        
              264  POP_BLOCK        
              266  CALL_FINALLY        346  'to 346'
              268  RETURN_VALUE     
            270_0  COME_FROM_FINALLY    12  '12'

 L.  38       270  DUP_TOP          
              272  LOAD_GLOBAL              pymysql
              274  LOAD_ATTR                MySQLError
              276  COMPARE_OP               exception-match
          278_280  POP_JUMP_IF_FALSE   340  'to 340'
              282  POP_TOP          
              284  STORE_FAST               'e'
              286  POP_TOP          
              288  SETUP_FINALLY       328  'to 328'

 L.  39       290  LOAD_FAST                'conn'
              292  LOAD_METHOD              rollback
              294  CALL_METHOD_0         0  ''
              296  POP_TOP          

 L.  40       298  LOAD_GLOBAL              logger
              300  LOAD_METHOD              error
              302  LOAD_STR                 '数据库错误: '
              304  LOAD_FAST                'e'
              306  BINARY_ADD       
              308  CALL_METHOD_1         1  ''
              310  POP_TOP          

 L.  41       312  LOAD_GLOBAL              AssertionError
              314  LOAD_STR                 '数据库错误: '
              316  LOAD_FAST                'e'
              318  BINARY_ADD       
              320  CALL_FUNCTION_1       1  ''
              322  RAISE_VARARGS_1       1  ''
              324  POP_BLOCK        
              326  BEGIN_FINALLY    
            328_0  COME_FROM_FINALLY   288  '288'
              328  LOAD_CONST               None
              330  STORE_FAST               'e'
              332  DELETE_FAST              'e'
              334  END_FINALLY      
              336  POP_EXCEPT       
              338  JUMP_FORWARD        342  'to 342'
            340_0  COME_FROM           278  '278'
              340  END_FINALLY      
            342_0  COME_FROM           338  '338'
              342  POP_BLOCK        
              344  BEGIN_FINALLY    
            346_0  COME_FROM           266  '266'
            346_1  COME_FROM           152  '152'
            346_2  COME_FROM_FINALLY     8  '8'

 L.  44       346  SETUP_FINALLY       360  'to 360'

 L.  45       348  LOAD_FAST                'cursor'
              350  LOAD_METHOD              close
              352  CALL_METHOD_0         0  ''
              354  POP_TOP          
              356  POP_BLOCK        
              358  JUMP_FORWARD        462  'to 462'
            360_0  COME_FROM_FINALLY   346  '346'

 L.  46       360  DUP_TOP          
              362  LOAD_GLOBAL              pymysql
              364  LOAD_ATTR                MySQLError
              366  COMPARE_OP               exception-match
          368_370  POP_JUMP_IF_FALSE   410  'to 410'
              372  POP_TOP          
              374  STORE_FAST               'e'
              376  POP_TOP          
              378  SETUP_FINALLY       398  'to 398'

 L.  47       380  LOAD_GLOBAL              logger
              382  LOAD_METHOD              error
              384  LOAD_STR                 '关闭cursor出错: '
              386  LOAD_FAST                'e'
              388  BINARY_ADD       
              390  CALL_METHOD_1         1  ''
              392  POP_TOP          
              394  POP_BLOCK        
              396  BEGIN_FINALLY    
            398_0  COME_FROM_FINALLY   378  '378'
              398  LOAD_CONST               None
              400  STORE_FAST               'e'
              402  DELETE_FAST              'e'
              404  END_FINALLY      
              406  POP_EXCEPT       
              408  JUMP_FORWARD        462  'to 462'
            410_0  COME_FROM           368  '368'

 L.  48       410  DUP_TOP          
              412  LOAD_GLOBAL              pymysql
              414  LOAD_ATTR                OperationalError
              416  COMPARE_OP               exception-match
          418_420  POP_JUMP_IF_FALSE   460  'to 460'
              422  POP_TOP          
              424  STORE_FAST               'e'
              426  POP_TOP          
              428  SETUP_FINALLY       448  'to 448'

 L.  49       430  LOAD_GLOBAL              logger
              432  LOAD_METHOD              error
              434  LOAD_STR                 '关闭cursor出错: '
              436  LOAD_FAST                'e'
              438  BINARY_ADD       
              440  CALL_METHOD_1         1  ''
              442  POP_TOP          
              444  POP_BLOCK        
              446  BEGIN_FINALLY    
            448_0  COME_FROM_FINALLY   428  '428'
              448  LOAD_CONST               None
              450  STORE_FAST               'e'
              452  DELETE_FAST              'e'
              454  END_FINALLY      
              456  POP_EXCEPT       
              458  JUMP_FORWARD        462  'to 462'
            460_0  COME_FROM           418  '418'
              460  END_FINALLY      
            462_0  COME_FROM           458  '458'
            462_1  COME_FROM           408  '408'
            462_2  COME_FROM           358  '358'

 L.  50       462  SETUP_FINALLY       476  'to 476'

 L.  51       464  LOAD_FAST                'conn'
              466  LOAD_METHOD              close
              468  CALL_METHOD_0         0  ''
              470  POP_TOP          
              472  POP_BLOCK        
              474  JUMP_FORWARD        578  'to 578'
            476_0  COME_FROM_FINALLY   462  '462'

 L.  52       476  DUP_TOP          
              478  LOAD_GLOBAL              pymysql
              480  LOAD_ATTR                MySQLError
              482  COMPARE_OP               exception-match
          484_486  POP_JUMP_IF_FALSE   526  'to 526'
              488  POP_TOP          
              490  STORE_FAST               'e'
              492  POP_TOP          
              494  SETUP_FINALLY       514  'to 514'

 L.  53       496  LOAD_GLOBAL              logger
              498  LOAD_METHOD              error
              500  LOAD_STR                 '关闭数据库连接出错: '
              502  LOAD_FAST                'e'
              504  BINARY_ADD       
              506  CALL_METHOD_1         1  ''
              508  POP_TOP          
              510  POP_BLOCK        
              512  BEGIN_FINALLY    
            514_0  COME_FROM_FINALLY   494  '494'
              514  LOAD_CONST               None
              516  STORE_FAST               'e'
              518  DELETE_FAST              'e'
              520  END_FINALLY      
              522  POP_EXCEPT       
              524  JUMP_FORWARD        578  'to 578'
            526_0  COME_FROM           484  '484'

 L.  54       526  DUP_TOP          
              528  LOAD_GLOBAL              pymysql
              530  LOAD_ATTR                OperationalError
              532  COMPARE_OP               exception-match
          534_536  POP_JUMP_IF_FALSE   576  'to 576'
              538  POP_TOP          
              540  STORE_FAST               'e'
              542  POP_TOP          
              544  SETUP_FINALLY       564  'to 564'

 L.  55       546  LOAD_GLOBAL              logger
              548  LOAD_METHOD              error
              550  LOAD_STR                 '关闭数据库连接出错: '
              552  LOAD_FAST                'e'
              554  BINARY_ADD       
              556  CALL_METHOD_1         1  ''
              558  POP_TOP          
              560  POP_BLOCK        
              562  BEGIN_FINALLY    
            564_0  COME_FROM_FINALLY   544  '544'
              564  LOAD_CONST               None
              566  STORE_FAST               'e'
              568  DELETE_FAST              'e'
              570  END_FINALLY      
              572  POP_EXCEPT       
              574  JUMP_FORWARD        578  'to 578'
            576_0  COME_FROM           534  '534'
              576  END_FINALLY      
            578_0  COME_FROM           574  '574'
            578_1  COME_FROM           524  '524'
            578_2  COME_FROM           474  '474'
              578  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 150


def queryfrommysql--- This code section failed: ---

 L.  66         0  LOAD_FAST                'conn'
                2  LOAD_METHOD              cursor
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'cursor'

 L.  67      8_10  SETUP_FINALLY       324  'to 324'
               12  SETUP_FINALLY       248  'to 248'

 L.  68        14  LOAD_GLOBAL              logger
               16  LOAD_ATTR                info
               18  LOAD_STR                 '\n数据库执行SQL: '
               20  LOAD_FAST                'sql'
               22  BINARY_ADD       
               24  LOAD_CONST               True
               26  LOAD_CONST               True
               28  LOAD_CONST               ('html', 'also_console')
               30  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               32  POP_TOP          

 L.  69        34  LOAD_FAST                'cursor'
               36  LOAD_METHOD              execute
               38  LOAD_FAST                'sql'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'count'

 L.  71        44  LOAD_FAST                'cursor'
               46  LOAD_METHOD              fetchall
               48  CALL_METHOD_0         0  ''
               50  STORE_FAST               'result'

 L.  72        52  BUILD_LIST_0          0 
               54  STORE_FAST               'fields_list'

 L.  73        56  LOAD_FAST                'cursor'
               58  LOAD_ATTR                description
               60  GET_ITER         
               62  FOR_ITER             82  'to 82'
               64  STORE_FAST               'field'

 L.  75        66  LOAD_FAST                'fields_list'
               68  LOAD_METHOD              append
               70  LOAD_FAST                'field'
               72  LOAD_CONST               0
               74  BINARY_SUBSCR    
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
               80  JUMP_BACK            62  'to 62'

 L.  76        82  LOAD_FAST                'conn'
               84  LOAD_METHOD              commit
               86  CALL_METHOD_0         0  ''
               88  POP_TOP          

 L.  77        90  LOAD_FAST                'result'
               92  LOAD_CONST               None
               94  COMPARE_OP               is
               96  POP_JUMP_IF_TRUE    110  'to 110'
               98  LOAD_GLOBAL              len
              100  LOAD_FAST                'result'
              102  CALL_FUNCTION_1       1  ''
              104  LOAD_CONST               0
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   136  'to 136'
            110_0  COME_FROM            96  '96'

 L.  78       110  LOAD_GLOBAL              logger
              112  LOAD_ATTR                info
              114  LOAD_STR                 '数据库返回结果: None'
              116  LOAD_CONST               True
              118  LOAD_CONST               True
              120  LOAD_CONST               ('html', 'also_console')
              122  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              124  POP_TOP          

 L.  79       126  POP_BLOCK        
              128  POP_BLOCK        
              130  CALL_FINALLY        324  'to 324'
              132  LOAD_CONST               None
              134  RETURN_VALUE     
            136_0  COME_FROM           108  '108'

 L.  80       136  BUILD_LIST_0          0 
              138  STORE_FAST               'result_list'

 L.  81       140  LOAD_GLOBAL              range
              142  LOAD_GLOBAL              len
              144  LOAD_FAST                'result'
              146  CALL_FUNCTION_1       1  ''
              148  CALL_FUNCTION_1       1  ''
              150  GET_ITER         
              152  FOR_ITER            214  'to 214'
              154  STORE_FAST               'i'

 L.  82       156  BUILD_MAP_0           0 
              158  STORE_FAST               'row_dict'

 L.  83       160  LOAD_FAST                'result'
              162  LOAD_FAST                'i'
              164  BINARY_SUBSCR    
              166  STORE_FAST               'row'

 L.  84       168  LOAD_GLOBAL              range
              170  LOAD_GLOBAL              len
              172  LOAD_FAST                'row'
              174  CALL_FUNCTION_1       1  ''
              176  CALL_FUNCTION_1       1  ''
              178  GET_ITER         
              180  FOR_ITER            202  'to 202'
              182  STORE_FAST               'j'

 L.  85       184  LOAD_FAST                'row'
              186  LOAD_FAST                'j'
              188  BINARY_SUBSCR    
              190  LOAD_FAST                'row_dict'
              192  LOAD_FAST                'fields_list'
              194  LOAD_FAST                'j'
              196  BINARY_SUBSCR    
              198  STORE_SUBSCR     
              200  JUMP_BACK           180  'to 180'

 L.  86       202  LOAD_FAST                'result_list'
              204  LOAD_METHOD              append
              206  LOAD_FAST                'row_dict'
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          
              212  JUMP_BACK           152  'to 152'

 L.  87       214  LOAD_GLOBAL              logger
              216  LOAD_ATTR                info
              218  LOAD_STR                 '数据库返回结果: '
              220  LOAD_GLOBAL              str
              222  LOAD_FAST                'result_list'
              224  CALL_FUNCTION_1       1  ''
              226  BINARY_ADD       
              228  LOAD_CONST               True
              230  LOAD_CONST               True
              232  LOAD_CONST               ('html', 'also_console')
              234  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              236  POP_TOP          

 L.  88       238  LOAD_FAST                'result_list'
              240  POP_BLOCK        
              242  POP_BLOCK        
              244  CALL_FINALLY        324  'to 324'
              246  RETURN_VALUE     
            248_0  COME_FROM_FINALLY    12  '12'

 L.  89       248  DUP_TOP          
              250  LOAD_GLOBAL              pymysql
              252  LOAD_ATTR                MySQLError
              254  COMPARE_OP               exception-match
          256_258  POP_JUMP_IF_FALSE   318  'to 318'
              260  POP_TOP          
              262  STORE_FAST               'e'
              264  POP_TOP          
              266  SETUP_FINALLY       306  'to 306'

 L.  90       268  LOAD_FAST                'conn'
              270  LOAD_METHOD              rollback
              272  CALL_METHOD_0         0  ''
              274  POP_TOP          

 L.  91       276  LOAD_GLOBAL              logger
              278  LOAD_METHOD              error
              280  LOAD_STR                 '数据库错误: '
              282  LOAD_FAST                'e'
              284  BINARY_ADD       
              286  CALL_METHOD_1         1  ''
              288  POP_TOP          

 L.  92       290  LOAD_GLOBAL              AssertionError
              292  LOAD_STR                 '数据库错误: '
              294  LOAD_FAST                'e'
              296  BINARY_ADD       
              298  CALL_FUNCTION_1       1  ''
              300  RAISE_VARARGS_1       1  ''
              302  POP_BLOCK        
              304  BEGIN_FINALLY    
            306_0  COME_FROM_FINALLY   266  '266'
              306  LOAD_CONST               None
              308  STORE_FAST               'e'
              310  DELETE_FAST              'e'
              312  END_FINALLY      
              314  POP_EXCEPT       
              316  JUMP_FORWARD        320  'to 320'
            318_0  COME_FROM           256  '256'
              318  END_FINALLY      
            320_0  COME_FROM           316  '316'
              320  POP_BLOCK        
              322  BEGIN_FINALLY    
            324_0  COME_FROM           244  '244'
            324_1  COME_FROM           130  '130'
            324_2  COME_FROM_FINALLY     8  '8'

 L.  95       324  SETUP_FINALLY       338  'to 338'

 L.  96       326  LOAD_FAST                'cursor'
              328  LOAD_METHOD              close
              330  CALL_METHOD_0         0  ''
              332  POP_TOP          
              334  POP_BLOCK        
              336  JUMP_FORWARD        440  'to 440'
            338_0  COME_FROM_FINALLY   324  '324'

 L.  97       338  DUP_TOP          
              340  LOAD_GLOBAL              pymysql
              342  LOAD_ATTR                MySQLError
              344  COMPARE_OP               exception-match
          346_348  POP_JUMP_IF_FALSE   388  'to 388'
              350  POP_TOP          
              352  STORE_FAST               'e'
              354  POP_TOP          
              356  SETUP_FINALLY       376  'to 376'

 L.  98       358  LOAD_GLOBAL              logger
              360  LOAD_METHOD              error
              362  LOAD_STR                 '关闭cursor出错: '
              364  LOAD_FAST                'e'
              366  BINARY_ADD       
              368  CALL_METHOD_1         1  ''
              370  POP_TOP          
              372  POP_BLOCK        
              374  BEGIN_FINALLY    
            376_0  COME_FROM_FINALLY   356  '356'
              376  LOAD_CONST               None
              378  STORE_FAST               'e'
              380  DELETE_FAST              'e'
              382  END_FINALLY      
              384  POP_EXCEPT       
              386  JUMP_FORWARD        440  'to 440'
            388_0  COME_FROM           346  '346'

 L.  99       388  DUP_TOP          
              390  LOAD_GLOBAL              pymysql
              392  LOAD_ATTR                OperationalError
              394  COMPARE_OP               exception-match
          396_398  POP_JUMP_IF_FALSE   438  'to 438'
              400  POP_TOP          
              402  STORE_FAST               'e'
              404  POP_TOP          
              406  SETUP_FINALLY       426  'to 426'

 L. 100       408  LOAD_GLOBAL              logger
              410  LOAD_METHOD              error
              412  LOAD_STR                 '关闭cursor出错: '
              414  LOAD_FAST                'e'
              416  BINARY_ADD       
              418  CALL_METHOD_1         1  ''
              420  POP_TOP          
              422  POP_BLOCK        
              424  BEGIN_FINALLY    
            426_0  COME_FROM_FINALLY   406  '406'
              426  LOAD_CONST               None
              428  STORE_FAST               'e'
              430  DELETE_FAST              'e'
              432  END_FINALLY      
              434  POP_EXCEPT       
              436  JUMP_FORWARD        440  'to 440'
            438_0  COME_FROM           396  '396'
              438  END_FINALLY      
            440_0  COME_FROM           436  '436'
            440_1  COME_FROM           386  '386'
            440_2  COME_FROM           336  '336'

 L. 101       440  SETUP_FINALLY       454  'to 454'

 L. 102       442  LOAD_FAST                'conn'
              444  LOAD_METHOD              close
              446  CALL_METHOD_0         0  ''
              448  POP_TOP          
              450  POP_BLOCK        
              452  JUMP_FORWARD        556  'to 556'
            454_0  COME_FROM_FINALLY   440  '440'

 L. 103       454  DUP_TOP          
              456  LOAD_GLOBAL              pymysql
              458  LOAD_ATTR                MySQLError
              460  COMPARE_OP               exception-match
          462_464  POP_JUMP_IF_FALSE   504  'to 504'
              466  POP_TOP          
              468  STORE_FAST               'e'
              470  POP_TOP          
              472  SETUP_FINALLY       492  'to 492'

 L. 104       474  LOAD_GLOBAL              logger
              476  LOAD_METHOD              error
              478  LOAD_STR                 '关闭数据库连接出错: '
              480  LOAD_FAST                'e'
              482  BINARY_ADD       
              484  CALL_METHOD_1         1  ''
              486  POP_TOP          
              488  POP_BLOCK        
              490  BEGIN_FINALLY    
            492_0  COME_FROM_FINALLY   472  '472'
              492  LOAD_CONST               None
              494  STORE_FAST               'e'
              496  DELETE_FAST              'e'
              498  END_FINALLY      
              500  POP_EXCEPT       
              502  JUMP_FORWARD        556  'to 556'
            504_0  COME_FROM           462  '462'

 L. 105       504  DUP_TOP          
              506  LOAD_GLOBAL              pymysql
              508  LOAD_ATTR                OperationalError
              510  COMPARE_OP               exception-match
          512_514  POP_JUMP_IF_FALSE   554  'to 554'
              516  POP_TOP          
              518  STORE_FAST               'e'
              520  POP_TOP          
              522  SETUP_FINALLY       542  'to 542'

 L. 106       524  LOAD_GLOBAL              logger
              526  LOAD_METHOD              error
              528  LOAD_STR                 '关闭数据库连接出错: '
              530  LOAD_FAST                'e'
              532  BINARY_ADD       
              534  CALL_METHOD_1         1  ''
              536  POP_TOP          
              538  POP_BLOCK        
              540  BEGIN_FINALLY    
            542_0  COME_FROM_FINALLY   522  '522'
              542  LOAD_CONST               None
              544  STORE_FAST               'e'
              546  DELETE_FAST              'e'
              548  END_FINALLY      
              550  POP_EXCEPT       
              552  JUMP_FORWARD        556  'to 556'
            554_0  COME_FROM           512  '512'
              554  END_FINALLY      
            556_0  COME_FROM           552  '552'
            556_1  COME_FROM           502  '502'
            556_2  COME_FROM           452  '452'
              556  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 128


def excutemysql--- This code section failed: ---

 L. 115         0  LOAD_FAST                'conn'
                2  LOAD_METHOD              cursor
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'cursor'

 L. 116         8  SETUP_FINALLY       158  'to 158'
               10  SETUP_FINALLY        84  'to 84'

 L. 117        12  LOAD_GLOBAL              logger
               14  LOAD_ATTR                info
               16  LOAD_STR                 '\n数据库执行SQL: '
               18  LOAD_FAST                'sql'
               20  BINARY_ADD       
               22  LOAD_CONST               True
               24  LOAD_CONST               True
               26  LOAD_CONST               ('html', 'also_console')
               28  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               30  POP_TOP          

 L. 118        32  LOAD_FAST                'cursor'
               34  LOAD_METHOD              execute
               36  LOAD_FAST                'sql'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'count'

 L. 119        42  LOAD_GLOBAL              logger
               44  LOAD_ATTR                info
               46  LOAD_STR                 '被影响的行数: '
               48  LOAD_GLOBAL              str
               50  LOAD_FAST                'count'
               52  CALL_FUNCTION_1       1  ''
               54  BINARY_ADD       
               56  LOAD_CONST               True
               58  LOAD_CONST               True
               60  LOAD_CONST               ('html', 'also_console')
               62  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               64  POP_TOP          

 L. 120        66  LOAD_FAST                'conn'
               68  LOAD_METHOD              commit
               70  CALL_METHOD_0         0  ''
               72  POP_TOP          

 L. 121        74  LOAD_FAST                'count'
               76  POP_BLOCK        
               78  POP_BLOCK        
               80  CALL_FINALLY        158  'to 158'
               82  RETURN_VALUE     
             84_0  COME_FROM_FINALLY    10  '10'

 L. 122        84  DUP_TOP          
               86  LOAD_GLOBAL              pymysql
               88  LOAD_ATTR                MySQLError
               90  COMPARE_OP               exception-match
               92  POP_JUMP_IF_FALSE   152  'to 152'
               94  POP_TOP          
               96  STORE_FAST               'e'
               98  POP_TOP          
              100  SETUP_FINALLY       140  'to 140'

 L. 123       102  LOAD_FAST                'conn'
              104  LOAD_METHOD              rollback
              106  CALL_METHOD_0         0  ''
              108  POP_TOP          

 L. 124       110  LOAD_GLOBAL              logger
              112  LOAD_METHOD              error
              114  LOAD_STR                 '数据库错误: '
              116  LOAD_FAST                'e'
              118  BINARY_ADD       
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          

 L. 125       124  LOAD_GLOBAL              AssertionError
              126  LOAD_STR                 '数据库错误: '
              128  LOAD_FAST                'e'
              130  BINARY_ADD       
              132  CALL_FUNCTION_1       1  ''
              134  RAISE_VARARGS_1       1  ''
              136  POP_BLOCK        
              138  BEGIN_FINALLY    
            140_0  COME_FROM_FINALLY   100  '100'
              140  LOAD_CONST               None
              142  STORE_FAST               'e'
              144  DELETE_FAST              'e'
              146  END_FINALLY      
              148  POP_EXCEPT       
              150  JUMP_FORWARD        154  'to 154'
            152_0  COME_FROM            92  '92'
              152  END_FINALLY      
            154_0  COME_FROM           150  '150'
              154  POP_BLOCK        
              156  BEGIN_FINALLY    
            158_0  COME_FROM            80  '80'
            158_1  COME_FROM_FINALLY     8  '8'

 L. 128       158  SETUP_FINALLY       172  'to 172'

 L. 129       160  LOAD_FAST                'cursor'
              162  LOAD_METHOD              close
              164  CALL_METHOD_0         0  ''
              166  POP_TOP          
              168  POP_BLOCK        
              170  JUMP_FORWARD        272  'to 272'
            172_0  COME_FROM_FINALLY   158  '158'

 L. 130       172  DUP_TOP          
              174  LOAD_GLOBAL              pymysql
              176  LOAD_ATTR                MySQLError
              178  COMPARE_OP               exception-match
              180  POP_JUMP_IF_FALSE   220  'to 220'
              182  POP_TOP          
              184  STORE_FAST               'e'
              186  POP_TOP          
              188  SETUP_FINALLY       208  'to 208'

 L. 131       190  LOAD_GLOBAL              logger
              192  LOAD_METHOD              error
              194  LOAD_STR                 '关闭cursor出错: '
              196  LOAD_FAST                'e'
              198  BINARY_ADD       
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          
              204  POP_BLOCK        
              206  BEGIN_FINALLY    
            208_0  COME_FROM_FINALLY   188  '188'
              208  LOAD_CONST               None
              210  STORE_FAST               'e'
              212  DELETE_FAST              'e'
              214  END_FINALLY      
              216  POP_EXCEPT       
              218  JUMP_FORWARD        272  'to 272'
            220_0  COME_FROM           180  '180'

 L. 132       220  DUP_TOP          
              222  LOAD_GLOBAL              pymysql
              224  LOAD_ATTR                OperationalError
              226  COMPARE_OP               exception-match
          228_230  POP_JUMP_IF_FALSE   270  'to 270'
              232  POP_TOP          
              234  STORE_FAST               'e'
              236  POP_TOP          
              238  SETUP_FINALLY       258  'to 258'

 L. 133       240  LOAD_GLOBAL              logger
              242  LOAD_METHOD              error
              244  LOAD_STR                 '关闭cursor出错: '
              246  LOAD_FAST                'e'
              248  BINARY_ADD       
              250  CALL_METHOD_1         1  ''
              252  POP_TOP          
              254  POP_BLOCK        
              256  BEGIN_FINALLY    
            258_0  COME_FROM_FINALLY   238  '238'
              258  LOAD_CONST               None
              260  STORE_FAST               'e'
              262  DELETE_FAST              'e'
              264  END_FINALLY      
              266  POP_EXCEPT       
              268  JUMP_FORWARD        272  'to 272'
            270_0  COME_FROM           228  '228'
              270  END_FINALLY      
            272_0  COME_FROM           268  '268'
            272_1  COME_FROM           218  '218'
            272_2  COME_FROM           170  '170'

 L. 134       272  SETUP_FINALLY       286  'to 286'

 L. 135       274  LOAD_FAST                'conn'
              276  LOAD_METHOD              close
              278  CALL_METHOD_0         0  ''
              280  POP_TOP          
              282  POP_BLOCK        
              284  JUMP_FORWARD        388  'to 388'
            286_0  COME_FROM_FINALLY   272  '272'

 L. 136       286  DUP_TOP          
              288  LOAD_GLOBAL              pymysql
              290  LOAD_ATTR                MySQLError
              292  COMPARE_OP               exception-match
          294_296  POP_JUMP_IF_FALSE   336  'to 336'
              298  POP_TOP          
              300  STORE_FAST               'e'
              302  POP_TOP          
              304  SETUP_FINALLY       324  'to 324'

 L. 137       306  LOAD_GLOBAL              logger
              308  LOAD_METHOD              error
              310  LOAD_STR                 '关闭数据库连接出错: '
              312  LOAD_FAST                'e'
              314  BINARY_ADD       
              316  CALL_METHOD_1         1  ''
              318  POP_TOP          
              320  POP_BLOCK        
              322  BEGIN_FINALLY    
            324_0  COME_FROM_FINALLY   304  '304'
              324  LOAD_CONST               None
              326  STORE_FAST               'e'
              328  DELETE_FAST              'e'
              330  END_FINALLY      
              332  POP_EXCEPT       
              334  JUMP_FORWARD        388  'to 388'
            336_0  COME_FROM           294  '294'

 L. 138       336  DUP_TOP          
              338  LOAD_GLOBAL              pymysql
              340  LOAD_ATTR                OperationalError
              342  COMPARE_OP               exception-match
          344_346  POP_JUMP_IF_FALSE   386  'to 386'
              348  POP_TOP          
              350  STORE_FAST               'e'
              352  POP_TOP          
              354  SETUP_FINALLY       374  'to 374'

 L. 139       356  LOAD_GLOBAL              logger
              358  LOAD_METHOD              error
              360  LOAD_STR                 '关闭数据库连接出错: '
              362  LOAD_FAST                'e'
              364  BINARY_ADD       
              366  CALL_METHOD_1         1  ''
              368  POP_TOP          
              370  POP_BLOCK        
              372  BEGIN_FINALLY    
            374_0  COME_FROM_FINALLY   354  '354'
              374  LOAD_CONST               None
              376  STORE_FAST               'e'
              378  DELETE_FAST              'e'
              380  END_FINALLY      
              382  POP_EXCEPT       
              384  JUMP_FORWARD        388  'to 388'
            386_0  COME_FROM           344  '344'
              386  END_FINALLY      
            388_0  COME_FROM           384  '384'
            388_1  COME_FROM           334  '334'
            388_2  COME_FROM           284  '284'
              388  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 76