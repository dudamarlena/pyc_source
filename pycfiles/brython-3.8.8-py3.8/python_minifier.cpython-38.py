# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\brython\python_minifier.py
# Compiled at: 2020-03-16 10:39:04
# Size of source mod 2**32: 6060 bytes
"""Minifier for Python code

The module exposes a single function : minify(src), where src is
a string with the original Python code.

The function returns a string with a minified version of the original :
- indentation is reduced to the minimum (1 space for each level)
- comments are removed, except on the first 2 lines
- lines starting with a string are removed (considered as doc strings), except
  if the next line doesn't start with the same indent, like in
      # --------------------------------
      def f():
          'function with docstring only'
      print('ok')
      # --------------------------------
"""
import os, token, tokenize, re, io
from keyword import kwlist
for kw in ('async', 'await'):
    if kw not in kwlist:
        kwlist.append(kw)
else:
    async_types = []
    if hasattr(tokenize, 'ASYNC'):
        async_types.append(tokenize.ASYNC)
    if hasattr(tokenize, 'AWAIT'):
        async_types.append(tokenize.AWAIT)

    def minify--- This code section failed: ---

 L.  38         0  LOAD_GLOBAL              io
                2  LOAD_METHOD              BytesIO
                4  LOAD_FAST                'src'
                6  LOAD_METHOD              encode
                8  LOAD_STR                 'utf-8'
               10  CALL_METHOD_1         1  ''
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'file_obj'

 L.  39        16  LOAD_GLOBAL              tokenize
               18  LOAD_METHOD              tokenize
               20  LOAD_FAST                'file_obj'
               22  LOAD_ATTR                readline
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'token_generator'

 L.  41        28  LOAD_STR                 ''
               30  STORE_FAST               'out'

 L.  42        32  LOAD_CONST               0
               34  STORE_FAST               'line'

 L.  43        36  LOAD_CONST               None
               38  STORE_FAST               'last_item'

 L.  44        40  LOAD_CONST               None
               42  STORE_FAST               'last_type'

 L.  45        44  LOAD_CONST               0
               46  STORE_FAST               'indent'

 L.  46        48  BUILD_LIST_0          0 
               50  STORE_FAST               'brackets'

 L.  47        52  LOAD_FAST                'src'
               54  LOAD_METHOD              split
               56  LOAD_STR                 '\n'
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               'orig_lines'

 L.  50        62  LOAD_GLOBAL              next
               64  LOAD_FAST                'token_generator'
               66  CALL_FUNCTION_1       1  ''
               68  LOAD_ATTR                string
               70  STORE_FAST               'encoding'

 L.  52        72  LOAD_GLOBAL              io
               74  LOAD_METHOD              BytesIO
               76  LOAD_FAST                'src'
               78  LOAD_METHOD              encode
               80  LOAD_FAST                'encoding'
               82  CALL_METHOD_1         1  ''
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'file_obj'

 L.  53        88  LOAD_GLOBAL              tokenize
               90  LOAD_METHOD              tokenize
               92  LOAD_FAST                'file_obj'
               94  LOAD_ATTR                readline
               96  CALL_METHOD_1         1  ''
               98  STORE_FAST               'token_generator'

 L.  55       100  LOAD_FAST                'token_generator'
              102  GET_ITER         
            104_0  COME_FROM           540  '540'
            104_1  COME_FROM           356  '356'
          104_106  FOR_ITER            876  'to 876'
              108  STORE_FAST               'item'

 L.  57       110  LOAD_GLOBAL              token
              112  LOAD_ATTR                tok_name
              114  LOAD_FAST                'item'
              116  LOAD_ATTR                type
              118  BINARY_SUBSCR    
              120  LOAD_STR                 'OP'
              122  COMPARE_OP               ==
              124  POP_JUMP_IF_FALSE   168  'to 168'

 L.  58       126  LOAD_FAST                'item'
              128  LOAD_ATTR                string
              130  LOAD_STR                 '([{'
              132  COMPARE_OP               in
              134  POP_JUMP_IF_FALSE   150  'to 150'

 L.  59       136  LOAD_FAST                'brackets'
              138  LOAD_METHOD              append
              140  LOAD_FAST                'item'
              142  LOAD_ATTR                string
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          
              148  JUMP_FORWARD        168  'to 168'
            150_0  COME_FROM           134  '134'

 L.  60       150  LOAD_FAST                'item'
              152  LOAD_ATTR                string
              154  LOAD_STR                 '}])'
              156  COMPARE_OP               in
              158  POP_JUMP_IF_FALSE   168  'to 168'

 L.  61       160  LOAD_FAST                'brackets'
              162  LOAD_METHOD              pop
              164  CALL_METHOD_0         0  ''
              166  POP_TOP          
            168_0  COME_FROM           158  '158'
            168_1  COME_FROM           148  '148'
            168_2  COME_FROM           124  '124'

 L.  63       168  LOAD_FAST                'item'
              170  LOAD_ATTR                start
              172  LOAD_CONST               0
              174  BINARY_SUBSCR    
              176  STORE_FAST               'sline'

 L.  64       178  LOAD_FAST                'sline'
              180  LOAD_CONST               0
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   188  'to 188'

 L.  65       186  JUMP_BACK           104  'to 104'
            188_0  COME_FROM           184  '184'

 L.  68       188  LOAD_FAST                'item'
              190  LOAD_ATTR                type
              192  LOAD_GLOBAL              tokenize
              194  LOAD_ATTR                INDENT
              196  COMPARE_OP               ==
              198  POP_JUMP_IF_FALSE   210  'to 210'

 L.  69       200  LOAD_FAST                'indent'
              202  LOAD_CONST               1
              204  INPLACE_ADD      
              206  STORE_FAST               'indent'
              208  JUMP_FORWARD        232  'to 232'
            210_0  COME_FROM           198  '198'

 L.  70       210  LOAD_FAST                'item'
              212  LOAD_ATTR                type
              214  LOAD_GLOBAL              tokenize
              216  LOAD_ATTR                DEDENT
              218  COMPARE_OP               ==
              220  POP_JUMP_IF_FALSE   232  'to 232'

 L.  71       222  LOAD_FAST                'indent'
              224  LOAD_CONST               1
              226  INPLACE_SUBTRACT 
              228  STORE_FAST               'indent'

 L.  72       230  JUMP_BACK           104  'to 104'
            232_0  COME_FROM           220  '220'
            232_1  COME_FROM           208  '208'

 L.  74       232  LOAD_FAST                'sline'
              234  LOAD_FAST                'line'
              236  COMPARE_OP               >
          238_240  POP_JUMP_IF_FALSE   476  'to 476'

 L.  76       242  LOAD_FAST                'out'
              244  LOAD_METHOD              count
              246  LOAD_STR                 '\n'
              248  CALL_METHOD_1         1  ''
              250  LOAD_FAST                'sline'
              252  LOAD_CONST               1
              254  BINARY_SUBTRACT  
              256  COMPARE_OP               <
          258_260  POP_JUMP_IF_FALSE   298  'to 298'

 L.  77       262  LOAD_FAST                'last_item'
              264  LOAD_ATTR                line
              266  LOAD_METHOD              rstrip
              268  CALL_METHOD_0         0  ''
              270  LOAD_METHOD              endswith
              272  LOAD_STR                 '\\'
              274  CALL_METHOD_1         1  ''
          276_278  POP_JUMP_IF_FALSE   288  'to 288'

 L.  78       280  LOAD_FAST                'out'
              282  LOAD_STR                 '\\'
              284  INPLACE_ADD      
              286  STORE_FAST               'out'
            288_0  COME_FROM           276  '276'

 L.  79       288  LOAD_FAST                'out'
              290  LOAD_STR                 '\n'
              292  INPLACE_ADD      
              294  STORE_FAST               'out'
              296  JUMP_BACK           242  'to 242'
            298_0  COME_FROM           258  '258'

 L.  81       298  LOAD_FAST                'brackets'
          300_302  POP_JUMP_IF_TRUE    380  'to 380'
              304  LOAD_FAST                'item'
              306  LOAD_ATTR                type
              308  LOAD_GLOBAL              tokenize
              310  LOAD_ATTR                STRING
              312  COMPARE_OP               ==
          314_316  POP_JUMP_IF_FALSE   380  'to 380'

 L.  82       318  LOAD_FAST                'last_type'
              320  LOAD_GLOBAL              tokenize
              322  LOAD_ATTR                NEWLINE
              324  LOAD_GLOBAL              tokenize
              326  LOAD_ATTR                INDENT
              328  LOAD_CONST               None
              330  BUILD_TUPLE_3         3 
              332  COMPARE_OP               in
          334_336  POP_JUMP_IF_FALSE   380  'to 380'

 L.  87       338  LOAD_FAST                'out'
              340  LOAD_STR                 ' '
              342  LOAD_FAST                'indent'
              344  BINARY_MULTIPLY  
              346  LOAD_STR                 "''"
              348  BINARY_ADD       
              350  INPLACE_ADD      
              352  STORE_FAST               'out'

 L.  88       354  LOAD_FAST                'preserve_lines'
              356  POP_JUMP_IF_FALSE   104  'to 104'

 L.  89       358  LOAD_FAST                'out'
              360  LOAD_STR                 '\n'
              362  LOAD_FAST                'item'
              364  LOAD_ATTR                string
              366  LOAD_METHOD              count
              368  LOAD_STR                 '\n'
              370  CALL_METHOD_1         1  ''
              372  BINARY_MULTIPLY  
              374  INPLACE_ADD      
              376  STORE_FAST               'out'

 L.  90       378  JUMP_BACK           104  'to 104'
            380_0  COME_FROM           334  '334'
            380_1  COME_FROM           314  '314'
            380_2  COME_FROM           300  '300'

 L.  91       380  LOAD_FAST                'out'
              382  LOAD_STR                 ' '
              384  LOAD_FAST                'indent'
              386  BINARY_MULTIPLY  
              388  INPLACE_ADD      
              390  STORE_FAST               'out'

 L.  92       392  LOAD_FAST                'item'
              394  LOAD_ATTR                type
              396  LOAD_GLOBAL              tokenize
              398  LOAD_ATTR                INDENT
              400  LOAD_GLOBAL              tokenize
              402  LOAD_ATTR                COMMENT
              404  BUILD_TUPLE_2         2 
              406  COMPARE_OP               not-in
          408_410  POP_JUMP_IF_FALSE   424  'to 424'

 L.  93       412  LOAD_FAST                'out'
              414  LOAD_FAST                'item'
              416  LOAD_ATTR                string
              418  INPLACE_ADD      
              420  STORE_FAST               'out'
              422  JUMP_FORWARD        820  'to 820'
            424_0  COME_FROM           408  '408'

 L.  94       424  LOAD_FAST                'item'
              426  LOAD_ATTR                type
              428  LOAD_GLOBAL              tokenize
              430  LOAD_ATTR                COMMENT
              432  COMPARE_OP               ==
          434_436  POP_JUMP_IF_FALSE   820  'to 820'

 L.  95       438  LOAD_FAST                'line'
              440  LOAD_CONST               2
              442  COMPARE_OP               <=

 L.  94   444_446  POP_JUMP_IF_FALSE   820  'to 820'

 L.  95       448  LOAD_FAST                'item'
              450  LOAD_ATTR                line
              452  LOAD_METHOD              startswith
              454  LOAD_STR                 '#!'
              456  CALL_METHOD_1         1  ''

 L.  94   458_460  POP_JUMP_IF_FALSE   820  'to 820'

 L.  98       462  LOAD_FAST                'out'
              464  LOAD_FAST                'item'
              466  LOAD_ATTR                string
              468  INPLACE_ADD      
              470  STORE_FAST               'out'
          472_474  JUMP_FORWARD        820  'to 820'
            476_0  COME_FROM           238  '238'

 L. 100       476  LOAD_FAST                'item'
              478  LOAD_ATTR                type
              480  LOAD_GLOBAL              tokenize
              482  LOAD_ATTR                COMMENT
              484  COMPARE_OP               ==
          486_488  POP_JUMP_IF_FALSE   492  'to 492'

 L. 101       490  JUMP_BACK           104  'to 104'
            492_0  COME_FROM           486  '486'

 L. 102       492  LOAD_FAST                'brackets'
          494_496  POP_JUMP_IF_TRUE    564  'to 564'
              498  LOAD_FAST                'item'
              500  LOAD_ATTR                type
              502  LOAD_GLOBAL              tokenize
              504  LOAD_ATTR                STRING
              506  COMPARE_OP               ==
          508_510  POP_JUMP_IF_FALSE   564  'to 564'

 L. 103       512  LOAD_FAST                'last_type'
              514  LOAD_GLOBAL              tokenize
              516  LOAD_ATTR                NEWLINE
              518  LOAD_GLOBAL              tokenize
              520  LOAD_ATTR                INDENT
              522  BUILD_TUPLE_2         2 
              524  COMPARE_OP               in

 L. 102   526_528  POP_JUMP_IF_FALSE   564  'to 564'

 L. 106       530  LOAD_FAST                'out'
              532  LOAD_STR                 "''"
              534  INPLACE_ADD      
              536  STORE_FAST               'out'

 L. 107       538  LOAD_FAST                'preserve_lines'
              540  POP_JUMP_IF_FALSE   104  'to 104'

 L. 108       542  LOAD_FAST                'out'
              544  LOAD_STR                 '\n'
              546  LOAD_FAST                'item'
              548  LOAD_ATTR                string
              550  LOAD_METHOD              count
              552  LOAD_STR                 '\n'
              554  CALL_METHOD_1         1  ''
              556  BINARY_MULTIPLY  
              558  INPLACE_ADD      
              560  STORE_FAST               'out'

 L. 109       562  JUMP_BACK           104  'to 104'
            564_0  COME_FROM           526  '526'
            564_1  COME_FROM           508  '508'
            564_2  COME_FROM           494  '494'

 L. 110       564  LOAD_GLOBAL              tokenize
              566  LOAD_ATTR                NAME
              568  LOAD_GLOBAL              tokenize
              570  LOAD_ATTR                NUMBER
              572  BUILD_LIST_2          2 
              574  LOAD_GLOBAL              async_types
              576  BINARY_ADD       
              578  STORE_FAST               'previous_types'

 L. 111       580  LOAD_FAST                'item'
              582  LOAD_ATTR                type
              584  LOAD_GLOBAL              tokenize
              586  LOAD_ATTR                NAME
              588  LOAD_GLOBAL              tokenize
              590  LOAD_ATTR                NUMBER
              592  LOAD_GLOBAL              tokenize
              594  LOAD_ATTR                OP
              596  BUILD_TUPLE_3         3 
              598  COMPARE_OP               in
          600_602  POP_JUMP_IF_FALSE   674  'to 674'

 L. 112       604  LOAD_FAST                'last_type'
              606  LOAD_FAST                'previous_types'
              608  COMPARE_OP               in

 L. 111   610_612  POP_JUMP_IF_FALSE   674  'to 674'

 L. 114       614  LOAD_FAST                'item'
              616  LOAD_ATTR                type
              618  LOAD_GLOBAL              tokenize
              620  LOAD_ATTR                OP
              622  COMPARE_OP               !=
          624_626  POP_JUMP_IF_TRUE    664  'to 664'

 L. 115       628  LOAD_FAST                'item'
              630  LOAD_ATTR                string
              632  LOAD_STR                 ',()[].=:{}+&'
              634  COMPARE_OP               not-in

 L. 114   636_638  POP_JUMP_IF_TRUE    664  'to 664'

 L. 116       640  LOAD_FAST                'last_type'
              642  LOAD_GLOBAL              tokenize
              644  LOAD_ATTR                NAME
              646  COMPARE_OP               ==

 L. 114   648_650  POP_JUMP_IF_FALSE   810  'to 810'

 L. 117       652  LOAD_FAST                'last_item'
              654  LOAD_ATTR                string
              656  LOAD_GLOBAL              kwlist
              658  COMPARE_OP               in

 L. 114   660_662  POP_JUMP_IF_FALSE   810  'to 810'
            664_0  COME_FROM           636  '636'
            664_1  COME_FROM           624  '624'

 L. 118       664  LOAD_FAST                'out'
              666  LOAD_STR                 ' '
              668  INPLACE_ADD      
              670  STORE_FAST               'out'
              672  JUMP_FORWARD        810  'to 810'
            674_0  COME_FROM           610  '610'
            674_1  COME_FROM           600  '600'

 L. 119       674  LOAD_FAST                'item'
              676  LOAD_ATTR                type
              678  LOAD_GLOBAL              tokenize
              680  LOAD_ATTR                STRING
              682  COMPARE_OP               ==
          684_686  POP_JUMP_IF_FALSE   716  'to 716'

 L. 120       688  LOAD_FAST                'last_type'
              690  LOAD_GLOBAL              tokenize
              692  LOAD_ATTR                NAME
              694  LOAD_GLOBAL              tokenize
              696  LOAD_ATTR                NUMBER
              698  BUILD_TUPLE_2         2 
              700  COMPARE_OP               in

 L. 119   702_704  POP_JUMP_IF_FALSE   716  'to 716'

 L. 122       706  LOAD_FAST                'out'
              708  LOAD_STR                 ' '
              710  INPLACE_ADD      
              712  STORE_FAST               'out'
              714  JUMP_FORWARD        810  'to 810'
            716_0  COME_FROM           702  '702'
            716_1  COME_FROM           684  '684'

 L. 123       716  LOAD_FAST                'item'
              718  LOAD_ATTR                type
              720  LOAD_GLOBAL              tokenize
              722  LOAD_ATTR                NAME
              724  COMPARE_OP               ==
          726_728  POP_JUMP_IF_FALSE   778  'to 778'

 L. 124       730  LOAD_FAST                'item'
              732  LOAD_ATTR                string
              734  LOAD_STR                 'import'
              736  COMPARE_OP               ==

 L. 123   738_740  POP_JUMP_IF_FALSE   778  'to 778'

 L. 125       742  LOAD_FAST                'last_item'
              744  LOAD_ATTR                type
              746  LOAD_GLOBAL              tokenize
              748  LOAD_ATTR                OP
              750  COMPARE_OP               ==

 L. 123   752_754  POP_JUMP_IF_FALSE   778  'to 778'

 L. 126       756  LOAD_FAST                'last_item'
              758  LOAD_ATTR                string
              760  LOAD_STR                 '.'
              762  COMPARE_OP               ==

 L. 123   764_766  POP_JUMP_IF_FALSE   778  'to 778'
            768_0  COME_FROM           422  '422'

 L. 128       768  LOAD_FAST                'out'
              770  LOAD_STR                 ' '
              772  INPLACE_ADD      
              774  STORE_FAST               'out'
              776  JUMP_FORWARD        810  'to 810'
            778_0  COME_FROM           764  '764'
            778_1  COME_FROM           752  '752'
            778_2  COME_FROM           738  '738'
            778_3  COME_FROM           726  '726'

 L. 129       778  LOAD_FAST                'item'
              780  LOAD_ATTR                type
              782  LOAD_GLOBAL              async_types
              784  COMPARE_OP               in
          786_788  POP_JUMP_IF_FALSE   810  'to 810'

 L. 130       790  LOAD_FAST                'last_item'
              792  LOAD_ATTR                type
              794  LOAD_FAST                'previous_types'
              796  COMPARE_OP               in

 L. 129   798_800  POP_JUMP_IF_FALSE   810  'to 810'

 L. 131       802  LOAD_FAST                'out'
              804  LOAD_STR                 ' '
              806  INPLACE_ADD      
              808  STORE_FAST               'out'
            810_0  COME_FROM           798  '798'
            810_1  COME_FROM           786  '786'
            810_2  COME_FROM           776  '776'
            810_3  COME_FROM           714  '714'
            810_4  COME_FROM           672  '672'
            810_5  COME_FROM           660  '660'
            810_6  COME_FROM           648  '648'

 L. 132       810  LOAD_FAST                'out'
              812  LOAD_FAST                'item'
              814  LOAD_ATTR                string
              816  INPLACE_ADD      
              818  STORE_FAST               'out'
            820_0  COME_FROM           472  '472'
            820_1  COME_FROM           458  '458'
            820_2  COME_FROM           444  '444'
            820_3  COME_FROM           434  '434'

 L. 134       820  LOAD_FAST                'item'
              822  LOAD_ATTR                end
              824  LOAD_CONST               0
              826  BINARY_SUBSCR    
              828  STORE_FAST               'line'

 L. 135       830  LOAD_FAST                'item'
              832  STORE_FAST               'last_item'

 L. 136       834  LOAD_FAST                'item'
              836  LOAD_ATTR                type
              838  LOAD_GLOBAL              tokenize
              840  LOAD_ATTR                NL
              842  COMPARE_OP               ==
          844_846  POP_JUMP_IF_FALSE   868  'to 868'
              848  LOAD_FAST                'last_type'
              850  LOAD_GLOBAL              tokenize
              852  LOAD_ATTR                COMMENT
              854  COMPARE_OP               ==
          856_858  POP_JUMP_IF_FALSE   868  'to 868'

 L. 138       860  LOAD_GLOBAL              tokenize
              862  LOAD_ATTR                NEWLINE
              864  STORE_FAST               'last_type'
              866  JUMP_BACK           104  'to 104'
            868_0  COME_FROM           856  '856'
            868_1  COME_FROM           844  '844'

 L. 140       868  LOAD_FAST                'item'
              870  LOAD_ATTR                type
              872  STORE_FAST               'last_type'
              874  JUMP_BACK           104  'to 104'

 L. 143       876  LOAD_GLOBAL              re
              878  LOAD_METHOD              sub
              880  LOAD_STR                 '^\\s+$'
              882  LOAD_STR                 ''
              884  LOAD_FAST                'out'
              886  LOAD_GLOBAL              re
              888  LOAD_ATTR                M
              890  CALL_METHOD_4         4  ''
              892  STORE_FAST               'out'

 L. 145       894  LOAD_FAST                'preserve_lines'
          896_898  POP_JUMP_IF_TRUE    950  'to 950'

 L. 147       900  LOAD_GLOBAL              re
              902  LOAD_METHOD              sub
              904  LOAD_STR                 "^''\n"
              906  LOAD_STR                 ''
              908  LOAD_FAST                'out'
              910  CALL_METHOD_3         3  ''
              912  STORE_FAST               'out'

 L. 150       914  LOAD_GLOBAL              re
              916  LOAD_METHOD              sub
              918  LOAD_STR                 '\n( *\n)+'
              920  LOAD_STR                 '\n'
              922  LOAD_FAST                'out'
              924  CALL_METHOD_3         3  ''
              926  STORE_FAST               'out'

 L. 154       928  LOAD_CODE                <code_object repl>
              930  LOAD_STR                 'minify.<locals>.repl'
              932  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              934  STORE_FAST               'repl'

 L. 158       936  LOAD_GLOBAL              re
              938  LOAD_METHOD              sub
              940  LOAD_STR                 "\n( *)''\n( *)"
              942  LOAD_FAST                'repl'
              944  LOAD_FAST                'out'
              946  CALL_METHOD_3         3  ''
              948  STORE_FAST               'out'
            950_0  COME_FROM           896  '896'

 L. 160       950  LOAD_FAST                'out'
              952  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 674_0