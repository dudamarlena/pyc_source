# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.privateer/test/test_serve.py
# Compiled at: 2011-03-23 12:21:54
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, shutil
from base64 import b64encode
from wsgi_intercept import httplib2_intercept
import wsgi_intercept, httplib2
from urllib import urlencode
from simplejson import dumps, loads
from tiddlyweb.config import config
from tiddlyweb.web import serve
from tiddlywebplugins.utils import get_store
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.user import User

def setup_module(module):
    try:
        shutil.rmtree('store')
    except:
        pass

    def app():
        return serve.load_app()

    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app)
    module.store = get_store(config)
    module.http = httplib2.Http()
    user = User('cdent')
    user.set_password('cowpoo')
    store.put(user)
    module.authorization = b64encode('cdent:cowpoo')
    user = User('fnd')
    user.set_password('whitespace')
    store.put(user)
    module.other_auth = b64encode('fnd:whitespace')
    bag = Bag('ho')
    bag.policy.read = ['cdent']
    store.put(bag)
    tiddler = Tiddler('junk', 'ho')
    tiddler.text = 'i am unique'
    store.put(tiddler)
    bag = Bag('cars')
    bag.policy.read = ['fnd']
    store.put(bag)
    tiddler = Tiddler('mazda', 'cars')
    tiddler.text = 'funky green'
    store.put(tiddler)


