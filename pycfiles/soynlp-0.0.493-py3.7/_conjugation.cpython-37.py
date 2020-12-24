# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soynlp/lemmatizer/_conjugation.py
# Compiled at: 2018-11-26 12:18:34
# Size of source mod 2**32: 15977 bytes
from soynlp.hangle import compose, decompose
positive_moum = set('ㅏㅑㅗㅛ')
negative_moum = set('ㅓㅕㅜㅠ')
neuter_moum = set('ㅡㅣ')
pos_to_neg = {'ㅏ':'ㅓ', 
 'ㅑ':'ㅕ', 
 'ㅗ':'ㅜ', 
 'ㅛ':'ㅠ'}
neg_to_pos = {'ㅓ':'ㅏ', 
 'ㅕ':'ㅑ', 
 'ㅜ':'ㅗ', 
 'ㅠ':'ㅛ'}

def conjugate_chat(stem, ending, enforce_moum_harmoney=False, debug=False):
    if not ending:
        return {
         stem}
    else:
        candidates = conjugate(stem, ending, enforce_moum_harmoney, debug)
        l_len = len(stem)
        l_last = list(decompose(stem[(-1)]))
        l_last_ = stem[(-1)]
        r_first = list(decompose(ending[0]))
        if r_first[1] == ' ':
            if r_first[0] != ' ':
                l = stem[:-1] + compose(l_last[0], l_last[1], r_first[0])
                r = ending[1:]
                surface = l + r
                candidates.add(surface)
                if r_first[1] != ' ':
                    candidates.add(stem + ending)
                if debug:
                    print('어미의 첫 글자가 자음인 경우: {}'.format(surface))
    return candidates


