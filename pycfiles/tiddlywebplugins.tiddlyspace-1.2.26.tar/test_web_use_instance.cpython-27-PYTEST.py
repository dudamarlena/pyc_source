# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyspace/test/test_web_use_instance.py
# Compiled at: 2013-08-20 13:22:51
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from test.fixtures import make_test_env, make_fake_space, get_auth
from wsgi_intercept import httplib2_intercept
import wsgi_intercept, httplib2, simplejson
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.model.user import User

def setup_module(module):
    make_test_env(module)
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)
    wsgi_intercept.add_wsgi_intercept('thing.0.0.0.0', 8080, app_fn)
    wsgi_intercept.add_wsgi_intercept('other.0.0.0.0', 8080, app_fn)
    wsgi_intercept.add_wsgi_intercept('foo.0.0.0.0', 8080, app_fn)


def test_home_page_exist():
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/', method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'Sign up'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_space_not_exist():
    http = httplib2.Http()
    response, content = http.request('http://thing.0.0.0.0:8080/', method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '404'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_space_does_exist():
    make_fake_space(store, 'thing')
    http = httplib2.Http()
    response, content = http.request('http://thing.0.0.0.0:8080/', method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_space_has_limited_view--- This code section failed: ---

 L.  49         0  LOAD_GLOBAL           0  'make_fake_space'
                3  LOAD_GLOBAL           1  'store'
                6  LOAD_CONST               'other'
                9  CALL_FUNCTION_2       2  None
               12  POP_TOP          

 L.  50        13  LOAD_GLOBAL           2  'httplib2'
               16  LOAD_ATTR             3  'Http'
               19  CALL_FUNCTION_0       0  None
               22  STORE_FAST            0  'http'

 L.  51        25  LOAD_FAST             0  'http'
               28  LOAD_ATTR             4  'request'
               31  LOAD_CONST               'http://thing.0.0.0.0:8080/recipes'
               34  LOAD_CONST               'method'

 L.  52        37  LOAD_CONST               'GET'
               40  CALL_FUNCTION_257   257  None
               43  UNPACK_SEQUENCE_2     2 
               46  STORE_FAST            1  'response'
               49  STORE_FAST            2  'content'

 L.  54        52  LOAD_FAST             1  'response'
               55  LOAD_CONST               'status'
               58  BINARY_SUBSCR    
               59  LOAD_CONST               '200'
               62  COMPARE_OP            2  ==
               65  POP_JUMP_IF_TRUE     77  'to 77'
               68  LOAD_ASSERT              AssertionError
               71  LOAD_FAST             2  'content'
               74  RAISE_VARARGS_2       2  None

 L.  55        77  LOAD_CONST               'other_'
               80  LOAD_FAST             2  'content'
               83  COMPARE_OP            7  not-in
               86  POP_JUMP_IF_TRUE     98  'to 98'
               89  LOAD_ASSERT              AssertionError
               92  LOAD_FAST             2  'content'
               95  RAISE_VARARGS_2       2  None

 L.  56        98  LOAD_CONST               'thing_'
              101  LOAD_FAST             2  'content'
              104  COMPARE_OP            6  in
              107  POP_JUMP_IF_TRUE    119  'to 119'
              110  LOAD_ASSERT              AssertionError
              113  LOAD_FAST             2  'content'
              116  RAISE_VARARGS_2       2  None

 L.  58       119  LOAD_FAST             0  'http'
              122  LOAD_ATTR             4  'request'
              125  LOAD_CONST               'http://thing.0.0.0.0:8080/bags'
              128  LOAD_CONST               'method'

 L.  59       131  LOAD_CONST               'GET'
              134  CALL_FUNCTION_257   257  None
              137  UNPACK_SEQUENCE_2     2 
              140  STORE_FAST            1  'response'
              143  STORE_FAST            2  'content'

 L.  61       146  LOAD_FAST             1  'response'
              149  LOAD_CONST               'status'
              152  BINARY_SUBSCR    
              153  STORE_FAST            3  '@py_assert0'
              156  LOAD_CONST               '200'
              159  STORE_FAST            4  '@py_assert3'
              162  LOAD_FAST             3  '@py_assert0'
              165  LOAD_FAST             4  '@py_assert3'
              168  COMPARE_OP            2  ==
              171  STORE_FAST            5  '@py_assert2'
              174  LOAD_FAST             5  '@py_assert2'
              177  POP_JUMP_IF_TRUE    290  'to 290'
              180  LOAD_GLOBAL           6  '@pytest_ar'
              183  LOAD_ATTR             7  '_call_reprcompare'
              186  LOAD_CONST               ('==',)
              189  LOAD_FAST             5  '@py_assert2'
              192  BUILD_TUPLE_1         1 
              195  LOAD_CONST               ('%(py1)s == %(py4)s',)
              198  LOAD_FAST             3  '@py_assert0'
              201  LOAD_FAST             4  '@py_assert3'
              204  BUILD_TUPLE_2         2 
              207  CALL_FUNCTION_4       4  None
              210  BUILD_MAP_2           2  None
              213  LOAD_GLOBAL           6  '@pytest_ar'
              216  LOAD_ATTR             8  '_saferepr'
              219  LOAD_FAST             3  '@py_assert0'
              222  CALL_FUNCTION_1       1  None
              225  LOAD_CONST               'py1'
              228  STORE_MAP        
              229  LOAD_GLOBAL           6  '@pytest_ar'
              232  LOAD_ATTR             8  '_saferepr'
              235  LOAD_FAST             4  '@py_assert3'
              238  CALL_FUNCTION_1       1  None
              241  LOAD_CONST               'py4'
              244  STORE_MAP        
              245  BINARY_MODULO    
              246  STORE_FAST            6  '@py_format5'
              249  LOAD_CONST               'assert %(py6)s'
              252  BUILD_MAP_1           1  None
              255  LOAD_FAST             6  '@py_format5'
              258  LOAD_CONST               'py6'
              261  STORE_MAP        
              262  BINARY_MODULO    
              263  STORE_FAST            7  '@py_format7'
              266  LOAD_GLOBAL           5  'AssertionError'
              269  LOAD_GLOBAL           6  '@pytest_ar'
              272  LOAD_ATTR             9  '_format_explanation'
              275  LOAD_FAST             7  '@py_format7'
              278  CALL_FUNCTION_1       1  None
              281  CALL_FUNCTION_1       1  None
              284  RAISE_VARARGS_1       1  None
              287  JUMP_FORWARD          0  'to 290'
            290_0  COME_FROM           287  '287'
              290  LOAD_CONST               None
              293  DUP_TOP          
              294  STORE_FAST            3  '@py_assert0'
              297  DUP_TOP          
              298  STORE_FAST            5  '@py_assert2'
              301  STORE_FAST            4  '@py_assert3'

 L.  62       304  LOAD_CONST               'other_'
              307  LOAD_FAST             2  'content'
              310  COMPARE_OP            7  not-in
              313  POP_JUMP_IF_TRUE    325  'to 325'
              316  LOAD_ASSERT              AssertionError
              319  LOAD_FAST             2  'content'
              322  RAISE_VARARGS_2       2  None

 L.  63       325  LOAD_CONST               'thing_'
              328  LOAD_FAST             2  'content'
              331  COMPARE_OP            6  in
              334  POP_JUMP_IF_TRUE    346  'to 346'
              337  LOAD_ASSERT              AssertionError
              340  LOAD_FAST             2  'content'
              343  RAISE_VARARGS_2       2  None

 L.  65       346  LOAD_FAST             0  'http'
              349  LOAD_ATTR             4  'request'

 L.  66       352  LOAD_CONST               'http://thing.0.0.0.0:8080/bags/thing_public/tiddlers'
              355  LOAD_CONST               'method'

 L.  67       358  LOAD_CONST               'GET'
              361  CALL_FUNCTION_257   257  None
              364  UNPACK_SEQUENCE_2     2 
              367  STORE_FAST            1  'response'
              370  STORE_FAST            2  'content'

 L.  68       373  LOAD_FAST             1  'response'
              376  LOAD_CONST               'status'
              379  BINARY_SUBSCR    
              380  STORE_FAST            3  '@py_assert0'
              383  LOAD_CONST               '200'
              386  STORE_FAST            4  '@py_assert3'
              389  LOAD_FAST             3  '@py_assert0'
              392  LOAD_FAST             4  '@py_assert3'
              395  COMPARE_OP            2  ==
              398  STORE_FAST            5  '@py_assert2'
              401  LOAD_FAST             5  '@py_assert2'
              404  POP_JUMP_IF_TRUE    517  'to 517'
              407  LOAD_GLOBAL           6  '@pytest_ar'
              410  LOAD_ATTR             7  '_call_reprcompare'
              413  LOAD_CONST               ('==',)
              416  LOAD_FAST             5  '@py_assert2'
              419  BUILD_TUPLE_1         1 
              422  LOAD_CONST               ('%(py1)s == %(py4)s',)
              425  LOAD_FAST             3  '@py_assert0'
              428  LOAD_FAST             4  '@py_assert3'
              431  BUILD_TUPLE_2         2 
              434  CALL_FUNCTION_4       4  None
              437  BUILD_MAP_2           2  None
              440  LOAD_GLOBAL           6  '@pytest_ar'
              443  LOAD_ATTR             8  '_saferepr'
              446  LOAD_FAST             3  '@py_assert0'
              449  CALL_FUNCTION_1       1  None
              452  LOAD_CONST               'py1'
              455  STORE_MAP        
              456  LOAD_GLOBAL           6  '@pytest_ar'
              459  LOAD_ATTR             8  '_saferepr'
              462  LOAD_FAST             4  '@py_assert3'
              465  CALL_FUNCTION_1       1  None
              468  LOAD_CONST               'py4'
              471  STORE_MAP        
              472  BINARY_MODULO    
              473  STORE_FAST            6  '@py_format5'
              476  LOAD_CONST               'assert %(py6)s'
              479  BUILD_MAP_1           1  None
              482  LOAD_FAST             6  '@py_format5'
              485  LOAD_CONST               'py6'
              488  STORE_MAP        
              489  BINARY_MODULO    
              490  STORE_FAST            7  '@py_format7'
              493  LOAD_GLOBAL           5  'AssertionError'
              496  LOAD_GLOBAL           6  '@pytest_ar'
              499  LOAD_ATTR             9  '_format_explanation'
              502  LOAD_FAST             7  '@py_format7'
              505  CALL_FUNCTION_1       1  None
              508  CALL_FUNCTION_1       1  None
              511  RAISE_VARARGS_1       1  None
              514  JUMP_FORWARD          0  'to 517'
            517_0  COME_FROM           514  '514'
              517  LOAD_CONST               None
              520  DUP_TOP          
              521  STORE_FAST            3  '@py_assert0'
              524  DUP_TOP          
              525  STORE_FAST            5  '@py_assert2'
              528  STORE_FAST            4  '@py_assert3'

 L.  70       531  LOAD_FAST             0  'http'
              534  LOAD_ATTR             4  'request'

 L.  71       537  LOAD_CONST               'http://thing.0.0.0.0:8080/bags/other_public/tiddlers'
              540  LOAD_CONST               'method'

 L.  72       543  LOAD_CONST               'GET'
              546  CALL_FUNCTION_257   257  None
              549  UNPACK_SEQUENCE_2     2 
              552  STORE_FAST            1  'response'
              555  STORE_FAST            2  'content'

 L.  73       558  LOAD_FAST             1  'response'
              561  LOAD_CONST               'status'
              564  BINARY_SUBSCR    
              565  LOAD_CONST               '404'
              568  COMPARE_OP            2  ==
              571  POP_JUMP_IF_TRUE    583  'to 583'
              574  LOAD_ASSERT              AssertionError
              577  LOAD_FAST             2  'content'
              580  RAISE_VARARGS_2       2  None

 L.  75       583  LOAD_FAST             0  'http'
              586  LOAD_ATTR             4  'request'

 L.  76       589  LOAD_CONST               'http://other.0.0.0.0:8080/bags'
              592  LOAD_CONST               'method'

 L.  77       595  LOAD_CONST               'GET'
              598  CALL_FUNCTION_257   257  None
              601  UNPACK_SEQUENCE_2     2 
              604  STORE_FAST            1  'response'
              607  STORE_FAST            2  'content'

 L.  78       610  LOAD_FAST             1  'response'
              613  LOAD_CONST               'status'
              616  BINARY_SUBSCR    
              617  LOAD_CONST               '200'
              620  COMPARE_OP            2  ==
              623  POP_JUMP_IF_TRUE    635  'to 635'
              626  LOAD_ASSERT              AssertionError
              629  LOAD_FAST             2  'content'
              632  RAISE_VARARGS_2       2  None

 L.  79       635  LOAD_CONST               'other_'
              638  LOAD_FAST             2  'content'
              641  COMPARE_OP            6  in
              644  POP_JUMP_IF_TRUE    656  'to 656'
              647  LOAD_ASSERT              AssertionError
              650  LOAD_FAST             2  'content'
              653  RAISE_VARARGS_2       2  None

 L.  80       656  LOAD_CONST               'thing_'
              659  LOAD_FAST             2  'content'
              662  COMPARE_OP            7  not-in
              665  POP_JUMP_IF_TRUE    677  'to 677'
              668  LOAD_ASSERT              AssertionError
              671  LOAD_FAST             2  'content'
              674  RAISE_VARARGS_2       2  None

 L.  82       677  LOAD_FAST             0  'http'
              680  LOAD_ATTR             4  'request'

 L.  83       683  LOAD_CONST               'http://0.0.0.0:8080/bags'
              686  LOAD_CONST               'method'

 L.  84       689  LOAD_CONST               'GET'
              692  CALL_FUNCTION_257   257  None
              695  UNPACK_SEQUENCE_2     2 
              698  STORE_FAST            1  'response'
              701  STORE_FAST            2  'content'

 L.  85       704  LOAD_FAST             1  'response'
              707  LOAD_CONST               'status'
              710  BINARY_SUBSCR    
              711  LOAD_CONST               '200'
              714  COMPARE_OP            2  ==
              717  POP_JUMP_IF_TRUE    729  'to 729'
              720  LOAD_ASSERT              AssertionError
              723  LOAD_FAST             2  'content'
              726  RAISE_VARARGS_2       2  None

 L.  86       729  LOAD_CONST               'other_'
              732  LOAD_FAST             2  'content'
              735  COMPARE_OP            6  in
              738  POP_JUMP_IF_TRUE    750  'to 750'
              741  LOAD_ASSERT              AssertionError
              744  LOAD_FAST             2  'content'
              747  RAISE_VARARGS_2       2  None

 L.  87       750  LOAD_CONST               'thing_'
              753  LOAD_FAST             2  'content'
              756  COMPARE_OP            6  in
              759  POP_JUMP_IF_TRUE    771  'to 771'
              762  LOAD_ASSERT              AssertionError
              765  LOAD_FAST             2  'content'
              768  RAISE_VARARGS_2       2  None

 L.  89       771  LOAD_FAST             0  'http'
              774  LOAD_ATTR             4  'request'

 L.  90       777  LOAD_CONST               'http://thing.0.0.0.0:8080/bags/thing_public/tiddlers'
              780  LOAD_CONST               'method'

 L.  91       783  LOAD_CONST               'GET'
              786  CALL_FUNCTION_257   257  None
              789  UNPACK_SEQUENCE_2     2 
              792  STORE_FAST            1  'response'
              795  STORE_FAST            2  'content'

 L.  92       798  LOAD_FAST             1  'response'
              801  LOAD_CONST               'status'
              804  BINARY_SUBSCR    
              805  LOAD_CONST               '200'
              808  COMPARE_OP            2  ==
              811  POP_JUMP_IF_TRUE    823  'to 823'
              814  LOAD_ASSERT              AssertionError
              817  LOAD_FAST             2  'content'
              820  RAISE_VARARGS_2       2  None

 L.  94       823  LOAD_FAST             0  'http'
              826  LOAD_ATTR             4  'request'

 L.  95       829  LOAD_CONST               'http://thing.0.0.0.0:8080/bags/other_public/tiddlers'
              832  LOAD_CONST               'method'

 L.  96       835  LOAD_CONST               'GET'
              838  CALL_FUNCTION_257   257  None
              841  UNPACK_SEQUENCE_2     2 
              844  STORE_FAST            1  'response'
              847  STORE_FAST            2  'content'

 L.  97       850  LOAD_FAST             1  'response'
              853  LOAD_CONST               'status'
              856  BINARY_SUBSCR    
              857  LOAD_CONST               '404'
              860  COMPARE_OP            2  ==
              863  POP_JUMP_IF_TRUE    875  'to 875'
              866  LOAD_ASSERT              AssertionError
              869  LOAD_FAST             2  'content'
              872  RAISE_VARARGS_2       2  None

 L.  99       875  LOAD_GLOBAL          11  'Tiddler'
              878  LOAD_CONST               'tiddler1'
              881  LOAD_CONST               'thing_public'
              884  CALL_FUNCTION_2       2  None
              887  STORE_FAST            8  'tiddler1'

 L. 100       890  LOAD_GLOBAL          11  'Tiddler'
              893  LOAD_CONST               'tiddler2'
              896  LOAD_CONST               'other_public'
              899  CALL_FUNCTION_2       2  None
              902  STORE_FAST            9  'tiddler2'

 L. 101       905  LOAD_CONST               'ohhai'
              908  DUP_TOP          
              909  LOAD_FAST             8  'tiddler1'
              912  STORE_ATTR           12  'text'
              915  LOAD_FAST             9  'tiddler2'
              918  STORE_ATTR           12  'text'

 L. 102       921  LOAD_GLOBAL           1  'store'
              924  LOAD_ATTR            13  'put'
              927  LOAD_FAST             8  'tiddler1'
              930  CALL_FUNCTION_1       1  None
              933  POP_TOP          

 L. 103       934  LOAD_GLOBAL           1  'store'
              937  LOAD_ATTR            13  'put'
              940  LOAD_FAST             9  'tiddler2'
              943  CALL_FUNCTION_1       1  None
              946  POP_TOP          

 L. 105       947  LOAD_FAST             0  'http'
              950  LOAD_ATTR             4  'request'

 L. 106       953  LOAD_CONST               'http://thing.0.0.0.0:8080/search?q=ohhai'
              956  LOAD_CONST               'headers'

 L. 107       959  BUILD_MAP_1           1  None
              962  LOAD_CONST               'application/json'
              965  LOAD_CONST               'Accept'
              968  STORE_MAP        
              969  LOAD_CONST               'method'

 L. 108       972  LOAD_CONST               'GET'
              975  CALL_FUNCTION_513   513  None
              978  UNPACK_SEQUENCE_2     2 
              981  STORE_FAST            1  'response'
              984  STORE_FAST            2  'content'

 L. 109       987  LOAD_FAST             1  'response'
              990  LOAD_CONST               'status'
              993  BINARY_SUBSCR    
              994  LOAD_CONST               '200'
              997  COMPARE_OP            2  ==
             1000  POP_JUMP_IF_TRUE   1012  'to 1012'
             1003  LOAD_ASSERT              AssertionError
             1006  LOAD_FAST             2  'content'
             1009  RAISE_VARARGS_2       2  None

 L. 111      1012  LOAD_GLOBAL          14  'simplejson'
             1015  LOAD_ATTR            15  'loads'
             1018  LOAD_FAST             2  'content'
             1021  CALL_FUNCTION_1       1  None
             1024  STORE_FAST           10  'info'

 L. 112      1027  LOAD_GLOBAL          16  'len'
             1030  LOAD_FAST            10  'info'
             1033  CALL_FUNCTION_1       1  None
             1036  STORE_FAST            5  '@py_assert2'
             1039  LOAD_CONST               1
             1042  STORE_FAST           11  '@py_assert5'
             1045  LOAD_FAST             5  '@py_assert2'
             1048  LOAD_FAST            11  '@py_assert5'
             1051  COMPARE_OP            2  ==
             1054  STORE_FAST           12  '@py_assert4'
             1057  LOAD_FAST            12  '@py_assert4'
             1060  POP_JUMP_IF_TRUE   1283  'to 1283'
             1063  LOAD_GLOBAL           6  '@pytest_ar'
             1066  LOAD_ATTR             7  '_call_reprcompare'
             1069  LOAD_CONST               ('==',)
             1072  LOAD_FAST            12  '@py_assert4'
             1075  BUILD_TUPLE_1         1 
             1078  LOAD_CONST               ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',)
             1081  LOAD_FAST             5  '@py_assert2'
             1084  LOAD_FAST            11  '@py_assert5'
             1087  BUILD_TUPLE_2         2 
             1090  CALL_FUNCTION_4       4  None
             1093  BUILD_MAP_4           4  None
             1096  LOAD_CONST               'len'
             1099  LOAD_GLOBAL          17  '@py_builtins'
             1102  LOAD_ATTR            18  'locals'
             1105  CALL_FUNCTION_0       0  None
             1108  COMPARE_OP            6  in
             1111  POP_JUMP_IF_TRUE   1129  'to 1129'
             1114  LOAD_GLOBAL           6  '@pytest_ar'
             1117  LOAD_ATTR            19  '_should_repr_global_name'
             1120  LOAD_GLOBAL          16  'len'
             1123  CALL_FUNCTION_1       1  None
           1126_0  COME_FROM          1111  '1111'
             1126  POP_JUMP_IF_FALSE  1144  'to 1144'
             1129  LOAD_GLOBAL           6  '@pytest_ar'
             1132  LOAD_ATTR             8  '_saferepr'
             1135  LOAD_GLOBAL          16  'len'
             1138  CALL_FUNCTION_1       1  None
             1141  JUMP_FORWARD          3  'to 1147'
             1144  LOAD_CONST               'len'
           1147_0  COME_FROM          1141  '1141'
             1147  LOAD_CONST               'py0'
             1150  STORE_MAP        
             1151  LOAD_CONST               'info'
             1154  LOAD_GLOBAL          17  '@py_builtins'
             1157  LOAD_ATTR            18  'locals'
             1160  CALL_FUNCTION_0       0  None
             1163  COMPARE_OP            6  in
             1166  POP_JUMP_IF_TRUE   1184  'to 1184'
             1169  LOAD_GLOBAL           6  '@pytest_ar'
             1172  LOAD_ATTR            19  '_should_repr_global_name'
             1175  LOAD_FAST            10  'info'
             1178  CALL_FUNCTION_1       1  None
           1181_0  COME_FROM          1166  '1166'
             1181  POP_JUMP_IF_FALSE  1199  'to 1199'
             1184  LOAD_GLOBAL           6  '@pytest_ar'
             1187  LOAD_ATTR             8  '_saferepr'
             1190  LOAD_FAST            10  'info'
             1193  CALL_FUNCTION_1       1  None
             1196  JUMP_FORWARD          3  'to 1202'
             1199  LOAD_CONST               'info'
           1202_0  COME_FROM          1196  '1196'
             1202  LOAD_CONST               'py1'
             1205  STORE_MAP        
             1206  LOAD_GLOBAL           6  '@pytest_ar'
             1209  LOAD_ATTR             8  '_saferepr'
             1212  LOAD_FAST             5  '@py_assert2'
             1215  CALL_FUNCTION_1       1  None
             1218  LOAD_CONST               'py3'
             1221  STORE_MAP        
             1222  LOAD_GLOBAL           6  '@pytest_ar'
             1225  LOAD_ATTR             8  '_saferepr'
             1228  LOAD_FAST            11  '@py_assert5'
             1231  CALL_FUNCTION_1       1  None
             1234  LOAD_CONST               'py6'
             1237  STORE_MAP        
             1238  BINARY_MODULO    
             1239  STORE_FAST            7  '@py_format7'
             1242  LOAD_CONST               'assert %(py8)s'
             1245  BUILD_MAP_1           1  None
             1248  LOAD_FAST             7  '@py_format7'
             1251  LOAD_CONST               'py8'
             1254  STORE_MAP        
             1255  BINARY_MODULO    
             1256  STORE_FAST           13  '@py_format9'
             1259  LOAD_GLOBAL           5  'AssertionError'
             1262  LOAD_GLOBAL           6  '@pytest_ar'
             1265  LOAD_ATTR             9  '_format_explanation'
             1268  LOAD_FAST            13  '@py_format9'
             1271  CALL_FUNCTION_1       1  None
             1274  CALL_FUNCTION_1       1  None
             1277  RAISE_VARARGS_1       1  None
             1280  JUMP_FORWARD          0  'to 1283'
           1283_0  COME_FROM          1280  '1280'
             1283  LOAD_CONST               None
             1286  DUP_TOP          
             1287  STORE_FAST            5  '@py_assert2'
             1290  DUP_TOP          
             1291  STORE_FAST           12  '@py_assert4'
             1294  STORE_FAST           11  '@py_assert5'

 L. 113      1297  LOAD_FAST            10  'info'
             1300  LOAD_CONST               0
             1303  BINARY_SUBSCR    
             1304  LOAD_CONST               'title'
             1307  BINARY_SUBSCR    
             1308  STORE_FAST            3  '@py_assert0'
             1311  LOAD_FAST             8  'tiddler1'
             1314  LOAD_ATTR            20  'title'
             1317  STORE_FAST           12  '@py_assert4'
             1320  LOAD_FAST             3  '@py_assert0'
             1323  LOAD_FAST            12  '@py_assert4'
             1326  COMPARE_OP            2  ==
             1329  STORE_FAST            5  '@py_assert2'
             1332  LOAD_FAST             5  '@py_assert2'
             1335  POP_JUMP_IF_TRUE   1503  'to 1503'
             1338  LOAD_GLOBAL           6  '@pytest_ar'
             1341  LOAD_ATTR             7  '_call_reprcompare'
             1344  LOAD_CONST               ('==',)
             1347  LOAD_FAST             5  '@py_assert2'
             1350  BUILD_TUPLE_1         1 
             1353  LOAD_CONST               ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.title\n}',)
             1356  LOAD_FAST             3  '@py_assert0'
             1359  LOAD_FAST            12  '@py_assert4'
             1362  BUILD_TUPLE_2         2 
             1365  CALL_FUNCTION_4       4  None
             1368  BUILD_MAP_3           3  None
             1371  LOAD_GLOBAL           6  '@pytest_ar'
             1374  LOAD_ATTR             8  '_saferepr'
             1377  LOAD_FAST             3  '@py_assert0'
             1380  CALL_FUNCTION_1       1  None
             1383  LOAD_CONST               'py1'
             1386  STORE_MAP        
             1387  LOAD_CONST               'tiddler1'
             1390  LOAD_GLOBAL          17  '@py_builtins'
             1393  LOAD_ATTR            18  'locals'
             1396  CALL_FUNCTION_0       0  None
             1399  COMPARE_OP            6  in
             1402  POP_JUMP_IF_TRUE   1420  'to 1420'
             1405  LOAD_GLOBAL           6  '@pytest_ar'
             1408  LOAD_ATTR            19  '_should_repr_global_name'
             1411  LOAD_FAST             8  'tiddler1'
             1414  CALL_FUNCTION_1       1  None
           1417_0  COME_FROM          1402  '1402'
             1417  POP_JUMP_IF_FALSE  1435  'to 1435'
             1420  LOAD_GLOBAL           6  '@pytest_ar'
             1423  LOAD_ATTR             8  '_saferepr'
             1426  LOAD_FAST             8  'tiddler1'
             1429  CALL_FUNCTION_1       1  None
             1432  JUMP_FORWARD          3  'to 1438'
             1435  LOAD_CONST               'tiddler1'
           1438_0  COME_FROM          1432  '1432'
             1438  LOAD_CONST               'py3'
             1441  STORE_MAP        
             1442  LOAD_GLOBAL           6  '@pytest_ar'
             1445  LOAD_ATTR             8  '_saferepr'
             1448  LOAD_FAST            12  '@py_assert4'
             1451  CALL_FUNCTION_1       1  None
             1454  LOAD_CONST               'py5'
             1457  STORE_MAP        
             1458  BINARY_MODULO    
             1459  STORE_FAST           14  '@py_format6'
             1462  LOAD_CONST               'assert %(py7)s'
             1465  BUILD_MAP_1           1  None
             1468  LOAD_FAST            14  '@py_format6'
             1471  LOAD_CONST               'py7'
             1474  STORE_MAP        
             1475  BINARY_MODULO    
             1476  STORE_FAST           15  '@py_format8'
             1479  LOAD_GLOBAL           5  'AssertionError'
             1482  LOAD_GLOBAL           6  '@pytest_ar'
             1485  LOAD_ATTR             9  '_format_explanation'
             1488  LOAD_FAST            15  '@py_format8'
             1491  CALL_FUNCTION_1       1  None
             1494  CALL_FUNCTION_1       1  None
             1497  RAISE_VARARGS_1       1  None
             1500  JUMP_FORWARD          0  'to 1503'
           1503_0  COME_FROM          1500  '1500'
             1503  LOAD_CONST               None
             1506  DUP_TOP          
             1507  STORE_FAST            3  '@py_assert0'
             1510  DUP_TOP          
             1511  STORE_FAST            5  '@py_assert2'
             1514  STORE_FAST           12  '@py_assert4'

 L. 115      1517  LOAD_FAST             0  'http'
             1520  LOAD_ATTR             4  'request'

 L. 116      1523  LOAD_CONST               'http://other.0.0.0.0:8080/search?q=ohhai'
             1526  LOAD_CONST               'headers'

 L. 117      1529  BUILD_MAP_1           1  None
             1532  LOAD_CONST               'application/json'
             1535  LOAD_CONST               'Accept'
             1538  STORE_MAP        
             1539  LOAD_CONST               'method'

 L. 118      1542  LOAD_CONST               'GET'
             1545  CALL_FUNCTION_513   513  None
             1548  UNPACK_SEQUENCE_2     2 
             1551  STORE_FAST            1  'response'
             1554  STORE_FAST            2  'content'

 L. 119      1557  LOAD_FAST             1  'response'
             1560  LOAD_CONST               'status'
             1563  BINARY_SUBSCR    
             1564  LOAD_CONST               '200'
             1567  COMPARE_OP            2  ==
             1570  POP_JUMP_IF_TRUE   1582  'to 1582'
             1573  LOAD_ASSERT              AssertionError
             1576  LOAD_FAST             2  'content'
             1579  RAISE_VARARGS_2       2  None

 L. 121      1582  LOAD_GLOBAL          14  'simplejson'
             1585  LOAD_ATTR            15  'loads'
             1588  LOAD_FAST             2  'content'
             1591  CALL_FUNCTION_1       1  None
             1594  STORE_FAST           10  'info'

 L. 122      1597  LOAD_GLOBAL          16  'len'
             1600  LOAD_FAST            10  'info'
             1603  CALL_FUNCTION_1       1  None
             1606  STORE_FAST            5  '@py_assert2'
             1609  LOAD_CONST               1
             1612  STORE_FAST           11  '@py_assert5'
             1615  LOAD_FAST             5  '@py_assert2'
             1618  LOAD_FAST            11  '@py_assert5'
             1621  COMPARE_OP            2  ==
             1624  STORE_FAST           12  '@py_assert4'
             1627  LOAD_FAST            12  '@py_assert4'
             1630  POP_JUMP_IF_TRUE   1853  'to 1853'
             1633  LOAD_GLOBAL           6  '@pytest_ar'
             1636  LOAD_ATTR             7  '_call_reprcompare'
             1639  LOAD_CONST               ('==',)
             1642  LOAD_FAST            12  '@py_assert4'
             1645  BUILD_TUPLE_1         1 
             1648  LOAD_CONST               ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',)
             1651  LOAD_FAST             5  '@py_assert2'
             1654  LOAD_FAST            11  '@py_assert5'
             1657  BUILD_TUPLE_2         2 
             1660  CALL_FUNCTION_4       4  None
             1663  BUILD_MAP_4           4  None
             1666  LOAD_CONST               'len'
             1669  LOAD_GLOBAL          17  '@py_builtins'
             1672  LOAD_ATTR            18  'locals'
             1675  CALL_FUNCTION_0       0  None
             1678  COMPARE_OP            6  in
             1681  POP_JUMP_IF_TRUE   1699  'to 1699'
             1684  LOAD_GLOBAL           6  '@pytest_ar'
             1687  LOAD_ATTR            19  '_should_repr_global_name'
             1690  LOAD_GLOBAL          16  'len'
             1693  CALL_FUNCTION_1       1  None
           1696_0  COME_FROM          1681  '1681'
             1696  POP_JUMP_IF_FALSE  1714  'to 1714'
             1699  LOAD_GLOBAL           6  '@pytest_ar'
             1702  LOAD_ATTR             8  '_saferepr'
             1705  LOAD_GLOBAL          16  'len'
             1708  CALL_FUNCTION_1       1  None
             1711  JUMP_FORWARD          3  'to 1717'
             1714  LOAD_CONST               'len'
           1717_0  COME_FROM          1711  '1711'
             1717  LOAD_CONST               'py0'
             1720  STORE_MAP        
             1721  LOAD_CONST               'info'
             1724  LOAD_GLOBAL          17  '@py_builtins'
             1727  LOAD_ATTR            18  'locals'
             1730  CALL_FUNCTION_0       0  None
             1733  COMPARE_OP            6  in
             1736  POP_JUMP_IF_TRUE   1754  'to 1754'
             1739  LOAD_GLOBAL           6  '@pytest_ar'
             1742  LOAD_ATTR            19  '_should_repr_global_name'
             1745  LOAD_FAST            10  'info'
             1748  CALL_FUNCTION_1       1  None
           1751_0  COME_FROM          1736  '1736'
             1751  POP_JUMP_IF_FALSE  1769  'to 1769'
             1754  LOAD_GLOBAL           6  '@pytest_ar'
             1757  LOAD_ATTR             8  '_saferepr'
             1760  LOAD_FAST            10  'info'
             1763  CALL_FUNCTION_1       1  None
             1766  JUMP_FORWARD          3  'to 1772'
             1769  LOAD_CONST               'info'
           1772_0  COME_FROM          1766  '1766'
             1772  LOAD_CONST               'py1'
             1775  STORE_MAP        
             1776  LOAD_GLOBAL           6  '@pytest_ar'
             1779  LOAD_ATTR             8  '_saferepr'
             1782  LOAD_FAST             5  '@py_assert2'
             1785  CALL_FUNCTION_1       1  None
             1788  LOAD_CONST               'py3'
             1791  STORE_MAP        
             1792  LOAD_GLOBAL           6  '@pytest_ar'
             1795  LOAD_ATTR             8  '_saferepr'
             1798  LOAD_FAST            11  '@py_assert5'
             1801  CALL_FUNCTION_1       1  None
             1804  LOAD_CONST               'py6'
             1807  STORE_MAP        
             1808  BINARY_MODULO    
             1809  STORE_FAST            7  '@py_format7'
             1812  LOAD_CONST               'assert %(py8)s'
             1815  BUILD_MAP_1           1  None
             1818  LOAD_FAST             7  '@py_format7'
             1821  LOAD_CONST               'py8'
             1824  STORE_MAP        
             1825  BINARY_MODULO    
             1826  STORE_FAST           13  '@py_format9'
             1829  LOAD_GLOBAL           5  'AssertionError'
             1832  LOAD_GLOBAL           6  '@pytest_ar'
             1835  LOAD_ATTR             9  '_format_explanation'
             1838  LOAD_FAST            13  '@py_format9'
             1841  CALL_FUNCTION_1       1  None
             1844  CALL_FUNCTION_1       1  None
             1847  RAISE_VARARGS_1       1  None
             1850  JUMP_FORWARD          0  'to 1853'
           1853_0  COME_FROM          1850  '1850'
             1853  LOAD_CONST               None
             1856  DUP_TOP          
             1857  STORE_FAST            5  '@py_assert2'
             1860  DUP_TOP          
             1861  STORE_FAST           12  '@py_assert4'
             1864  STORE_FAST           11  '@py_assert5'

 L. 123      1867  LOAD_FAST            10  'info'
             1870  LOAD_CONST               0
             1873  BINARY_SUBSCR    
             1874  LOAD_CONST               'title'
             1877  BINARY_SUBSCR    
             1878  STORE_FAST            3  '@py_assert0'
             1881  LOAD_FAST             9  'tiddler2'
             1884  LOAD_ATTR            20  'title'
             1887  STORE_FAST           12  '@py_assert4'
             1890  LOAD_FAST             3  '@py_assert0'
             1893  LOAD_FAST            12  '@py_assert4'
             1896  COMPARE_OP            2  ==
             1899  STORE_FAST            5  '@py_assert2'
             1902  LOAD_FAST             5  '@py_assert2'
             1905  POP_JUMP_IF_TRUE   2073  'to 2073'
             1908  LOAD_GLOBAL           6  '@pytest_ar'
             1911  LOAD_ATTR             7  '_call_reprcompare'
             1914  LOAD_CONST               ('==',)
             1917  LOAD_FAST             5  '@py_assert2'
             1920  BUILD_TUPLE_1         1 
             1923  LOAD_CONST               ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.title\n}',)
             1926  LOAD_FAST             3  '@py_assert0'
             1929  LOAD_FAST            12  '@py_assert4'
             1932  BUILD_TUPLE_2         2 
             1935  CALL_FUNCTION_4       4  None
             1938  BUILD_MAP_3           3  None
             1941  LOAD_GLOBAL           6  '@pytest_ar'
             1944  LOAD_ATTR             8  '_saferepr'
             1947  LOAD_FAST             3  '@py_assert0'
             1950  CALL_FUNCTION_1       1  None
             1953  LOAD_CONST               'py1'
             1956  STORE_MAP        
             1957  LOAD_CONST               'tiddler2'
             1960  LOAD_GLOBAL          17  '@py_builtins'
             1963  LOAD_ATTR            18  'locals'
             1966  CALL_FUNCTION_0       0  None
             1969  COMPARE_OP            6  in
             1972  POP_JUMP_IF_TRUE   1990  'to 1990'
             1975  LOAD_GLOBAL           6  '@pytest_ar'
             1978  LOAD_ATTR            19  '_should_repr_global_name'
             1981  LOAD_FAST             9  'tiddler2'
             1984  CALL_FUNCTION_1       1  None
           1987_0  COME_FROM          1972  '1972'
             1987  POP_JUMP_IF_FALSE  2005  'to 2005'
             1990  LOAD_GLOBAL           6  '@pytest_ar'
             1993  LOAD_ATTR             8  '_saferepr'
             1996  LOAD_FAST             9  'tiddler2'
             1999  CALL_FUNCTION_1       1  None
             2002  JUMP_FORWARD          3  'to 2008'
             2005  LOAD_CONST               'tiddler2'
           2008_0  COME_FROM          2002  '2002'
             2008  LOAD_CONST               'py3'
             2011  STORE_MAP        
             2012  LOAD_GLOBAL           6  '@pytest_ar'
             2015  LOAD_ATTR             8  '_saferepr'
             2018  LOAD_FAST            12  '@py_assert4'
             2021  CALL_FUNCTION_1       1  None
             2024  LOAD_CONST               'py5'
             2027  STORE_MAP        
             2028  BINARY_MODULO    
             2029  STORE_FAST           14  '@py_format6'
             2032  LOAD_CONST               'assert %(py7)s'
             2035  BUILD_MAP_1           1  None
             2038  LOAD_FAST            14  '@py_format6'
             2041  LOAD_CONST               'py7'
             2044  STORE_MAP        
             2045  BINARY_MODULO    
             2046  STORE_FAST           15  '@py_format8'
             2049  LOAD_GLOBAL           5  'AssertionError'
             2052  LOAD_GLOBAL           6  '@pytest_ar'
             2055  LOAD_ATTR             9  '_format_explanation'
             2058  LOAD_FAST            15  '@py_format8'
             2061  CALL_FUNCTION_1       1  None
             2064  CALL_FUNCTION_1       1  None
             2067  RAISE_VARARGS_1       1  None
             2070  JUMP_FORWARD          0  'to 2073'
           2073_0  COME_FROM          2070  '2070'
             2073  LOAD_CONST               None
             2076  DUP_TOP          
             2077  STORE_FAST            3  '@py_assert0'
             2080  DUP_TOP          
             2081  STORE_FAST            5  '@py_assert2'
             2084  STORE_FAST           12  '@py_assert4'

 L. 125      2087  LOAD_FAST             0  'http'
             2090  LOAD_ATTR             4  'request'

 L. 126      2093  LOAD_CONST               'http://0.0.0.0:8080/search?q=ohhai'
             2096  LOAD_CONST               'headers'

 L. 127      2099  BUILD_MAP_1           1  None
             2102  LOAD_CONST               'application/json'
             2105  LOAD_CONST               'Accept'
             2108  STORE_MAP        
             2109  LOAD_CONST               'method'

 L. 128      2112  LOAD_CONST               'GET'
             2115  CALL_FUNCTION_513   513  None
             2118  UNPACK_SEQUENCE_2     2 
             2121  STORE_FAST            1  'response'
             2124  STORE_FAST            2  'content'

 L. 129      2127  LOAD_FAST             1  'response'
             2130  LOAD_CONST               'status'
             2133  BINARY_SUBSCR    
             2134  LOAD_CONST               '200'
             2137  COMPARE_OP            2  ==
             2140  POP_JUMP_IF_TRUE   2152  'to 2152'
             2143  LOAD_ASSERT              AssertionError
             2146  LOAD_FAST             2  'content'
             2149  RAISE_VARARGS_2       2  None

 L. 131      2152  LOAD_GLOBAL          14  'simplejson'
             2155  LOAD_ATTR            15  'loads'
             2158  LOAD_FAST             2  'content'
             2161  CALL_FUNCTION_1       1  None
             2164  STORE_FAST           10  'info'

 L. 132      2167  LOAD_GLOBAL          16  'len'
             2170  LOAD_FAST            10  'info'
             2173  CALL_FUNCTION_1       1  None
             2176  STORE_FAST            5  '@py_assert2'
             2179  LOAD_CONST               2
             2182  STORE_FAST           11  '@py_assert5'
             2185  LOAD_FAST             5  '@py_assert2'
             2188  LOAD_FAST            11  '@py_assert5'
             2191  COMPARE_OP            2  ==
             2194  STORE_FAST           12  '@py_assert4'
             2197  LOAD_FAST            12  '@py_assert4'
             2200  POP_JUMP_IF_TRUE   2423  'to 2423'
             2203  LOAD_GLOBAL           6  '@pytest_ar'
             2206  LOAD_ATTR             7  '_call_reprcompare'
             2209  LOAD_CONST               ('==',)
             2212  LOAD_FAST            12  '@py_assert4'
             2215  BUILD_TUPLE_1         1 
             2218  LOAD_CONST               ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',)
             2221  LOAD_FAST             5  '@py_assert2'
             2224  LOAD_FAST            11  '@py_assert5'
             2227  BUILD_TUPLE_2         2 
             2230  CALL_FUNCTION_4       4  None
             2233  BUILD_MAP_4           4  None
             2236  LOAD_CONST               'len'
             2239  LOAD_GLOBAL          17  '@py_builtins'
             2242  LOAD_ATTR            18  'locals'
             2245  CALL_FUNCTION_0       0  None
             2248  COMPARE_OP            6  in
             2251  POP_JUMP_IF_TRUE   2269  'to 2269'
             2254  LOAD_GLOBAL           6  '@pytest_ar'
             2257  LOAD_ATTR            19  '_should_repr_global_name'
             2260  LOAD_GLOBAL          16  'len'
             2263  CALL_FUNCTION_1       1  None
           2266_0  COME_FROM          2251  '2251'
             2266  POP_JUMP_IF_FALSE  2284  'to 2284'
             2269  LOAD_GLOBAL           6  '@pytest_ar'
             2272  LOAD_ATTR             8  '_saferepr'
             2275  LOAD_GLOBAL          16  'len'
             2278  CALL_FUNCTION_1       1  None
             2281  JUMP_FORWARD          3  'to 2287'
             2284  LOAD_CONST               'len'
           2287_0  COME_FROM          2281  '2281'
             2287  LOAD_CONST               'py0'
             2290  STORE_MAP        
             2291  LOAD_CONST               'info'
             2294  LOAD_GLOBAL          17  '@py_builtins'
             2297  LOAD_ATTR            18  'locals'
             2300  CALL_FUNCTION_0       0  None
             2303  COMPARE_OP            6  in
             2306  POP_JUMP_IF_TRUE   2324  'to 2324'
             2309  LOAD_GLOBAL           6  '@pytest_ar'
             2312  LOAD_ATTR            19  '_should_repr_global_name'
             2315  LOAD_FAST            10  'info'
             2318  CALL_FUNCTION_1       1  None
           2321_0  COME_FROM          2306  '2306'
             2321  POP_JUMP_IF_FALSE  2339  'to 2339'
             2324  LOAD_GLOBAL           6  '@pytest_ar'
             2327  LOAD_ATTR             8  '_saferepr'
             2330  LOAD_FAST            10  'info'
             2333  CALL_FUNCTION_1       1  None
             2336  JUMP_FORWARD          3  'to 2342'
             2339  LOAD_CONST               'info'
           2342_0  COME_FROM          2336  '2336'
             2342  LOAD_CONST               'py1'
             2345  STORE_MAP        
             2346  LOAD_GLOBAL           6  '@pytest_ar'
             2349  LOAD_ATTR             8  '_saferepr'
             2352  LOAD_FAST             5  '@py_assert2'
             2355  CALL_FUNCTION_1       1  None
             2358  LOAD_CONST               'py3'
             2361  STORE_MAP        
             2362  LOAD_GLOBAL           6  '@pytest_ar'
             2365  LOAD_ATTR             8  '_saferepr'
             2368  LOAD_FAST            11  '@py_assert5'
             2371  CALL_FUNCTION_1       1  None
             2374  LOAD_CONST               'py6'
             2377  STORE_MAP        
             2378  BINARY_MODULO    
             2379  STORE_FAST            7  '@py_format7'
             2382  LOAD_CONST               'assert %(py8)s'
             2385  BUILD_MAP_1           1  None
             2388  LOAD_FAST             7  '@py_format7'
             2391  LOAD_CONST               'py8'
             2394  STORE_MAP        
             2395  BINARY_MODULO    
             2396  STORE_FAST           13  '@py_format9'
             2399  LOAD_GLOBAL           5  'AssertionError'
             2402  LOAD_GLOBAL           6  '@pytest_ar'
             2405  LOAD_ATTR             9  '_format_explanation'
             2408  LOAD_FAST            13  '@py_format9'
             2411  CALL_FUNCTION_1       1  None
             2414  CALL_FUNCTION_1       1  None
             2417  RAISE_VARARGS_1       1  None
             2420  JUMP_FORWARD          0  'to 2423'
           2423_0  COME_FROM          2420  '2420'
             2423  LOAD_CONST               None
             2426  DUP_TOP          
             2427  STORE_FAST            5  '@py_assert2'
             2430  DUP_TOP          
             2431  STORE_FAST           12  '@py_assert4'
             2434  STORE_FAST           11  '@py_assert5'
             2437  LOAD_CONST               None
             2440  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 2437


