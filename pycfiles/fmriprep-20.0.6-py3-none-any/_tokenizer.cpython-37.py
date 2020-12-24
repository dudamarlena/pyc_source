# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/pip/pip/_vendor/html5lib/_tokenizer.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 76580 bytes
from __future__ import absolute_import, division, unicode_literals
import pip._vendor.six as chr
from collections import deque
from .constants import spaceCharacters
from .constants import entities
from .constants import asciiLetters, asciiUpper2Lower
from .constants import digits, hexDigits, EOF
from .constants import tokenTypes, tagTokenTypes
from .constants import replacementCharacters
from ._inputstream import HTMLInputStream
from ._trie import Trie
entitiesTrie = Trie(entities)

class HTMLTokenizer(object):
    __doc__ = ' This class takes care of tokenizing HTML.\n\n    * self.currentToken\n      Holds the token that is currently being processed.\n\n    * self.state\n      Holds a reference to the method to be invoked... XXX\n\n    * self.stream\n      Points to HTMLInputStream object.\n    '

    def __init__(self, stream, parser=None, **kwargs):
        self.stream = HTMLInputStream(stream, **kwargs)
        self.parser = parser
        self.escapeFlag = False
        self.lastFourChars = []
        self.state = self.dataState
        self.escape = False
        self.currentToken = None
        super(HTMLTokenizer, self).__init__()

    def __iter__(self):
        """ This is where the magic happens.

        We do our usually processing through the states and when we have a token
        to return we yield the token which pauses processing until the next token
        is requested.
        """
        self.tokenQueue = deque([])
        while self.state():
            while self.stream.errors:
                yield {'type':tokenTypes['ParseError'],  'data':self.stream.errors.pop(0)}

            while self.tokenQueue:
                yield self.tokenQueue.popleft()

    def consumeNumberEntity--- This code section failed: ---

 L.  71         0  LOAD_GLOBAL              digits
                2  STORE_FAST               'allowed'

 L.  72         4  LOAD_CONST               10
                6  STORE_FAST               'radix'

 L.  73         8  LOAD_FAST                'isHex'
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L.  74        12  LOAD_GLOBAL              hexDigits
               14  STORE_FAST               'allowed'

 L.  75        16  LOAD_CONST               16
               18  STORE_FAST               'radix'
             20_0  COME_FROM            10  '10'

 L.  77        20  BUILD_LIST_0          0 
               22  STORE_FAST               'charStack'

 L.  81        24  LOAD_FAST                'self'
               26  LOAD_ATTR                stream
               28  LOAD_METHOD              char
               30  CALL_METHOD_0         0  '0 positional arguments'
               32  STORE_FAST               'c'

 L.  82        34  SETUP_LOOP           76  'to 76'
               36  LOAD_FAST                'c'
               38  LOAD_FAST                'allowed'
               40  COMPARE_OP               in
               42  POP_JUMP_IF_FALSE    74  'to 74'
               44  LOAD_FAST                'c'
               46  LOAD_GLOBAL              EOF
               48  COMPARE_OP               is-not
               50  POP_JUMP_IF_FALSE    74  'to 74'

 L.  83        52  LOAD_FAST                'charStack'
               54  LOAD_METHOD              append
               56  LOAD_FAST                'c'
               58  CALL_METHOD_1         1  '1 positional argument'
               60  POP_TOP          

 L.  84        62  LOAD_FAST                'self'
               64  LOAD_ATTR                stream
               66  LOAD_METHOD              char
               68  CALL_METHOD_0         0  '0 positional arguments'
               70  STORE_FAST               'c'
               72  JUMP_BACK            36  'to 36'
             74_0  COME_FROM            50  '50'
             74_1  COME_FROM            42  '42'
               74  POP_BLOCK        
             76_0  COME_FROM_LOOP       34  '34'

 L.  87        76  LOAD_GLOBAL              int
               78  LOAD_STR                 ''
               80  LOAD_METHOD              join
               82  LOAD_FAST                'charStack'
               84  CALL_METHOD_1         1  '1 positional argument'
               86  LOAD_FAST                'radix'
               88  CALL_FUNCTION_2       2  '2 positional arguments'
               90  STORE_FAST               'charAsInt'

 L.  90        92  LOAD_FAST                'charAsInt'
               94  LOAD_GLOBAL              replacementCharacters
               96  COMPARE_OP               in
               98  POP_JUMP_IF_FALSE   140  'to 140'

 L.  91       100  LOAD_GLOBAL              replacementCharacters
              102  LOAD_FAST                'charAsInt'
              104  BINARY_SUBSCR    
              106  STORE_FAST               'char'

 L.  92       108  LOAD_FAST                'self'
              110  LOAD_ATTR                tokenQueue
              112  LOAD_METHOD              append
              114  LOAD_GLOBAL              tokenTypes
              116  LOAD_STR                 'ParseError'
              118  BINARY_SUBSCR    

 L.  93       120  LOAD_STR                 'illegal-codepoint-for-numeric-entity'

 L.  94       122  LOAD_STR                 'charAsInt'
              124  LOAD_FAST                'charAsInt'
              126  BUILD_MAP_1           1 
              128  LOAD_CONST               ('type', 'data', 'datavars')
              130  BUILD_CONST_KEY_MAP_3     3 
              132  CALL_METHOD_1         1  '1 positional argument'
              134  POP_TOP          
          136_138  JUMP_FORWARD        494  'to 494'
            140_0  COME_FROM            98  '98'

 L.  95       140  LOAD_CONST               55296
              142  LOAD_FAST                'charAsInt'
              144  DUP_TOP          
              146  ROT_THREE        
              148  COMPARE_OP               <=
              150  POP_JUMP_IF_FALSE   160  'to 160'
              152  LOAD_CONST               57343
              154  COMPARE_OP               <=
              156  POP_JUMP_IF_TRUE    170  'to 170'
              158  JUMP_FORWARD        162  'to 162'
            160_0  COME_FROM           150  '150'
              160  POP_TOP          
            162_0  COME_FROM           158  '158'

 L.  96       162  LOAD_FAST                'charAsInt'
              164  LOAD_CONST               1114111
              166  COMPARE_OP               >
              168  POP_JUMP_IF_FALSE   206  'to 206'
            170_0  COME_FROM           156  '156'

 L.  97       170  LOAD_STR                 '�'
              172  STORE_FAST               'char'

 L.  98       174  LOAD_FAST                'self'
              176  LOAD_ATTR                tokenQueue
              178  LOAD_METHOD              append
              180  LOAD_GLOBAL              tokenTypes
              182  LOAD_STR                 'ParseError'
              184  BINARY_SUBSCR    

 L.  99       186  LOAD_STR                 'illegal-codepoint-for-numeric-entity'

 L. 100       188  LOAD_STR                 'charAsInt'
              190  LOAD_FAST                'charAsInt'
              192  BUILD_MAP_1           1 
              194  LOAD_CONST               ('type', 'data', 'datavars')
              196  BUILD_CONST_KEY_MAP_3     3 
              198  CALL_METHOD_1         1  '1 positional argument'
              200  POP_TOP          
          202_204  JUMP_FORWARD        494  'to 494'
            206_0  COME_FROM           168  '168'

 L. 103       206  LOAD_CONST               1
              208  LOAD_FAST                'charAsInt'
              210  DUP_TOP          
              212  ROT_THREE        
              214  COMPARE_OP               <=
              216  POP_JUMP_IF_FALSE   228  'to 228'
              218  LOAD_CONST               8
              220  COMPARE_OP               <=
          222_224  POP_JUMP_IF_TRUE    390  'to 390'
              226  JUMP_FORWARD        230  'to 230'
            228_0  COME_FROM           216  '216'
              228  POP_TOP          
            230_0  COME_FROM           226  '226'

 L. 104       230  LOAD_CONST               14
              232  LOAD_FAST                'charAsInt'
              234  DUP_TOP          
              236  ROT_THREE        
              238  COMPARE_OP               <=
              240  POP_JUMP_IF_FALSE   252  'to 252'
              242  LOAD_CONST               31
              244  COMPARE_OP               <=
          246_248  POP_JUMP_IF_TRUE    390  'to 390'
              250  JUMP_FORWARD        254  'to 254'
            252_0  COME_FROM           240  '240'
              252  POP_TOP          
            254_0  COME_FROM           250  '250'

 L. 105       254  LOAD_CONST               127
              256  LOAD_FAST                'charAsInt'
              258  DUP_TOP          
              260  ROT_THREE        
              262  COMPARE_OP               <=
          264_266  POP_JUMP_IF_FALSE   278  'to 278'
              268  LOAD_CONST               159
              270  COMPARE_OP               <=
          272_274  POP_JUMP_IF_TRUE    390  'to 390'
              276  JUMP_FORWARD        280  'to 280'
            278_0  COME_FROM           264  '264'
              278  POP_TOP          
            280_0  COME_FROM           276  '276'

 L. 106       280  LOAD_CONST               64976
              282  LOAD_FAST                'charAsInt'
              284  DUP_TOP          
              286  ROT_THREE        
              288  COMPARE_OP               <=
          290_292  POP_JUMP_IF_FALSE   304  'to 304'
              294  LOAD_CONST               65007
              296  COMPARE_OP               <=
          298_300  POP_JUMP_IF_TRUE    390  'to 390'
              302  JUMP_FORWARD        306  'to 306'
            304_0  COME_FROM           290  '290'
              304  POP_TOP          
            306_0  COME_FROM           302  '302'

 L. 107       306  LOAD_FAST                'charAsInt'
              308  LOAD_GLOBAL              frozenset
              310  LOAD_CONST               11
              312  LOAD_CONST               65534
              314  LOAD_CONST               65535
              316  LOAD_CONST               131070

 L. 108       318  LOAD_CONST               131071
              320  LOAD_CONST               196606
              322  LOAD_CONST               196607
              324  LOAD_CONST               262142

 L. 109       326  LOAD_CONST               262143
              328  LOAD_CONST               327678
              330  LOAD_CONST               327679
              332  LOAD_CONST               393214

 L. 110       334  LOAD_CONST               393215
              336  LOAD_CONST               458750
              338  LOAD_CONST               458751
              340  LOAD_CONST               524286

 L. 111       342  LOAD_CONST               524287
              344  LOAD_CONST               589822
              346  LOAD_CONST               589823
              348  LOAD_CONST               655358

 L. 112       350  LOAD_CONST               655359
              352  LOAD_CONST               720894
              354  LOAD_CONST               720895
              356  LOAD_CONST               786430

 L. 113       358  LOAD_CONST               786431
              360  LOAD_CONST               851966
              362  LOAD_CONST               851967
              364  LOAD_CONST               917502

 L. 114       366  LOAD_CONST               917503
              368  LOAD_CONST               983038
              370  LOAD_CONST               983039
              372  LOAD_CONST               1048574

 L. 115       374  LOAD_CONST               1048575
              376  LOAD_CONST               1114110
              378  LOAD_CONST               1114111
              380  BUILD_LIST_35        35 
              382  CALL_FUNCTION_1       1  '1 positional argument'
              384  COMPARE_OP               in
          386_388  POP_JUMP_IF_FALSE   418  'to 418'
            390_0  COME_FROM           298  '298'
            390_1  COME_FROM           272  '272'
            390_2  COME_FROM           246  '246'
            390_3  COME_FROM           222  '222'

 L. 116       390  LOAD_FAST                'self'
              392  LOAD_ATTR                tokenQueue
              394  LOAD_METHOD              append
              396  LOAD_GLOBAL              tokenTypes
              398  LOAD_STR                 'ParseError'
              400  BINARY_SUBSCR    

 L. 118       402  LOAD_STR                 'illegal-codepoint-for-numeric-entity'

 L. 119       404  LOAD_STR                 'charAsInt'
              406  LOAD_FAST                'charAsInt'
              408  BUILD_MAP_1           1 
              410  LOAD_CONST               ('type', 'data', 'datavars')
              412  BUILD_CONST_KEY_MAP_3     3 
              414  CALL_METHOD_1         1  '1 positional argument'
              416  POP_TOP          
            418_0  COME_FROM           386  '386'

 L. 120       418  SETUP_EXCEPT        432  'to 432'

 L. 123       420  LOAD_GLOBAL              chr
              422  LOAD_FAST                'charAsInt'
              424  CALL_FUNCTION_1       1  '1 positional argument'
              426  STORE_FAST               'char'
              428  POP_BLOCK        
              430  JUMP_FORWARD        494  'to 494'
            432_0  COME_FROM_EXCEPT    418  '418'

 L. 124       432  DUP_TOP          
              434  LOAD_GLOBAL              ValueError
              436  COMPARE_OP               exception-match
          438_440  POP_JUMP_IF_FALSE   492  'to 492'
              442  POP_TOP          
              444  POP_TOP          
              446  POP_TOP          

 L. 125       448  LOAD_FAST                'charAsInt'
              450  LOAD_CONST               65536
              452  BINARY_SUBTRACT  
              454  STORE_FAST               'v'

 L. 126       456  LOAD_GLOBAL              chr
              458  LOAD_CONST               55296
              460  LOAD_FAST                'v'
              462  LOAD_CONST               10
              464  BINARY_RSHIFT    
              466  BINARY_OR        
              468  CALL_FUNCTION_1       1  '1 positional argument'
              470  LOAD_GLOBAL              chr
              472  LOAD_CONST               56320
              474  LOAD_FAST                'v'
              476  LOAD_CONST               1023
              478  BINARY_AND       
              480  BINARY_OR        
              482  CALL_FUNCTION_1       1  '1 positional argument'
              484  BINARY_ADD       
              486  STORE_FAST               'char'
              488  POP_EXCEPT       
              490  JUMP_FORWARD        494  'to 494'
            492_0  COME_FROM           438  '438'
              492  END_FINALLY      
            494_0  COME_FROM           490  '490'
            494_1  COME_FROM           430  '430'
            494_2  COME_FROM           202  '202'
            494_3  COME_FROM           136  '136'

 L. 130       494  LOAD_FAST                'c'
              496  LOAD_STR                 ';'
              498  COMPARE_OP               !=
          500_502  POP_JUMP_IF_FALSE   538  'to 538'

 L. 131       504  LOAD_FAST                'self'
              506  LOAD_ATTR                tokenQueue
              508  LOAD_METHOD              append
              510  LOAD_GLOBAL              tokenTypes
              512  LOAD_STR                 'ParseError'
              514  BINARY_SUBSCR    

 L. 132       516  LOAD_STR                 'numeric-entity-without-semicolon'
              518  LOAD_CONST               ('type', 'data')
              520  BUILD_CONST_KEY_MAP_2     2 
              522  CALL_METHOD_1         1  '1 positional argument'
              524  POP_TOP          

 L. 133       526  LOAD_FAST                'self'
              528  LOAD_ATTR                stream
              530  LOAD_METHOD              unget
              532  LOAD_FAST                'c'
              534  CALL_METHOD_1         1  '1 positional argument'
              536  POP_TOP          
            538_0  COME_FROM           500  '500'

 L. 135       538  LOAD_FAST                'char'
              540  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 418_0

    def consumeEntity--- This code section failed: ---

 L. 139         0  LOAD_STR                 '&'
                2  STORE_FAST               'output'

 L. 141         4  LOAD_FAST                'self'
                6  LOAD_ATTR                stream
                8  LOAD_METHOD              char
               10  CALL_METHOD_0         0  '0 positional arguments'
               12  BUILD_LIST_1          1 
               14  STORE_FAST               'charStack'

 L. 142        16  LOAD_FAST                'charStack'
               18  LOAD_CONST               0
               20  BINARY_SUBSCR    
               22  LOAD_GLOBAL              spaceCharacters
               24  COMPARE_OP               in
               26  POP_JUMP_IF_TRUE     66  'to 66'
               28  LOAD_FAST                'charStack'
               30  LOAD_CONST               0
               32  BINARY_SUBSCR    
               34  LOAD_GLOBAL              EOF
               36  LOAD_STR                 '<'
               38  LOAD_STR                 '&'
               40  BUILD_TUPLE_3         3 
               42  COMPARE_OP               in
               44  POP_JUMP_IF_TRUE     66  'to 66'

 L. 143        46  LOAD_FAST                'allowedChar'
               48  LOAD_CONST               None
               50  COMPARE_OP               is-not
               52  POP_JUMP_IF_FALSE    86  'to 86'
               54  LOAD_FAST                'allowedChar'
               56  LOAD_FAST                'charStack'
               58  LOAD_CONST               0
               60  BINARY_SUBSCR    
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    86  'to 86'
             66_0  COME_FROM            44  '44'
             66_1  COME_FROM            26  '26'

 L. 144        66  LOAD_FAST                'self'
               68  LOAD_ATTR                stream
               70  LOAD_METHOD              unget
               72  LOAD_FAST                'charStack'
               74  LOAD_CONST               0
               76  BINARY_SUBSCR    
               78  CALL_METHOD_1         1  '1 positional argument'
               80  POP_TOP          
            82_84  JUMP_FORWARD        630  'to 630'
             86_0  COME_FROM            64  '64'
             86_1  COME_FROM            52  '52'

 L. 146        86  LOAD_FAST                'charStack'
               88  LOAD_CONST               0
               90  BINARY_SUBSCR    
               92  LOAD_STR                 '#'
               94  COMPARE_OP               ==
            96_98  POP_JUMP_IF_FALSE   268  'to 268'

 L. 148       100  LOAD_CONST               False
              102  STORE_FAST               'hex'

 L. 149       104  LOAD_FAST                'charStack'
              106  LOAD_METHOD              append
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                stream
              112  LOAD_METHOD              char
              114  CALL_METHOD_0         0  '0 positional arguments'
              116  CALL_METHOD_1         1  '1 positional argument'
              118  POP_TOP          

 L. 150       120  LOAD_FAST                'charStack'
              122  LOAD_CONST               -1
              124  BINARY_SUBSCR    
              126  LOAD_CONST               ('x', 'X')
              128  COMPARE_OP               in
              130  POP_JUMP_IF_FALSE   152  'to 152'

 L. 151       132  LOAD_CONST               True
              134  STORE_FAST               'hex'

 L. 152       136  LOAD_FAST                'charStack'
              138  LOAD_METHOD              append
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                stream
              144  LOAD_METHOD              char
              146  CALL_METHOD_0         0  '0 positional arguments'
              148  CALL_METHOD_1         1  '1 positional argument'
              150  POP_TOP          
            152_0  COME_FROM           130  '130'

 L. 155       152  LOAD_FAST                'hex'
              154  POP_JUMP_IF_FALSE   168  'to 168'
              156  LOAD_FAST                'charStack'
              158  LOAD_CONST               -1
              160  BINARY_SUBSCR    
              162  LOAD_GLOBAL              hexDigits
              164  COMPARE_OP               in
              166  POP_JUMP_IF_TRUE    184  'to 184'
            168_0  COME_FROM           154  '154'

 L. 156       168  LOAD_FAST                'hex'
              170  POP_JUMP_IF_TRUE    212  'to 212'
              172  LOAD_FAST                'charStack'
              174  LOAD_CONST               -1
              176  BINARY_SUBSCR    
              178  LOAD_GLOBAL              digits
              180  COMPARE_OP               in
              182  POP_JUMP_IF_FALSE   212  'to 212'
            184_0  COME_FROM           166  '166'

 L. 158       184  LOAD_FAST                'self'
              186  LOAD_ATTR                stream
              188  LOAD_METHOD              unget
              190  LOAD_FAST                'charStack'
              192  LOAD_CONST               -1
              194  BINARY_SUBSCR    
              196  CALL_METHOD_1         1  '1 positional argument'
              198  POP_TOP          

 L. 159       200  LOAD_FAST                'self'
              202  LOAD_METHOD              consumeNumberEntity
              204  LOAD_FAST                'hex'
              206  CALL_METHOD_1         1  '1 positional argument'
              208  STORE_FAST               'output'
              210  JUMP_FORWARD        630  'to 630'
            212_0  COME_FROM           182  '182'
            212_1  COME_FROM           170  '170'

 L. 162       212  LOAD_FAST                'self'
              214  LOAD_ATTR                tokenQueue
              216  LOAD_METHOD              append
              218  LOAD_GLOBAL              tokenTypes
              220  LOAD_STR                 'ParseError'
              222  BINARY_SUBSCR    

 L. 163       224  LOAD_STR                 'expected-numeric-entity'
              226  LOAD_CONST               ('type', 'data')
              228  BUILD_CONST_KEY_MAP_2     2 
              230  CALL_METHOD_1         1  '1 positional argument'
              232  POP_TOP          

 L. 164       234  LOAD_FAST                'self'
              236  LOAD_ATTR                stream
              238  LOAD_METHOD              unget
              240  LOAD_FAST                'charStack'
              242  LOAD_METHOD              pop
              244  CALL_METHOD_0         0  '0 positional arguments'
              246  CALL_METHOD_1         1  '1 positional argument'
              248  POP_TOP          

 L. 165       250  LOAD_STR                 '&'
              252  LOAD_STR                 ''
              254  LOAD_METHOD              join
              256  LOAD_FAST                'charStack'
              258  CALL_METHOD_1         1  '1 positional argument'
              260  BINARY_ADD       
              262  STORE_FAST               'output'
          264_266  JUMP_FORWARD        630  'to 630'
            268_0  COME_FROM            96  '96'

 L. 173       268  SETUP_LOOP          326  'to 326'
              270  LOAD_FAST                'charStack'
              272  LOAD_CONST               -1
              274  BINARY_SUBSCR    
              276  LOAD_GLOBAL              EOF
              278  COMPARE_OP               is-not
          280_282  POP_JUMP_IF_FALSE   324  'to 324'

 L. 174       284  LOAD_GLOBAL              entitiesTrie
              286  LOAD_METHOD              has_keys_with_prefix
              288  LOAD_STR                 ''
              290  LOAD_METHOD              join
              292  LOAD_FAST                'charStack'
              294  CALL_METHOD_1         1  '1 positional argument'
              296  CALL_METHOD_1         1  '1 positional argument'
          298_300  POP_JUMP_IF_TRUE    304  'to 304'

 L. 175       302  BREAK_LOOP       
            304_0  COME_FROM           298  '298'

 L. 176       304  LOAD_FAST                'charStack'
              306  LOAD_METHOD              append
              308  LOAD_FAST                'self'
              310  LOAD_ATTR                stream
              312  LOAD_METHOD              char
              314  CALL_METHOD_0         0  '0 positional arguments'
              316  CALL_METHOD_1         1  '1 positional argument'
              318  POP_TOP          
          320_322  JUMP_BACK           270  'to 270'
            324_0  COME_FROM           280  '280'
              324  POP_BLOCK        
            326_0  COME_FROM_LOOP      268  '268'

 L. 182       326  SETUP_EXCEPT        364  'to 364'

 L. 183       328  LOAD_GLOBAL              entitiesTrie
              330  LOAD_METHOD              longest_prefix
              332  LOAD_STR                 ''
              334  LOAD_METHOD              join
              336  LOAD_FAST                'charStack'
              338  LOAD_CONST               None
              340  LOAD_CONST               -1
              342  BUILD_SLICE_2         2 
              344  BINARY_SUBSCR    
              346  CALL_METHOD_1         1  '1 positional argument'
              348  CALL_METHOD_1         1  '1 positional argument'
              350  STORE_FAST               'entityName'

 L. 184       352  LOAD_GLOBAL              len
              354  LOAD_FAST                'entityName'
              356  CALL_FUNCTION_1       1  '1 positional argument'
              358  STORE_FAST               'entityLength'
              360  POP_BLOCK        
              362  JUMP_FORWARD        390  'to 390'
            364_0  COME_FROM_EXCEPT    326  '326'

 L. 185       364  DUP_TOP          
              366  LOAD_GLOBAL              KeyError
              368  COMPARE_OP               exception-match
          370_372  POP_JUMP_IF_FALSE   388  'to 388'
              374  POP_TOP          
              376  POP_TOP          
              378  POP_TOP          

 L. 186       380  LOAD_CONST               None
              382  STORE_FAST               'entityName'
              384  POP_EXCEPT       
              386  JUMP_FORWARD        390  'to 390'
            388_0  COME_FROM           370  '370'
              388  END_FINALLY      
            390_0  COME_FROM           386  '386'
            390_1  COME_FROM           362  '362'

 L. 188       390  LOAD_FAST                'entityName'
              392  LOAD_CONST               None
              394  COMPARE_OP               is-not
          396_398  POP_JUMP_IF_FALSE   578  'to 578'

 L. 189       400  LOAD_FAST                'entityName'
              402  LOAD_CONST               -1
              404  BINARY_SUBSCR    
              406  LOAD_STR                 ';'
              408  COMPARE_OP               !=
          410_412  POP_JUMP_IF_FALSE   436  'to 436'

 L. 190       414  LOAD_FAST                'self'
              416  LOAD_ATTR                tokenQueue
              418  LOAD_METHOD              append
              420  LOAD_GLOBAL              tokenTypes
              422  LOAD_STR                 'ParseError'
              424  BINARY_SUBSCR    

 L. 191       426  LOAD_STR                 'named-entity-without-semicolon'
              428  LOAD_CONST               ('type', 'data')
              430  BUILD_CONST_KEY_MAP_2     2 
              432  CALL_METHOD_1         1  '1 positional argument'
              434  POP_TOP          
            436_0  COME_FROM           410  '410'

 L. 192       436  LOAD_FAST                'entityName'
              438  LOAD_CONST               -1
              440  BINARY_SUBSCR    
              442  LOAD_STR                 ';'
              444  COMPARE_OP               !=
          446_448  POP_JUMP_IF_FALSE   530  'to 530'
              450  LOAD_FAST                'fromAttribute'
          452_454  POP_JUMP_IF_FALSE   530  'to 530'

 L. 193       456  LOAD_FAST                'charStack'
              458  LOAD_FAST                'entityLength'
              460  BINARY_SUBSCR    
              462  LOAD_GLOBAL              asciiLetters
              464  COMPARE_OP               in
          466_468  POP_JUMP_IF_TRUE    498  'to 498'

 L. 194       470  LOAD_FAST                'charStack'
              472  LOAD_FAST                'entityLength'
              474  BINARY_SUBSCR    
              476  LOAD_GLOBAL              digits
              478  COMPARE_OP               in
          480_482  POP_JUMP_IF_TRUE    498  'to 498'

 L. 195       484  LOAD_FAST                'charStack'
              486  LOAD_FAST                'entityLength'
              488  BINARY_SUBSCR    
              490  LOAD_STR                 '='
              492  COMPARE_OP               ==
          494_496  POP_JUMP_IF_FALSE   530  'to 530'
            498_0  COME_FROM           480  '480'
            498_1  COME_FROM           466  '466'

 L. 196       498  LOAD_FAST                'self'
              500  LOAD_ATTR                stream
              502  LOAD_METHOD              unget
              504  LOAD_FAST                'charStack'
              506  LOAD_METHOD              pop
              508  CALL_METHOD_0         0  '0 positional arguments'
              510  CALL_METHOD_1         1  '1 positional argument'
              512  POP_TOP          

 L. 197       514  LOAD_STR                 '&'
              516  LOAD_STR                 ''
              518  LOAD_METHOD              join
              520  LOAD_FAST                'charStack'
              522  CALL_METHOD_1         1  '1 positional argument'
              524  BINARY_ADD       
              526  STORE_FAST               'output'
              528  JUMP_FORWARD        576  'to 576'
            530_0  COME_FROM           494  '494'
            530_1  COME_FROM           452  '452'
            530_2  COME_FROM           446  '446'

 L. 199       530  LOAD_GLOBAL              entities
              532  LOAD_FAST                'entityName'
              534  BINARY_SUBSCR    
              536  STORE_FAST               'output'

 L. 200       538  LOAD_FAST                'self'
              540  LOAD_ATTR                stream
              542  LOAD_METHOD              unget
              544  LOAD_FAST                'charStack'
              546  LOAD_METHOD              pop
              548  CALL_METHOD_0         0  '0 positional arguments'
              550  CALL_METHOD_1         1  '1 positional argument'
              552  POP_TOP          

 L. 201       554  LOAD_FAST                'output'
              556  LOAD_STR                 ''
              558  LOAD_METHOD              join
              560  LOAD_FAST                'charStack'
              562  LOAD_FAST                'entityLength'
              564  LOAD_CONST               None
              566  BUILD_SLICE_2         2 
              568  BINARY_SUBSCR    
              570  CALL_METHOD_1         1  '1 positional argument'
              572  INPLACE_ADD      
            574_0  COME_FROM           210  '210'
              574  STORE_FAST               'output'
            576_0  COME_FROM           528  '528'
              576  JUMP_FORWARD        630  'to 630'
            578_0  COME_FROM           396  '396'

 L. 203       578  LOAD_FAST                'self'
              580  LOAD_ATTR                tokenQueue
              582  LOAD_METHOD              append
              584  LOAD_GLOBAL              tokenTypes
              586  LOAD_STR                 'ParseError'
              588  BINARY_SUBSCR    

 L. 204       590  LOAD_STR                 'expected-named-entity'
              592  LOAD_CONST               ('type', 'data')
              594  BUILD_CONST_KEY_MAP_2     2 
              596  CALL_METHOD_1         1  '1 positional argument'
              598  POP_TOP          

 L. 205       600  LOAD_FAST                'self'
              602  LOAD_ATTR                stream
              604  LOAD_METHOD              unget
              606  LOAD_FAST                'charStack'
              608  LOAD_METHOD              pop
              610  CALL_METHOD_0         0  '0 positional arguments'
              612  CALL_METHOD_1         1  '1 positional argument'
              614  POP_TOP          

 L. 206       616  LOAD_STR                 '&'
              618  LOAD_STR                 ''
              620  LOAD_METHOD              join
              622  LOAD_FAST                'charStack'
              624  CALL_METHOD_1         1  '1 positional argument'
              626  BINARY_ADD       
              628  STORE_FAST               'output'
            630_0  COME_FROM           576  '576'
            630_1  COME_FROM           264  '264'
            630_2  COME_FROM            82  '82'

 L. 208       630  LOAD_FAST                'fromAttribute'
          632_634  POP_JUMP_IF_FALSE   664  'to 664'

 L. 209       636  LOAD_FAST                'self'
              638  LOAD_ATTR                currentToken
              640  LOAD_STR                 'data'
              642  BINARY_SUBSCR    
              644  LOAD_CONST               -1
              646  BINARY_SUBSCR    
              648  LOAD_CONST               1
              650  DUP_TOP_TWO      
              652  BINARY_SUBSCR    
              654  LOAD_FAST                'output'
              656  INPLACE_ADD      
              658  ROT_THREE        
              660  STORE_SUBSCR     
              662  JUMP_FORWARD        706  'to 706'
            664_0  COME_FROM           632  '632'

 L. 211       664  LOAD_FAST                'output'
              666  LOAD_GLOBAL              spaceCharacters
              668  COMPARE_OP               in
          670_672  POP_JUMP_IF_FALSE   680  'to 680'

 L. 212       674  LOAD_STR                 'SpaceCharacters'
              676  STORE_FAST               'tokenType'
              678  JUMP_FORWARD        684  'to 684'
            680_0  COME_FROM           670  '670'

 L. 214       680  LOAD_STR                 'Characters'
              682  STORE_FAST               'tokenType'
            684_0  COME_FROM           678  '678'

 L. 215       684  LOAD_FAST                'self'
              686  LOAD_ATTR                tokenQueue
              688  LOAD_METHOD              append
              690  LOAD_GLOBAL              tokenTypes
              692  LOAD_FAST                'tokenType'
              694  BINARY_SUBSCR    
              696  LOAD_FAST                'output'
              698  LOAD_CONST               ('type', 'data')
              700  BUILD_CONST_KEY_MAP_2     2 
              702  CALL_METHOD_1         1  '1 positional argument'
              704  POP_TOP          
            706_0  COME_FROM           662  '662'