def conjugate--- This code section failed: ---

 L.  48         0  LOAD_FAST                'ending'
                2  POP_JUMP_IF_TRUE      8  'to 8'
                4  LOAD_ASSERT              AssertionError
                6  RAISE_VARARGS_1       1  'exception instance'
              8_0  COME_FROM             2  '2'

 L.  50         8  LOAD_GLOBAL              len
               10  LOAD_FAST                'stem'
               12  CALL_FUNCTION_1       1  '1 positional argument'
               14  STORE_FAST               'l_len'

 L.  51        16  LOAD_GLOBAL              list
               18  LOAD_GLOBAL              decompose
               20  LOAD_FAST                'stem'
               22  LOAD_CONST               -1
               24  BINARY_SUBSCR    
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  STORE_FAST               'l_last'

 L.  52        32  LOAD_FAST                'stem'
               34  LOAD_CONST               -1
               36  BINARY_SUBSCR    
               38  STORE_FAST               'l_last_'

 L.  53        40  LOAD_GLOBAL              list
               42  LOAD_GLOBAL              decompose
               44  LOAD_FAST                'ending'
               46  LOAD_CONST               0
               48  BINARY_SUBSCR    
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  CALL_FUNCTION_1       1  '1 positional argument'
               54  STORE_FAST               'r_first'

 L.  57        56  LOAD_FAST                'enforce_moum_harmoney'
            58_60  POP_JUMP_IF_FALSE   294  'to 294'

 L.  58        62  LOAD_FAST                'l_last'
               64  LOAD_CONST               2
               66  BINARY_SUBSCR    
               68  LOAD_STR                 'ㅂ'
               70  COMPARE_OP               !=
               72  POP_JUMP_IF_FALSE   146  'to 146'
               74  LOAD_FAST                'l_last'
               76  LOAD_CONST               1
               78  BINARY_SUBSCR    
               80  LOAD_GLOBAL              positive_moum
               82  COMPARE_OP               in
               84  POP_JUMP_IF_FALSE   146  'to 146'

 L.  59        86  LOAD_FAST                'r_first'
               88  LOAD_CONST               0
               90  BINARY_SUBSCR    
               92  LOAD_STR                 'ㅇ'
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   146  'to 146'
               98  LOAD_FAST                'r_first'
              100  LOAD_CONST               1
              102  BINARY_SUBSCR    
              104  LOAD_GLOBAL              negative_moum
              106  COMPARE_OP               in
              108  POP_JUMP_IF_FALSE   146  'to 146'

 L.  60       110  LOAD_GLOBAL              neg_to_pos
              112  LOAD_FAST                'r_first'
              114  LOAD_CONST               1
              116  BINARY_SUBSCR    
              118  BINARY_SUBSCR    
              120  LOAD_FAST                'r_first'
              122  LOAD_CONST               1
              124  STORE_SUBSCR     

 L.  61       126  LOAD_GLOBAL              compose
              128  LOAD_FAST                'r_first'
              130  CALL_FUNCTION_EX      0  'positional arguments only'
              132  LOAD_FAST                'ending'
              134  LOAD_CONST               1
              136  LOAD_CONST               None
              138  BUILD_SLICE_2         2 
              140  BINARY_SUBSCR    
              142  BINARY_ADD       
              144  STORE_FAST               'ending'
            146_0  COME_FROM           108  '108'
            146_1  COME_FROM            96  '96'
            146_2  COME_FROM            84  '84'
            146_3  COME_FROM            72  '72'

 L.  62       146  LOAD_FAST                'l_last'
              148  LOAD_CONST               2
              150  BINARY_SUBSCR    
              152  LOAD_STR                 'ㅂ'
              154  COMPARE_OP               !=
              156  POP_JUMP_IF_FALSE   230  'to 230'
              158  LOAD_FAST                'l_last'
              160  LOAD_CONST               1
              162  BINARY_SUBSCR    
              164  LOAD_GLOBAL              negative_moum
              166  COMPARE_OP               in
              168  POP_JUMP_IF_FALSE   230  'to 230'

 L.  63       170  LOAD_FAST                'r_first'
              172  LOAD_CONST               0
              174  BINARY_SUBSCR    
              176  LOAD_STR                 'ㅇ'
              178  COMPARE_OP               ==
              180  POP_JUMP_IF_FALSE   230  'to 230'
              182  LOAD_FAST                'r_first'
              184  LOAD_CONST               1
              186  BINARY_SUBSCR    
              188  LOAD_GLOBAL              positive_moum
              190  COMPARE_OP               in
              192  POP_JUMP_IF_FALSE   230  'to 230'

 L.  64       194  LOAD_GLOBAL              pos_to_neg
              196  LOAD_FAST                'r_first'
              198  LOAD_CONST               1
              200  BINARY_SUBSCR    
              202  BINARY_SUBSCR    
              204  LOAD_FAST                'r_first'
              206  LOAD_CONST               1
              208  STORE_SUBSCR     

 L.  65       210  LOAD_GLOBAL              compose
              212  LOAD_FAST                'r_first'
              214  CALL_FUNCTION_EX      0  'positional arguments only'
              216  LOAD_FAST                'ending'
              218  LOAD_CONST               1
              220  LOAD_CONST               None
              222  BUILD_SLICE_2         2 
              224  BINARY_SUBSCR    
              226  BINARY_ADD       
              228  STORE_FAST               'ending'
            230_0  COME_FROM           192  '192'
            230_1  COME_FROM           180  '180'
            230_2  COME_FROM           168  '168'
            230_3  COME_FROM           156  '156'

 L.  66       230  LOAD_FAST                'l_last'
              232  LOAD_CONST               1
              234  BINARY_SUBSCR    
              236  LOAD_GLOBAL              neuter_moum
              238  COMPARE_OP               in
          240_242  POP_JUMP_IF_FALSE   294  'to 294'
              244  LOAD_FAST                'r_first'
              246  LOAD_CONST               1
              248  BINARY_SUBSCR    
              250  LOAD_GLOBAL              positive_moum
              252  COMPARE_OP               in
          254_256  POP_JUMP_IF_FALSE   294  'to 294'

 L.  67       258  LOAD_GLOBAL              pos_to_neg
              260  LOAD_FAST                'r_first'
              262  LOAD_CONST               1
              264  BINARY_SUBSCR    
              266  BINARY_SUBSCR    
              268  LOAD_FAST                'r_first'
              270  LOAD_CONST               1
              272  STORE_SUBSCR     

 L.  68       274  LOAD_GLOBAL              compose
              276  LOAD_FAST                'r_first'
              278  CALL_FUNCTION_EX      0  'positional arguments only'
              280  LOAD_FAST                'ending'
              282  LOAD_CONST               1
              284  LOAD_CONST               None
              286  BUILD_SLICE_2         2 
              288  BINARY_SUBSCR    
              290  BINARY_ADD       
              292  STORE_FAST               'ending'
            294_0  COME_FROM           254  '254'
            294_1  COME_FROM           240  '240'
            294_2  COME_FROM            58  '58'

 L.  76       294  LOAD_FAST                'r_first'
              296  LOAD_CONST               1
              298  BINARY_SUBSCR    
              300  LOAD_STR                 ' '
              302  COMPARE_OP               !=
          304_306  POP_JUMP_IF_FALSE   328  'to 328'
              308  LOAD_GLOBAL              compose
              310  LOAD_FAST                'r_first'
              312  LOAD_CONST               0
              314  BINARY_SUBSCR    
              316  LOAD_FAST                'r_first'
              318  LOAD_CONST               1
              320  BINARY_SUBSCR    
              322  LOAD_STR                 ' '
              324  CALL_FUNCTION_3       3  '3 positional arguments'
              326  JUMP_FORWARD        334  'to 334'
            328_0  COME_FROM           304  '304'
              328  LOAD_FAST                'ending'
              330  LOAD_CONST               0
              332  BINARY_SUBSCR    
            334_0  COME_FROM           326  '326'
              334  STORE_FAST               'r_first_'

 L.  78       336  LOAD_GLOBAL              set
              338  CALL_FUNCTION_0       0  '0 positional arguments'
              340  STORE_FAST               'candidates'

 L.  80       342  LOAD_FAST                'debug'
          344_346  POP_JUMP_IF_FALSE   376  'to 376'

 L.  81       348  LOAD_GLOBAL              print
              350  LOAD_STR                 'l_last = {}'
              352  LOAD_METHOD              format
              354  LOAD_FAST                'l_last'
              356  CALL_METHOD_1         1  '1 positional argument'
              358  CALL_FUNCTION_1       1  '1 positional argument'
              360  POP_TOP          

 L.  82       362  LOAD_GLOBAL              print
              364  LOAD_STR                 'r_first = {}'
              366  LOAD_METHOD              format
              368  LOAD_FAST                'r_first'
              370  CALL_METHOD_1         1  '1 positional argument'
              372  CALL_FUNCTION_1       1  '1 positional argument'
              374  POP_TOP          
            376_0  COME_FROM           344  '344'

 L.  84       376  LOAD_FAST                'ending'
              378  LOAD_CONST               0
              380  BINARY_SUBSCR    
              382  LOAD_STR                 '다'
              384  COMPARE_OP               ==
          386_388  POP_JUMP_IF_FALSE   428  'to 428'

 L.  85       390  LOAD_FAST                'stem'
              392  LOAD_FAST                'ending'
              394  BINARY_ADD       
              396  STORE_FAST               'surface'

 L.  86       398  LOAD_FAST                'candidates'
              400  LOAD_METHOD              add
              402  LOAD_FAST                'surface'
              404  CALL_METHOD_1         1  '1 positional argument'
              406  POP_TOP          

 L.  87       408  LOAD_FAST                'debug'
          410_412  POP_JUMP_IF_FALSE   428  'to 428'

 L.  88       414  LOAD_GLOBAL              print
              416  LOAD_STR                 "'다'로 시작하는 어미: {}"
              418  LOAD_METHOD              format
              420  LOAD_FAST                'surface'
              422  CALL_METHOD_1         1  '1 positional argument'
              424  CALL_FUNCTION_1       1  '1 positional argument'
              426  POP_TOP          
            428_0  COME_FROM           410  '410'
            428_1  COME_FROM           386  '386'

 L.  91       428  LOAD_FAST                'l_last'
              430  LOAD_CONST               2
              432  BINARY_SUBSCR    
              434  LOAD_STR                 'ㄷ'
              436  COMPARE_OP               ==
          438_440  POP_JUMP_IF_FALSE   540  'to 540'
              442  LOAD_FAST                'r_first'
              444  LOAD_CONST               0
              446  BINARY_SUBSCR    
              448  LOAD_STR                 'ㅇ'
              450  COMPARE_OP               ==
          452_454  POP_JUMP_IF_FALSE   540  'to 540'

 L.  92       456  LOAD_FAST                'stem'
              458  LOAD_CONST               None
              460  LOAD_CONST               -1
              462  BUILD_SLICE_2         2 
              464  BINARY_SUBSCR    
              466  LOAD_GLOBAL              compose
              468  LOAD_FAST                'l_last'
              470  LOAD_CONST               0
              472  BINARY_SUBSCR    
              474  LOAD_FAST                'l_last'
              476  LOAD_CONST               1
              478  BINARY_SUBSCR    
              480  LOAD_STR                 'ㄹ'
              482  CALL_FUNCTION_3       3  '3 positional arguments'
              484  BINARY_ADD       
              486  STORE_FAST               'l'

 L.  93       488  LOAD_FAST                'l'
              490  LOAD_FAST                'ending'
              492  BINARY_ADD       
              494  STORE_FAST               'surface'

 L.  94       496  LOAD_FAST                'candidates'
              498  LOAD_METHOD              add
              500  LOAD_FAST                'surface'
              502  CALL_METHOD_1         1  '1 positional argument'
              504  POP_TOP          

 L.  95       506  LOAD_FAST                'candidates'
              508  LOAD_METHOD              add
              510  LOAD_FAST                'stem'
              512  LOAD_FAST                'ending'
              514  BINARY_ADD       
              516  CALL_METHOD_1         1  '1 positional argument'
              518  POP_TOP          

 L.  96       520  LOAD_FAST                'debug'
          522_524  POP_JUMP_IF_FALSE   540  'to 540'

 L.  97       526  LOAD_GLOBAL              print
              528  LOAD_STR                 'ㄷ 불규칙: {}'
              530  LOAD_METHOD              format
              532  LOAD_FAST                'surface'
              534  CALL_METHOD_1         1  '1 positional argument'
              536  CALL_FUNCTION_1       1  '1 positional argument'
              538  POP_TOP          
            540_0  COME_FROM           522  '522'
            540_1  COME_FROM           452  '452'
            540_2  COME_FROM           438  '438'

 L. 100       540  LOAD_FAST                'l_last_'
              542  LOAD_STR                 '르'
              544  COMPARE_OP               ==
          546_548  POP_JUMP_IF_FALSE   710  'to 710'
              550  LOAD_FAST                'stem'
              552  LOAD_CONST               -2
              554  LOAD_CONST               None
              556  BUILD_SLICE_2         2 
              558  BINARY_SUBSCR    
              560  LOAD_STR                 '푸르'
              562  COMPARE_OP               !=
          564_566  POP_JUMP_IF_FALSE   710  'to 710'

 L. 101       568  LOAD_FAST                'r_first_'
              570  LOAD_STR                 '아'
              572  COMPARE_OP               ==
          574_576  POP_JUMP_IF_TRUE    588  'to 588'
              578  LOAD_FAST                'r_first_'
              580  LOAD_STR                 '어'
              582  COMPARE_OP               ==
          584_586  POP_JUMP_IF_FALSE   710  'to 710'
            588_0  COME_FROM           574  '574'
              588  LOAD_FAST                'l_len'
              590  LOAD_CONST               2
              592  COMPARE_OP               >=
          594_596  POP_JUMP_IF_FALSE   710  'to 710'

 L. 102       598  LOAD_GLOBAL              decompose
              600  LOAD_FAST                'stem'
              602  LOAD_CONST               -2
              604  BINARY_SUBSCR    
              606  CALL_FUNCTION_1       1  '1 positional argument'
              608  UNPACK_SEQUENCE_3     3 
              610  STORE_FAST               'c0'
              612  STORE_FAST               'c1'
              614  STORE_FAST               'c2'

 L. 103       616  LOAD_FAST                'stem'
              618  LOAD_CONST               None
              620  LOAD_CONST               -2
              622  BUILD_SLICE_2         2 
              624  BINARY_SUBSCR    
              626  LOAD_GLOBAL              compose
              628  LOAD_FAST                'c0'
              630  LOAD_FAST                'c1'
              632  LOAD_STR                 'ㄹ'
              634  CALL_FUNCTION_3       3  '3 positional arguments'
              636  BINARY_ADD       
              638  STORE_FAST               'l'

 L. 104       640  LOAD_GLOBAL              compose
              642  LOAD_STR                 'ㄹ'
              644  LOAD_FAST                'r_first'
              646  LOAD_CONST               1
              648  BINARY_SUBSCR    
              650  LOAD_FAST                'r_first'
              652  LOAD_CONST               2
              654  BINARY_SUBSCR    
              656  CALL_FUNCTION_3       3  '3 positional arguments'
              658  LOAD_FAST                'ending'
              660  LOAD_CONST               1
              662  LOAD_CONST               None
              664  BUILD_SLICE_2         2 
              666  BINARY_SUBSCR    
              668  BINARY_ADD       
              670  STORE_FAST               'r'

 L. 105       672  LOAD_FAST                'l'
              674  LOAD_FAST                'r'
              676  BINARY_ADD       
              678  STORE_FAST               'surface'

 L. 106       680  LOAD_FAST                'candidates'
              682  LOAD_METHOD              add
              684  LOAD_FAST                'surface'
              686  CALL_METHOD_1         1  '1 positional argument'
              688  POP_TOP          

 L. 107       690  LOAD_FAST                'debug'
          692_694  POP_JUMP_IF_FALSE   710  'to 710'

 L. 108       696  LOAD_GLOBAL              print
              698  LOAD_STR                 '르 불규칙: {}'
              700  LOAD_METHOD              format
              702  LOAD_FAST                'surface'
              704  CALL_METHOD_1         1  '1 positional argument'
              706  CALL_FUNCTION_1       1  '1 positional argument'
              708  POP_TOP          
            710_0  COME_FROM           692  '692'
            710_1  COME_FROM           594  '594'
            710_2  COME_FROM           584  '584'
            710_3  COME_FROM           564  '564'
            710_4  COME_FROM           546  '546'

 L. 113       710  LOAD_FAST                'l_last'
              712  LOAD_CONST               2
              714  BINARY_SUBSCR    
              716  LOAD_STR                 'ㅂ'
              718  COMPARE_OP               ==
          720_722  POP_JUMP_IF_FALSE  1012  'to 1012'

 L. 114       724  LOAD_FAST                'stem'
              726  LOAD_CONST               None
              728  LOAD_CONST               -1
              730  BUILD_SLICE_2         2 
              732  BINARY_SUBSCR    
              734  LOAD_GLOBAL              compose
              736  LOAD_FAST                'l_last'
              738  LOAD_CONST               0
              740  BINARY_SUBSCR    
              742  LOAD_FAST                'l_last'
              744  LOAD_CONST               1
              746  BINARY_SUBSCR    
              748  LOAD_STR                 ' '
              750  CALL_FUNCTION_3       3  '3 positional arguments'
              752  BINARY_ADD       
              754  STORE_FAST               'l'

 L. 115       756  LOAD_FAST                'r_first_'
              758  LOAD_STR                 '어'
              760  COMPARE_OP               ==
          762_764  POP_JUMP_IF_TRUE    776  'to 776'
              766  LOAD_FAST                'r_first_'
              768  LOAD_STR                 '아'
              770  COMPARE_OP               ==
          772_774  POP_JUMP_IF_FALSE   960  'to 960'
            776_0  COME_FROM           762  '762'

 L. 116       776  LOAD_FAST                'l_len'
              778  LOAD_CONST               2
              780  COMPARE_OP               >=
          782_784  POP_JUMP_IF_FALSE   832  'to 832'
              786  LOAD_FAST                'l_last_'
              788  LOAD_STR                 '답'
              790  COMPARE_OP               ==
          792_794  POP_JUMP_IF_TRUE    826  'to 826'
              796  LOAD_FAST                'l_last_'
              798  LOAD_STR                 '곱'
              800  COMPARE_OP               ==
          802_804  POP_JUMP_IF_TRUE    826  'to 826'
              806  LOAD_FAST                'l_last_'
              808  LOAD_STR                 '깝'
              810  COMPARE_OP               ==
          812_814  POP_JUMP_IF_TRUE    826  'to 826'
              816  LOAD_FAST                'l_last_'
              818  LOAD_STR                 '롭'
              820  COMPARE_OP               ==
          822_824  POP_JUMP_IF_FALSE   832  'to 832'
            826_0  COME_FROM           812  '812'
            826_1  COME_FROM           802  '802'
            826_2  COME_FROM           792  '792'

 L. 117       826  LOAD_STR                 'ㅝ'
              828  STORE_FAST               'c1'
              830  JUMP_FORWARD        892  'to 892'
            832_0  COME_FROM           822  '822'
            832_1  COME_FROM           782  '782'

 L. 118       832  LOAD_FAST                'r_first'
              834  LOAD_CONST               1
              836  BINARY_SUBSCR    
              838  LOAD_STR                 'ㅗ'
              840  COMPARE_OP               ==
          842_844  POP_JUMP_IF_FALSE   852  'to 852'

 L. 119       846  LOAD_STR                 'ㅘ'
              848  STORE_FAST               'c1'
              850  JUMP_FORWARD        892  'to 892'
            852_0  COME_FROM           842  '842'

 L. 120       852  LOAD_FAST                'r_first'
              854  LOAD_CONST               1
              856  BINARY_SUBSCR    
              858  LOAD_STR                 'ㅜ'
              860  COMPARE_OP               ==
          862_864  POP_JUMP_IF_FALSE   872  'to 872'

 L. 121       866  LOAD_STR                 'ㅝ'
              868  STORE_FAST               'c1'
              870  JUMP_FORWARD        892  'to 892'
            872_0  COME_FROM           862  '862'

 L. 122       872  LOAD_FAST                'r_first_'
              874  LOAD_STR                 '어'
              876  COMPARE_OP               ==
          878_880  POP_JUMP_IF_FALSE   888  'to 888'

 L. 123       882  LOAD_STR                 'ㅝ'
              884  STORE_FAST               'c1'
              886  JUMP_FORWARD        892  'to 892'
            888_0  COME_FROM           878  '878'

 L. 125       888  LOAD_STR                 'ㅘ'
              890  STORE_FAST               'c1'
            892_0  COME_FROM           886  '886'
            892_1  COME_FROM           870  '870'
            892_2  COME_FROM           850  '850'
            892_3  COME_FROM           830  '830'

 L. 126       892  LOAD_GLOBAL              compose
              894  LOAD_STR                 'ㅇ'
              896  LOAD_FAST                'c1'
              898  LOAD_FAST                'r_first'
              900  LOAD_CONST               2
              902  BINARY_SUBSCR    
              904  CALL_FUNCTION_3       3  '3 positional arguments'
              906  LOAD_FAST                'ending'
              908  LOAD_CONST               1
              910  LOAD_CONST               None
              912  BUILD_SLICE_2         2 
              914  BINARY_SUBSCR    
              916  BINARY_ADD       
              918  STORE_FAST               'r'

 L. 127       920  LOAD_FAST                'l'
              922  LOAD_FAST                'r'
              924  BINARY_ADD       
              926  STORE_FAST               'surface'

 L. 128       928  LOAD_FAST                'candidates'
              930  LOAD_METHOD              add
              932  LOAD_FAST                'surface'
              934  CALL_METHOD_1         1  '1 positional argument'
              936  POP_TOP          

 L. 129       938  LOAD_FAST                'debug'
          940_942  POP_JUMP_IF_FALSE  1012  'to 1012'

 L. 130       944  LOAD_GLOBAL              print
              946  LOAD_STR                 'ㅂ 불규칙: {}'
              948  LOAD_METHOD              format
              950  LOAD_FAST                'surface'
              952  CALL_METHOD_1         1  '1 positional argument'
              954  CALL_FUNCTION_1       1  '1 positional argument'
              956  POP_TOP          
              958  JUMP_FORWARD       1012  'to 1012'
            960_0  COME_FROM           772  '772'

 L. 131       960  LOAD_FAST                'r_first'
              962  LOAD_CONST               0
              964  BINARY_SUBSCR    
              966  LOAD_STR                 'ㅇ'
              968  COMPARE_OP               ==
          970_972  POP_JUMP_IF_FALSE  1012  'to 1012'

 L. 132       974  LOAD_FAST                'l'
              976  LOAD_FAST                'ending'
              978  BINARY_ADD       
              980  STORE_FAST               'surface'

 L. 133       982  LOAD_FAST                'candidates'
              984  LOAD_METHOD              add
              986  LOAD_FAST                'surface'
              988  CALL_METHOD_1         1  '1 positional argument'
              990  POP_TOP          

 L. 134       992  LOAD_FAST                'debug'
          994_996  POP_JUMP_IF_FALSE  1012  'to 1012'

 L. 135       998  LOAD_GLOBAL              print
             1000  LOAD_STR                 'ㅂ 불규칙: {}'
             1002  LOAD_METHOD              format
             1004  LOAD_FAST                'surface'
             1006  CALL_METHOD_1         1  '1 positional argument'
             1008  CALL_FUNCTION_1       1  '1 positional argument'
             1010  POP_TOP          
           1012_0  COME_FROM           994  '994'
           1012_1  COME_FROM           970  '970'
           1012_2  COME_FROM           958  '958'
           1012_3  COME_FROM           940  '940'
           1012_4  COME_FROM           720  '720'

 L. 139      1012  LOAD_FAST                'r_first'
             1014  LOAD_CONST               1
             1016  BINARY_SUBSCR    
             1018  LOAD_STR                 ' '
             1020  COMPARE_OP               ==
         1022_1024  POP_JUMP_IF_FALSE  1210  'to 1210'
             1026  LOAD_FAST                'r_first'
             1028  LOAD_CONST               0
             1030  BINARY_SUBSCR    
             1032  LOAD_STR                 'ㄴ'
             1034  COMPARE_OP               ==
         1036_1038  POP_JUMP_IF_TRUE   1096  'to 1096'
             1040  LOAD_FAST                'r_first'
             1042  LOAD_CONST               0
             1044  BINARY_SUBSCR    
             1046  LOAD_STR                 'ㄹ'
             1048  COMPARE_OP               ==
         1050_1052  POP_JUMP_IF_TRUE   1096  'to 1096'
             1054  LOAD_FAST                'r_first'
             1056  LOAD_CONST               0
             1058  BINARY_SUBSCR    
             1060  LOAD_STR                 'ㅁ'
             1062  COMPARE_OP               ==
         1064_1066  POP_JUMP_IF_TRUE   1096  'to 1096'
             1068  LOAD_FAST                'r_first'
             1070  LOAD_CONST               0
             1072  BINARY_SUBSCR    
             1074  LOAD_STR                 'ㅂ'
             1076  COMPARE_OP               ==
         1078_1080  POP_JUMP_IF_TRUE   1096  'to 1096'
             1082  LOAD_FAST                'r_first'
             1084  LOAD_CONST               0
             1086  BINARY_SUBSCR    
             1088  LOAD_STR                 'ㅆ'
             1090  COMPARE_OP               ==
         1092_1094  POP_JUMP_IF_FALSE  1210  'to 1210'
           1096_0  COME_FROM          1078  '1078'
           1096_1  COME_FROM          1064  '1064'
           1096_2  COME_FROM          1050  '1050'
           1096_3  COME_FROM          1036  '1036'

 L. 140      1096  LOAD_FAST                'stem'
             1098  LOAD_CONST               None
             1100  LOAD_CONST               -1
             1102  BUILD_SLICE_2         2 
             1104  BINARY_SUBSCR    
             1106  LOAD_GLOBAL              compose
             1108  LOAD_FAST                'l_last'
             1110  LOAD_CONST               0
             1112  BINARY_SUBSCR    
             1114  LOAD_FAST                'l_last'
             1116  LOAD_CONST               1
             1118  BINARY_SUBSCR    
             1120  LOAD_FAST                'r_first'
             1122  LOAD_CONST               0
             1124  BINARY_SUBSCR    
             1126  CALL_FUNCTION_3       3  '3 positional arguments'
             1128  BINARY_ADD       
             1130  STORE_FAST               'l'

 L. 141      1132  LOAD_FAST                'ending'
             1134  LOAD_CONST               1
             1136  LOAD_CONST               None
             1138  BUILD_SLICE_2         2 
             1140  BINARY_SUBSCR    
             1142  STORE_FAST               'r'

 L. 142      1144  LOAD_FAST                'l'
             1146  LOAD_FAST                'r'
             1148  BINARY_ADD       
             1150  STORE_FAST               'surface'

 L. 143      1152  LOAD_FAST                'candidates'
             1154  LOAD_METHOD              add
             1156  LOAD_FAST                'surface'
             1158  CALL_METHOD_1         1  '1 positional argument'
             1160  POP_TOP          

 L. 144      1162  LOAD_FAST                'r_first'
             1164  LOAD_CONST               1
             1166  BINARY_SUBSCR    
             1168  LOAD_STR                 ' '
             1170  COMPARE_OP               !=
         1172_1174  POP_JUMP_IF_FALSE  1190  'to 1190'

 L. 145      1176  LOAD_FAST                'candidates'
             1178  LOAD_METHOD              add
             1180  LOAD_FAST                'stem'
             1182  LOAD_FAST                'ending'
             1184  BINARY_ADD       
             1186  CALL_METHOD_1         1  '1 positional argument'
             1188  POP_TOP          
           1190_0  COME_FROM          1172  '1172'

 L. 146      1190  LOAD_FAST                'debug'
         1192_1194  POP_JUMP_IF_FALSE  1210  'to 1210'

 L. 147      1196  LOAD_GLOBAL              print
             1198  LOAD_STR                 '어미의 첫 글자가 -ㄴ, -ㄹ, -ㅁ-, -ㅂ, -ㅆ 인 경우: {}'
             1200  LOAD_METHOD              format
             1202  LOAD_FAST                'surface'
             1204  CALL_METHOD_1         1  '1 positional argument'
             1206  CALL_FUNCTION_1       1  '1 positional argument'
             1208  POP_TOP          
           1210_0  COME_FROM          1192  '1192'
           1210_1  COME_FROM          1092  '1092'
           1210_2  COME_FROM          1022  '1022'

 L. 151      1210  LOAD_FAST                'l_last'
             1212  LOAD_CONST               2
             1214  BINARY_SUBSCR    
             1216  LOAD_STR                 'ㅅ'
             1218  COMPARE_OP               ==
         1220_1222  POP_JUMP_IF_FALSE  1328  'to 1328'
             1224  LOAD_FAST                'r_first'
             1226  LOAD_CONST               0
             1228  BINARY_SUBSCR    
             1230  LOAD_STR                 'ㅇ'
             1232  COMPARE_OP               ==
         1234_1236  POP_JUMP_IF_FALSE  1328  'to 1328'

 L. 152      1238  LOAD_FAST                'stem'
             1240  LOAD_CONST               -1
             1242  BINARY_SUBSCR    
             1244  LOAD_STR                 '벗'
             1246  COMPARE_OP               ==
         1248_1250  POP_JUMP_IF_FALSE  1258  'to 1258'

 L. 153      1252  LOAD_FAST                'stem'
             1254  STORE_FAST               'l'
             1256  JUMP_FORWARD       1290  'to 1290'
           1258_0  COME_FROM          1248  '1248'

 L. 155      1258  LOAD_FAST                'stem'
             1260  LOAD_CONST               None
             1262  LOAD_CONST               -1
             1264  BUILD_SLICE_2         2 
             1266  BINARY_SUBSCR    
             1268  LOAD_GLOBAL              compose
             1270  LOAD_FAST                'l_last'
             1272  LOAD_CONST               0
             1274  BINARY_SUBSCR    
             1276  LOAD_FAST                'l_last'
             1278  LOAD_CONST               1
             1280  BINARY_SUBSCR    
             1282  LOAD_STR                 ' '
             1284  CALL_FUNCTION_3       3  '3 positional arguments'
             1286  BINARY_ADD       
             1288  STORE_FAST               'l'
           1290_0  COME_FROM          1256  '1256'

 L. 156      1290  LOAD_FAST                'l'
             1292  LOAD_FAST                'ending'
             1294  BINARY_ADD       
             1296  STORE_FAST               'surface'

 L. 157      1298  LOAD_FAST                'candidates'
             1300  LOAD_METHOD              add
             1302  LOAD_FAST                'surface'
             1304  CALL_METHOD_1         1  '1 positional argument'
             1306  POP_TOP          

 L. 158      1308  LOAD_FAST                'debug'
         1310_1312  POP_JUMP_IF_FALSE  1328  'to 1328'

 L. 159      1314  LOAD_GLOBAL              print
             1316  LOAD_STR                 'ㅅ 불규칙: {}'
             1318  LOAD_METHOD              format
             1320  LOAD_FAST                'surface'
             1322  CALL_METHOD_1         1  '1 positional argument'
             1324  CALL_FUNCTION_1       1  '1 positional argument'
             1326  POP_TOP          
           1328_0  COME_FROM          1310  '1310'
           1328_1  COME_FROM          1234  '1234'
           1328_2  COME_FROM          1220  '1220'

 L. 162      1328  LOAD_FAST                'l_last'
             1330  LOAD_CONST               1
             1332  BINARY_SUBSCR    
             1334  LOAD_STR                 'ㅜ'
             1336  COMPARE_OP               ==
         1338_1340  POP_JUMP_IF_FALSE  1494  'to 1494'
             1342  LOAD_FAST                'l_last'
             1344  LOAD_CONST               2
             1346  BINARY_SUBSCR    
             1348  LOAD_STR                 ' '
             1350  COMPARE_OP               ==
         1352_1354  POP_JUMP_IF_FALSE  1494  'to 1494'
             1356  LOAD_FAST                'r_first'
             1358  LOAD_CONST               0
             1360  BINARY_SUBSCR    
             1362  LOAD_STR                 'ㅇ'
             1364  COMPARE_OP               ==
         1366_1368  POP_JUMP_IF_FALSE  1494  'to 1494'
             1370  LOAD_FAST                'r_first'
             1372  LOAD_CONST               1
             1374  BINARY_SUBSCR    
             1376  LOAD_STR                 'ㅓ'
             1378  COMPARE_OP               ==
         1380_1382  POP_JUMP_IF_FALSE  1494  'to 1494'

 L. 163      1384  LOAD_FAST                'l_last_'
             1386  LOAD_STR                 '푸'
             1388  COMPARE_OP               ==
         1390_1392  POP_JUMP_IF_FALSE  1412  'to 1412'

 L. 164      1394  LOAD_FAST                'stem'
             1396  LOAD_CONST               None
             1398  LOAD_CONST               -1
             1400  BUILD_SLICE_2         2 
             1402  BINARY_SUBSCR    
             1404  LOAD_STR                 '퍼'
             1406  BINARY_ADD       
             1408  STORE_FAST               'l'
             1410  JUMP_FORWARD       1444  'to 1444'
           1412_0  COME_FROM          1390  '1390'

 L. 166      1412  LOAD_FAST                'stem'
             1414  LOAD_CONST               None
             1416  LOAD_CONST               -1
             1418  BUILD_SLICE_2         2 
             1420  BINARY_SUBSCR    
             1422  LOAD_GLOBAL              compose
             1424  LOAD_FAST                'l_last'
             1426  LOAD_CONST               0
             1428  BINARY_SUBSCR    
             1430  LOAD_STR                 'ㅝ'
             1432  LOAD_FAST                'r_first'
             1434  LOAD_CONST               2
             1436  BINARY_SUBSCR    
             1438  CALL_FUNCTION_3       3  '3 positional arguments'
             1440  BINARY_ADD       
             1442  STORE_FAST               'l'
           1444_0  COME_FROM          1410  '1410'

 L. 167      1444  LOAD_FAST                'ending'
             1446  LOAD_CONST               1
             1448  LOAD_CONST               None
             1450  BUILD_SLICE_2         2 
             1452  BINARY_SUBSCR    
             1454  STORE_FAST               'r'

 L. 168      1456  LOAD_FAST                'l'
             1458  LOAD_FAST                'r'
             1460  BINARY_ADD       
             1462  STORE_FAST               'surface'

 L. 169      1464  LOAD_FAST                'candidates'
             1466  LOAD_METHOD              add
             1468  LOAD_FAST                'surface'
             1470  CALL_METHOD_1         1  '1 positional argument'
             1472  POP_TOP          

 L. 170      1474  LOAD_FAST                'debug'
         1476_1478  POP_JUMP_IF_FALSE  1494  'to 1494'

 L. 171      1480  LOAD_GLOBAL              print
             1482  LOAD_STR                 '우 불규칙: {}'
             1484  LOAD_METHOD              format
             1486  LOAD_FAST                'surface'
             1488  CALL_METHOD_1         1  '1 positional argument'
             1490  CALL_FUNCTION_1       1  '1 positional argument'
             1492  POP_TOP          
           1494_0  COME_FROM          1476  '1476'
           1494_1  COME_FROM          1380  '1380'
           1494_2  COME_FROM          1366  '1366'
           1494_3  COME_FROM          1352  '1352'
           1494_4  COME_FROM          1338  '1338'

 L. 174      1494  LOAD_FAST                'l_last'
             1496  LOAD_CONST               1
             1498  BINARY_SUBSCR    
             1500  LOAD_STR                 'ㅗ'
             1502  COMPARE_OP               ==
         1504_1506  POP_JUMP_IF_FALSE  1632  'to 1632'
             1508  LOAD_FAST                'l_last'
             1510  LOAD_CONST               2
             1512  BINARY_SUBSCR    
             1514  LOAD_STR                 ' '
             1516  COMPARE_OP               ==
         1518_1520  POP_JUMP_IF_FALSE  1632  'to 1632'
             1522  LOAD_FAST                'r_first'
             1524  LOAD_CONST               0
             1526  BINARY_SUBSCR    
             1528  LOAD_STR                 'ㅇ'
             1530  COMPARE_OP               ==
         1532_1534  POP_JUMP_IF_FALSE  1632  'to 1632'
             1536  LOAD_FAST                'r_first'
             1538  LOAD_CONST               1
             1540  BINARY_SUBSCR    
             1542  LOAD_STR                 'ㅏ'
             1544  COMPARE_OP               ==
         1546_1548  POP_JUMP_IF_FALSE  1632  'to 1632'

 L. 175      1550  LOAD_FAST                'stem'
             1552  LOAD_CONST               None
             1554  LOAD_CONST               -1
             1556  BUILD_SLICE_2         2 
             1558  BINARY_SUBSCR    
             1560  LOAD_GLOBAL              compose
             1562  LOAD_FAST                'l_last'
             1564  LOAD_CONST               0
             1566  BINARY_SUBSCR    
             1568  LOAD_STR                 'ㅘ'
             1570  LOAD_FAST                'r_first'
             1572  LOAD_CONST               2
             1574  BINARY_SUBSCR    
             1576  CALL_FUNCTION_3       3  '3 positional arguments'
             1578  BINARY_ADD       
             1580  STORE_FAST               'l'

 L. 176      1582  LOAD_FAST                'ending'
             1584  LOAD_CONST               1
             1586  LOAD_CONST               None
             1588  BUILD_SLICE_2         2 
             1590  BINARY_SUBSCR    
             1592  STORE_FAST               'r'

 L. 177      1594  LOAD_FAST                'l'
             1596  LOAD_FAST                'r'
             1598  BINARY_ADD       
             1600  STORE_FAST               'surface'

 L. 178      1602  LOAD_FAST                'candidates'
             1604  LOAD_METHOD              add
             1606  LOAD_FAST                'surface'
             1608  CALL_METHOD_1         1  '1 positional argument'
             1610  POP_TOP          

 L. 179      1612  LOAD_FAST                'debug'
         1614_1616  POP_JUMP_IF_FALSE  1632  'to 1632'

 L. 180      1618  LOAD_GLOBAL              print
             1620  LOAD_STR                 '오 활용: {}'
             1622  LOAD_METHOD              format
             1624  LOAD_FAST                'surface'
             1626  CALL_METHOD_1         1  '1 positional argument'
             1628  CALL_FUNCTION_1       1  '1 positional argument'
             1630  POP_TOP          
           1632_0  COME_FROM          1614  '1614'
           1632_1  COME_FROM          1546  '1546'
           1632_2  COME_FROM          1532  '1532'
           1632_3  COME_FROM          1518  '1518'
           1632_4  COME_FROM          1504  '1504'

 L. 183      1632  LOAD_FAST                'l_last'
             1634  LOAD_CONST               1
             1636  BINARY_SUBSCR    
             1638  LOAD_STR                 'ㅡ'
             1640  COMPARE_OP               ==
         1642_1644  POP_JUMP_IF_FALSE  1838  'to 1838'
             1646  LOAD_FAST                'l_last'
             1648  LOAD_CONST               2
             1650  BINARY_SUBSCR    
             1652  LOAD_STR                 ' '
             1654  COMPARE_OP               ==
         1656_1658  POP_JUMP_IF_FALSE  1838  'to 1838'
             1660  LOAD_FAST                'r_first'
             1662  LOAD_CONST               0
             1664  BINARY_SUBSCR    
             1666  LOAD_STR                 'ㅇ'
             1668  COMPARE_OP               ==
         1670_1672  POP_JUMP_IF_FALSE  1838  'to 1838'

 L. 184      1674  LOAD_FAST                'l_last'
             1676  LOAD_CONST               0
             1678  BINARY_SUBSCR    
             1680  LOAD_STR                 'ㅇ'
             1682  COMPARE_OP               ==
         1684_1686  POP_JUMP_IF_FALSE  1720  'to 1720'
             1688  LOAD_GLOBAL              len
             1690  LOAD_FAST                'stem'
             1692  CALL_FUNCTION_1       1  '1 positional argument'
             1694  LOAD_CONST               1
             1696  COMPARE_OP               >
         1698_1700  POP_JUMP_IF_FALSE  1720  'to 1720'

 L. 185      1702  LOAD_FAST                'stem'
             1704  LOAD_CONST               None
             1706  LOAD_CONST               -1
             1708  BUILD_SLICE_2         2 
             1710  BINARY_SUBSCR    
             1712  LOAD_FAST                'ending'
             1714  BINARY_ADD       
             1716  STORE_FAST               'surface'
             1718  JUMP_FORWARD       1788  'to 1788'
           1720_0  COME_FROM          1698  '1698'
           1720_1  COME_FROM          1684  '1684'

 L. 186      1720  LOAD_FAST                'l_last'
             1722  LOAD_CONST               0
             1724  BINARY_SUBSCR    
             1726  LOAD_STR                 'ㄹ'
             1728  COMPARE_OP               !=
         1730_1732  POP_JUMP_IF_FALSE  1784  'to 1784'

 L. 187      1734  LOAD_FAST                'stem'
             1736  LOAD_CONST               None
             1738  LOAD_CONST               -1
             1740  BUILD_SLICE_2         2 
             1742  BINARY_SUBSCR    
             1744  LOAD_GLOBAL              compose
             1746  LOAD_FAST                'l_last'
             1748  LOAD_CONST               0
             1750  BINARY_SUBSCR    
             1752  LOAD_FAST                'r_first'
             1754  LOAD_CONST               1
             1756  BINARY_SUBSCR    
             1758  LOAD_FAST                'r_first'
             1760  LOAD_CONST               2
             1762  BINARY_SUBSCR    
             1764  CALL_FUNCTION_3       3  '3 positional arguments'
             1766  BINARY_ADD       
             1768  LOAD_FAST                'ending'
             1770  LOAD_CONST               1
             1772  LOAD_CONST               None
             1774  BUILD_SLICE_2         2 
             1776  BINARY_SUBSCR    
             1778  BINARY_ADD       
             1780  STORE_FAST               'surface'
             1782  JUMP_FORWARD       1788  'to 1788'
           1784_0  COME_FROM          1730  '1730'

 L. 189      1784  LOAD_CONST               None
             1786  STORE_FAST               'surface'
           1788_0  COME_FROM          1782  '1782'
           1788_1  COME_FROM          1718  '1718'

 L. 190      1788  LOAD_FAST                'surface'
             1790  LOAD_CONST               None
             1792  COMPARE_OP               is-not
         1794_1796  POP_JUMP_IF_FALSE  1808  'to 1808'

 L. 191      1798  LOAD_FAST                'candidates'
             1800  LOAD_METHOD              add
             1802  LOAD_FAST                'surface'
             1804  CALL_METHOD_1         1  '1 positional argument'
             1806  POP_TOP          
           1808_0  COME_FROM          1794  '1794'

 L. 192      1808  LOAD_FAST                'debug'
         1810_1812  POP_JUMP_IF_FALSE  1838  'to 1838'
             1814  LOAD_FAST                'surface'
             1816  LOAD_CONST               None
             1818  COMPARE_OP               is-not
         1820_1822  POP_JUMP_IF_FALSE  1838  'to 1838'

 L. 193      1824  LOAD_GLOBAL              print
             1826  LOAD_STR                 'ㅡ 탈락 불규칙: {}'
             1828  LOAD_METHOD              format
             1830  LOAD_FAST                'surface'
             1832  CALL_METHOD_1         1  '1 positional argument'
             1834  CALL_FUNCTION_1       1  '1 positional argument'
             1836  POP_TOP          
           1838_0  COME_FROM          1820  '1820'
           1838_1  COME_FROM          1810  '1810'
           1838_2  COME_FROM          1670  '1670'
           1838_3  COME_FROM          1656  '1656'
           1838_4  COME_FROM          1642  '1642'

 L. 197      1838  LOAD_FAST                'ending'
             1840  LOAD_CONST               None
             1842  LOAD_CONST               2
             1844  BUILD_SLICE_2         2 
             1846  BINARY_SUBSCR    
             1848  LOAD_STR                 '어라'
             1850  COMPARE_OP               ==
         1852_1854  POP_JUMP_IF_TRUE   1874  'to 1874'
             1856  LOAD_FAST                'ending'
             1858  LOAD_CONST               None
             1860  LOAD_CONST               2
             1862  BUILD_SLICE_2         2 
             1864  BINARY_SUBSCR    
             1866  LOAD_STR                 '아라'
             1868  COMPARE_OP               ==
         1870_1872  POP_JUMP_IF_FALSE  2088  'to 2088'
           1874_0  COME_FROM          1852  '1852'

 L. 199      1874  LOAD_FAST                'stem'
             1876  LOAD_CONST               -1
             1878  BINARY_SUBSCR    
             1880  LOAD_STR                 '오'
             1882  COMPARE_OP               ==
         1884_1886  POP_JUMP_IF_FALSE  1918  'to 1918'

 L. 200      1888  LOAD_FAST                'stem'
             1890  LOAD_CONST               None
             1892  LOAD_CONST               -1
             1894  BUILD_SLICE_2         2 
             1896  BINARY_SUBSCR    
             1898  STORE_FAST               'l'

 L. 201      1900  LOAD_STR                 '와'
             1902  LOAD_FAST                'ending'
             1904  LOAD_CONST               1
             1906  LOAD_CONST               None
             1908  BUILD_SLICE_2         2 
             1910  BINARY_SUBSCR    
             1912  BINARY_ADD       
             1914  STORE_FAST               'r'
             1916  JUMP_FORWARD       2050  'to 2050'
           1918_0  COME_FROM          1884  '1884'

 L. 203      1918  LOAD_FAST                'stem'
             1920  LOAD_CONST               -1
             1922  BINARY_SUBSCR    
             1924  LOAD_STR                 '우'
             1926  COMPARE_OP               ==
         1928_1930  POP_JUMP_IF_FALSE  1962  'to 1962'

 L. 204      1932  LOAD_FAST                'stem'
             1934  LOAD_CONST               None
             1936  LOAD_CONST               -1
             1938  BUILD_SLICE_2         2 
             1940  BINARY_SUBSCR    
             1942  STORE_FAST               'l'

 L. 205      1944  LOAD_STR                 '워'
             1946  LOAD_FAST                'ending'
             1948  LOAD_CONST               1
             1950  LOAD_CONST               None
             1952  BUILD_SLICE_2         2 
             1954  BINARY_SUBSCR    
             1956  BINARY_ADD       
             1958  STORE_FAST               'r'
             1960  JUMP_FORWARD       2050  'to 2050'
           1962_0  COME_FROM          1928  '1928'

 L. 207      1962  LOAD_FAST                'stem'
             1964  LOAD_CONST               -1
             1966  BINARY_SUBSCR    
             1968  LOAD_STR                 '가'
             1970  COMPARE_OP               ==
         1972_1974  POP_JUMP_IF_FALSE  1994  'to 1994'

 L. 208      1976  LOAD_FAST                'stem'
             1978  STORE_FAST               'l'

 L. 209      1980  LOAD_FAST                'ending'
             1982  LOAD_CONST               1
             1984  LOAD_CONST               None
             1986  BUILD_SLICE_2         2 
             1988  BINARY_SUBSCR    
             1990  STORE_FAST               'r'
             1992  JUMP_FORWARD       2050  'to 2050'
           1994_0  COME_FROM          1972  '1972'

 L. 211      1994  LOAD_FAST                'l_last'
             1996  LOAD_CONST               1
             1998  BINARY_SUBSCR    
             2000  LOAD_GLOBAL              negative_moum
             2002  COMPARE_OP               in
         2004_2006  POP_JUMP_IF_FALSE  2030  'to 2030'

 L. 212      2008  LOAD_FAST                'stem'
             2010  STORE_FAST               'l'

 L. 213      2012  LOAD_STR                 '어'
             2014  LOAD_FAST                'ending'
             2016  LOAD_CONST               1
             2018  LOAD_CONST               None
             2020  BUILD_SLICE_2         2 
             2022  BINARY_SUBSCR    
             2024  BINARY_ADD       
             2026  STORE_FAST               'r'
             2028  JUMP_FORWARD       2050  'to 2050'
           2030_0  COME_FROM          2004  '2004'

 L. 215      2030  LOAD_FAST                'stem'
             2032  STORE_FAST               'l'

 L. 216      2034  LOAD_STR                 '아'
             2036  LOAD_FAST                'ending'
             2038  LOAD_CONST               1
             2040  LOAD_CONST               None
             2042  BUILD_SLICE_2         2 
             2044  BINARY_SUBSCR    
             2046  BINARY_ADD       
             2048  STORE_FAST               'r'
           2050_0  COME_FROM          2028  '2028'
           2050_1  COME_FROM          1992  '1992'
           2050_2  COME_FROM          1960  '1960'
           2050_3  COME_FROM          1916  '1916'

 L. 217      2050  LOAD_FAST                'l'
             2052  LOAD_FAST                'r'
             2054  BINARY_ADD       
             2056  STORE_FAST               'surface'

 L. 218      2058  LOAD_FAST                'candidates'
             2060  LOAD_METHOD              add
             2062  LOAD_FAST                'surface'
             2064  CALL_METHOD_1         1  '1 positional argument'
             2066  POP_TOP          

 L. 219      2068  LOAD_FAST                'debug'
         2070_2072  POP_JUMP_IF_FALSE  2088  'to 2088'

 L. 220      2074  LOAD_GLOBAL              print
             2076  LOAD_STR                 '거라/너라 불규칙: {}'
             2078  LOAD_METHOD              format
             2080  LOAD_FAST                'surface'
             2082  CALL_METHOD_1         1  '1 positional argument'
             2084  CALL_FUNCTION_1       1  '1 positional argument'
             2086  POP_TOP          
           2088_0  COME_FROM          2070  '2070'
           2088_1  COME_FROM          1870  '1870'

 L. 223      2088  LOAD_FAST                'l_last_'
             2090  LOAD_STR                 '르'
             2092  COMPARE_OP               ==
         2094_2096  POP_JUMP_IF_FALSE  2214  'to 2214'
             2098  LOAD_FAST                'stem'
             2100  LOAD_CONST               -2
             2102  LOAD_CONST               None
             2104  BUILD_SLICE_2         2 
             2106  BINARY_SUBSCR    
             2108  LOAD_STR                 '구르'
             2110  COMPARE_OP               !=
         2112_2114  POP_JUMP_IF_FALSE  2214  'to 2214'

 L. 224      2116  LOAD_FAST                'r_first'
             2118  LOAD_CONST               0
             2120  BINARY_SUBSCR    
             2122  LOAD_STR                 'ㅇ'
             2124  COMPARE_OP               ==
         2126_2128  POP_JUMP_IF_FALSE  2214  'to 2214'
             2130  LOAD_FAST                'r_first'
             2132  LOAD_CONST               1
             2134  BINARY_SUBSCR    
             2136  LOAD_STR                 'ㅓ'
             2138  COMPARE_OP               ==
         2140_2142  POP_JUMP_IF_FALSE  2214  'to 2214'

 L. 225      2144  LOAD_GLOBAL              compose
             2146  LOAD_STR                 'ㄹ'
             2148  LOAD_FAST                'r_first'
             2150  LOAD_CONST               1
             2152  BINARY_SUBSCR    
             2154  LOAD_FAST                'r_first'
             2156  LOAD_CONST               2
             2158  BINARY_SUBSCR    
             2160  CALL_FUNCTION_3       3  '3 positional arguments'
             2162  LOAD_FAST                'ending'
             2164  LOAD_CONST               1
             2166  LOAD_CONST               None
             2168  BUILD_SLICE_2         2 
             2170  BINARY_SUBSCR    
             2172  BINARY_ADD       
             2174  STORE_FAST               'r'

 L. 226      2176  LOAD_FAST                'stem'
             2178  LOAD_FAST                'r'
             2180  BINARY_ADD       
             2182  STORE_FAST               'surface'

 L. 227      2184  LOAD_FAST                'candidates'
             2186  LOAD_METHOD              add
             2188  LOAD_FAST                'surface'
             2190  CALL_METHOD_1         1  '1 positional argument'
             2192  POP_TOP          

 L. 228      2194  LOAD_FAST                'debug'
         2196_2198  POP_JUMP_IF_FALSE  2214  'to 2214'

 L. 229      2200  LOAD_GLOBAL              print
             2202  LOAD_STR                 '러 불규칙: {}'
             2204  LOAD_METHOD              format
             2206  LOAD_FAST                'surface'
             2208  CALL_METHOD_1         1  '1 positional argument'
             2210  CALL_FUNCTION_1       1  '1 positional argument'
             2212  POP_TOP          
           2214_0  COME_FROM          2196  '2196'
           2214_1  COME_FROM          2140  '2140'
           2214_2  COME_FROM          2126  '2126'
           2214_3  COME_FROM          2112  '2112'
           2214_4  COME_FROM          2094  '2094'

 L. 233      2214  LOAD_FAST                'l_last_'
             2216  LOAD_STR                 '하'
             2218  COMPARE_OP               ==
         2220_2222  POP_JUMP_IF_FALSE  2396  'to 2396'
             2224  LOAD_FAST                'r_first'
             2226  LOAD_CONST               0
             2228  BINARY_SUBSCR    
             2230  LOAD_STR                 'ㅇ'
             2232  COMPARE_OP               ==
         2234_2236  POP_JUMP_IF_FALSE  2396  'to 2396'
             2238  LOAD_FAST                'r_first'
             2240  LOAD_CONST               1
             2242  BINARY_SUBSCR    
             2244  LOAD_STR                 'ㅏ'
             2246  COMPARE_OP               ==
         2248_2250  POP_JUMP_IF_TRUE   2266  'to 2266'
             2252  LOAD_FAST                'r_first'
             2254  LOAD_CONST               1
             2256  BINARY_SUBSCR    
             2258  LOAD_STR                 'ㅓ'
             2260  COMPARE_OP               ==
         2262_2264  POP_JUMP_IF_FALSE  2396  'to 2396'
           2266_0  COME_FROM          2248  '2248'

 L. 235      2266  LOAD_GLOBAL              compose
             2268  LOAD_FAST                'r_first'
             2270  LOAD_CONST               0
             2272  BINARY_SUBSCR    
             2274  LOAD_STR                 'ㅕ'
             2276  LOAD_FAST                'r_first'
             2278  LOAD_CONST               2
             2280  BINARY_SUBSCR    
             2282  CALL_FUNCTION_3       3  '3 positional arguments'
             2284  LOAD_FAST                'ending'
             2286  LOAD_CONST               1
             2288  LOAD_CONST               None
             2290  BUILD_SLICE_2         2 
             2292  BINARY_SUBSCR    
             2294  BINARY_ADD       
             2296  STORE_FAST               'r'

 L. 236      2298  LOAD_FAST                'stem'
             2300  LOAD_FAST                'r'
             2302  BINARY_ADD       
             2304  STORE_FAST               'surface0'

 L. 237      2306  LOAD_FAST                'candidates'
             2308  LOAD_METHOD              add
             2310  LOAD_FAST                'surface0'
             2312  CALL_METHOD_1         1  '1 positional argument'
             2314  POP_TOP          

 L. 239      2316  LOAD_FAST                'stem'
             2318  LOAD_CONST               None
             2320  LOAD_CONST               -1
             2322  BUILD_SLICE_2         2 
             2324  BINARY_SUBSCR    
             2326  LOAD_GLOBAL              compose
             2328  LOAD_STR                 'ㅎ'
             2330  LOAD_STR                 'ㅐ'
             2332  LOAD_FAST                'r_first'
             2334  LOAD_CONST               2
             2336  BINARY_SUBSCR    
             2338  CALL_FUNCTION_3       3  '3 positional arguments'
             2340  BINARY_ADD       
             2342  STORE_FAST               'l'

 L. 240      2344  LOAD_FAST                'ending'
             2346  LOAD_CONST               1
             2348  LOAD_CONST               None
             2350  BUILD_SLICE_2         2 
             2352  BINARY_SUBSCR    
             2354  STORE_FAST               'r'

 L. 241      2356  LOAD_FAST                'l'
             2358  LOAD_FAST                'r'
             2360  BINARY_ADD       
             2362  STORE_FAST               'surface1'

 L. 242      2364  LOAD_FAST                'candidates'
             2366  LOAD_METHOD              add
             2368  LOAD_FAST                'surface1'
             2370  CALL_METHOD_1         1  '1 positional argument'
             2372  POP_TOP          

 L. 243      2374  LOAD_FAST                'debug'
         2376_2378  POP_JUMP_IF_FALSE  2396  'to 2396'

 L. 244      2380  LOAD_GLOBAL              print
             2382  LOAD_STR                 '여 불규칙: {}, {}'
             2384  LOAD_METHOD              format
             2386  LOAD_FAST                'surface0'
             2388  LOAD_FAST                'surface1'
             2390  CALL_METHOD_2         2  '2 positional arguments'
             2392  CALL_FUNCTION_1       1  '1 positional argument'
             2394  POP_TOP          
           2396_0  COME_FROM          2376  '2376'
           2396_1  COME_FROM          2262  '2262'
           2396_2  COME_FROM          2234  '2234'
           2396_3  COME_FROM          2220  '2220'

 L. 248      2396  LOAD_FAST                'l_last'
             2398  LOAD_CONST               2
             2400  BINARY_SUBSCR    
             2402  LOAD_STR                 'ㅎ'
             2404  COMPARE_OP               ==
         2406_2408  POP_JUMP_IF_FALSE  2524  'to 2524'
             2410  LOAD_FAST                'r_first'
             2412  LOAD_CONST               1
             2414  BINARY_SUBSCR    
             2416  LOAD_STR                 ' '
             2418  COMPARE_OP               !=
         2420_2422  POP_JUMP_IF_FALSE  2524  'to 2524'

 L. 249      2424  LOAD_FAST                'l_last_'
             2426  LOAD_STR                 '좋'
             2428  COMPARE_OP               ==
         2430_2432  POP_JUMP_IF_TRUE   2444  'to 2444'
             2434  LOAD_FAST                'l_last_'
             2436  LOAD_STR                 '놓'
             2438  COMPARE_OP               ==
         2440_2442  POP_JUMP_IF_FALSE  2450  'to 2450'
           2444_0  COME_FROM          2430  '2430'

 L. 250      2444  LOAD_FAST                'stem'
             2446  STORE_FAST               'l'
             2448  JUMP_FORWARD       2482  'to 2482'
           2450_0  COME_FROM          2440  '2440'

 L. 252      2450  LOAD_FAST                'stem'
             2452  LOAD_CONST               None
             2454  LOAD_CONST               -1
             2456  BUILD_SLICE_2         2 
             2458  BINARY_SUBSCR    
             2460  LOAD_GLOBAL              compose
             2462  LOAD_FAST                'l_last'
             2464  LOAD_CONST               0
             2466  BINARY_SUBSCR    
             2468  LOAD_FAST                'l_last'
             2470  LOAD_CONST               1
             2472  BINARY_SUBSCR    
             2474  LOAD_STR                 ' '
             2476  CALL_FUNCTION_3       3  '3 positional arguments'
             2478  BINARY_ADD       
             2480  STORE_FAST               'l'
           2482_0  COME_FROM          2448  '2448'

 L. 253      2482  LOAD_FAST                'ending'
             2484  STORE_FAST               'r'

 L. 254      2486  LOAD_FAST                'l'
             2488  LOAD_FAST                'r'
             2490  BINARY_ADD       
             2492  STORE_FAST               'surface'

 L. 255      2494  LOAD_FAST                'candidates'
             2496  LOAD_METHOD              add
             2498  LOAD_FAST                'surface'
             2500  CALL_METHOD_1         1  '1 positional argument'
             2502  POP_TOP          

 L. 256      2504  LOAD_FAST                'debug'
         2506_2508  POP_JUMP_IF_FALSE  2524  'to 2524'

 L. 257      2510  LOAD_GLOBAL              print
             2512  LOAD_STR                 'ㅎ 탈락 불규칙: {}'
             2514  LOAD_METHOD              format
             2516  LOAD_FAST                'surface'
             2518  CALL_METHOD_1         1  '1 positional argument'
             2520  CALL_FUNCTION_1       1  '1 positional argument'
             2522  POP_TOP          
           2524_0  COME_FROM          2506  '2506'
           2524_1  COME_FROM          2420  '2420'
           2524_2  COME_FROM          2406  '2406'

 L. 261      2524  LOAD_FAST                'l_last'
             2526  LOAD_CONST               2
             2528  BINARY_SUBSCR    
             2530  LOAD_STR                 'ㅎ'
             2532  COMPARE_OP               ==
         2534_2536  POP_JUMP_IF_FALSE  2690  'to 2690'
             2538  LOAD_FAST                'l_last_'
             2540  LOAD_STR                 '좋'
             2542  COMPARE_OP               !=
         2544_2546  POP_JUMP_IF_FALSE  2690  'to 2690'

 L. 262      2548  LOAD_FAST                'r_first'
             2550  LOAD_CONST               0
             2552  BINARY_SUBSCR    
             2554  LOAD_STR                 'ㅇ'
             2556  COMPARE_OP               ==
         2558_2560  POP_JUMP_IF_FALSE  2576  'to 2576'
             2562  LOAD_FAST                'r_first'
             2564  LOAD_CONST               1
             2566  BINARY_SUBSCR    
             2568  LOAD_STR                 'ㅏ'
             2570  COMPARE_OP               ==
         2572_2574  POP_JUMP_IF_TRUE   2590  'to 2590'
           2576_0  COME_FROM          2558  '2558'
             2576  LOAD_FAST                'r_first'
             2578  LOAD_CONST               1
             2580  BINARY_SUBSCR    
             2582  LOAD_STR                 'ㅓ'
             2584  COMPARE_OP               ==
         2586_2588  POP_JUMP_IF_FALSE  2690  'to 2690'
           2590_0  COME_FROM          2572  '2572'

 L. 263      2590  LOAD_FAST                'stem'
             2592  LOAD_CONST               None
             2594  LOAD_CONST               -1
             2596  BUILD_SLICE_2         2 
             2598  BINARY_SUBSCR    
             2600  LOAD_GLOBAL              compose
             2602  LOAD_FAST                'l_last'
             2604  LOAD_CONST               0
             2606  BINARY_SUBSCR    
             2608  LOAD_FAST                'r_first'
             2610  LOAD_CONST               1
             2612  BINARY_SUBSCR    
             2614  LOAD_STR                 'ㅏ'
             2616  COMPARE_OP               ==
         2618_2620  POP_JUMP_IF_FALSE  2626  'to 2626'
             2622  LOAD_STR                 'ㅐ'
             2624  JUMP_FORWARD       2628  'to 2628'
           2626_0  COME_FROM          2618  '2618'
             2626  LOAD_STR                 'ㅔ'
           2628_0  COME_FROM          2624  '2624'
             2628  LOAD_FAST                'r_first'
             2630  LOAD_CONST               2
             2632  BINARY_SUBSCR    
             2634  CALL_FUNCTION_3       3  '3 positional arguments'
             2636  BINARY_ADD       
             2638  STORE_FAST               'l'

 L. 264      2640  LOAD_FAST                'ending'
             2642  LOAD_CONST               1
             2644  LOAD_CONST               None
             2646  BUILD_SLICE_2         2 
             2648  BINARY_SUBSCR    
             2650  STORE_FAST               'r'

 L. 265      2652  LOAD_FAST                'l'
             2654  LOAD_FAST                'r'
             2656  BINARY_ADD       
             2658  STORE_FAST               'surface'

 L. 266      2660  LOAD_FAST                'candidates'
             2662  LOAD_METHOD              add
             2664  LOAD_FAST                'surface'
             2666  CALL_METHOD_1         1  '1 positional argument'
             2668  POP_TOP          

 L. 267      2670  LOAD_FAST                'debug'
         2672_2674  POP_JUMP_IF_FALSE  2690  'to 2690'

 L. 268      2676  LOAD_GLOBAL              print
             2678  LOAD_STR                 'ㅎ 축약 불규칙: {}'
             2680  LOAD_METHOD              format
             2682  LOAD_FAST                'surface'
             2684  CALL_METHOD_1         1  '1 positional argument'
             2686  CALL_FUNCTION_1       1  '1 positional argument'
             2688  POP_TOP          
           2690_0  COME_FROM          2672  '2672'
           2690_1  COME_FROM          2586  '2586'
           2690_2  COME_FROM          2544  '2544'
           2690_3  COME_FROM          2534  '2534'

 L. 272      2690  LOAD_FAST                'l_last'
             2692  LOAD_CONST               2
             2694  BINARY_SUBSCR    
             2696  LOAD_STR                 'ㅎ'
             2698  COMPARE_OP               ==
         2700_2702  POP_JUMP_IF_FALSE  2770  'to 2770'
             2704  LOAD_FAST                'r_first'
             2706  LOAD_CONST               0
             2708  BINARY_SUBSCR    
             2710  LOAD_STR                 'ㄴ'
             2712  COMPARE_OP               ==
         2714_2716  POP_JUMP_IF_FALSE  2770  'to 2770'
             2718  LOAD_FAST                'r_first'
             2720  LOAD_CONST               1
             2722  BINARY_SUBSCR    
             2724  LOAD_STR                 ' '
             2726  COMPARE_OP               !=
         2728_2730  POP_JUMP_IF_FALSE  2770  'to 2770'

 L. 273      2732  LOAD_FAST                'stem'
             2734  LOAD_FAST                'ending'
             2736  BINARY_ADD       
             2738  STORE_FAST               'surface'

 L. 274      2740  LOAD_FAST                'candidates'
             2742  LOAD_METHOD              add
             2744  LOAD_FAST                'surface'
             2746  CALL_METHOD_1         1  '1 positional argument'
             2748  POP_TOP          

 L. 275      2750  LOAD_FAST                'debug'
         2752_2754  POP_JUMP_IF_FALSE  2770  'to 2770'

 L. 276      2756  LOAD_GLOBAL              print
             2758  LOAD_STR                 'ㅎ + 네 불규칙: {}'
             2760  LOAD_METHOD              format
             2762  LOAD_FAST                'surface'
             2764  CALL_METHOD_1         1  '1 positional argument'
             2766  CALL_FUNCTION_1       1  '1 positional argument'
             2768  POP_TOP          
           2770_0  COME_FROM          2752  '2752'
           2770_1  COME_FROM          2728  '2728'
           2770_2  COME_FROM          2714  '2714'
           2770_3  COME_FROM          2700  '2700'

 L. 279      2770  LOAD_FAST                'r_first_'
             2772  LOAD_STR                 '어'
             2774  COMPARE_OP               ==
         2776_2778  POP_JUMP_IF_FALSE  2900  'to 2900'
             2780  LOAD_FAST                'l_last'
             2782  LOAD_CONST               1
             2784  BINARY_SUBSCR    
             2786  LOAD_STR                 'ㅣ'
             2788  COMPARE_OP               ==
         2790_2792  POP_JUMP_IF_FALSE  2900  'to 2900'
             2794  LOAD_FAST                'l_last'
             2796  LOAD_CONST               2
             2798  BINARY_SUBSCR    
             2800  LOAD_STR                 ' '
             2802  COMPARE_OP               ==
         2804_2806  POP_JUMP_IF_FALSE  2900  'to 2900'

 L. 280      2808  LOAD_FAST                'stem'
             2810  LOAD_CONST               None
             2812  LOAD_CONST               -1
             2814  BUILD_SLICE_2         2 
             2816  BINARY_SUBSCR    
             2818  LOAD_GLOBAL              compose
             2820  LOAD_FAST                'l_last'
             2822  LOAD_CONST               0
             2824  BINARY_SUBSCR    
             2826  LOAD_STR                 'ㅕ'
             2828  LOAD_FAST                'r_first'
             2830  LOAD_CONST               2
             2832  BINARY_SUBSCR    
             2834  CALL_FUNCTION_3       3  '3 positional arguments'
             2836  BINARY_ADD       
             2838  LOAD_FAST                'ending'
             2840  LOAD_CONST               1
             2842  LOAD_CONST               None
             2844  BUILD_SLICE_2         2 
             2846  BINARY_SUBSCR    
             2848  BINARY_ADD       
             2850  STORE_FAST               'surface'

 L. 281      2852  LOAD_FAST                'candidates'
             2854  LOAD_METHOD              add
             2856  LOAD_FAST                'surface'
             2858  CALL_METHOD_1         1  '1 positional argument'
             2860  POP_TOP          

 L. 282      2862  LOAD_FAST                'stem'
             2864  LOAD_FAST                'ending'
             2866  BINARY_ADD       
             2868  STORE_FAST               'surface'

 L. 283      2870  LOAD_FAST                'candidates'
             2872  LOAD_METHOD              add
             2874  LOAD_FAST                'surface'
             2876  CALL_METHOD_1         1  '1 positional argument'
             2878  POP_TOP          

 L. 284      2880  LOAD_FAST                'debug'
         2882_2884  POP_JUMP_IF_FALSE  2900  'to 2900'

 L. 285      2886  LOAD_GLOBAL              print
             2888  LOAD_STR                 '이 + 어 -> 여 규칙: {}'
             2890  LOAD_METHOD              format
             2892  LOAD_FAST                'surface'
             2894  CALL_METHOD_1         1  '1 positional argument'
             2896  CALL_FUNCTION_1       1  '1 positional argument'
             2898  POP_TOP          
           2900_0  COME_FROM          2882  '2882'
           2900_1  COME_FROM          2804  '2804'
           2900_2  COME_FROM          2790  '2790'
           2900_3  COME_FROM          2776  '2776'

 L. 287      2900  LOAD_FAST                'candidates'
         2902_2904  POP_JUMP_IF_TRUE   3072  'to 3072'
             2906  LOAD_FAST                'r_first'
             2908  LOAD_CONST               1
             2910  BINARY_SUBSCR    
             2912  LOAD_STR                 ' '
             2914  COMPARE_OP               !=
         2916_2918  POP_JUMP_IF_FALSE  3072  'to 3072'

 L. 288      2920  LOAD_FAST                'l_last'
             2922  LOAD_CONST               2
             2924  BINARY_SUBSCR    
             2926  LOAD_STR                 ' '
             2928  COMPARE_OP               ==
         2930_2932  POP_JUMP_IF_FALSE  3034  'to 3034'
             2934  LOAD_FAST                'r_first'
             2936  LOAD_CONST               0
             2938  BINARY_SUBSCR    
             2940  LOAD_STR                 'ㅇ'
             2942  COMPARE_OP               ==
         2944_2946  POP_JUMP_IF_FALSE  3034  'to 3034'
             2948  LOAD_FAST                'r_first'
             2950  LOAD_CONST               1
             2952  BINARY_SUBSCR    
             2954  LOAD_FAST                'l_last'
             2956  LOAD_CONST               1
             2958  BINARY_SUBSCR    
             2960  COMPARE_OP               ==
         2962_2964  POP_JUMP_IF_FALSE  3034  'to 3034'

 L. 289      2966  LOAD_FAST                'stem'
             2968  LOAD_CONST               None
             2970  LOAD_CONST               -1
             2972  BUILD_SLICE_2         2 
             2974  BINARY_SUBSCR    
             2976  LOAD_GLOBAL              compose
             2978  LOAD_FAST                'l_last'
             2980  LOAD_CONST               0
             2982  BINARY_SUBSCR    
             2984  LOAD_FAST                'l_last'
             2986  LOAD_CONST               1
             2988  BINARY_SUBSCR    
             2990  LOAD_FAST                'r_first'
             2992  LOAD_CONST               2
             2994  BINARY_SUBSCR    
             2996  CALL_FUNCTION_3       3  '3 positional arguments'
             2998  BINARY_ADD       
             3000  STORE_FAST               'l'

 L. 290      3002  LOAD_FAST                'ending'
             3004  LOAD_CONST               1
             3006  LOAD_CONST               None
             3008  BUILD_SLICE_2         2 
             3010  BINARY_SUBSCR    
             3012  STORE_FAST               'r'

 L. 291      3014  LOAD_FAST                'l'
             3016  LOAD_FAST                'r'
             3018  BINARY_ADD       
             3020  STORE_FAST               'surface'

 L. 292      3022  LOAD_FAST                'candidates'
             3024  LOAD_METHOD              add
             3026  LOAD_FAST                'surface'
             3028  CALL_METHOD_1         1  '1 positional argument'
             3030  POP_TOP          
             3032  JUMP_FORWARD       3052  'to 3052'
           3034_0  COME_FROM          2962  '2962'
           3034_1  COME_FROM          2944  '2944'
           3034_2  COME_FROM          2930  '2930'

 L. 294      3034  LOAD_FAST                'stem'
             3036  LOAD_FAST                'ending'
             3038  BINARY_ADD       
             3040  STORE_FAST               'surface'

 L. 295      3042  LOAD_FAST                'candidates'
             3044  LOAD_METHOD              add
             3046  LOAD_FAST                'surface'
             3048  CALL_METHOD_1         1  '1 positional argument'
             3050  POP_TOP          
           3052_0  COME_FROM          3032  '3032'

 L. 296      3052  LOAD_FAST                'debug'
         3054_3056  POP_JUMP_IF_FALSE  3072  'to 3072'

 L. 297      3058  LOAD_GLOBAL              print
             3060  LOAD_STR                 'L + R 규칙 결합: {}'
             3062  LOAD_METHOD              format
             3064  LOAD_FAST                'surface'
             3066  CALL_METHOD_1         1  '1 positional argument'
             3068  CALL_FUNCTION_1       1  '1 positional argument'
             3070  POP_TOP          
           3072_0  COME_FROM          3054  '3054'
           3072_1  COME_FROM          2916  '2916'
           3072_2  COME_FROM          2902  '2902'

 L. 299      3072  LOAD_FAST                'candidates'
             3074  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 830