def test_space_not_expose_subscription_recipes():
    make_fake_space(store, 'foo')
    make_fake_space(store, 'bar')
    make_fake_space(store, 'baz')
    public_recipe = store.get(Recipe('foo_public'))
    private_recipe = store.get(Recipe('foo_private'))
    public_recipe_list = public_recipe.get_recipe()
    private_recipe_list = private_recipe.get_recipe()
    public_recipe_list.insert(-1, ('bar_public', ''))
    private_recipe_list.insert(-2, ('bar_public', ''))
    public_recipe.set_recipe(public_recipe_list)
    private_recipe.set_recipe(private_recipe_list)
    store.put(public_recipe)
    store.put(private_recipe)
    http = httplib2.Http()
    user = User('foo')
    user.set_password('foobar')
    store.put(user)
    user_cookie = get_auth('foo', 'foobar')
    response, content = http.request('http://foo.0.0.0.0:8080/recipes', method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    if not 'foo_public' in content:
        raise AssertionError, content
        if not 'foo_private' not in content:
            raise AssertionError, content
            if not 'bar_public' not in content:
                raise AssertionError, content
                if not 'bar_private' not in content:
                    raise AssertionError, content
                    if not 'baz_' not in content:
                        raise AssertionError, content
                        response, content = http.request('http://foo.0.0.0.0:8080/recipes/foo_public', method='GET')
                        @py_assert0 = response['status']
                        @py_assert3 = '200'
                        @py_assert2 = @py_assert0 == @py_assert3
                        if not @py_assert2:
                            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
                            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
                        @py_assert0 = @py_assert2 = @py_assert3 = None
                        response, content = http.request('http://foo.0.0.0.0:8080/recipes/foo_private', method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie})
                        @py_assert0 = response['status']
                        @py_assert3 = '200'
                        @py_assert2 = @py_assert0 == @py_assert3
                        @py_format5 = @py_assert2 or @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
                        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
                    @py_assert0 = @py_assert2 = @py_assert3 = None
                    response, content = http.request('http://foo.0.0.0.0:8080/recipes/bar_public', method='GET')
                    @py_assert0 = response['status']
                    @py_assert3 = '404'
                    @py_assert2 = @py_assert0 == @py_assert3
                    @py_format5 = @py_assert2 or @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
                    @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format7))
                @py_assert0 = @py_assert2 = @py_assert3 = None
                response, content = http.request('http://foo.0.0.0.0:8080/recipes/bar_private', method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie})
                @py_assert0 = response['status']
                @py_assert3 = '404'
                @py_assert2 = @py_assert0 == @py_assert3
                @py_format5 = @py_assert2 or @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None
            response, content = http.request('http://foo.0.0.0.0:8080/recipes/baz_public', method='GET')
            @py_assert0 = response['status']
            @py_assert3 = '404'
            @py_assert2 = @py_assert0 == @py_assert3
            @py_format5 = @py_assert2 or @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        response, content = http.request('http://foo.0.0.0.0:8080/recipes/baz_private', method='GET')
        @py_assert0 = response['status']
        @py_assert3 = '404'
        @py_assert2 = @py_assert0 == @py_assert3
        @py_format5 = @py_assert2 or @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_disable_ControlView--- This code section failed: ---

 L. 201         0  LOAD_GLOBAL           0  'make_fake_space'
                3  LOAD_GLOBAL           1  'store'
                6  LOAD_CONST               'foo'
                9  CALL_FUNCTION_2       2  None
               12  POP_TOP          

 L. 202        13  LOAD_GLOBAL           0  'make_fake_space'
               16  LOAD_GLOBAL           1  'store'
               19  LOAD_CONST               'bar'
               22  CALL_FUNCTION_2       2  None
               25  POP_TOP          

 L. 203        26  LOAD_GLOBAL           2  'httplib2'
               29  LOAD_ATTR             3  'Http'
               32  CALL_FUNCTION_0       0  None
               35  STORE_FAST            0  'http'

 L. 205        38  LOAD_FAST             0  'http'
               41  LOAD_ATTR             4  'request'
               44  LOAD_CONST               'http://foo.0.0.0.0:8080/recipes'
               47  LOAD_CONST               'method'

 L. 206        50  LOAD_CONST               'GET'
               53  CALL_FUNCTION_257   257  None
               56  UNPACK_SEQUENCE_2     2 
               59  STORE_FAST            1  'response'
               62  STORE_FAST            2  'content'

 L. 208        65  LOAD_CONST               'foo_public'
               68  LOAD_FAST             2  'content'
               71  COMPARE_OP            6  in
               74  POP_JUMP_IF_TRUE     86  'to 86'
               77  LOAD_ASSERT              AssertionError
               80  LOAD_FAST             2  'content'
               83  RAISE_VARARGS_2       2  None

 L. 209        86  LOAD_CONST               'bar_public'
               89  LOAD_FAST             2  'content'
               92  COMPARE_OP            7  not-in
               95  POP_JUMP_IF_TRUE    107  'to 107'
               98  LOAD_ASSERT              AssertionError
              101  LOAD_FAST             2  'content'
              104  RAISE_VARARGS_2       2  None

 L. 211       107  LOAD_FAST             0  'http'
              110  LOAD_ATTR             4  'request'
              113  LOAD_CONST               'http://foo.0.0.0.0:8080/recipes'
              116  LOAD_CONST               'headers'

 L. 212       119  BUILD_MAP_1           1  None
              122  LOAD_CONST               'false'
              125  LOAD_CONST               'X-ControlView'
              128  STORE_MAP        
              129  LOAD_CONST               'method'

 L. 213       132  LOAD_CONST               'GET'
              135  CALL_FUNCTION_513   513  None
              138  UNPACK_SEQUENCE_2     2 
              141  STORE_FAST            1  'response'
              144  STORE_FAST            2  'content'

 L. 215       147  LOAD_CONST               'foo_public'
              150  LOAD_FAST             2  'content'
              153  COMPARE_OP            6  in
              156  POP_JUMP_IF_TRUE    168  'to 168'
              159  LOAD_ASSERT              AssertionError
              162  LOAD_FAST             2  'content'
              165  RAISE_VARARGS_2       2  None

 L. 216       168  LOAD_CONST               'bar_public'
              171  LOAD_FAST             2  'content'
              174  COMPARE_OP            6  in
              177  POP_JUMP_IF_TRUE    189  'to 189'
              180  LOAD_ASSERT              AssertionError
              183  LOAD_FAST             2  'content'
              186  RAISE_VARARGS_2       2  None

 L. 218       189  LOAD_FAST             0  'http'
              192  LOAD_ATTR             4  'request'
              195  LOAD_CONST               'http://foo.0.0.0.0:8080/recipes'
              198  LOAD_CONST               'headers'

 L. 219       201  BUILD_MAP_1           1  None
              204  LOAD_CONST               'true'
              207  LOAD_CONST               'X-ControlView'
              210  STORE_MAP        
              211  LOAD_CONST               'method'

 L. 220       214  LOAD_CONST               'GET'
              217  CALL_FUNCTION_513   513  None
              220  UNPACK_SEQUENCE_2     2 
              223  STORE_FAST            1  'response'
              226  STORE_FAST            2  'content'

 L. 222       229  LOAD_CONST               'foo_public'
              232  LOAD_FAST             2  'content'
              235  COMPARE_OP            6  in
              238  POP_JUMP_IF_TRUE    250  'to 250'
              241  LOAD_ASSERT              AssertionError
              244  LOAD_FAST             2  'content'
              247  RAISE_VARARGS_2       2  None

 L. 223       250  LOAD_CONST               'bar_public'
              253  LOAD_FAST             2  'content'
              256  COMPARE_OP            7  not-in
              259  POP_JUMP_IF_TRUE    271  'to 271'
              262  LOAD_ASSERT              AssertionError
              265  LOAD_FAST             2  'content'
              268  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_FAST' instruction at offset 265