def test_basic_tiddler--- This code section failed: ---

 L.  61         0  LOAD_GLOBAL           0  'http'
                3  LOAD_ATTR             1  'request'

 L.  62         6  LOAD_CONST               'http://0.0.0.0:8080/bags/ho/tiddlers/junk.txt'
                9  CALL_FUNCTION_1       1  None
               12  UNPACK_SEQUENCE_2     2 
               15  STORE_FAST            0  'response'
               18  STORE_FAST            1  'content'

 L.  63        21  LOAD_FAST             0  'response'
               24  LOAD_CONST               'status'
               27  BINARY_SUBSCR    
               28  STORE_FAST            2  '@py_assert0'
               31  LOAD_CONST               '401'
               34  STORE_FAST            3  '@py_assert3'
               37  LOAD_FAST             2  '@py_assert0'
               40  LOAD_FAST             3  '@py_assert3'
               43  COMPARE_OP            2  ==
               46  STORE_FAST            4  '@py_assert2'
               49  LOAD_FAST             4  '@py_assert2'
               52  POP_JUMP_IF_TRUE    165  'to 165'
               55  LOAD_GLOBAL           2  '@pytest_ar'
               58  LOAD_ATTR             3  '_call_reprcompare'
               61  LOAD_CONST               ('==',)
               64  LOAD_FAST             4  '@py_assert2'
               67  BUILD_TUPLE_1         1 
               70  LOAD_CONST               ('%(py1)s == %(py4)s',)
               73  LOAD_FAST             2  '@py_assert0'
               76  LOAD_FAST             3  '@py_assert3'
               79  BUILD_TUPLE_2         2 
               82  CALL_FUNCTION_4       4  None
               85  BUILD_MAP_2           2  None
               88  LOAD_GLOBAL           2  '@pytest_ar'
               91  LOAD_ATTR             4  '_saferepr'
               94  LOAD_FAST             2  '@py_assert0'
               97  CALL_FUNCTION_1       1  None
              100  LOAD_CONST               'py1'
              103  STORE_MAP        
              104  LOAD_GLOBAL           2  '@pytest_ar'
              107  LOAD_ATTR             4  '_saferepr'
              110  LOAD_FAST             3  '@py_assert3'
              113  CALL_FUNCTION_1       1  None
              116  LOAD_CONST               'py4'
              119  STORE_MAP        
              120  BINARY_MODULO    
              121  STORE_FAST            5  '@py_format5'
              124  LOAD_CONST               'assert %(py6)s'
              127  BUILD_MAP_1           1  None
              130  LOAD_FAST             5  '@py_format5'
              133  LOAD_CONST               'py6'
              136  STORE_MAP        
              137  BINARY_MODULO    
              138  STORE_FAST            6  '@py_format7'
              141  LOAD_GLOBAL           5  'AssertionError'
              144  LOAD_GLOBAL           2  '@pytest_ar'
              147  LOAD_ATTR             6  '_format_explanation'
              150  LOAD_FAST             6  '@py_format7'
              153  CALL_FUNCTION_1       1  None
              156  CALL_FUNCTION_1       1  None
              159  RAISE_VARARGS_1       1  None
              162  JUMP_FORWARD          0  'to 165'
            165_0  COME_FROM           162  '162'
              165  LOAD_CONST               None
              168  DUP_TOP          
              169  STORE_FAST            2  '@py_assert0'
              172  DUP_TOP          
              173  STORE_FAST            4  '@py_assert2'
              176  STORE_FAST            3  '@py_assert3'

 L.  65       179  LOAD_GLOBAL           8  '_make_mapping'
              182  LOAD_CONST               'http://0.0.0.0:8080/bags/ho/tiddlers/junk.txt'

 L.  66       185  LOAD_GLOBAL           9  'authorization'
              188  CALL_FUNCTION_2       2  None
              191  STORE_FAST            7  'location'

 L.  67       194  LOAD_CONST               'http://0.0.0.0:8080/_/'
              197  STORE_FAST            2  '@py_assert0'
              200  LOAD_FAST             2  '@py_assert0'
              203  LOAD_FAST             7  'location'
              206  COMPARE_OP            6  in
              209  STORE_FAST            4  '@py_assert2'
              212  LOAD_FAST             4  '@py_assert2'
              215  POP_JUMP_IF_TRUE    374  'to 374'
              218  LOAD_GLOBAL           2  '@pytest_ar'
              221  LOAD_ATTR             3  '_call_reprcompare'
              224  LOAD_CONST               ('in',)
              227  LOAD_FAST             4  '@py_assert2'
              230  BUILD_TUPLE_1         1 
              233  LOAD_CONST               ('%(py1)s in %(py3)s',)
              236  LOAD_FAST             2  '@py_assert0'
              239  LOAD_FAST             7  'location'
              242  BUILD_TUPLE_2         2 
              245  CALL_FUNCTION_4       4  None
              248  BUILD_MAP_2           2  None
              251  LOAD_GLOBAL           2  '@pytest_ar'
              254  LOAD_ATTR             4  '_saferepr'
              257  LOAD_FAST             2  '@py_assert0'
              260  CALL_FUNCTION_1       1  None
              263  LOAD_CONST               'py1'
              266  STORE_MAP        
              267  LOAD_CONST               'location'
              270  LOAD_GLOBAL          10  '@py_builtins'
              273  LOAD_ATTR            11  'locals'
              276  CALL_FUNCTION_0       0  None
              279  DUP_TOP          
              280  ROT_THREE        
              281  COMPARE_OP            6  in
              284  JUMP_IF_FALSE_OR_POP   302  'to 302'
              287  LOAD_GLOBAL          10  '@py_builtins'
              290  LOAD_ATTR            12  'globals'
              293  CALL_FUNCTION_0       0  None
              296  COMPARE_OP            9  is-not
              299  JUMP_FORWARD          2  'to 304'
            302_0  COME_FROM           284  '284'
              302  ROT_TWO          
              303  POP_TOP          
            304_0  COME_FROM           299  '299'
              304  POP_JUMP_IF_FALSE   322  'to 322'
              307  LOAD_GLOBAL           2  '@pytest_ar'
              310  LOAD_ATTR             4  '_saferepr'
              313  LOAD_FAST             7  'location'
              316  CALL_FUNCTION_1       1  None
              319  JUMP_FORWARD          3  'to 325'
              322  LOAD_CONST               'location'
            325_0  COME_FROM           319  '319'
              325  LOAD_CONST               'py3'
              328  STORE_MAP        
              329  BINARY_MODULO    
              330  STORE_FAST            8  '@py_format4'
              333  LOAD_CONST               'assert %(py5)s'
              336  BUILD_MAP_1           1  None
              339  LOAD_FAST             8  '@py_format4'
              342  LOAD_CONST               'py5'
              345  STORE_MAP        
              346  BINARY_MODULO    
              347  STORE_FAST            9  '@py_format6'
              350  LOAD_GLOBAL           5  'AssertionError'
              353  LOAD_GLOBAL           2  '@pytest_ar'
              356  LOAD_ATTR             6  '_format_explanation'
              359  LOAD_FAST             9  '@py_format6'
              362  CALL_FUNCTION_1       1  None
              365  CALL_FUNCTION_1       1  None
              368  RAISE_VARARGS_1       1  None
              371  JUMP_FORWARD          0  'to 374'
            374_0  COME_FROM           371  '371'
              374  LOAD_CONST               None
              377  DUP_TOP          
              378  STORE_FAST            2  '@py_assert0'
              381  STORE_FAST            4  '@py_assert2'

 L.  69       384  LOAD_GLOBAL           0  'http'
              387  LOAD_ATTR             1  'request'
              390  LOAD_FAST             7  'location'
              393  CALL_FUNCTION_1       1  None
              396  UNPACK_SEQUENCE_2     2 
              399  STORE_FAST            0  'response'
              402  STORE_FAST            1  'content'

 L.  70       405  LOAD_FAST             0  'response'
              408  LOAD_CONST               'status'
              411  BINARY_SUBSCR    
              412  LOAD_CONST               '200'
              415  COMPARE_OP            2  ==
              418  POP_JUMP_IF_TRUE    430  'to 430'
              421  LOAD_ASSERT              AssertionError
              424  LOAD_FAST             1  'content'
              427  RAISE_VARARGS_2       2  None

 L.  71       430  LOAD_CONST               'i am unique'
              433  STORE_FAST            2  '@py_assert0'
              436  LOAD_FAST             2  '@py_assert0'
              439  LOAD_FAST             1  'content'
              442  COMPARE_OP            6  in
              445  STORE_FAST            4  '@py_assert2'
              448  LOAD_FAST             4  '@py_assert2'
              451  POP_JUMP_IF_TRUE    610  'to 610'
              454  LOAD_GLOBAL           2  '@pytest_ar'
              457  LOAD_ATTR             3  '_call_reprcompare'
              460  LOAD_CONST               ('in',)
              463  LOAD_FAST             4  '@py_assert2'
              466  BUILD_TUPLE_1         1 
              469  LOAD_CONST               ('%(py1)s in %(py3)s',)
              472  LOAD_FAST             2  '@py_assert0'
              475  LOAD_FAST             1  'content'
              478  BUILD_TUPLE_2         2 
              481  CALL_FUNCTION_4       4  None
              484  BUILD_MAP_2           2  None
              487  LOAD_GLOBAL           2  '@pytest_ar'
              490  LOAD_ATTR             4  '_saferepr'
              493  LOAD_FAST             2  '@py_assert0'
              496  CALL_FUNCTION_1       1  None
              499  LOAD_CONST               'py1'
              502  STORE_MAP        
              503  LOAD_CONST               'content'
              506  LOAD_GLOBAL          10  '@py_builtins'
              509  LOAD_ATTR            11  'locals'
              512  CALL_FUNCTION_0       0  None
              515  DUP_TOP          
              516  ROT_THREE        
              517  COMPARE_OP            6  in
              520  JUMP_IF_FALSE_OR_POP   538  'to 538'
              523  LOAD_GLOBAL          10  '@py_builtins'
              526  LOAD_ATTR            12  'globals'
              529  CALL_FUNCTION_0       0  None
              532  COMPARE_OP            9  is-not
              535  JUMP_FORWARD          2  'to 540'
            538_0  COME_FROM           520  '520'
              538  ROT_TWO          
              539  POP_TOP          
            540_0  COME_FROM           535  '535'
              540  POP_JUMP_IF_FALSE   558  'to 558'
              543  LOAD_GLOBAL           2  '@pytest_ar'
              546  LOAD_ATTR             4  '_saferepr'
              549  LOAD_FAST             1  'content'
              552  CALL_FUNCTION_1       1  None
              555  JUMP_FORWARD          3  'to 561'
              558  LOAD_CONST               'content'
            561_0  COME_FROM           555  '555'
              561  LOAD_CONST               'py3'
              564  STORE_MAP        
              565  BINARY_MODULO    
              566  STORE_FAST            8  '@py_format4'
              569  LOAD_CONST               'assert %(py5)s'
              572  BUILD_MAP_1           1  None
              575  LOAD_FAST             8  '@py_format4'
              578  LOAD_CONST               'py5'
              581  STORE_MAP        
              582  BINARY_MODULO    
              583  STORE_FAST            9  '@py_format6'
              586  LOAD_GLOBAL           5  'AssertionError'
              589  LOAD_GLOBAL           2  '@pytest_ar'
              592  LOAD_ATTR             6  '_format_explanation'
              595  LOAD_FAST             9  '@py_format6'
              598  CALL_FUNCTION_1       1  None
              601  CALL_FUNCTION_1       1  None
              604  RAISE_VARARGS_1       1  None
              607  JUMP_FORWARD          0  'to 610'
            610_0  COME_FROM           607  '607'
              610  LOAD_CONST               None
              613  DUP_TOP          
              614  STORE_FAST            2  '@py_assert0'
              617  STORE_FAST            4  '@py_assert2'

 L.  73       620  LOAD_GLOBAL           0  'http'
              623  LOAD_ATTR             1  'request'
              626  LOAD_FAST             7  'location'
              629  LOAD_CONST               'method'
              632  LOAD_CONST               'PUT'
              635  CALL_FUNCTION_257   257  None
              638  UNPACK_SEQUENCE_2     2 
              641  STORE_FAST            0  'response'
              644  STORE_FAST            1  'content'

 L.  74       647  LOAD_FAST             0  'response'
              650  LOAD_CONST               'status'
              653  BINARY_SUBSCR    
              654  STORE_FAST            2  '@py_assert0'
              657  LOAD_CONST               '405'
              660  STORE_FAST            3  '@py_assert3'
              663  LOAD_FAST             2  '@py_assert0'
              666  LOAD_FAST             3  '@py_assert3'
              669  COMPARE_OP            2  ==
              672  STORE_FAST            4  '@py_assert2'
              675  LOAD_FAST             4  '@py_assert2'
              678  POP_JUMP_IF_TRUE    791  'to 791'
              681  LOAD_GLOBAL           2  '@pytest_ar'
              684  LOAD_ATTR             3  '_call_reprcompare'
              687  LOAD_CONST               ('==',)
              690  LOAD_FAST             4  '@py_assert2'
              693  BUILD_TUPLE_1         1 
              696  LOAD_CONST               ('%(py1)s == %(py4)s',)
              699  LOAD_FAST             2  '@py_assert0'
              702  LOAD_FAST             3  '@py_assert3'
              705  BUILD_TUPLE_2         2 
              708  CALL_FUNCTION_4       4  None
              711  BUILD_MAP_2           2  None
              714  LOAD_GLOBAL           2  '@pytest_ar'
              717  LOAD_ATTR             4  '_saferepr'
              720  LOAD_FAST             2  '@py_assert0'
              723  CALL_FUNCTION_1       1  None
              726  LOAD_CONST               'py1'
              729  STORE_MAP        
              730  LOAD_GLOBAL           2  '@pytest_ar'
              733  LOAD_ATTR             4  '_saferepr'
              736  LOAD_FAST             3  '@py_assert3'
              739  CALL_FUNCTION_1       1  None
              742  LOAD_CONST               'py4'
              745  STORE_MAP        
              746  BINARY_MODULO    
              747  STORE_FAST            5  '@py_format5'
              750  LOAD_CONST               'assert %(py6)s'
              753  BUILD_MAP_1           1  None
              756  LOAD_FAST             5  '@py_format5'
              759  LOAD_CONST               'py6'
              762  STORE_MAP        
              763  BINARY_MODULO    
              764  STORE_FAST            6  '@py_format7'
              767  LOAD_GLOBAL           5  'AssertionError'
              770  LOAD_GLOBAL           2  '@pytest_ar'
              773  LOAD_ATTR             6  '_format_explanation'
              776  LOAD_FAST             6  '@py_format7'
              779  CALL_FUNCTION_1       1  None
              782  CALL_FUNCTION_1       1  None
              785  RAISE_VARARGS_1       1  None
              788  JUMP_FORWARD          0  'to 791'
            791_0  COME_FROM           788  '788'
              791  LOAD_CONST               None
              794  DUP_TOP          
              795  STORE_FAST            2  '@py_assert0'
              798  DUP_TOP          
              799  STORE_FAST            4  '@py_assert2'
              802  STORE_FAST            3  '@py_assert3'

 L.  76       805  LOAD_GLOBAL           0  'http'
              808  LOAD_ATTR             1  'request'
              811  LOAD_CONST               'http://0.0.0.0:8080/_/nonono'
              814  CALL_FUNCTION_1       1  None
              817  UNPACK_SEQUENCE_2     2 
              820  STORE_FAST            0  'response'
              823  STORE_FAST            1  'content'

 L.  77       826  LOAD_FAST             0  'response'
              829  LOAD_CONST               'status'
              832  BINARY_SUBSCR    
              833  STORE_FAST            2  '@py_assert0'
              836  LOAD_CONST               '404'
              839  STORE_FAST            3  '@py_assert3'
              842  LOAD_FAST             2  '@py_assert0'
              845  LOAD_FAST             3  '@py_assert3'
              848  COMPARE_OP            2  ==
              851  STORE_FAST            4  '@py_assert2'
              854  LOAD_FAST             4  '@py_assert2'
              857  POP_JUMP_IF_TRUE    970  'to 970'
              860  LOAD_GLOBAL           2  '@pytest_ar'
              863  LOAD_ATTR             3  '_call_reprcompare'
              866  LOAD_CONST               ('==',)
              869  LOAD_FAST             4  '@py_assert2'
              872  BUILD_TUPLE_1         1 
              875  LOAD_CONST               ('%(py1)s == %(py4)s',)
              878  LOAD_FAST             2  '@py_assert0'
              881  LOAD_FAST             3  '@py_assert3'
              884  BUILD_TUPLE_2         2 
              887  CALL_FUNCTION_4       4  None
              890  BUILD_MAP_2           2  None
              893  LOAD_GLOBAL           2  '@pytest_ar'
              896  LOAD_ATTR             4  '_saferepr'
              899  LOAD_FAST             2  '@py_assert0'
              902  CALL_FUNCTION_1       1  None
              905  LOAD_CONST               'py1'
              908  STORE_MAP        
              909  LOAD_GLOBAL           2  '@pytest_ar'
              912  LOAD_ATTR             4  '_saferepr'
              915  LOAD_FAST             3  '@py_assert3'
              918  CALL_FUNCTION_1       1  None
              921  LOAD_CONST               'py4'
              924  STORE_MAP        
              925  BINARY_MODULO    
              926  STORE_FAST            5  '@py_format5'
              929  LOAD_CONST               'assert %(py6)s'
              932  BUILD_MAP_1           1  None
              935  LOAD_FAST             5  '@py_format5'
              938  LOAD_CONST               'py6'
              941  STORE_MAP        
              942  BINARY_MODULO    
              943  STORE_FAST            6  '@py_format7'
              946  LOAD_GLOBAL           5  'AssertionError'
              949  LOAD_GLOBAL           2  '@pytest_ar'
              952  LOAD_ATTR             6  '_format_explanation'
              955  LOAD_FAST             6  '@py_format7'
              958  CALL_FUNCTION_1       1  None
              961  CALL_FUNCTION_1       1  None
              964  RAISE_VARARGS_1       1  None
              967  JUMP_FORWARD          0  'to 970'
            970_0  COME_FROM           967  '967'
              970  LOAD_CONST               None
              973  DUP_TOP          
              974  STORE_FAST            2  '@py_assert0'
              977  DUP_TOP          
              978  STORE_FAST            4  '@py_assert2'
              981  STORE_FAST            3  '@py_assert3'

 L.  79       984  LOAD_GLOBAL           0  'http'
              987  LOAD_ATTR             1  'request'
              990  LOAD_FAST             7  'location'
              993  LOAD_CONST               'method'
              996  LOAD_CONST               'DELETE'
              999  CALL_FUNCTION_257   257  None
             1002  UNPACK_SEQUENCE_2     2 
             1005  STORE_FAST            0  'response'
             1008  STORE_FAST            1  'content'

 L.  80      1011  LOAD_FAST             0  'response'
             1014  LOAD_CONST               'status'
             1017  BINARY_SUBSCR    
             1018  LOAD_CONST               '403'
             1021  COMPARE_OP            2  ==
             1024  POP_JUMP_IF_TRUE   1036  'to 1036'
             1027  LOAD_ASSERT              AssertionError
             1030  LOAD_FAST             1  'content'
             1033  RAISE_VARARGS_2       2  None

 L.  82      1036  LOAD_GLOBAL           0  'http'
             1039  LOAD_ATTR             1  'request'
             1042  LOAD_FAST             7  'location'
             1045  LOAD_CONST               'method'
             1048  LOAD_CONST               'DELETE'
             1051  LOAD_CONST               'headers'

 L.  83      1054  BUILD_MAP_1           1  None
             1057  LOAD_CONST               'Basic %s'
             1060  LOAD_GLOBAL          13  'other_auth'
             1063  BINARY_MODULO    
             1064  LOAD_CONST               'Authorization'
             1067  STORE_MAP        
             1068  CALL_FUNCTION_513   513  None
             1071  UNPACK_SEQUENCE_2     2 
             1074  STORE_FAST            0  'response'
             1077  STORE_FAST            1  'content'

 L.  84      1080  LOAD_FAST             0  'response'
             1083  LOAD_CONST               'status'
             1086  BINARY_SUBSCR    
             1087  LOAD_CONST               '404'
             1090  COMPARE_OP            2  ==
             1093  POP_JUMP_IF_TRUE   1105  'to 1105'
             1096  LOAD_ASSERT              AssertionError
             1099  LOAD_FAST             1  'content'
             1102  RAISE_VARARGS_2       2  None

 L.  86      1105  LOAD_GLOBAL           0  'http'
             1108  LOAD_ATTR             1  'request'
             1111  LOAD_FAST             7  'location'
             1114  LOAD_CONST               'method'
             1117  LOAD_CONST               'DELETE'
             1120  LOAD_CONST               'headers'

 L.  87      1123  BUILD_MAP_1           1  None
             1126  LOAD_CONST               'Basic %s'
             1129  LOAD_GLOBAL           9  'authorization'
             1132  BINARY_MODULO    
             1133  LOAD_CONST               'Authorization'
             1136  STORE_MAP        
             1137  CALL_FUNCTION_513   513  None
             1140  UNPACK_SEQUENCE_2     2 
             1143  STORE_FAST            0  'response'
             1146  STORE_FAST            1  'content'

 L.  88      1149  LOAD_FAST             0  'response'
             1152  LOAD_CONST               'status'
             1155  BINARY_SUBSCR    
             1156  LOAD_CONST               '204'
             1159  COMPARE_OP            2  ==
             1162  POP_JUMP_IF_TRUE   1174  'to 1174'
             1165  LOAD_ASSERT              AssertionError
             1168  LOAD_FAST             1  'content'
             1171  RAISE_VARARGS_2       2  None

 L.  90      1174  LOAD_GLOBAL           0  'http'
             1177  LOAD_ATTR             1  'request'
             1180  LOAD_FAST             7  'location'
             1183  CALL_FUNCTION_1       1  None
             1186  UNPACK_SEQUENCE_2     2 
             1189  STORE_FAST            0  'response'
             1192  STORE_FAST            1  'content'

 L.  91      1195  LOAD_FAST             0  'response'
             1198  LOAD_CONST               'status'
             1201  BINARY_SUBSCR    
             1202  LOAD_CONST               '404'
             1205  COMPARE_OP            2  ==
             1208  POP_JUMP_IF_TRUE   1220  'to 1220'
             1211  LOAD_ASSERT              AssertionError
             1214  LOAD_FAST             1  'content'
             1217  RAISE_VARARGS_2       2  None
             1220  LOAD_CONST               None
             1223  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 1220