Parse error at or near `COME_FROM' instruction at offset 574_0

    def processEntityInAttribute(self, allowedChar):
        """This method replaces the need for "entityInAttributeValueState".
        """
        self.consumeEntity(allowedChar=allowedChar, fromAttribute=True)

    def emitCurrentToken(self):
        """This method is a generic handler for emitting the tags. It also sets
        the state to "data" because that's what's needed after a token has been
        emitted.
        """
        token = self.currentToken
        if token['type'] in tagTokenTypes:
            token['name'] = token['name'].translate(asciiUpper2Lower)
            if token['type'] == tokenTypes['EndTag']:
                if token['data']:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'attributes-in-end-tag'})
                if token['selfClosing']:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'self-closing-flag-on-end-tag'})
        self.tokenQueue.append(token)
        self.state = self.dataState

    def dataState(self):
        data = self.stream.char()
        if data == '&':
            self.state = self.entityDataState
        else:
            if data == '<':
                self.state = self.tagOpenState
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'\x00'})
                else:
                    if data is EOF:
                        return False
                    if data in spaceCharacters:
                        self.tokenQueue.append({'type':tokenTypes['SpaceCharacters'],  'data':data + self.stream.charsUntil(spaceCharacters, True)})
                    else:
                        chars = self.stream.charsUntil(('&', '<', '\x00'))
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data + chars})
        return True

    def entityDataState(self):
        self.consumeEntity()
        self.state = self.dataState
        return True

    def rcdataState(self):
        data = self.stream.char()
        if data == '&':
            self.state = self.characterReferenceInRcdata
        else:
            if data == '<':
                self.state = self.rcdataLessThanSignState
            else:
                if data == EOF:
                    return False
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
                else:
                    if data in spaceCharacters:
                        self.tokenQueue.append({'type':tokenTypes['SpaceCharacters'],  'data':data + self.stream.charsUntil(spaceCharacters, True)})
                    else:
                        chars = self.stream.charsUntil(('&', '<', '\x00'))
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data + chars})
        return True

    def characterReferenceInRcdata(self):
        self.consumeEntity()
        self.state = self.rcdataState
        return True

    def rawtextState(self):
        data = self.stream.char()
        if data == '<':
            self.state = self.rawtextLessThanSignState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
            else:
                if data == EOF:
                    return False
                chars = self.stream.charsUntil(('<', '\x00'))
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data + chars})
        return True

    def scriptDataState(self):
        data = self.stream.char()
        if data == '<':
            self.state = self.scriptDataLessThanSignState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
            else:
                if data == EOF:
                    return False
                chars = self.stream.charsUntil(('<', '\x00'))
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data + chars})
        return True

    def plaintextState(self):
        data = self.stream.char()
        if data == EOF:
            return False
        elif data == '\x00':
            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
        else:
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data + self.stream.charsUntil('\x00')})
        return True

    def tagOpenState(self):
        data = self.stream.char()
        if data == '!':
            self.state = self.markupDeclarationOpenState
        else:
            if data == '/':
                self.state = self.closeTagOpenState
            else:
                if data in asciiLetters:
                    self.currentToken = {'type':tokenTypes['StartTag'], 
                     'name':data, 
                     'data':[],  'selfClosing':False, 
                     'selfClosingAcknowledged':False}
                    self.state = self.tagNameState
                else:
                    if data == '>':
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-tag-name-but-got-right-bracket'})
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<>'})
                        self.state = self.dataState
                    else:
                        if data == '?':
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-tag-name-but-got-question-mark'})
                            self.stream.unget(data)
                            self.state = self.bogusCommentState
                        else:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-tag-name'})
                            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<'})
                            self.stream.unget(data)
                            self.state = self.dataState
        return True

    def closeTagOpenState(self):
        data = self.stream.char()
        if data in asciiLetters:
            self.currentToken = {'type':tokenTypes['EndTag'], 
             'name':data,  'data':[],  'selfClosing':False}
            self.state = self.tagNameState
        else:
            if data == '>':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-closing-tag-but-got-right-bracket'})
                self.state = self.dataState
            else:
                if data is EOF:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-closing-tag-but-got-eof'})
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</'})
                    self.state = self.dataState
                else:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-closing-tag-but-got-char', 
                     'datavars':{'data': data}})
                    self.stream.unget(data)
                    self.state = self.bogusCommentState
        return True

    def tagNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeAttributeNameState
        else:
            if data == '>':
                self.emitCurrentToken()
            else:
                if data is EOF:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-tag-name'})
                    self.state = self.dataState
                else:
                    if data == '/':
                        self.state = self.selfClosingStartTagState
                    else:
                        if data == '\x00':
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                            self.currentToken['name'] += '�'
                        else:
                            self.currentToken['name'] += data
        return True

    def rcdataLessThanSignState(self):
        data = self.stream.char()
        if data == '/':
            self.temporaryBuffer = ''
            self.state = self.rcdataEndTagOpenState
        else:
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<'})
            self.stream.unget(data)
            self.state = self.rcdataState
        return True

    def rcdataEndTagOpenState(self):
        data = self.stream.char()
        if data in asciiLetters:
            self.temporaryBuffer += data
            self.state = self.rcdataEndTagNameState
        else:
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</'})
            self.stream.unget(data)
            self.state = self.rcdataState
        return True

    def rcdataEndTagNameState(self):
        appropriate = self.currentToken and self.currentToken['name'].lower() == self.temporaryBuffer.lower()
        data = self.stream.char()
        if data in spaceCharacters and appropriate:
            self.currentToken = {'type':tokenTypes['EndTag'], 
             'name':self.temporaryBuffer, 
             'data':[],  'selfClosing':False}
            self.state = self.beforeAttributeNameState
        else:
            if data == '/' and appropriate:
                self.currentToken = {'type':tokenTypes['EndTag'], 
                 'name':self.temporaryBuffer, 
                 'data':[],  'selfClosing':False}
                self.state = self.selfClosingStartTagState
            else:
                if data == '>' and appropriate:
                    self.currentToken = {'type':tokenTypes['EndTag'], 
                     'name':self.temporaryBuffer, 
                     'data':[],  'selfClosing':False}
                    self.emitCurrentToken()
                    self.state = self.dataState
                else:
                    if data in asciiLetters:
                        self.temporaryBuffer += data
                    else:
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</' + self.temporaryBuffer})
                        self.stream.unget(data)
                        self.state = self.rcdataState
        return True

    def rawtextLessThanSignState(self):
        data = self.stream.char()
        if data == '/':
            self.temporaryBuffer = ''
            self.state = self.rawtextEndTagOpenState
        else:
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<'})
            self.stream.unget(data)
            self.state = self.rawtextState
        return True

    def rawtextEndTagOpenState(self):
        data = self.stream.char()
        if data in asciiLetters:
            self.temporaryBuffer += data
            self.state = self.rawtextEndTagNameState
        else:
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</'})
            self.stream.unget(data)
            self.state = self.rawtextState
        return True

    def rawtextEndTagNameState(self):
        appropriate = self.currentToken and self.currentToken['name'].lower() == self.temporaryBuffer.lower()
        data = self.stream.char()
        if data in spaceCharacters and appropriate:
            self.currentToken = {'type':tokenTypes['EndTag'], 
             'name':self.temporaryBuffer, 
             'data':[],  'selfClosing':False}
            self.state = self.beforeAttributeNameState
        else:
            if data == '/' and appropriate:
                self.currentToken = {'type':tokenTypes['EndTag'], 
                 'name':self.temporaryBuffer, 
                 'data':[],  'selfClosing':False}
                self.state = self.selfClosingStartTagState
            else:
                if data == '>' and appropriate:
                    self.currentToken = {'type':tokenTypes['EndTag'], 
                     'name':self.temporaryBuffer, 
                     'data':[],  'selfClosing':False}
                    self.emitCurrentToken()
                    self.state = self.dataState
                else:
                    if data in asciiLetters:
                        self.temporaryBuffer += data
                    else:
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</' + self.temporaryBuffer})
                        self.stream.unget(data)
                        self.state = self.rawtextState
        return True

    def scriptDataLessThanSignState(self):
        data = self.stream.char()
        if data == '/':
            self.temporaryBuffer = ''
            self.state = self.scriptDataEndTagOpenState
        else:
            if data == '!':
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<!'})
                self.state = self.scriptDataEscapeStartState
            else:
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<'})
                self.stream.unget(data)
                self.state = self.scriptDataState
        return True

    def scriptDataEndTagOpenState(self):
        data = self.stream.char()
        if data in asciiLetters:
            self.temporaryBuffer += data
            self.state = self.scriptDataEndTagNameState
        else:
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</'})
            self.stream.unget(data)
            self.state = self.scriptDataState
        return True

    def scriptDataEndTagNameState(self):
        appropriate = self.currentToken and self.currentToken['name'].lower() == self.temporaryBuffer.lower()
        data = self.stream.char()
        if data in spaceCharacters and appropriate:
            self.currentToken = {'type':tokenTypes['EndTag'], 
             'name':self.temporaryBuffer, 
             'data':[],  'selfClosing':False}
            self.state = self.beforeAttributeNameState
        else:
            if data == '/' and appropriate:
                self.currentToken = {'type':tokenTypes['EndTag'], 
                 'name':self.temporaryBuffer, 
                 'data':[],  'selfClosing':False}
                self.state = self.selfClosingStartTagState
            else:
                if data == '>' and appropriate:
                    self.currentToken = {'type':tokenTypes['EndTag'], 
                     'name':self.temporaryBuffer, 
                     'data':[],  'selfClosing':False}
                    self.emitCurrentToken()
                    self.state = self.dataState
                else:
                    if data in asciiLetters:
                        self.temporaryBuffer += data
                    else:
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</' + self.temporaryBuffer})
                        self.stream.unget(data)
                        self.state = self.scriptDataState
        return True

    def scriptDataEscapeStartState(self):
        data = self.stream.char()
        if data == '-':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'-'})
            self.state = self.scriptDataEscapeStartDashState
        else:
            self.stream.unget(data)
            self.state = self.scriptDataState
        return True

    def scriptDataEscapeStartDashState(self):
        data = self.stream.char()
        if data == '-':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'-'})
            self.state = self.scriptDataEscapedDashDashState
        else:
            self.stream.unget(data)
            self.state = self.scriptDataState
        return True

    def scriptDataEscapedState(self):
        data = self.stream.char()
        if data == '-':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'-'})
            self.state = self.scriptDataEscapedDashState
        else:
            if data == '<':
                self.state = self.scriptDataEscapedLessThanSignState
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
                else:
                    if data == EOF:
                        self.state = self.dataState
                    else:
                        chars = self.stream.charsUntil(('<', '-', '\x00'))
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data + chars})
        return True

    def scriptDataEscapedDashState(self):
        data = self.stream.char()
        if data == '-':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'-'})
            self.state = self.scriptDataEscapedDashDashState
        else:
            if data == '<':
                self.state = self.scriptDataEscapedLessThanSignState
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
                    self.state = self.scriptDataEscapedState
                else:
                    if data == EOF:
                        self.state = self.dataState
                    else:
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
                        self.state = self.scriptDataEscapedState
        return True

    def scriptDataEscapedDashDashState(self):
        data = self.stream.char()
        if data == '-':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'-'})
        else:
            if data == '<':
                self.state = self.scriptDataEscapedLessThanSignState
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'>'})
                    self.state = self.scriptDataState
                else:
                    if data == '\x00':
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
                        self.state = self.scriptDataEscapedState
                    else:
                        if data == EOF:
                            self.state = self.dataState
                        else:
                            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
                            self.state = self.scriptDataEscapedState
        return True

    def scriptDataEscapedLessThanSignState(self):
        data = self.stream.char()
        if data == '/':
            self.temporaryBuffer = ''
            self.state = self.scriptDataEscapedEndTagOpenState
        else:
            if data in asciiLetters:
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<' + data})
                self.temporaryBuffer = data
                self.state = self.scriptDataDoubleEscapeStartState
            else:
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<'})
                self.stream.unget(data)
                self.state = self.scriptDataEscapedState
        return True

    def scriptDataEscapedEndTagOpenState(self):
        data = self.stream.char()
        if data in asciiLetters:
            self.temporaryBuffer = data
            self.state = self.scriptDataEscapedEndTagNameState
        else:
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</'})
            self.stream.unget(data)
            self.state = self.scriptDataEscapedState
        return True

    def scriptDataEscapedEndTagNameState(self):
        appropriate = self.currentToken and self.currentToken['name'].lower() == self.temporaryBuffer.lower()
        data = self.stream.char()
        if data in spaceCharacters and appropriate:
            self.currentToken = {'type':tokenTypes['EndTag'], 
             'name':self.temporaryBuffer, 
             'data':[],  'selfClosing':False}
            self.state = self.beforeAttributeNameState
        else:
            if data == '/' and appropriate:
                self.currentToken = {'type':tokenTypes['EndTag'], 
                 'name':self.temporaryBuffer, 
                 'data':[],  'selfClosing':False}
                self.state = self.selfClosingStartTagState
            else:
                if data == '>' and appropriate:
                    self.currentToken = {'type':tokenTypes['EndTag'], 
                     'name':self.temporaryBuffer, 
                     'data':[],  'selfClosing':False}
                    self.emitCurrentToken()
                    self.state = self.dataState
                else:
                    if data in asciiLetters:
                        self.temporaryBuffer += data
                    else:
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</' + self.temporaryBuffer})
                        self.stream.unget(data)
                        self.state = self.scriptDataEscapedState
        return True

    def scriptDataDoubleEscapeStartState(self):
        data = self.stream.char()
        if data in spaceCharacters | frozenset(('/', '>')):
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
            if self.temporaryBuffer.lower() == 'script':
                self.state = self.scriptDataDoubleEscapedState
            else:
                self.state = self.scriptDataEscapedState
        elif data in asciiLetters:
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
            self.temporaryBuffer += data
        else:
            self.stream.unget(data)
            self.state = self.scriptDataEscapedState
        return True

    def scriptDataDoubleEscapedState(self):
        data = self.stream.char()
        if data == '-':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'-'})
            self.state = self.scriptDataDoubleEscapedDashState
        else:
            if data == '<':
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<'})
                self.state = self.scriptDataDoubleEscapedLessThanSignState
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
                else:
                    if data == EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-script-in-script'})
                        self.state = self.dataState
                    else:
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
        return True

    def scriptDataDoubleEscapedDashState(self):
        data = self.stream.char()
        if data == '-':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'-'})
            self.state = self.scriptDataDoubleEscapedDashDashState
        else:
            if data == '<':
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<'})
                self.state = self.scriptDataDoubleEscapedLessThanSignState
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
                    self.state = self.scriptDataDoubleEscapedState
                else:
                    if data == EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-script-in-script'})
                        self.state = self.dataState
                    else:
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
                        self.state = self.scriptDataDoubleEscapedState
        return True

    def scriptDataDoubleEscapedDashDashState(self):
        data = self.stream.char()
        if data == '-':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'-'})
        else:
            if data == '<':
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<'})
                self.state = self.scriptDataDoubleEscapedLessThanSignState
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'>'})
                    self.state = self.scriptDataState
                else:
                    if data == '\x00':
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
                        self.state = self.scriptDataDoubleEscapedState
                    else:
                        if data == EOF:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-script-in-script'})
                            self.state = self.dataState
                        else:
                            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
                            self.state = self.scriptDataDoubleEscapedState
        return True

    def scriptDataDoubleEscapedLessThanSignState(self):
        data = self.stream.char()
        if data == '/':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'/'})
            self.temporaryBuffer = ''
            self.state = self.scriptDataDoubleEscapeEndState
        else:
            self.stream.unget(data)
            self.state = self.scriptDataDoubleEscapedState
        return True

    def scriptDataDoubleEscapeEndState(self):
        data = self.stream.char()
        if data in spaceCharacters | frozenset(('/', '>')):
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
            if self.temporaryBuffer.lower() == 'script':
                self.state = self.scriptDataEscapedState
            else:
                self.state = self.scriptDataDoubleEscapedState
        elif data in asciiLetters:
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
            self.temporaryBuffer += data
        else:
            self.stream.unget(data)
            self.state = self.scriptDataDoubleEscapedState
        return True

    def beforeAttributeNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.stream.charsUntil(spaceCharacters, True)
        else:
            if data in asciiLetters:
                self.currentToken['data'].append([data, ''])
                self.state = self.attributeNameState
            else:
                if data == '>':
                    self.emitCurrentToken()
                else:
                    if data == '/':
                        self.state = self.selfClosingStartTagState
                    else:
                        if data in ("'", '"', '=', '<'):
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-character-in-attribute-name'})
                            self.currentToken['data'].append([data, ''])
                            self.state = self.attributeNameState
                        else:
                            if data == '\x00':
                                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                                self.currentToken['data'].append(['�', ''])
                                self.state = self.attributeNameState
                            else:
                                if data is EOF:
                                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-attribute-name-but-got-eof'})
                                    self.state = self.dataState
                                else:
                                    self.currentToken['data'].append([data, ''])
                                    self.state = self.attributeNameState
        return True

    def attributeNameState(self):
        data = self.stream.char()
        leavingThisState = True
        emitToken = False
        if data == '=':
            self.state = self.beforeAttributeValueState
        else:
            if data in asciiLetters:
                self.currentToken['data'][(-1)][0] += data + self.stream.charsUntil(asciiLetters, True)
                leavingThisState = False
            else:
                if data == '>':
                    emitToken = True
                else:
                    if data in spaceCharacters:
                        self.state = self.afterAttributeNameState
                    else:
                        if data == '/':
                            self.state = self.selfClosingStartTagState
                        else:
                            if data == '\x00':
                                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                                self.currentToken['data'][(-1)][0] += '�'
                                leavingThisState = False
                            else:
                                if data in ("'", '"', '<'):
                                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-character-in-attribute-name'})
                                    self.currentToken['data'][(-1)][0] += data
                                    leavingThisState = False
                                else:
                                    if data is EOF:
                                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-attribute-name'})
                                        self.state = self.dataState
                                    else:
                                        self.currentToken['data'][(-1)][0] += data
                                        leavingThisState = False
        if leavingThisState:
            self.currentToken['data'][(-1)][0] = self.currentToken['data'][(-1)][0].translate(asciiUpper2Lower)
            for name, _ in self.currentToken['data'][:-1]:
                if self.currentToken['data'][(-1)][0] == name:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'duplicate-attribute'})
                    break

            if emitToken:
                self.emitCurrentToken()
        return True

    def afterAttributeNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.stream.charsUntil(spaceCharacters, True)
        else:
            if data == '=':
                self.state = self.beforeAttributeValueState
            else:
                if data == '>':
                    self.emitCurrentToken()
                else:
                    if data in asciiLetters:
                        self.currentToken['data'].append([data, ''])
                        self.state = self.attributeNameState
                    else:
                        if data == '/':
                            self.state = self.selfClosingStartTagState
                        else:
                            if data == '\x00':
                                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                                self.currentToken['data'].append(['�', ''])
                                self.state = self.attributeNameState
                            else:
                                if data in ("'", '"', '<'):
                                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-character-after-attribute-name'})
                                    self.currentToken['data'].append([data, ''])
                                    self.state = self.attributeNameState
                                else:
                                    if data is EOF:
                                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-end-of-tag-but-got-eof'})
                                        self.state = self.dataState
                                    else:
                                        self.currentToken['data'].append([data, ''])
                                        self.state = self.attributeNameState
        return True

    def beforeAttributeValueState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.stream.charsUntil(spaceCharacters, True)
        else:
            if data == '"':
                self.state = self.attributeValueDoubleQuotedState
            else:
                if data == '&':
                    self.state = self.attributeValueUnQuotedState
                    self.stream.unget(data)
                else:
                    if data == "'":
                        self.state = self.attributeValueSingleQuotedState
                    else:
                        if data == '>':
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-attribute-value-but-got-right-bracket'})
                            self.emitCurrentToken()
                        else:
                            if data == '\x00':
                                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                                self.currentToken['data'][(-1)][1] += '�'
                                self.state = self.attributeValueUnQuotedState
                            else:
                                if data in ('=', '<', '`'):
                                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'equals-in-unquoted-attribute-value'})
                                    self.currentToken['data'][(-1)][1] += data
                                    self.state = self.attributeValueUnQuotedState
                                else:
                                    if data is EOF:
                                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-attribute-value-but-got-eof'})
                                        self.state = self.dataState
                                    else:
                                        self.currentToken['data'][(-1)][1] += data
                                        self.state = self.attributeValueUnQuotedState
        return True

    def attributeValueDoubleQuotedState(self):
        data = self.stream.char()
        if data == '"':
            self.state = self.afterAttributeValueState
        else:
            if data == '&':
                self.processEntityInAttribute('"')
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.currentToken['data'][(-1)][1] += '�'
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-attribute-value-double-quote'})
                        self.state = self.dataState
                    else:
                        self.currentToken['data'][(-1)][1] += data + self.stream.charsUntil(('"',
                                                                                             '&',
                                                                                             '\x00'))
        return True

    def attributeValueSingleQuotedState(self):
        data = self.stream.char()
        if data == "'":
            self.state = self.afterAttributeValueState
        else:
            if data == '&':
                self.processEntityInAttribute("'")
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.currentToken['data'][(-1)][1] += '�'
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-attribute-value-single-quote'})
                        self.state = self.dataState
                    else:
                        self.currentToken['data'][(-1)][1] += data + self.stream.charsUntil(("'",
                                                                                             '&',
                                                                                             '\x00'))
        return True

    def attributeValueUnQuotedState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeAttributeNameState
        else:
            if data == '&':
                self.processEntityInAttribute('>')
            else:
                if data == '>':
                    self.emitCurrentToken()
                else:
                    if data in ('"', "'", '=', '<', '`'):
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-character-in-unquoted-attribute-value'})
                        self.currentToken['data'][(-1)][1] += data
                    else:
                        if data == '\x00':
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                            self.currentToken['data'][(-1)][1] += '�'
                        else:
                            if data is EOF:
                                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-attribute-value-no-quotes'})
                                self.state = self.dataState
                            else:
                                self.currentToken['data'][(-1)][1] += data + self.stream.charsUntil(frozenset(('&',
                                                                                                               '>',
                                                                                                               '"',
                                                                                                               "'",
                                                                                                               '=',
                                                                                                               '<',
                                                                                                               '`',
                                                                                                               '\x00')) | spaceCharacters)
        return True

    def afterAttributeValueState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeAttributeNameState
        else:
            if data == '>':
                self.emitCurrentToken()
            else:
                if data == '/':
                    self.state = self.selfClosingStartTagState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-EOF-after-attribute-value'})
                        self.stream.unget(data)
                        self.state = self.dataState
                    else:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-character-after-attribute-value'})
                        self.stream.unget(data)
                        self.state = self.beforeAttributeNameState
        return True

    def selfClosingStartTagState(self):
        data = self.stream.char()
        if data == '>':
            self.currentToken['selfClosing'] = True
            self.emitCurrentToken()
        else:
            if data is EOF:
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-EOF-after-solidus-in-tag'})
                self.stream.unget(data)
                self.state = self.dataState
            else:
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-character-after-solidus-in-tag'})
                self.stream.unget(data)
                self.state = self.beforeAttributeNameState
        return True

    def bogusCommentState(self):
        data = self.stream.charsUntil('>')
        data = data.replace('\x00', '�')
        self.tokenQueue.append({'type':tokenTypes['Comment'], 
         'data':data})
        self.stream.char()
        self.state = self.dataState
        return True

    def markupDeclarationOpenState(self):
        charStack = [
         self.stream.char()]
        if charStack[(-1)] == '-':
            charStack.append(self.stream.char())
            if charStack[(-1)] == '-':
                self.currentToken = {'type':tokenTypes['Comment'], 
                 'data':''}
                self.state = self.commentStartState
                return True
        else:
            if charStack[(-1)] in ('d', 'D'):
                matched = True
                for expected in (('o', 'O'), ('c', 'C'), ('t', 'T'), ('y', 'Y'), ('p', 'P'),
                                 ('e', 'E')):
                    charStack.append(self.stream.char())
                    if charStack[(-1)] not in expected:
                        matched = False
                        break

                if matched:
                    self.currentToken = {'type':tokenTypes['Doctype'], 
                     'name':'', 
                     'publicId':None, 
                     'systemId':None,  'correct':True}
                    self.state = self.doctypeState
                    return True
            else:
                if charStack[(-1)] == '[':
                    if self.parser is not None:
                        if self.parser.tree.openElements:
                            if self.parser.tree.openElements[(-1)].namespace != self.parser.tree.defaultNamespace:
                                matched = True
                                for expected in ('C', 'D', 'A', 'T', 'A', '['):
                                    charStack.append(self.stream.char())
                                    if charStack[(-1)] != expected:
                                        matched = False
                                        break

                                if matched:
                                    self.state = self.cdataSectionState
                                    return True
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-dashes-or-doctype'})
                while charStack:
                    self.stream.unget(charStack.pop())

                self.state = self.bogusCommentState
                return True

    def commentStartState(self):
        data = self.stream.char()
        if data == '-':
            self.state = self.commentStartDashState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['data'] += '�'
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'incorrect-comment'})
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-comment'})
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.currentToken['data'] += data
                        self.state = self.commentState
        return True

    def commentStartDashState(self):
        data = self.stream.char()
        if data == '-':
            self.state = self.commentEndState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['data'] += '-�'
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'incorrect-comment'})
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-comment'})
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.currentToken['data'] += '-' + data
                        self.state = self.commentState
        return True

    def commentState(self):
        data = self.stream.char()
        if data == '-':
            self.state = self.commentEndDashState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['data'] += '�'
            else:
                if data is EOF:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-comment'})
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    self.currentToken['data'] += data + self.stream.charsUntil(('-',
                                                                                '\x00'))
        return True

    def commentEndDashState(self):
        data = self.stream.char()
        if data == '-':
            self.state = self.commentEndState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['data'] += '-�'
                self.state = self.commentState
            else:
                if data is EOF:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-comment-end-dash'})
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    self.currentToken['data'] += '-' + data
                    self.state = self.commentState
        return True

    def commentEndState(self):
        data = self.stream.char()
        if data == '>':
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['data'] += '--�'
                self.state = self.commentState
            else:
                if data == '!':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-bang-after-double-dash-in-comment'})
                    self.state = self.commentEndBangState
                else:
                    if data == '-':
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-dash-after-double-dash-in-comment'})
                        self.currentToken['data'] += data
                    else:
                        if data is EOF:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-comment-double-dash'})
                            self.tokenQueue.append(self.currentToken)
                            self.state = self.dataState
                        else:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-comment'})
                            self.currentToken['data'] += '--' + data
                            self.state = self.commentState
        return True

    def commentEndBangState(self):
        data = self.stream.char()
        if data == '>':
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            if data == '-':
                self.currentToken['data'] += '--!'
                self.state = self.commentEndDashState
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.currentToken['data'] += '--!�'
                    self.state = self.commentState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-comment-end-bang-state'})
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.currentToken['data'] += '--!' + data
                        self.state = self.commentState
        return True

    def doctypeState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeDoctypeNameState
        else:
            if data is EOF:
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-doctype-name-but-got-eof'})
                self.currentToken['correct'] = False
                self.tokenQueue.append(self.currentToken)
                self.state = self.dataState
            else:
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'need-space-after-doctype'})
                self.stream.unget(data)
                self.state = self.beforeDoctypeNameState
        return True

    def beforeDoctypeNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        elif data == '>':
            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-doctype-name-but-got-right-bracket'})
            self.currentToken['correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['name'] = '�'
                self.state = self.doctypeNameState
            else:
                if data is EOF:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-doctype-name-but-got-eof'})
                    self.currentToken['correct'] = False
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    self.currentToken['name'] = data
                    self.state = self.doctypeNameState
        return True

    def doctypeNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.currentToken['name'] = self.currentToken['name'].translate(asciiUpper2Lower)
            self.state = self.afterDoctypeNameState
        else:
            if data == '>':
                self.currentToken['name'] = self.currentToken['name'].translate(asciiUpper2Lower)
                self.tokenQueue.append(self.currentToken)
                self.state = self.dataState
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.currentToken['name'] += '�'
                    self.state = self.doctypeNameState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype-name'})
                        self.currentToken['correct'] = False
                        self.currentToken['name'] = self.currentToken['name'].translate(asciiUpper2Lower)
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.currentToken['name'] += data
        return True

    def afterDoctypeNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        elif data == '>':
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            if data is EOF:
                self.currentToken['correct'] = False
                self.stream.unget(data)
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                self.tokenQueue.append(self.currentToken)
                self.state = self.dataState
            else:
                if data in ('p', 'P'):
                    matched = True
                    for expected in (('u', 'U'), ('b', 'B'), ('l', 'L'), ('i', 'I'),
                                     ('c', 'C')):
                        data = self.stream.char()
                        if data not in expected:
                            matched = False
                            break

                    if matched:
                        self.state = self.afterDoctypePublicKeywordState
                        return True
                else:
                    if data in ('s', 'S'):
                        matched = True
                        for expected in (('y', 'Y'), ('s', 'S'), ('t', 'T'), ('e', 'E'),
                                         ('m', 'M')):
                            data = self.stream.char()
                            if data not in expected:
                                matched = False
                                break

                        if matched:
                            self.state = self.afterDoctypeSystemKeywordState
                            return True
                    self.stream.unget(data)
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-space-or-right-bracket-in-doctype', 
                     'datavars':{'data': data}})
                    self.currentToken['correct'] = False
                    self.state = self.bogusDoctypeState
        return True

    def afterDoctypePublicKeywordState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeDoctypePublicIdentifierState
        else:
            if data in ("'", '"'):
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                self.stream.unget(data)
                self.state = self.beforeDoctypePublicIdentifierState
            else:
                if data is EOF:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                    self.currentToken['correct'] = False
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    self.stream.unget(data)
                    self.state = self.beforeDoctypePublicIdentifierState
        return True

    def beforeDoctypePublicIdentifierState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        elif data == '"':
            self.currentToken['publicId'] = ''
            self.state = self.doctypePublicIdentifierDoubleQuotedState
        else:
            if data == "'":
                self.currentToken['publicId'] = ''
                self.state = self.doctypePublicIdentifierSingleQuotedState
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-end-of-doctype'})
                    self.currentToken['correct'] = False
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                        self.currentToken['correct'] = False
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                        self.currentToken['correct'] = False
                        self.state = self.bogusDoctypeState
        return True

    def doctypePublicIdentifierDoubleQuotedState(self):
        data = self.stream.char()
        if data == '"':
            self.state = self.afterDoctypePublicIdentifierState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['publicId'] += '�'
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-end-of-doctype'})
                    self.currentToken['correct'] = False
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                        self.currentToken['correct'] = False
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.currentToken['publicId'] += data
        return True

    def doctypePublicIdentifierSingleQuotedState(self):
        data = self.stream.char()
        if data == "'":
            self.state = self.afterDoctypePublicIdentifierState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['publicId'] += '�'
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-end-of-doctype'})
                    self.currentToken['correct'] = False
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                        self.currentToken['correct'] = False
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.currentToken['publicId'] += data
        return True

    def afterDoctypePublicIdentifierState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.betweenDoctypePublicAndSystemIdentifiersState
        else:
            if data == '>':
                self.tokenQueue.append(self.currentToken)
                self.state = self.dataState
            else:
                if data == '"':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                    self.currentToken['systemId'] = ''
                    self.state = self.doctypeSystemIdentifierDoubleQuotedState
                else:
                    if data == "'":
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                        self.currentToken['systemId'] = ''
                        self.state = self.doctypeSystemIdentifierSingleQuotedState
                    else:
                        if data is EOF:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                            self.currentToken['correct'] = False
                            self.tokenQueue.append(self.currentToken)
                            self.state = self.dataState
                        else:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                            self.currentToken['correct'] = False
                            self.state = self.bogusDoctypeState
        return True

    def betweenDoctypePublicAndSystemIdentifiersState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        elif data == '>':
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            if data == '"':
                self.currentToken['systemId'] = ''
                self.state = self.doctypeSystemIdentifierDoubleQuotedState
            else:
                if data == "'":
                    self.currentToken['systemId'] = ''
                    self.state = self.doctypeSystemIdentifierSingleQuotedState
                else:
                    if data == EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                        self.currentToken['correct'] = False
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                        self.currentToken['correct'] = False
                        self.state = self.bogusDoctypeState
        return True

    def afterDoctypeSystemKeywordState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeDoctypeSystemIdentifierState
        else:
            if data in ("'", '"'):
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                self.stream.unget(data)
                self.state = self.beforeDoctypeSystemIdentifierState
            else:
                if data is EOF:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                    self.currentToken['correct'] = False
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    self.stream.unget(data)
                    self.state = self.beforeDoctypeSystemIdentifierState
        return True

    def beforeDoctypeSystemIdentifierState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        elif data == '"':
            self.currentToken['systemId'] = ''
            self.state = self.doctypeSystemIdentifierDoubleQuotedState
        else:
            if data == "'":
                self.currentToken['systemId'] = ''
                self.state = self.doctypeSystemIdentifierSingleQuotedState
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                    self.currentToken['correct'] = False
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                        self.currentToken['correct'] = False
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                        self.currentToken['correct'] = False
                        self.state = self.bogusDoctypeState
        return True

    def doctypeSystemIdentifierDoubleQuotedState(self):
        data = self.stream.char()
        if data == '"':
            self.state = self.afterDoctypeSystemIdentifierState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['systemId'] += '�'
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-end-of-doctype'})
                    self.currentToken['correct'] = False
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                        self.currentToken['correct'] = False
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.currentToken['systemId'] += data
        return True

    def doctypeSystemIdentifierSingleQuotedState(self):
        data = self.stream.char()
        if data == "'":
            self.state = self.afterDoctypeSystemIdentifierState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['systemId'] += '�'
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-end-of-doctype'})
                    self.currentToken['correct'] = False
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                        self.currentToken['correct'] = False
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.currentToken['systemId'] += data
        return True

    def afterDoctypeSystemIdentifierState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        elif data == '>':
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            if data is EOF:
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                self.currentToken['correct'] = False
                self.tokenQueue.append(self.currentToken)
                self.state = self.dataState
            else:
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                self.state = self.bogusDoctypeState
        return True

    def bogusDoctypeState(self):
        data = self.stream.char()
        if data == '>':
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            if data is EOF:
                self.stream.unget(data)
                self.tokenQueue.append(self.currentToken)
                self.state = self.dataState
            else:
                return True

    def cdataSectionState(self):
        data = []
        while True:
            data.append(self.stream.charsUntil(']'))
            data.append(self.stream.charsUntil('>'))
            char = self.stream.char()
            if char == EOF:
                break
            else:
                assert char == '>'
                if data[(-1)][-2:] == ']]':
                    data[-1] = data[(-1)][:-2]
                    break
                else:
                    data.append(char)

        data = ''.join(data)
        nullCount = data.count('\x00')
        if nullCount > 0:
            for _ in range(nullCount):
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})

            data = data.replace('\x00', '�')
        if data:
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
        self.state = self.dataState
        return True