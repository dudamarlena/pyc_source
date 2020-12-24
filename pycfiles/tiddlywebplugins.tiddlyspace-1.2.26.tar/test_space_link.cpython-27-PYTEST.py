# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyspace/test/test_space_link.py
# Compiled at: 2013-08-20 13:22:51
"""
Test so-called "friendly" uris: links to tiddlers
in the current space from the root.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from test.fixtures import make_test_env, make_fake_space
from wsgi_intercept import httplib2_intercept
import wsgi_intercept, httplib2
from tiddlyweb.model.tiddler import Tiddler

def setup_module(module):
    make_test_env(module)
    make_fake_space(module.store, 'cdent')
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)
    wsgi_intercept.add_wsgi_intercept('cdent.0.0.0.0', 8080, app_fn)


def test_space_link--- This code section failed: ---

 L.  27         0  LOAD_GLOBAL           0  'Tiddler'
                3  LOAD_CONST               'HouseHold'
                6  LOAD_CONST               'cdent_public'
                9  CALL_FUNCTION_2       2  None
               12  STORE_FAST            0  'tiddler'

 L.  28        15  LOAD_GLOBAL           1  'store'
               18  LOAD_ATTR             2  'put'
               21  LOAD_FAST             0  'tiddler'
               24  CALL_FUNCTION_1       1  None
               27  POP_TOP          

 L.  29        28  LOAD_GLOBAL           3  'httplib2'
               31  LOAD_ATTR             4  'Http'
               34  CALL_FUNCTION_0       0  None
               37  STORE_FAST            1  'http'

 L.  32        40  LOAD_CONST               ('http://cdent.0.0.0.0:8080/recipes/cdent_public/tiddlers/HouseHold', '"/#%5B%5BHouseHold%5D%5D"')

 L.  34        43  LOAD_CONST               ('http://cdent.0.0.0.0:8080/bags/cdent_public/tiddlers/HouseHold', '"http://cdent.0.0.0.0:8080/#%5B%5BHouseHold%5D%5D"')

 L.  36        46  LOAD_CONST               ('http://cdent.0.0.0.0:8080/HouseHold', '"/#%5B%5BHouseHold%5D%5D"')

 L.  38        49  LOAD_CONST               ('http://0.0.0.0:8080/bags/cdent_public/tiddlers/HouseHold', '!"http://cdent.0.0.0.0:8080/#%5B%5BHouseHold%5D%5D"')
               52  BUILD_LIST_4          4 
               55  STORE_FAST            2  'urls'

 L.  40        58  SETUP_LOOP          279  'to 340'
               61  LOAD_FAST             2  'urls'
               64  GET_ITER         
               65  FOR_ITER            271  'to 339'
               68  UNPACK_SEQUENCE_2     2 
               71  STORE_FAST            3  'url'
               74  STORE_FAST            4  'expected'

 L.  41        77  LOAD_FAST             1  'http'
               80  LOAD_ATTR             5  'request'
               83  LOAD_FAST             3  'url'
               86  LOAD_CONST               'method'
               89  LOAD_CONST               'GET'
               92  CALL_FUNCTION_257   257  None
               95  UNPACK_SEQUENCE_2     2 
               98  STORE_FAST            5  'response'
              101  STORE_FAST            6  'content'

 L.  42       104  LOAD_FAST             5  'response'
              107  LOAD_CONST               'status'
              110  BINARY_SUBSCR    
              111  STORE_FAST            7  '@py_assert0'
              114  LOAD_CONST               '200'
              117  STORE_FAST            8  '@py_assert3'
              120  LOAD_FAST             7  '@py_assert0'
              123  LOAD_FAST             8  '@py_assert3'
              126  COMPARE_OP            2  ==
              129  STORE_FAST            9  '@py_assert2'
              132  LOAD_FAST             9  '@py_assert2'
              135  POP_JUMP_IF_TRUE    248  'to 248'
              138  LOAD_GLOBAL           6  '@pytest_ar'
              141  LOAD_ATTR             7  '_call_reprcompare'
              144  LOAD_CONST               ('==',)
              147  LOAD_FAST             9  '@py_assert2'
              150  BUILD_TUPLE_1         1 
              153  LOAD_CONST               ('%(py1)s == %(py4)s',)
              156  LOAD_FAST             7  '@py_assert0'
              159  LOAD_FAST             8  '@py_assert3'
              162  BUILD_TUPLE_2         2 
              165  CALL_FUNCTION_4       4  None
              168  BUILD_MAP_2           2  None
              171  LOAD_GLOBAL           6  '@pytest_ar'
              174  LOAD_ATTR             8  '_saferepr'
              177  LOAD_FAST             7  '@py_assert0'
              180  CALL_FUNCTION_1       1  None
              183  LOAD_CONST               'py1'
              186  STORE_MAP        
              187  LOAD_GLOBAL           6  '@pytest_ar'
              190  LOAD_ATTR             8  '_saferepr'
              193  LOAD_FAST             8  '@py_assert3'
              196  CALL_FUNCTION_1       1  None
              199  LOAD_CONST               'py4'
              202  STORE_MAP        
              203  BINARY_MODULO    
              204  STORE_FAST           10  '@py_format5'
              207  LOAD_CONST               'assert %(py6)s'
              210  BUILD_MAP_1           1  None
              213  LOAD_FAST            10  '@py_format5'
              216  LOAD_CONST               'py6'
              219  STORE_MAP        
              220  BINARY_MODULO    
              221  STORE_FAST           11  '@py_format7'
              224  LOAD_GLOBAL           9  'AssertionError'
              227  LOAD_GLOBAL           6  '@pytest_ar'
              230  LOAD_ATTR            10  '_format_explanation'
              233  LOAD_FAST            11  '@py_format7'
              236  CALL_FUNCTION_1       1  None
              239  CALL_FUNCTION_1       1  None
              242  RAISE_VARARGS_1       1  None
              245  JUMP_FORWARD          0  'to 248'
            248_0  COME_FROM           245  '245'
              248  LOAD_CONST               None
              251  DUP_TOP          
              252  STORE_FAST            7  '@py_assert0'
              255  DUP_TOP          
              256  STORE_FAST            9  '@py_assert2'
              259  STORE_FAST            8  '@py_assert3'

 L.  43       262  LOAD_FAST             4  'expected'
              265  LOAD_ATTR            12  'startswith'
              268  LOAD_CONST               '!'
              271  CALL_FUNCTION_1       1  None
              274  POP_JUMP_IF_FALSE   315  'to 315'

 L.  44       277  LOAD_FAST             4  'expected'
              280  LOAD_FAST             4  'expected'
              283  LOAD_CONST               1
              286  SLICE+1          
              287  COMPARE_OP            2  ==
              290  POP_TOP          

 L.  45       291  LOAD_FAST             4  'expected'
              294  LOAD_FAST             6  'content'
              297  COMPARE_OP            7  not-in
              300  POP_JUMP_IF_TRUE    336  'to 336'
              303  LOAD_ASSERT              AssertionError
              306  LOAD_FAST             6  'content'
              309  RAISE_VARARGS_2       2  None
              312  JUMP_BACK            65  'to 65'

 L.  47       315  LOAD_FAST             4  'expected'
              318  LOAD_FAST             6  'content'
              321  COMPARE_OP            6  in
              324  POP_JUMP_IF_TRUE     65  'to 65'
              327  LOAD_ASSERT              AssertionError
              330  LOAD_FAST             6  'content'
              333  RAISE_VARARGS_2       2  None
              336  JUMP_BACK            65  'to 65'
              339  POP_BLOCK        
            340_0  COME_FROM            58  '58'

 L.  49       340  LOAD_CONST               'http://0.0.0.0:8080/bags/tiddlyspace/tiddlers/Backstage'
              343  STORE_FAST            3  'url'

 L.  50       346  LOAD_FAST             1  'http'
              349  LOAD_ATTR             5  'request'
              352  LOAD_FAST             3  'url'
              355  LOAD_CONST               'method'
              358  LOAD_CONST               'GET'
              361  CALL_FUNCTION_257   257  None
              364  UNPACK_SEQUENCE_2     2 
              367  STORE_FAST            5  'response'
              370  STORE_FAST            6  'content'

 L.  51       373  LOAD_FAST             5  'response'
              376  LOAD_CONST               'status'
              379  BINARY_SUBSCR    
              380  STORE_FAST            7  '@py_assert0'
              383  LOAD_CONST               '200'
              386  STORE_FAST            8  '@py_assert3'
              389  LOAD_FAST             7  '@py_assert0'
              392  LOAD_FAST             8  '@py_assert3'
              395  COMPARE_OP            2  ==
              398  STORE_FAST            9  '@py_assert2'
              401  LOAD_FAST             9  '@py_assert2'
              404  POP_JUMP_IF_TRUE    517  'to 517'
              407  LOAD_GLOBAL           6  '@pytest_ar'
              410  LOAD_ATTR             7  '_call_reprcompare'
              413  LOAD_CONST               ('==',)
              416  LOAD_FAST             9  '@py_assert2'
              419  BUILD_TUPLE_1         1 
              422  LOAD_CONST               ('%(py1)s == %(py4)s',)
              425  LOAD_FAST             7  '@py_assert0'
              428  LOAD_FAST             8  '@py_assert3'
              431  BUILD_TUPLE_2         2 
              434  CALL_FUNCTION_4       4  None
              437  BUILD_MAP_2           2  None
              440  LOAD_GLOBAL           6  '@pytest_ar'
              443  LOAD_ATTR             8  '_saferepr'
              446  LOAD_FAST             7  '@py_assert0'
              449  CALL_FUNCTION_1       1  None
              452  LOAD_CONST               'py1'
              455  STORE_MAP        
              456  LOAD_GLOBAL           6  '@pytest_ar'
              459  LOAD_ATTR             8  '_saferepr'
              462  LOAD_FAST             8  '@py_assert3'
              465  CALL_FUNCTION_1       1  None
              468  LOAD_CONST               'py4'
              471  STORE_MAP        
              472  BINARY_MODULO    
              473  STORE_FAST           10  '@py_format5'
              476  LOAD_CONST               'assert %(py6)s'
              479  BUILD_MAP_1           1  None
              482  LOAD_FAST            10  '@py_format5'
              485  LOAD_CONST               'py6'
              488  STORE_MAP        
              489  BINARY_MODULO    
              490  STORE_FAST           11  '@py_format7'
              493  LOAD_GLOBAL           9  'AssertionError'
              496  LOAD_GLOBAL           6  '@pytest_ar'
              499  LOAD_ATTR            10  '_format_explanation'
              502  LOAD_FAST            11  '@py_format7'
              505  CALL_FUNCTION_1       1  None
              508  CALL_FUNCTION_1       1  None
              511  RAISE_VARARGS_1       1  None
              514  JUMP_FORWARD          0  'to 517'
            517_0  COME_FROM           514  '514'
              517  LOAD_CONST               None
              520  DUP_TOP          
              521  STORE_FAST            7  '@py_assert0'
              524  DUP_TOP          
              525  STORE_FAST            9  '@py_assert2'
              528  STORE_FAST            8  '@py_assert3'

 L.  52       531  LOAD_CONST               '/#%5B%5BBackstage%5D%5D'
              534  LOAD_FAST             6  'content'
              537  COMPARE_OP            7  not-in
              540  POP_JUMP_IF_TRUE    552  'to 552'
              543  LOAD_ASSERT              AssertionError
              546  LOAD_FAST             6  'content'
              549  RAISE_VARARGS_2       2  None

 L.  54       552  LOAD_GLOBAL           0  'Tiddler'
              555  LOAD_CONST               'ServerSettings'
              558  LOAD_CONST               'cdent_public'
              561  CALL_FUNCTION_2       2  None
              564  STORE_FAST            0  'tiddler'

 L.  55       567  LOAD_CONST               'index: HouseHold\n'
              570  LOAD_FAST             0  'tiddler'
              573  STORE_ATTR           13  'text'

 L.  56       576  LOAD_GLOBAL           1  'store'
              579  LOAD_ATTR             2  'put'
              582  LOAD_FAST             0  'tiddler'
              585  CALL_FUNCTION_1       1  None
              588  POP_TOP          

 L.  58       589  SETUP_LOOP          230  'to 822'
              592  LOAD_FAST             2  'urls'
              595  LOAD_CONST               3
              598  SLICE+2          
              599  GET_ITER         
              600  FOR_ITER            218  'to 821'
              603  UNPACK_SEQUENCE_2     2 
              606  STORE_FAST            3  'url'
              609  STORE_FAST            4  'expected'

 L.  59       612  LOAD_FAST             1  'http'
              615  LOAD_ATTR             5  'request'
              618  LOAD_FAST             3  'url'
              621  LOAD_CONST               'method'
              624  LOAD_CONST               'GET'
              627  CALL_FUNCTION_257   257  None
              630  UNPACK_SEQUENCE_2     2 
              633  STORE_FAST            5  'response'
              636  STORE_FAST            6  'content'

 L.  60       639  LOAD_FAST             5  'response'
              642  LOAD_CONST               'status'
              645  BINARY_SUBSCR    
              646  STORE_FAST            7  '@py_assert0'
              649  LOAD_CONST               '200'
              652  STORE_FAST            8  '@py_assert3'
              655  LOAD_FAST             7  '@py_assert0'
              658  LOAD_FAST             8  '@py_assert3'
              661  COMPARE_OP            2  ==
              664  STORE_FAST            9  '@py_assert2'
              667  LOAD_FAST             9  '@py_assert2'
              670  POP_JUMP_IF_TRUE    783  'to 783'
              673  LOAD_GLOBAL           6  '@pytest_ar'
              676  LOAD_ATTR             7  '_call_reprcompare'
              679  LOAD_CONST               ('==',)
              682  LOAD_FAST             9  '@py_assert2'
              685  BUILD_TUPLE_1         1 
              688  LOAD_CONST               ('%(py1)s == %(py4)s',)
              691  LOAD_FAST             7  '@py_assert0'
              694  LOAD_FAST             8  '@py_assert3'
              697  BUILD_TUPLE_2         2 
              700  CALL_FUNCTION_4       4  None
              703  BUILD_MAP_2           2  None
              706  LOAD_GLOBAL           6  '@pytest_ar'
              709  LOAD_ATTR             8  '_saferepr'
              712  LOAD_FAST             7  '@py_assert0'
              715  CALL_FUNCTION_1       1  None
              718  LOAD_CONST               'py1'
              721  STORE_MAP        
              722  LOAD_GLOBAL           6  '@pytest_ar'
              725  LOAD_ATTR             8  '_saferepr'
              728  LOAD_FAST             8  '@py_assert3'
              731  CALL_FUNCTION_1       1  None
              734  LOAD_CONST               'py4'
              737  STORE_MAP        
              738  BINARY_MODULO    
              739  STORE_FAST           10  '@py_format5'
              742  LOAD_CONST               'assert %(py6)s'
              745  BUILD_MAP_1           1  None
              748  LOAD_FAST            10  '@py_format5'
              751  LOAD_CONST               'py6'
              754  STORE_MAP        
              755  BINARY_MODULO    
              756  STORE_FAST           11  '@py_format7'
              759  LOAD_GLOBAL           9  'AssertionError'
              762  LOAD_GLOBAL           6  '@pytest_ar'
              765  LOAD_ATTR            10  '_format_explanation'
              768  LOAD_FAST            11  '@py_format7'
              771  CALL_FUNCTION_1       1  None
              774  CALL_FUNCTION_1       1  None
              777  RAISE_VARARGS_1       1  None
              780  JUMP_FORWARD          0  'to 783'
            783_0  COME_FROM           780  '780'
              783  LOAD_CONST               None
              786  DUP_TOP          
              787  STORE_FAST            7  '@py_assert0'
              790  DUP_TOP          
              791  STORE_FAST            9  '@py_assert2'
              794  STORE_FAST            8  '@py_assert3'

 L.  61       797  LOAD_FAST             4  'expected'
              800  LOAD_FAST             6  'content'
              803  COMPARE_OP            7  not-in
              806  POP_JUMP_IF_TRUE    600  'to 600'
              809  LOAD_ASSERT              AssertionError
              812  LOAD_FAST             6  'content'
              815  RAISE_VARARGS_2       2  None
              818  JUMP_BACK           600  'to 600'
              821  POP_BLOCK        
            822_0  COME_FROM           589  '589'
              822  LOAD_CONST               None
              825  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 339