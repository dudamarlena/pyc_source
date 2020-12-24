# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_cache.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 4461 bytes
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import unittest, time, jittor as jt
from jittor import LOG
import math, numpy as np
from .test_core import expect_error
from .test_fused_op import retry

def check_cache_code--- This code section failed: ---

 L.  22         0  LOAD_CONST               True
                2  STORE_FAST               'check_code'

 L.  23         4  LOAD_CONST               -1
                6  STORE_FAST               'error_line_num'

 L.  24         8  LOAD_GLOBAL              open
               10  LOAD_FAST                'fname'
               12  CALL_FUNCTION_1       1  '1 positional argument'
            14_16  SETUP_WITH          546  'to 546'
               18  STORE_FAST               'f'

 L.  25        20  LOAD_FAST                'f'
               22  LOAD_METHOD              readlines
               24  CALL_METHOD_0         0  '0 positional arguments'
               26  STORE_FAST               'lines'

 L.  26     28_30  SETUP_LOOP          542  'to 542'
               32  LOAD_GLOBAL              range
               34  LOAD_GLOBAL              len
               36  LOAD_FAST                'lines'
               38  CALL_FUNCTION_1       1  '1 positional argument'
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  GET_ITER         
             44_0  COME_FROM           534  '534'
            44_46  FOR_ITER            540  'to 540'
               48  STORE_FAST               'i'

 L.  27        50  LOAD_STR                 'memory_checker->check_hit('
               52  LOAD_FAST                'lines'
               54  LOAD_FAST                'i'
               56  BINARY_SUBSCR    
               58  COMPARE_OP               in
               60  POP_JUMP_IF_FALSE    64  'to 64'

 L.  28        62  CONTINUE             44  'to 44'
             64_0  COME_FROM            60  '60'

 L.  29        64  LOAD_FAST                'lines'
               66  LOAD_FAST                'i'
               68  BINARY_SUBSCR    
               70  STORE_FAST               'code'

 L.  30        72  BUILD_LIST_0          0 
               74  STORE_FAST               'address_pos'

 L.  31     76_78  SETUP_LOOP          532  'to 532'
               80  LOAD_GLOBAL              range
               82  LOAD_GLOBAL              len
               84  LOAD_FAST                'code'
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  CALL_FUNCTION_1       1  '1 positional argument'
               90  GET_ITER         
             92_0  COME_FROM           516  '516'
             92_1  COME_FROM           130  '130'
            92_94  FOR_ITER            530  'to 530'
               96  STORE_FAST               'j'

 L.  32        98  LOAD_FAST                'code'
              100  LOAD_FAST                'j'
              102  BINARY_SUBSCR    
              104  LOAD_STR                 '['
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   120  'to 120'

 L.  33       110  LOAD_FAST                'address_pos'
              112  LOAD_METHOD              append
              114  LOAD_FAST                'j'
              116  CALL_METHOD_1         1  '1 positional argument'
              118  POP_TOP          
            120_0  COME_FROM           108  '108'

 L.  34       120  LOAD_FAST                'code'
              122  LOAD_FAST                'j'
              124  BINARY_SUBSCR    
              126  LOAD_STR                 ']'
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE    92  'to 92'

 L.  35       132  LOAD_FAST                'address_pos'
              134  LOAD_CONST               -1
              136  BINARY_SUBSCR    
              138  LOAD_CONST               1
              140  BINARY_SUBTRACT  
              142  STORE_FAST               'sp'

 L.  36       144  LOAD_FAST                'address_pos'
              146  LOAD_CONST               None
              148  LOAD_CONST               -1
              150  BUILD_SLICE_2         2 
              152  BINARY_SUBSCR    
              154  STORE_FAST               'address_pos'

 L.  37       156  LOAD_FAST                'sp'
              158  LOAD_CONST               4
              160  COMPARE_OP               >=
              162  POP_JUMP_IF_FALSE   190  'to 190'
              164  LOAD_FAST                'code'
              166  LOAD_FAST                'sp'
              168  LOAD_CONST               4
              170  BINARY_SUBTRACT  
              172  LOAD_FAST                'sp'
              174  LOAD_CONST               1
              176  BINARY_ADD       
              178  BUILD_SLICE_2         2 
              180  BINARY_SUBSCR    
              182  LOAD_STR                 'shape'
              184  COMPARE_OP               ==
              186  POP_JUMP_IF_FALSE   190  'to 190'

 L.  38       188  CONTINUE             92  'to 92'
            190_0  COME_FROM           186  '186'
            190_1  COME_FROM           162  '162'

 L.  39       190  SETUP_LOOP          418  'to 418'
              192  LOAD_FAST                'sp'
              194  LOAD_CONST               0
              196  COMPARE_OP               >=
          198_200  POP_JUMP_IF_FALSE   416  'to 416'
              202  LOAD_FAST                'code'
              204  LOAD_FAST                'sp'
              206  BINARY_SUBSCR    
              208  LOAD_STR                 'A'
              210  COMPARE_OP               >=
              212  POP_JUMP_IF_FALSE   228  'to 228'
              214  LOAD_FAST                'code'
              216  LOAD_FAST                'sp'
              218  BINARY_SUBSCR    
              220  LOAD_STR                 'Z'
              222  COMPARE_OP               <=
          224_226  POP_JUMP_IF_TRUE    354  'to 354'
            228_0  COME_FROM           212  '212'
              228  LOAD_FAST                'code'
              230  LOAD_FAST                'sp'
              232  BINARY_SUBSCR    
              234  LOAD_STR                 'a'
              236  COMPARE_OP               >=
          238_240  POP_JUMP_IF_FALSE   256  'to 256'
              242  LOAD_FAST                'code'
              244  LOAD_FAST                'sp'
              246  BINARY_SUBSCR    
              248  LOAD_STR                 'z'
              250  COMPARE_OP               <=
          252_254  POP_JUMP_IF_TRUE    354  'to 354'
            256_0  COME_FROM           238  '238'

 L.  40       256  LOAD_FAST                'code'
              258  LOAD_FAST                'sp'
              260  BINARY_SUBSCR    
              262  LOAD_STR                 '0'
              264  COMPARE_OP               >=
          266_268  POP_JUMP_IF_FALSE   284  'to 284'
              270  LOAD_FAST                'code'
              272  LOAD_FAST                'sp'
              274  BINARY_SUBSCR    
              276  LOAD_STR                 '9'
              278  COMPARE_OP               <=
          280_282  POP_JUMP_IF_TRUE    354  'to 354'
            284_0  COME_FROM           266  '266'
              284  LOAD_FAST                'code'
              286  LOAD_FAST                'sp'
              288  BINARY_SUBSCR    
              290  LOAD_STR                 '_'
              292  COMPARE_OP               ==
          294_296  POP_JUMP_IF_TRUE    354  'to 354'
              298  LOAD_FAST                'code'
              300  LOAD_FAST                'sp'
              302  BINARY_SUBSCR    
              304  LOAD_STR                 '.'
              306  COMPARE_OP               ==
          308_310  POP_JUMP_IF_TRUE    354  'to 354'
              312  LOAD_FAST                'sp'
              314  LOAD_CONST               0
              316  COMPARE_OP               >
          318_320  POP_JUMP_IF_FALSE   416  'to 416'
              322  LOAD_FAST                'code'
              324  LOAD_FAST                'sp'
              326  BINARY_SUBSCR    
              328  LOAD_STR                 '>'
              330  COMPARE_OP               ==
          332_334  POP_JUMP_IF_FALSE   416  'to 416'
              336  LOAD_FAST                'code'
              338  LOAD_FAST                'sp'
              340  LOAD_CONST               1
              342  BINARY_SUBTRACT  
              344  BINARY_SUBSCR    
              346  LOAD_STR                 '-'
              348  COMPARE_OP               ==
          350_352  POP_JUMP_IF_FALSE   416  'to 416'
            354_0  COME_FROM           308  '308'
            354_1  COME_FROM           294  '294'
            354_2  COME_FROM           280  '280'
            354_3  COME_FROM           252  '252'
            354_4  COME_FROM           224  '224'

 L.  41       354  LOAD_FAST                'sp'
              356  LOAD_CONST               0
              358  COMPARE_OP               >
          360_362  POP_JUMP_IF_FALSE   406  'to 406'
              364  LOAD_FAST                'code'
              366  LOAD_FAST                'sp'
              368  BINARY_SUBSCR    
              370  LOAD_STR                 '>'
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   406  'to 406'
              378  LOAD_FAST                'code'
              380  LOAD_FAST                'sp'
              382  LOAD_CONST               1
              384  BINARY_SUBTRACT  
              386  BINARY_SUBSCR    
              388  LOAD_STR                 '-'
              390  COMPARE_OP               ==
          392_394  POP_JUMP_IF_FALSE   406  'to 406'

 L.  42       396  LOAD_FAST                'sp'
              398  LOAD_CONST               2
              400  INPLACE_SUBTRACT 
              402  STORE_FAST               'sp'
              404  JUMP_BACK           192  'to 192'
            406_0  COME_FROM           392  '392'
            406_1  COME_FROM           374  '374'
            406_2  COME_FROM           360  '360'

 L.  44       406  LOAD_FAST                'sp'
              408  LOAD_CONST               1
              410  INPLACE_SUBTRACT 
              412  STORE_FAST               'sp'
              414  JUMP_BACK           192  'to 192'
            416_0  COME_FROM           350  '350'
            416_1  COME_FROM           332  '332'
            416_2  COME_FROM           318  '318'
            416_3  COME_FROM           198  '198'
              416  POP_BLOCK        
            418_0  COME_FROM_LOOP      190  '190'

 L.  45       418  LOAD_FAST                'sp'
              420  LOAD_CONST               1
              422  INPLACE_ADD      
              424  STORE_FAST               'sp'

 L.  46       426  LOAD_FAST                'code'
              428  LOAD_FAST                'sp'
              430  LOAD_FAST                'j'
              432  LOAD_CONST               1
              434  BINARY_ADD       
              436  BUILD_SLICE_2         2 
              438  BINARY_SUBSCR    
              440  STORE_FAST               'check_var'

 L.  47       442  LOAD_FAST                'i'
              444  LOAD_CONST               1
              446  BINARY_SUBTRACT  
              448  STORE_FAST               'temp_i'

 L.  48       450  LOAD_CONST               False
              452  STORE_FAST               'have_check'

 L.  49       454  SETUP_LOOP          514  'to 514'
              456  LOAD_FAST                'temp_i'
              458  LOAD_CONST               0
              460  COMPARE_OP               >=
          462_464  POP_JUMP_IF_FALSE   512  'to 512'
              466  LOAD_STR                 'memory_checker->check_hit('
              468  LOAD_FAST                'lines'
              470  LOAD_FAST                'temp_i'
              472  BINARY_SUBSCR    
              474  COMPARE_OP               in
          476_478  POP_JUMP_IF_FALSE   512  'to 512'

 L.  50       480  LOAD_FAST                'check_var'
              482  LOAD_FAST                'lines'
              484  LOAD_FAST                'temp_i'
              486  BINARY_SUBSCR    
              488  COMPARE_OP               in
          490_492  POP_JUMP_IF_FALSE   500  'to 500'

 L.  51       494  LOAD_CONST               True
              496  STORE_FAST               'have_check'

 L.  52       498  BREAK_LOOP       
            500_0  COME_FROM           490  '490'

 L.  53       500  LOAD_FAST                'temp_i'
              502  LOAD_CONST               1
              504  INPLACE_SUBTRACT 
              506  STORE_FAST               'temp_i'
          508_510  JUMP_BACK           456  'to 456'
            512_0  COME_FROM           476  '476'
            512_1  COME_FROM           462  '462'
              512  POP_BLOCK        
            514_0  COME_FROM_LOOP      454  '454'

 L.  54       514  LOAD_FAST                'have_check'
              516  POP_JUMP_IF_TRUE     92  'to 92'

 L.  55       518  LOAD_CONST               False
              520  STORE_FAST               'check_code'

 L.  56       522  LOAD_FAST                'i'
              524  STORE_FAST               'error_line_num'

 L.  57       526  BREAK_LOOP       
              528  JUMP_BACK            92  'to 92'
              530  POP_BLOCK        
            532_0  COME_FROM_LOOP       76  '76'

 L.  58       532  LOAD_FAST                'check_code'
              534  POP_JUMP_IF_TRUE     44  'to 44'

 L.  59       536  BREAK_LOOP       
              538  JUMP_BACK            44  'to 44'
              540  POP_BLOCK        
            542_0  COME_FROM_LOOP       28  '28'
              542  POP_BLOCK        
              544  LOAD_CONST               None
            546_0  COME_FROM_WITH       14  '14'
              546  WITH_CLEANUP_START
              548  WITH_CLEANUP_FINISH
              550  END_FINALLY      

 L.  60       552  LOAD_FAST                'check_code'
          554_556  POP_JUMP_IF_TRUE    582  'to 582'
              558  LOAD_ASSERT              AssertionError
              560  LOAD_STR                 'check cache not found in line '
              562  LOAD_GLOBAL              str
              564  LOAD_FAST                'error_line_num'
              566  CALL_FUNCTION_1       1  '1 positional argument'
              568  BINARY_ADD       
              570  LOAD_STR                 ' of file '
              572  BINARY_ADD       
              574  LOAD_FAST                'fname'
              576  BINARY_ADD       
              578  CALL_FUNCTION_1       1  '1 positional argument'
              580  RAISE_VARARGS_1       1  'exception instance'
            582_0  COME_FROM           554  '554'