def _conjugate_stem(stem, debug=False):
    l_len = len(stem)
    l_last = decompose(stem[(-1)])
    l_last_ = stem[(-1)]
    candidates = {
     stem}
    if l_last[2] == 'ㄷ':
        l = stem[:-1] + compose(l_last[0], l_last[1], 'ㄹ')
        candidates.add(l)
        if debug:
            print('ㄷ 불규칙')
    if l_last_ == '르':
        if l_len >= 2:
            c0, c1, c2 = decompose(stem[(-2)])
            l = stem[:-2] + compose(c0, c1, 'ㄹ')
            candidates.add(l)
            if debug:
                print('르 불규칙')
    if l_last[2] == 'ㅂ':
        l = stem[:-1] + compose(l_last[0], l_last[1], ' ')
        candidates.add(l)
        if debug:
            print('ㅂ 불규칙')
    if l_last[2] == ' ':
        candidates.add(stem[:-1] + compose(l_last[0], l_last[1], 'ㄴ'))
        candidates.add(stem[:-1] + compose(l_last[0], l_last[1], 'ㄹ'))
        candidates.add(stem[:-1] + compose(l_last[0], l_last[1], 'ㅂ'))
        candidates.add(stem[:-1] + compose(l_last[0], l_last[1], 'ㅆ'))
        if debug:
            print('어미의 첫 글자가 -ㄴ, -ㄹ, -ㅂ, -ㅆ 일 경우')
    if l_last[2] == 'ㅅ' and stem[(-1)] != '벗':
        candidates.add(stem[:-1] + compose(l_last[0], l_last[1], ' '))
        if debug:
            print('ㅅ 불규칙')
        if l_last[1] == 'ㅜ' and l_last[2] == ' ':
            if l_last_ == '푸':
                l = '퍼'
    else:
        candidates.add(stem[:-1] + compose(l_last[0], 'ㅝ', ' '))
        candidates.add(stem[:-1] + compose(l_last[0], 'ㅝ', 'ㅆ'))
    if debug:
        print('우 불규칙')
    if l_last[1] == 'ㅗ':
        if l_last[2] == ' ':
            candidates.add(stem[:-1] + compose(l_last[0], 'ㅘ', ' '))
            candidates.add(stem[:-1] + compose(l_last[0], 'ㅘ', 'ㅆ'))
            if debug:
                print('오 + 았어 -> 왔어 규칙')
    if l_last[1] == 'ㅡ':
        if l_last[2] == ' ':
            candidates.add(stem[:-1] + compose(l_last[0], 'ㅓ', ' '))
            candidates.add(stem[:-1] + compose(l_last[0], 'ㅓ', 'ㅆ'))
            if l_last[0] == 'ㅇ':
                if len(stem) > 1:
                    candidates.add(stem[:-1])
            if debug:
                print('ㅡ 탈락 불규칙')
    if l_last_ == '하':
        candidates.add(stem[:-1] + '해')
        candidates.add(stem[:-1] + '했')
        if debug:
            print('하 -> 해, 했 활용')
    if l_last[2] == 'ㅎ':
        if l_last_ != '좋':
            candidates.add(stem[:-1] + compose(l_last[0], l_last[1], ' '))
            candidates.add(stem[:-1] + compose(l_last[0], l_last[1], 'ㄴ'))
            candidates.add(stem[:-1] + compose(l_last[0], l_last[1], 'ㄹ'))
            candidates.add(stem[:-1] + compose(l_last[0], l_last[1], 'ㅆ'))
            if debug:
                print('ㅎ 탈락 불규칙')
    if l_last[2] == 'ㅎ':
        if l_last_ != '좋':
            candidates.add(stem[:-1] + compose(l_last[0], 'ㅐ', 'ㅆ'))
            if debug:
                print('ㅎ 축약 불규칙')
    if l_last[1] == 'ㅣ':
        if l_last[2] == ' ':
            candidates.add(stem[:-1] + compose(l_last[0], 'ㅕ', 'ㅆ'))
            if debug:
                print('이었 -> 였 규칙')
    return candidates