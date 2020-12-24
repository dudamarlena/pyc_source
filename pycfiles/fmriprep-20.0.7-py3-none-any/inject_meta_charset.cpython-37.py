# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_vendor/html5lib/filters/inject_meta_charset.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 2945 bytes
from __future__ import absolute_import, division, unicode_literals
from . import base

class Filter(base.Filter):
    __doc__ = 'Injects ``<meta charset=ENCODING>`` tag into head of document'

    def __init__(self, source, encoding):
        """Creates a Filter

        :arg source: the source token stream

        :arg encoding: the encoding to set

        """
        base.Filter.__init__(self, source)
        self.encoding = encoding

    def __iter__--- This code section failed: ---

 L.  20         0  LOAD_STR                 'pre_head'
                2  STORE_FAST               'state'

 L.  21         4  LOAD_FAST                'self'
                6  LOAD_ATTR                encoding
                8  LOAD_CONST               None
               10  COMPARE_OP               is
               12  STORE_FAST               'meta_found'

 L.  22        14  BUILD_LIST_0          0 
               16  STORE_FAST               'pending'

 L.  24     18_20  SETUP_LOOP          474  'to 474'
               22  LOAD_GLOBAL              base
               24  LOAD_ATTR                Filter
               26  LOAD_METHOD              __iter__
               28  LOAD_FAST                'self'
               30  CALL_METHOD_1         1  '1 positional argument'
               32  GET_ITER         
            34_36  FOR_ITER            472  'to 472'
               38  STORE_FAST               'token'

 L.  25        40  LOAD_FAST                'token'
               42  LOAD_STR                 'type'
               44  BINARY_SUBSCR    
               46  STORE_FAST               'type'

 L.  26        48  LOAD_FAST                'type'
               50  LOAD_STR                 'StartTag'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    80  'to 80'

 L.  27        56  LOAD_FAST                'token'
               58  LOAD_STR                 'name'
               60  BINARY_SUBSCR    
               62  LOAD_METHOD              lower
               64  CALL_METHOD_0         0  '0 positional arguments'
               66  LOAD_STR                 'head'
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE    76  'to 76'

 L.  28        72  LOAD_STR                 'in_head'
               74  STORE_FAST               'state'
             76_0  COME_FROM            70  '70'
            76_78  JUMP_FORWARD        442  'to 442'
             80_0  COME_FROM            54  '54'

 L.  30        80  LOAD_FAST                'type'
               82  LOAD_STR                 'EmptyTag'
               84  COMPARE_OP               ==
            86_88  POP_JUMP_IF_FALSE   336  'to 336'

 L.  31        90  LOAD_FAST                'token'
               92  LOAD_STR                 'name'
               94  BINARY_SUBSCR    
               96  LOAD_METHOD              lower
               98  CALL_METHOD_0         0  '0 positional arguments'
              100  LOAD_STR                 'meta'
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   254  'to 254'

 L.  33       106  LOAD_CONST               False
              108  STORE_FAST               'has_http_equiv_content_type'

 L.  34       110  SETUP_LOOP          334  'to 334'
              112  LOAD_FAST                'token'
              114  LOAD_STR                 'data'
              116  BINARY_SUBSCR    
              118  LOAD_METHOD              items
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  GET_ITER         
            124_0  COME_FROM           204  '204'
            124_1  COME_FROM           192  '192'
              124  FOR_ITER            212  'to 212'
              126  UNPACK_SEQUENCE_2     2 
              128  UNPACK_SEQUENCE_2     2 
              130  STORE_FAST               'namespace'
              132  STORE_FAST               'name'
              134  STORE_FAST               'value'

 L.  35       136  LOAD_FAST                'namespace'
              138  LOAD_CONST               None
              140  COMPARE_OP               is-not
              142  POP_JUMP_IF_FALSE   148  'to 148'

 L.  36       144  CONTINUE            124  'to 124'
              146  JUMP_BACK           124  'to 124'
            148_0  COME_FROM           142  '142'

 L.  37       148  LOAD_FAST                'name'
              150  LOAD_METHOD              lower
              152  CALL_METHOD_0         0  '0 positional arguments'
              154  LOAD_STR                 'charset'
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   186  'to 186'

 L.  38       160  LOAD_FAST                'self'
              162  LOAD_ATTR                encoding
              164  LOAD_FAST                'token'
              166  LOAD_STR                 'data'
              168  BINARY_SUBSCR    
              170  LOAD_FAST                'namespace'
              172  LOAD_FAST                'name'
              174  BUILD_TUPLE_2         2 
              176  STORE_SUBSCR     

 L.  39       178  LOAD_CONST               True
              180  STORE_FAST               'meta_found'

 L.  40       182  BREAK_LOOP       
              184  JUMP_BACK           124  'to 124'
            186_0  COME_FROM           158  '158'

 L.  41       186  LOAD_FAST                'name'
              188  LOAD_STR                 'http-equiv'
              190  COMPARE_OP               ==
              192  POP_JUMP_IF_FALSE   124  'to 124'
              194  LOAD_FAST                'value'
              196  LOAD_METHOD              lower
              198  CALL_METHOD_0         0  '0 positional arguments'
              200  LOAD_STR                 'content-type'
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_FALSE   124  'to 124'

 L.  42       206  LOAD_CONST               True
              208  STORE_FAST               'has_http_equiv_content_type'
              210  JUMP_BACK           124  'to 124'
              212  POP_BLOCK        

 L.  44       214  LOAD_FAST                'has_http_equiv_content_type'
              216  POP_JUMP_IF_FALSE   252  'to 252'
              218  LOAD_CONST               (None, 'content')
              220  LOAD_FAST                'token'
              222  LOAD_STR                 'data'
              224  BINARY_SUBSCR    
              226  COMPARE_OP               in
              228  POP_JUMP_IF_FALSE   252  'to 252'

 L.  45       230  LOAD_STR                 'text/html; charset=%s'
              232  LOAD_FAST                'self'
              234  LOAD_ATTR                encoding
              236  BINARY_MODULO    
              238  LOAD_FAST                'token'
              240  LOAD_STR                 'data'
              242  BINARY_SUBSCR    
              244  LOAD_CONST               (None, 'content')
              246  STORE_SUBSCR     

 L.  46       248  LOAD_CONST               True
              250  STORE_FAST               'meta_found'
            252_0  COME_FROM           228  '228'
            252_1  COME_FROM           216  '216'
              252  JUMP_FORWARD        334  'to 334'
            254_0  COME_FROM           104  '104'

 L.  48       254  LOAD_FAST                'token'
              256  LOAD_STR                 'name'
              258  BINARY_SUBSCR    
              260  LOAD_METHOD              lower
              262  CALL_METHOD_0         0  '0 positional arguments'
              264  LOAD_STR                 'head'
              266  COMPARE_OP               ==
          268_270  POP_JUMP_IF_FALSE   442  'to 442'
              272  LOAD_FAST                'meta_found'
          274_276  POP_JUMP_IF_TRUE    442  'to 442'

 L.  50       278  LOAD_STR                 'StartTag'
              280  LOAD_STR                 'head'

 L.  51       282  LOAD_FAST                'token'
              284  LOAD_STR                 'data'
              286  BINARY_SUBSCR    
              288  LOAD_CONST               ('type', 'name', 'data')
              290  BUILD_CONST_KEY_MAP_3     3 
              292  YIELD_VALUE      
              294  POP_TOP          

 L.  52       296  LOAD_STR                 'EmptyTag'
              298  LOAD_STR                 'meta'

 L.  53       300  LOAD_CONST               (None, 'charset')
              302  LOAD_FAST                'self'
              304  LOAD_ATTR                encoding
              306  BUILD_MAP_1           1 
              308  LOAD_CONST               ('type', 'name', 'data')
              310  BUILD_CONST_KEY_MAP_3     3 
              312  YIELD_VALUE      
              314  POP_TOP          

 L.  54       316  LOAD_STR                 'EndTag'
              318  LOAD_STR                 'head'
              320  LOAD_CONST               ('type', 'name')
              322  BUILD_CONST_KEY_MAP_2     2 
              324  YIELD_VALUE      
              326  POP_TOP          

 L.  55       328  LOAD_CONST               True
              330  STORE_FAST               'meta_found'

 L.  56       332  CONTINUE             34  'to 34'
            334_0  COME_FROM           252  '252'
            334_1  COME_FROM_LOOP      110  '110'
              334  JUMP_FORWARD        442  'to 442'
            336_0  COME_FROM            86  '86'

 L.  58       336  LOAD_FAST                'type'
              338  LOAD_STR                 'EndTag'
              340  COMPARE_OP               ==
          342_344  POP_JUMP_IF_FALSE   442  'to 442'

 L.  59       346  LOAD_FAST                'token'
              348  LOAD_STR                 'name'
              350  BINARY_SUBSCR    
              352  LOAD_METHOD              lower
              354  CALL_METHOD_0         0  '0 positional arguments'
              356  LOAD_STR                 'head'
              358  COMPARE_OP               ==
          360_362  POP_JUMP_IF_FALSE   442  'to 442'
              364  LOAD_FAST                'pending'
          366_368  POP_JUMP_IF_FALSE   442  'to 442'

 L.  61       370  LOAD_FAST                'pending'
              372  LOAD_METHOD              pop
              374  LOAD_CONST               0
              376  CALL_METHOD_1         1  '1 positional argument'
              378  YIELD_VALUE      
              380  POP_TOP          

 L.  62       382  LOAD_FAST                'meta_found'
          384_386  POP_JUMP_IF_TRUE    408  'to 408'

 L.  63       388  LOAD_STR                 'EmptyTag'
              390  LOAD_STR                 'meta'

 L.  64       392  LOAD_CONST               (None, 'charset')
              394  LOAD_FAST                'self'
              396  LOAD_ATTR                encoding
              398  BUILD_MAP_1           1 
              400  LOAD_CONST               ('type', 'name', 'data')
              402  BUILD_CONST_KEY_MAP_3     3 
              404  YIELD_VALUE      
              406  POP_TOP          
            408_0  COME_FROM           384  '384'

 L.  65       408  SETUP_LOOP          434  'to 434'
              410  LOAD_FAST                'pending'
          412_414  POP_JUMP_IF_FALSE   432  'to 432'

 L.  66       416  LOAD_FAST                'pending'
              418  LOAD_METHOD              pop
              420  LOAD_CONST               0
              422  CALL_METHOD_1         1  '1 positional argument'
              424  YIELD_VALUE      
              426  POP_TOP          
          428_430  JUMP_BACK           410  'to 410'
            432_0  COME_FROM           412  '412'
              432  POP_BLOCK        
            434_0  COME_FROM_LOOP      408  '408'

 L.  67       434  LOAD_CONST               True
              436  STORE_FAST               'meta_found'

 L.  68       438  LOAD_STR                 'post_head'
              440  STORE_FAST               'state'
            442_0  COME_FROM           366  '366'
            442_1  COME_FROM           360  '360'
            442_2  COME_FROM           342  '342'
            442_3  COME_FROM           334  '334'
            442_4  COME_FROM           274  '274'
            442_5  COME_FROM           268  '268'
            442_6  COME_FROM            76  '76'

 L.  70       442  LOAD_FAST                'state'
              444  LOAD_STR                 'in_head'
              446  COMPARE_OP               ==
          448_450  POP_JUMP_IF_FALSE   464  'to 464'

 L.  71       452  LOAD_FAST                'pending'
              454  LOAD_METHOD              append
              456  LOAD_FAST                'token'
              458  CALL_METHOD_1         1  '1 positional argument'
              460  POP_TOP          
              462  JUMP_BACK            34  'to 34'
            464_0  COME_FROM           448  '448'

 L.  73       464  LOAD_FAST                'token'
              466  YIELD_VALUE      
              468  POP_TOP          
              470  JUMP_BACK            34  'to 34'
              472  POP_BLOCK        
            474_0  COME_FROM_LOOP       18  '18'

Parse error at or near `COME_FROM_LOOP' instruction at offset 334_1