def test_space_server_settings_twrelease():
    http = httplib2.Http()
    response, content = http.request('http://foo.0.0.0.0:8080/')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = '/bags/common/tiddlers/beta_jquery.js'
    @py_assert2 = @py_assert0 not in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = http.request('http://foo.0.0.0.0:8080/tiddlers.wiki')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = '/bags/common/tiddlers/beta_jquery.js'
    @py_assert2 = @py_assert0 not in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'TiddlyWiki created by Jeremy Ruston'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = http.request('http://foo.0.0.0.0:8080/tiddlers', headers={'Accept': 'text/x-tiddlywiki'})
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = '/bags/common/tiddlers/beta_jquery.js'
    @py_assert2 = @py_assert0 not in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'TiddlyWiki created by Jeremy Ruston'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    tiddler = Tiddler('ServerSettings', 'foo_public')
    tiddler.text = 'external: True\ntwrelease:beta'
    store.put(tiddler)
    tiddler2 = Tiddler('fooSetupFlag', 'foo_public')
    store.put(tiddler2)
    response, content = http.request('http://foo.0.0.0.0:8080/')
    if not response['status'] == '200':
        raise AssertionError, content
        @py_assert0 = '/bags/common/tiddlers/beta_jquery.js'
        @py_assert2 = @py_assert0 in content
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        response, content = http.request('http://foo.0.0.0.0:8080/tiddlers', headers={'Accept': 'text/x-tiddlywiki'})
        @py_assert0 = response['status']
        @py_assert3 = '200'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = '/bags/common/tiddlers/beta_jquery.js'
        @py_assert2 = @py_assert0 in content
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'TiddlyWiki created by Jeremy Ruston'
        @py_assert2 = @py_assert0 in content
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        tiddler = Tiddler('ServerSettings', 'foo_public')
        tiddler.text = 'external: True\ntwrelease=beta'
        store.put(tiddler)
        response, content = http.request('http://foo.0.0.0.0:8080/')
        @py_assert0 = response['status']
        @py_assert3 = '200'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = '/bags/common/tiddlers/beta_jquery.js'
        @py_assert2 = @py_assert0 not in content
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        tiddler = Tiddler('ServerSettings', 'foo_public')
        tiddler.text = 'external: True\n\ntwrelease:beta'
        store.put(tiddler)
        response, content = http.request('http://foo.0.0.0.0:8080/')
        @py_assert0 = response['status']
        @py_assert3 = '200'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = '/bags/common/tiddlers/beta_jquery.js'
        @py_assert2 = @py_assert0 in content
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        tiddler = Tiddler('ServerSettings', 'foo_public')
        tiddler.text = 'external: True'
        store.put(tiddler)
        response, content = http.request('http://foo.0.0.0.0:8080/')
        if not response['status'] == '200':
            raise AssertionError, content
            @py_assert0 = '/bags/common/tiddlers/twjquery.js'
            @py_assert2 = @py_assert0 in content
            if not @py_assert2:
                @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert0 = @py_assert2 = None
            response, content = http.request('http://foo.0.0.0.0:8080/tiddlers', headers={'Accept': 'text/x-tiddlywiki'})
            @py_assert0 = response['status']
            @py_assert3 = '200'
            @py_assert2 = @py_assert0 == @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None
            @py_assert0 = '/bags/common/tiddlers/twjquery.js'
            @py_assert2 = @py_assert0 in content
            if not @py_assert2:
                @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert0 = @py_assert2 = None
            @py_assert0 = '/bags/common/tiddlers/twcore.js'
            @py_assert2 = @py_assert0 in content
            if not @py_assert2:
                @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert0 = @py_assert2 = None
            @py_assert0 = 'TiddlyWiki created by Jeremy Ruston'
            @py_assert2 = @py_assert0 in content
            @py_format4 = @py_assert2 or @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        response, content = http.request('http://foo.0.0.0.0:8080/bags/common/tiddlers/twcore.js')
        @py_assert0 = response['status']
        @py_assert3 = '200'
        @py_assert2 = @py_assert0 == @py_assert3
        @py_format5 = @py_assert2 or @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_space_server_settings_filter():
    http = httplib2.Http()
    response, content = http.request('http://foo.0.0.0.0:8080/')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'tags="excludeLists '
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    tiddler = Tiddler('ServerSettings', 'foo_public')
    tiddler.text = 'twrelease:beta\nselect: tag:!excludeLists\n'
    store.put(tiddler)
    response, content = http.request('http://foo.0.0.0.0:8080/')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'tags="excludeLists '
    @py_assert2 = @py_assert0 not in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_space_server_settings_index():
    http = httplib2.Http()
    response, content = http.request('http://foo.0.0.0.0:8080/')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'TiddlyWiki'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    tiddler = Tiddler('ServerSettings', 'foo_public')
    tiddler.text = 'index: MySPA\n'
    store.put(tiddler)
    http = httplib2.Http()
    response, content = http.request('http://foo.0.0.0.0:8080/')
    @py_assert0 = response['status']
    @py_assert3 = '404'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    tiddler = Tiddler('MySPA', 'foo_public')
    tiddler.text = '<html><h1>Hello!</h1></html>'
    tiddler.type = 'text/html'
    store.put(tiddler)
    http = httplib2.Http()
    response, content = http.request('http://foo.0.0.0.0:8080/')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = '<h1>Hello!</h1>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'TiddlyWiki'
    @py_assert2 = @py_assert0 not in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'TiddlyWeb'
    @py_assert2 = @py_assert0 not in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_notifications_bag_visibility():
    """
    notifications bag is considered an ADMIN_BAG
    """
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/bags/notifications/tiddlers')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://foo.0.0.0.0:8080/bags/notifications/tiddlers')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_space_wiki_noscript_link_is_tiddlers():
    """
    The link in the noscript section of a space-based (recipe-created)
    tiddlywiki should be to /tiddlers not to the recipe.
    """
    tiddler = Tiddler('ServerSettings', 'foo_public')
    store.delete(tiddler)
    http = httplib2.Http()
    response, content = http.request('http://foo.0.0.0.0:8080/')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'you may still <a href="/tiddlers">browse'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = http.request('http://foo.0.0.0.0:8080/tiddlers.wiki')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'you may still <a href="/tiddlers">browse'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = http.request('http://foo.0.0.0.0:8080/recipes/foo_public/tiddlers.wiki')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'you may still <a href="/tiddlers">browse'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = http.request('http://foo.0.0.0.0:8080/bags/foo_public/tiddlers.wiki')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'you may still <a href="/bags/foo_public/tiddlers">browse'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return