def test_with_query():
    location = _make_mapping('http://0.0.0.0:8080/bags/ho/tiddlers?select=title:junk', authorization)
    @py_assert0 = 'http://0.0.0.0:8080/_/'
    @py_assert2 = @py_assert0 in location
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, location)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(location) if 'location' in @py_builtins.locals() is not @py_builtins.globals() else 'location'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = http.request(location)
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'junk'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() is not @py_builtins.globals() else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_lister():
    location_c_one = _make_mapping('http://0.0.0.0:8080/bags/ho/tiddlers/junk', authorization)
    location_c_two = _make_mapping('http://0.0.0.0:8080/bags/ho/tiddlers/junk.txt', authorization)
    location_f_one = _make_mapping('http://0.0.0.0:8080/bags/cars/tiddlers/mazda', other_auth)
    location_f_one = _make_mapping('http://0.0.0.0:8080/bags/cars/tiddlers/mazda.txt', other_auth)
    response, content = http.request('http://0.0.0.0:8080/_')
    @py_assert0 = response['status']
    @py_assert3 = '401'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://0.0.0.0:8080/_', headers={'Authorization': 'Basic %s' % authorization})
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'mazda'
    @py_assert2 = @py_assert0 not in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() is not @py_builtins.globals() else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    info = loads(content)
    @py_assert2 = len(info)
    @py_assert5 = 3
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() is not @py_builtins.globals() else 'len', 'py1': @pytest_ar._saferepr(info) if 'info' in @py_builtins.locals() is not @py_builtins.globals() else 'info', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    response, content = http.request('http://0.0.0.0:8080/_', headers={'Authorization': 'Basic %s' % other_auth})
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'junk'
    @py_assert2 = @py_assert0 not in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() is not @py_builtins.globals() else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    info = loads(content)
    @py_assert2 = len(info)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() is not @py_builtins.globals() else 'len', 'py1': @pytest_ar._saferepr(info) if 'info' in @py_builtins.locals() is not @py_builtins.globals() else 'info', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def _make_mapping--- This code section failed: ---

 L. 138         0  BUILD_MAP_1           1  None
                3  LOAD_FAST             0  'uri'
                6  LOAD_CONST               'uri'
                9  STORE_MAP        
               10  STORE_FAST            2  'post_data'

 L. 139        13  LOAD_GLOBAL           0  'dumps'
               16  LOAD_FAST             2  'post_data'
               19  CALL_FUNCTION_1       1  None
               22  STORE_FAST            3  'post_body'

 L. 140        25  LOAD_GLOBAL           1  'http'
               28  LOAD_ATTR             2  'request'
               31  LOAD_CONST               'http://0.0.0.0:8080/_'
               34  LOAD_CONST               'method'

 L. 141        37  LOAD_CONST               'POST'
               40  LOAD_CONST               'headers'

 L. 142        43  BUILD_MAP_2           2  None
               46  LOAD_CONST               'application/json'
               49  LOAD_CONST               'Content-type'
               52  STORE_MAP        

 L. 143        53  LOAD_CONST               'Basic %s'
               56  LOAD_FAST             1  'authorization'
               59  BINARY_MODULO    
               60  LOAD_CONST               'Authorization'
               63  STORE_MAP        
               64  LOAD_CONST               'body'

 L. 144        67  LOAD_FAST             3  'post_body'
               70  CALL_FUNCTION_769   769  None
               73  UNPACK_SEQUENCE_2     2 
               76  STORE_FAST            4  'response'
               79  STORE_FAST            5  'content'

 L. 145        82  LOAD_FAST             4  'response'
               85  LOAD_CONST               'status'
               88  BINARY_SUBSCR    
               89  LOAD_CONST               '201'
               92  COMPARE_OP            2  ==
               95  POP_JUMP_IF_TRUE    107  'to 107'
               98  LOAD_ASSERT              AssertionError
              101  LOAD_FAST             5  'content'
              104  RAISE_VARARGS_2       2  None

 L. 146       107  LOAD_FAST             4  'response'
              110  LOAD_CONST               'location'
              113  BINARY_SUBSCR    
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 114