Parse error at or near `POP_BLOCK' instruction at offset 416


class TestCache(unittest.TestCase):

    def test_reduce(self):

        @retry(10)
        def check(n, m, reduce_dim, cache_report_, error_rate_threshold):
            a = jt.random[n, m]
            a.sync()
            with jt.profile_scope(compile_options={'check_cache':1, 
             'replace_strategy':1,  'page_size':4096,  'vtop':0, 
             'tlb_size':64, 
             'tlb_ways':4,  'tlb_line_size':1,  'L1_size':32768, 
             'L1_ways':8,  'L1_line_size':64,  'L2_size':262144, 
             'L2_ways':8,  'L2_line_size':64,  'L3_size':15728640, 
             'L3_ways':20,  'L3_line_size':64},
              enable_tuner=0) as (report):
                c = a.sumreduce_dim
                c.sync()
            check_cache_code(report[1][1])
            cache_report = report[(-1)][-5:]
            for i in range(len(cache_report)):
                cache_report[i] = int(cache_report[i])

            for i in range(len(cache_report)):
                assert abs(cache_report[i] - cache_report_[i]) <= int(cache_report_[i] * error_rate_threshold), 'cache report error: ' + report[(-2)][(-(len(cache_report) - i))] + ' error, ' + str(cache_report[i]) + '!=' + str(cache_report_[i])

        error_threshold = 0.02
        check(100, 10000, 0, [3010004, 989, 125729, 63129, 63129], error_threshold)
        check(100, 10000, 1, [3000104, 981, 62510, 62510, 62510], error_threshold)
        check(10, 98765, 0, [3061719, 2034, 129645, 129645, 67905], error_threshold)
        check(10, 98765, 1, [2962964, 969, 61733, 61733, 61733], error_threshold)
        check(7779, 97, 0, [2263790, 740, 47170, 47170, 47170], error_threshold)
        check(7779, 97, 1, [2271472, 748, 47650, 47650, 47650], error_threshold)
        check(1024, 1024, 0, [3146756, 1029, 65603, 65603, 65603], error_threshold)
        check(1024, 1024, 1, [3146756, 1028, 65603, 65603, 65603], error_threshold)


if __name__ == '__main__':
    unittest.main()