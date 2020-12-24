# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyspace/test/test_safe_mode.py
# Compiled at: 2013-08-20 13:22:51
"""
Test safe mode which allows a member to recover a space
which has gone pear shaped as a result of the wrong or 
dangerous plugins.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from test.fixtures import make_test_env, make_fake_space
from wsgi_intercept import httplib2_intercept
import wsgi_intercept, httplib2, simplejson, Cookie
from tiddlyweb.model.user import User
from tiddlyweb.model.tiddler import Tiddler
AUTH_COOKIE = None

def setup_module(module):
    make_test_env(module)
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)
    wsgi_intercept.add_wsgi_intercept('cdent.0.0.0.0', 8080, app_fn)
    make_fake_space(module.store, 'cdent')
    user = User('cdent')
    user.set_password('cow')
    module.store.put(user)
    module.http = httplib2.Http()


def test_safe_403():
    response, content = http.request('http://cdent.0.0.0.0:8080/_safe', method='GET', headers={'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '403'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'membership required'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = http.request('http://cdent.0.0.0.0:8080/_safe', method='POST', headers={'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '403'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'membership required'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_safe_exists--- This code section failed: ---

 L.  49         0  LOAD_GLOBAL           0  'http'
                3  LOAD_ATTR             1  'request'

 L.  50         6  LOAD_CONST               'http://0.0.0.0:8080/challenge/tiddlywebplugins.tiddlyspace.cookie_form'
                9  LOAD_CONST               'body'

 L.  51        12  LOAD_CONST               'user=cdent&password=cow'
               15  LOAD_CONST               'method'

 L.  52        18  LOAD_CONST               'POST'
               21  LOAD_CONST               'headers'

 L.  53        24  BUILD_MAP_1           1  None
               27  LOAD_CONST               'application/x-www-form-urlencoded'
               30  LOAD_CONST               'Content-Type'
               33  STORE_MAP        
               34  CALL_FUNCTION_769   769  None
               37  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST            0  'response'
               43  STORE_FAST            1  'content'

 L.  54        46  LOAD_FAST             0  'response'
               49  LOAD_ATTR             2  'previous'
               52  LOAD_CONST               'status'
               55  BINARY_SUBSCR    
               56  STORE_FAST            2  '@py_assert0'
               59  LOAD_CONST               '303'
               62  STORE_FAST            3  '@py_assert3'
               65  LOAD_FAST             2  '@py_assert0'
               68  LOAD_FAST             3  '@py_assert3'
               71  COMPARE_OP            2  ==
               74  STORE_FAST            4  '@py_assert2'
               77  LOAD_FAST             4  '@py_assert2'
               80  UNARY_NOT        
               81  POP_JUMP_IF_FALSE   200  'to 200'
               84  LOAD_GLOBAL           3  '@pytest_ar'
               87  LOAD_ATTR             4  '_call_reprcompare'
               90  LOAD_CONST               '=='
               93  BUILD_TUPLE_1         1 
               96  LOAD_FAST             4  '@py_assert2'
               99  BUILD_TUPLE_1         1 
              102  LOAD_CONST               '%(py1)s == %(py4)s'
              105  BUILD_TUPLE_1         1 
              108  LOAD_FAST             2  '@py_assert0'
              111  LOAD_FAST             3  '@py_assert3'
              114  BUILD_TUPLE_2         2 
              117  CALL_FUNCTION_4       4  None
              120  BUILD_MAP_2           2  None
              123  LOAD_GLOBAL           3  '@pytest_ar'
              126  LOAD_ATTR             5  '_saferepr'
              129  LOAD_FAST             2  '@py_assert0'
              132  CALL_FUNCTION_1       1  None
              135  LOAD_CONST               'py1'
              138  STORE_MAP        
              139  LOAD_GLOBAL           3  '@pytest_ar'
              142  LOAD_ATTR             5  '_saferepr'
              145  LOAD_FAST             3  '@py_assert3'
              148  CALL_FUNCTION_1       1  None
              151  LOAD_CONST               'py4'
              154  STORE_MAP        
              155  BINARY_MODULO    
              156  STORE_FAST            5  '@py_format5'
              159  LOAD_CONST               'assert %(py6)s'
              162  BUILD_MAP_1           1  None
              165  LOAD_FAST             5  '@py_format5'
              168  LOAD_CONST               'py6'
              171  STORE_MAP        
              172  BINARY_MODULO    
              173  STORE_FAST            6  '@py_format7'
              176  LOAD_GLOBAL           6  'AssertionError'
              179  LOAD_GLOBAL           3  '@pytest_ar'
              182  LOAD_ATTR             7  '_format_explanation'
              185  LOAD_FAST             6  '@py_format7'
              188  CALL_FUNCTION_1       1  None
              191  CALL_FUNCTION_1       1  None
              194  RAISE_VARARGS_1       1  None
              197  JUMP_FORWARD          0  'to 200'
            200_0  COME_FROM           197  '197'
              200  LOAD_GLOBAL           8  'None'
              203  DUP_TOP          
              204  STORE_FAST            2  '@py_assert0'
              207  DUP_TOP          
              208  STORE_FAST            4  '@py_assert2'
              211  STORE_FAST            3  '@py_assert3'

 L.  56       214  LOAD_FAST             0  'response'
              217  LOAD_ATTR             2  'previous'
              220  LOAD_CONST               'set-cookie'
              223  BINARY_SUBSCR    
              224  STORE_FAST            7  'user_cookie'

 L.  57       227  LOAD_GLOBAL           9  'Cookie'
              230  LOAD_ATTR            10  'SimpleCookie'
              233  CALL_FUNCTION_0       0  None
              236  STORE_FAST            8  'cookie'

 L.  58       239  LOAD_FAST             8  'cookie'
              242  LOAD_ATTR            11  'load'
              245  LOAD_FAST             7  'user_cookie'
              248  CALL_FUNCTION_1       1  None
              251  POP_TOP          

 L.  59       252  LOAD_FAST             8  'cookie'
              255  LOAD_CONST               'tiddlyweb_user'
              258  BINARY_SUBSCR    
              259  LOAD_ATTR            12  'value'
              262  STORE_GLOBAL         13  'AUTH_COOKIE'

 L.  61       265  LOAD_GLOBAL           0  'http'
              268  LOAD_ATTR             1  'request'
              271  LOAD_CONST               'http://cdent.0.0.0.0:8080/_safe'
              274  LOAD_CONST               'method'

 L.  62       277  LOAD_CONST               'GET'
              280  LOAD_CONST               'headers'

 L.  63       283  BUILD_MAP_2           2  None
              286  LOAD_CONST               'application/json'
              289  LOAD_CONST               'Accept'
              292  STORE_MAP        

 L.  64       293  LOAD_CONST               'tiddlyweb_user="%s"'
              296  LOAD_GLOBAL          13  'AUTH_COOKIE'
              299  BINARY_MODULO    
              300  LOAD_CONST               'Cookie'
              303  STORE_MAP        
              304  CALL_FUNCTION_513   513  None
              307  UNPACK_SEQUENCE_2     2 
              310  STORE_FAST            0  'response'
              313  STORE_FAST            1  'content'

 L.  66       316  LOAD_FAST             0  'response'
              319  LOAD_CONST               'status'
              322  BINARY_SUBSCR    
              323  STORE_FAST            2  '@py_assert0'
              326  LOAD_CONST               '200'
              329  STORE_FAST            3  '@py_assert3'
              332  LOAD_FAST             2  '@py_assert0'
              335  LOAD_FAST             3  '@py_assert3'
              338  COMPARE_OP            2  ==
              341  STORE_FAST            4  '@py_assert2'
              344  LOAD_FAST             4  '@py_assert2'
              347  UNARY_NOT        
              348  POP_JUMP_IF_FALSE   467  'to 467'
              351  LOAD_GLOBAL           3  '@pytest_ar'
              354  LOAD_ATTR             4  '_call_reprcompare'
              357  LOAD_CONST               '=='
              360  BUILD_TUPLE_1         1 
              363  LOAD_FAST             4  '@py_assert2'
              366  BUILD_TUPLE_1         1 
              369  LOAD_CONST               '%(py1)s == %(py4)s'
              372  BUILD_TUPLE_1         1 
              375  LOAD_FAST             2  '@py_assert0'
              378  LOAD_FAST             3  '@py_assert3'
              381  BUILD_TUPLE_2         2 
              384  CALL_FUNCTION_4       4  None
              387  BUILD_MAP_2           2  None
              390  LOAD_GLOBAL           3  '@pytest_ar'
              393  LOAD_ATTR             5  '_saferepr'
              396  LOAD_FAST             2  '@py_assert0'
              399  CALL_FUNCTION_1       1  None
              402  LOAD_CONST               'py1'
              405  STORE_MAP        
              406  LOAD_GLOBAL           3  '@pytest_ar'
              409  LOAD_ATTR             5  '_saferepr'
              412  LOAD_FAST             3  '@py_assert3'
              415  CALL_FUNCTION_1       1  None
              418  LOAD_CONST               'py4'
              421  STORE_MAP        
              422  BINARY_MODULO    
              423  STORE_FAST            5  '@py_format5'
              426  LOAD_CONST               'assert %(py6)s'
              429  BUILD_MAP_1           1  None
              432  LOAD_FAST             5  '@py_format5'
              435  LOAD_CONST               'py6'
              438  STORE_MAP        
              439  BINARY_MODULO    
              440  STORE_FAST            6  '@py_format7'
              443  LOAD_GLOBAL           6  'AssertionError'
              446  LOAD_GLOBAL           3  '@pytest_ar'
              449  LOAD_ATTR             7  '_format_explanation'
              452  LOAD_FAST             6  '@py_format7'
              455  CALL_FUNCTION_1       1  None
              458  CALL_FUNCTION_1       1  None
              461  RAISE_VARARGS_1       1  None
              464  JUMP_FORWARD          0  'to 467'
            467_0  COME_FROM           464  '464'
              467  LOAD_GLOBAL           8  'None'
              470  DUP_TOP          
              471  STORE_FAST            2  '@py_assert0'
              474  DUP_TOP          
              475  STORE_FAST            4  '@py_assert2'
              478  STORE_FAST            3  '@py_assert3'

 L.  67       481  LOAD_CONST               'form'
              484  STORE_FAST            2  '@py_assert0'
              487  LOAD_FAST             2  '@py_assert0'
              490  LOAD_FAST             1  'content'
              493  COMPARE_OP            6  in
              496  STORE_FAST            4  '@py_assert2'
              499  LOAD_FAST             4  '@py_assert2'
              502  UNARY_NOT        
              503  POP_JUMP_IF_FALSE   661  'to 661'
              506  LOAD_GLOBAL           3  '@pytest_ar'
              509  LOAD_ATTR             4  '_call_reprcompare'
              512  LOAD_CONST               'in'
              515  BUILD_TUPLE_1         1 
              518  LOAD_FAST             4  '@py_assert2'
              521  BUILD_TUPLE_1         1 
              524  LOAD_CONST               '%(py1)s in %(py3)s'
              527  BUILD_TUPLE_1         1 
              530  LOAD_FAST             2  '@py_assert0'
              533  LOAD_FAST             1  'content'
              536  BUILD_TUPLE_2         2 
              539  CALL_FUNCTION_4       4  None
              542  BUILD_MAP_2           2  None
              545  LOAD_GLOBAL           3  '@pytest_ar'
              548  LOAD_ATTR             5  '_saferepr'
              551  LOAD_FAST             2  '@py_assert0'
              554  CALL_FUNCTION_1       1  None
              557  LOAD_CONST               'py1'
              560  STORE_MAP        
              561  LOAD_CONST               'content'
              564  LOAD_GLOBAL          14  '@py_builtins'
              567  LOAD_ATTR            15  'locals'
              570  CALL_FUNCTION_0       0  None
              573  COMPARE_OP            6  in
              576  JUMP_IF_TRUE_OR_POP   591  'to 591'
              579  LOAD_GLOBAL           3  '@pytest_ar'
              582  LOAD_ATTR            16  '_should_repr_global_name'
              585  LOAD_FAST             1  'content'
              588  CALL_FUNCTION_1       1  None
            591_0  COME_FROM           576  '576'
              591  POP_JUMP_IF_FALSE   609  'to 609'
              594  LOAD_GLOBAL           3  '@pytest_ar'
              597  LOAD_ATTR             5  '_saferepr'
              600  LOAD_FAST             1  'content'
              603  CALL_FUNCTION_1       1  None
              606  JUMP_FORWARD          3  'to 612'
              609  LOAD_CONST               'content'
            612_0  COME_FROM           606  '606'
              612  LOAD_CONST               'py3'
              615  STORE_MAP        
              616  BINARY_MODULO    
              617  STORE_FAST            9  '@py_format4'
              620  LOAD_CONST               'assert %(py5)s'
              623  BUILD_MAP_1           1  None
              626  LOAD_FAST             9  '@py_format4'
              629  LOAD_CONST               'py5'
              632  STORE_MAP        
              633  BINARY_MODULO    
              634  STORE_FAST           10  '@py_format6'
              637  LOAD_GLOBAL           6  'AssertionError'
              640  LOAD_GLOBAL           3  '@pytest_ar'
              643  LOAD_ATTR             7  '_format_explanation'
              646  LOAD_FAST            10  '@py_format6'
              649  CALL_FUNCTION_1       1  None
              652  CALL_FUNCTION_1       1  None
              655  RAISE_VARARGS_1       1  None
              658  JUMP_FORWARD          0  'to 661'
            661_0  COME_FROM           658  '658'
              661  LOAD_GLOBAL           8  'None'
              664  DUP_TOP          
              665  STORE_FAST            2  '@py_assert0'
              668  STORE_FAST            4  '@py_assert2'

 L.  68       671  LOAD_CONST               'Are you sure'
              674  STORE_FAST            2  '@py_assert0'
              677  LOAD_FAST             2  '@py_assert0'
              680  LOAD_FAST             1  'content'
              683  COMPARE_OP            6  in
              686  STORE_FAST            4  '@py_assert2'
              689  LOAD_FAST             4  '@py_assert2'
              692  UNARY_NOT        
              693  POP_JUMP_IF_FALSE   851  'to 851'
              696  LOAD_GLOBAL           3  '@pytest_ar'
              699  LOAD_ATTR             4  '_call_reprcompare'
              702  LOAD_CONST               'in'
              705  BUILD_TUPLE_1         1 
              708  LOAD_FAST             4  '@py_assert2'
              711  BUILD_TUPLE_1         1 
              714  LOAD_CONST               '%(py1)s in %(py3)s'
              717  BUILD_TUPLE_1         1 
              720  LOAD_FAST             2  '@py_assert0'
              723  LOAD_FAST             1  'content'
              726  BUILD_TUPLE_2         2 
              729  CALL_FUNCTION_4       4  None
              732  BUILD_MAP_2           2  None
              735  LOAD_GLOBAL           3  '@pytest_ar'
              738  LOAD_ATTR             5  '_saferepr'
              741  LOAD_FAST             2  '@py_assert0'
              744  CALL_FUNCTION_1       1  None
              747  LOAD_CONST               'py1'
              750  STORE_MAP        
              751  LOAD_CONST               'content'
              754  LOAD_GLOBAL          14  '@py_builtins'
              757  LOAD_ATTR            15  'locals'
              760  CALL_FUNCTION_0       0  None
              763  COMPARE_OP            6  in
              766  JUMP_IF_TRUE_OR_POP   781  'to 781'
              769  LOAD_GLOBAL           3  '@pytest_ar'
              772  LOAD_ATTR            16  '_should_repr_global_name'
              775  LOAD_FAST             1  'content'
              778  CALL_FUNCTION_1       1  None
            781_0  COME_FROM           766  '766'
              781  POP_JUMP_IF_FALSE   799  'to 799'
              784  LOAD_GLOBAL           3  '@pytest_ar'
              787  LOAD_ATTR             5  '_saferepr'
              790  LOAD_FAST             1  'content'
              793  CALL_FUNCTION_1       1  None
              796  JUMP_FORWARD          3  'to 802'
              799  LOAD_CONST               'content'
            802_0  COME_FROM           796  '796'
              802  LOAD_CONST               'py3'
              805  STORE_MAP        
              806  BINARY_MODULO    
              807  STORE_FAST            9  '@py_format4'
              810  LOAD_CONST               'assert %(py5)s'
              813  BUILD_MAP_1           1  None
              816  LOAD_FAST             9  '@py_format4'
              819  LOAD_CONST               'py5'
              822  STORE_MAP        
              823  BINARY_MODULO    
              824  STORE_FAST           10  '@py_format6'
              827  LOAD_GLOBAL           6  'AssertionError'
              830  LOAD_GLOBAL           3  '@pytest_ar'
              833  LOAD_ATTR             7  '_format_explanation'
              836  LOAD_FAST            10  '@py_format6'
              839  CALL_FUNCTION_1       1  None
              842  CALL_FUNCTION_1       1  None
              845  RAISE_VARARGS_1       1  None
              848  JUMP_FORWARD          0  'to 851'
            851_0  COME_FROM           848  '848'
              851  LOAD_GLOBAL           8  'None'
              854  DUP_TOP          
              855  STORE_FAST            2  '@py_assert0'
              858  STORE_FAST            4  '@py_assert2'

 L.  70       861  LOAD_GLOBAL           0  'http'
              864  LOAD_ATTR             1  'request'
              867  LOAD_CONST               'http://cdent.0.0.0.0:8080/_safe'
              870  LOAD_CONST               'method'

 L.  71       873  LOAD_CONST               'POST'
              876  LOAD_CONST               'headers'

 L.  72       879  BUILD_MAP_2           2  None
              882  LOAD_CONST               'application/json'
              885  LOAD_CONST               'Content-Type'
              888  STORE_MAP        

 L.  73       889  LOAD_CONST               'tiddlyweb_user="%s"'
              892  LOAD_GLOBAL          13  'AUTH_COOKIE'
              895  BINARY_MODULO    
              896  LOAD_CONST               'Cookie'
              899  STORE_MAP        
              900  CALL_FUNCTION_513   513  None
              903  UNPACK_SEQUENCE_2     2 
              906  STORE_FAST            0  'response'
              909  STORE_FAST            1  'content'

 L.  75       912  LOAD_FAST             0  'response'
              915  LOAD_CONST               'status'
              918  BINARY_SUBSCR    
              919  STORE_FAST            2  '@py_assert0'
              922  LOAD_CONST               '200'
              925  STORE_FAST            3  '@py_assert3'
              928  LOAD_FAST             2  '@py_assert0'
              931  LOAD_FAST             3  '@py_assert3'
              934  COMPARE_OP            2  ==
              937  STORE_FAST            4  '@py_assert2'
              940  LOAD_FAST             4  '@py_assert2'
              943  UNARY_NOT        
              944  POP_JUMP_IF_FALSE  1063  'to 1063'
              947  LOAD_GLOBAL           3  '@pytest_ar'
              950  LOAD_ATTR             4  '_call_reprcompare'
              953  LOAD_CONST               '=='
              956  BUILD_TUPLE_1         1 
              959  LOAD_FAST             4  '@py_assert2'
              962  BUILD_TUPLE_1         1 
              965  LOAD_CONST               '%(py1)s == %(py4)s'
              968  BUILD_TUPLE_1         1 
              971  LOAD_FAST             2  '@py_assert0'
              974  LOAD_FAST             3  '@py_assert3'
              977  BUILD_TUPLE_2         2 
              980  CALL_FUNCTION_4       4  None
              983  BUILD_MAP_2           2  None
              986  LOAD_GLOBAL           3  '@pytest_ar'
              989  LOAD_ATTR             5  '_saferepr'
              992  LOAD_FAST             2  '@py_assert0'
              995  CALL_FUNCTION_1       1  None
              998  LOAD_CONST               'py1'
             1001  STORE_MAP        
             1002  LOAD_GLOBAL           3  '@pytest_ar'
             1005  LOAD_ATTR             5  '_saferepr'
             1008  LOAD_FAST             3  '@py_assert3'
             1011  CALL_FUNCTION_1       1  None
             1014  LOAD_CONST               'py4'
             1017  STORE_MAP        
             1018  BINARY_MODULO    
             1019  STORE_FAST            5  '@py_format5'
             1022  LOAD_CONST               'assert %(py6)s'
             1025  BUILD_MAP_1           1  None
             1028  LOAD_FAST             5  '@py_format5'
             1031  LOAD_CONST               'py6'
             1034  STORE_MAP        
             1035  BINARY_MODULO    
             1036  STORE_FAST            6  '@py_format7'
             1039  LOAD_GLOBAL           6  'AssertionError'
             1042  LOAD_GLOBAL           3  '@pytest_ar'
             1045  LOAD_ATTR             7  '_format_explanation'
             1048  LOAD_FAST             6  '@py_format7'
             1051  CALL_FUNCTION_1       1  None
             1054  CALL_FUNCTION_1       1  None
             1057  RAISE_VARARGS_1       1  None
             1060  JUMP_FORWARD          0  'to 1063'
           1063_0  COME_FROM          1060  '1060'
             1063  LOAD_GLOBAL           8  'None'
             1066  DUP_TOP          
             1067  STORE_FAST            2  '@py_assert0'
             1070  DUP_TOP          
             1071  STORE_FAST            4  '@py_assert2'
             1074  STORE_FAST            3  '@py_assert3'

 L.  76      1077  LOAD_GLOBAL          17  'simplejson'
             1080  LOAD_ATTR            18  'loads'
             1083  LOAD_FAST             1  'content'
             1086  CALL_FUNCTION_1       1  None
             1089  STORE_FAST           11  'tiddlers'

 L.  77      1092  BUILD_LIST_0          0 
             1095  LOAD_FAST            11  'tiddlers'
             1098  GET_ITER         
             1099  FOR_ITER             26  'to 1128'
             1102  STORE_FAST           12  'tiddler'
             1105  LOAD_FAST            12  'tiddler'
             1108  LOAD_CONST               'title'
             1111  BINARY_SUBSCR    
             1112  LOAD_FAST            12  'tiddler'
             1115  LOAD_CONST               'bag'
             1118  BINARY_SUBSCR    
             1119  BUILD_TUPLE_2         2 
             1122  LIST_APPEND           2  None
             1125  JUMP_BACK          1099  'to 1099'
             1128  STORE_FAST           13  'tiddlers_info'

 L.  78      1131  LOAD_GLOBAL          19  'set'
             1134  LOAD_GENEXPR             '<code_object <genexpr>>'
             1137  MAKE_FUNCTION_0       0  None
             1140  LOAD_FAST            13  'tiddlers_info'
             1143  GET_ITER         
             1144  CALL_FUNCTION_1       1  None
             1147  CALL_FUNCTION_1       1  None
             1150  STORE_FAST           14  'bags'

 L.  79      1153  LOAD_GLOBAL          20  'list'
             1156  LOAD_FAST            14  'bags'
             1159  CALL_FUNCTION_1       1  None
             1162  STORE_FAST            3  '@py_assert3'
             1165  LOAD_GLOBAL          21  'sorted'
             1168  LOAD_FAST             3  '@py_assert3'
             1171  CALL_FUNCTION_1       1  None
             1174  STORE_FAST           15  '@py_assert5'
             1177  LOAD_CONST               'cdent_public'
             1180  LOAD_CONST               'system'
             1183  LOAD_CONST               'system-images_public'
             1186  LOAD_CONST               'system-info_public'
             1189  LOAD_CONST               'system-plugins_public'
             1192  LOAD_CONST               'system-theme_public'
             1195  LOAD_CONST               'tiddlyspace'
             1198  BUILD_LIST_7          7 
             1201  STORE_FAST           16  '@py_assert8'
             1204  LOAD_FAST            15  '@py_assert5'
             1207  LOAD_FAST            16  '@py_assert8'
             1210  COMPARE_OP            2  ==
             1213  STORE_FAST           17  '@py_assert7'
             1216  LOAD_FAST            17  '@py_assert7'
             1219  UNARY_NOT        
             1220  POP_JUMP_IF_FALSE  1520  'to 1520'
             1223  LOAD_GLOBAL           3  '@pytest_ar'
             1226  LOAD_ATTR             4  '_call_reprcompare'
             1229  LOAD_CONST               '=='
             1232  BUILD_TUPLE_1         1 
             1235  LOAD_FAST            17  '@py_assert7'
             1238  BUILD_TUPLE_1         1 
             1241  LOAD_CONST               '%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s'
             1244  BUILD_TUPLE_1         1 
             1247  LOAD_FAST            15  '@py_assert5'
             1250  LOAD_FAST            16  '@py_assert8'
             1253  BUILD_TUPLE_2         2 
             1256  CALL_FUNCTION_4       4  None
             1259  BUILD_MAP_6           6  None
             1262  LOAD_GLOBAL           3  '@pytest_ar'
             1265  LOAD_ATTR             5  '_saferepr'
             1268  LOAD_FAST            16  '@py_assert8'
             1271  CALL_FUNCTION_1       1  None
             1274  LOAD_CONST               'py9'
             1277  STORE_MAP        
             1278  LOAD_CONST               'sorted'
             1281  LOAD_GLOBAL          14  '@py_builtins'
             1284  LOAD_ATTR            15  'locals'
             1287  CALL_FUNCTION_0       0  None
             1290  COMPARE_OP            6  in
             1293  JUMP_IF_TRUE_OR_POP  1308  'to 1308'
             1296  LOAD_GLOBAL           3  '@pytest_ar'
             1299  LOAD_ATTR            16  '_should_repr_global_name'
             1302  LOAD_GLOBAL          21  'sorted'
             1305  CALL_FUNCTION_1       1  None
           1308_0  COME_FROM          1293  '1293'
             1308  POP_JUMP_IF_FALSE  1326  'to 1326'
             1311  LOAD_GLOBAL           3  '@pytest_ar'
             1314  LOAD_ATTR             5  '_saferepr'
             1317  LOAD_GLOBAL          21  'sorted'
             1320  CALL_FUNCTION_1       1  None
             1323  JUMP_FORWARD          3  'to 1329'
             1326  LOAD_CONST               'sorted'
           1329_0  COME_FROM          1323  '1323'
             1329  LOAD_CONST               'py0'
             1332  STORE_MAP        
             1333  LOAD_CONST               'list'
             1336  LOAD_GLOBAL          14  '@py_builtins'
             1339  LOAD_ATTR            15  'locals'
             1342  CALL_FUNCTION_0       0  None
             1345  COMPARE_OP            6  in
             1348  JUMP_IF_TRUE_OR_POP  1363  'to 1363'
             1351  LOAD_GLOBAL           3  '@pytest_ar'
             1354  LOAD_ATTR            16  '_should_repr_global_name'
             1357  LOAD_GLOBAL          20  'list'
             1360  CALL_FUNCTION_1       1  None
           1363_0  COME_FROM          1348  '1348'
             1363  POP_JUMP_IF_FALSE  1381  'to 1381'
             1366  LOAD_GLOBAL           3  '@pytest_ar'
             1369  LOAD_ATTR             5  '_saferepr'
             1372  LOAD_GLOBAL          20  'list'
             1375  CALL_FUNCTION_1       1  None
             1378  JUMP_FORWARD          3  'to 1384'
             1381  LOAD_CONST               'list'
           1384_0  COME_FROM          1378  '1378'
             1384  LOAD_CONST               'py1'
             1387  STORE_MAP        
             1388  LOAD_CONST               'bags'
             1391  LOAD_GLOBAL          14  '@py_builtins'
             1394  LOAD_ATTR            15  'locals'
             1397  CALL_FUNCTION_0       0  None
             1400  COMPARE_OP            6  in
             1403  JUMP_IF_TRUE_OR_POP  1418  'to 1418'
             1406  LOAD_GLOBAL           3  '@pytest_ar'
             1409  LOAD_ATTR            16  '_should_repr_global_name'
             1412  LOAD_FAST            14  'bags'
             1415  CALL_FUNCTION_1       1  None
           1418_0  COME_FROM          1403  '1403'
             1418  POP_JUMP_IF_FALSE  1436  'to 1436'
             1421  LOAD_GLOBAL           3  '@pytest_ar'
             1424  LOAD_ATTR             5  '_saferepr'
             1427  LOAD_FAST            14  'bags'
             1430  CALL_FUNCTION_1       1  None
             1433  JUMP_FORWARD          3  'to 1439'
             1436  LOAD_CONST               'bags'
           1439_0  COME_FROM          1433  '1433'
             1439  LOAD_CONST               'py2'
             1442  STORE_MAP        
             1443  LOAD_GLOBAL           3  '@pytest_ar'
             1446  LOAD_ATTR             5  '_saferepr'
             1449  LOAD_FAST             3  '@py_assert3'
             1452  CALL_FUNCTION_1       1  None
             1455  LOAD_CONST               'py4'
             1458  STORE_MAP        
             1459  LOAD_GLOBAL           3  '@pytest_ar'
             1462  LOAD_ATTR             5  '_saferepr'
             1465  LOAD_FAST            15  '@py_assert5'
             1468  CALL_FUNCTION_1       1  None
             1471  LOAD_CONST               'py6'
             1474  STORE_MAP        
             1475  BINARY_MODULO    
             1476  STORE_FAST           18  '@py_format10'
             1479  LOAD_CONST               'assert %(py11)s'
             1482  BUILD_MAP_1           1  None
             1485  LOAD_FAST            18  '@py_format10'
             1488  LOAD_CONST               'py11'
             1491  STORE_MAP        
             1492  BINARY_MODULO    
             1493  STORE_FAST           19  '@py_format12'
             1496  LOAD_GLOBAL           6  'AssertionError'
             1499  LOAD_GLOBAL           3  '@pytest_ar'
             1502  LOAD_ATTR             7  '_format_explanation'
             1505  LOAD_FAST            19  '@py_format12'
             1508  CALL_FUNCTION_1       1  None
             1511  CALL_FUNCTION_1       1  None
             1514  RAISE_VARARGS_1       1  None
             1517  JUMP_FORWARD          0  'to 1520'
           1520_0  COME_FROM          1517  '1517'
             1520  LOAD_GLOBAL           8  'None'
             1523  DUP_TOP          
             1524  STORE_FAST            3  '@py_assert3'
             1527  DUP_TOP          
             1528  STORE_FAST           15  '@py_assert5'
             1531  DUP_TOP          
             1532  STORE_FAST           17  '@py_assert7'
             1535  STORE_FAST           16  '@py_assert8'

 L.  83      1538  LOAD_CONST               'TiddlyWebAdaptor'
             1541  LOAD_CONST               'system'
             1544  BUILD_TUPLE_2         2 
             1547  STORE_FAST            2  '@py_assert0'
             1550  LOAD_FAST             2  '@py_assert0'
             1553  LOAD_FAST            13  'tiddlers_info'
             1556  COMPARE_OP            6  in
             1559  STORE_FAST            4  '@py_assert2'
             1562  LOAD_FAST             4  '@py_assert2'
             1565  UNARY_NOT        
             1566  POP_JUMP_IF_FALSE  1724  'to 1724'
             1569  LOAD_GLOBAL           3  '@pytest_ar'
             1572  LOAD_ATTR             4  '_call_reprcompare'
             1575  LOAD_CONST               'in'
             1578  BUILD_TUPLE_1         1 
             1581  LOAD_FAST             4  '@py_assert2'
             1584  BUILD_TUPLE_1         1 
             1587  LOAD_CONST               '%(py1)s in %(py3)s'
             1590  BUILD_TUPLE_1         1 
             1593  LOAD_FAST             2  '@py_assert0'
             1596  LOAD_FAST            13  'tiddlers_info'
             1599  BUILD_TUPLE_2         2 
             1602  CALL_FUNCTION_4       4  None
             1605  BUILD_MAP_2           2  None
             1608  LOAD_GLOBAL           3  '@pytest_ar'
             1611  LOAD_ATTR             5  '_saferepr'
             1614  LOAD_FAST             2  '@py_assert0'
             1617  CALL_FUNCTION_1       1  None
             1620  LOAD_CONST               'py1'
             1623  STORE_MAP        
             1624  LOAD_CONST               'tiddlers_info'
             1627  LOAD_GLOBAL          14  '@py_builtins'
             1630  LOAD_ATTR            15  'locals'
             1633  CALL_FUNCTION_0       0  None
             1636  COMPARE_OP            6  in
             1639  JUMP_IF_TRUE_OR_POP  1654  'to 1654'
             1642  LOAD_GLOBAL           3  '@pytest_ar'
             1645  LOAD_ATTR            16  '_should_repr_global_name'
             1648  LOAD_FAST            13  'tiddlers_info'
             1651  CALL_FUNCTION_1       1  None
           1654_0  COME_FROM          1639  '1639'
             1654  POP_JUMP_IF_FALSE  1672  'to 1672'
             1657  LOAD_GLOBAL           3  '@pytest_ar'
             1660  LOAD_ATTR             5  '_saferepr'
             1663  LOAD_FAST            13  'tiddlers_info'
             1666  CALL_FUNCTION_1       1  None
             1669  JUMP_FORWARD          3  'to 1675'
             1672  LOAD_CONST               'tiddlers_info'
           1675_0  COME_FROM          1669  '1669'
             1675  LOAD_CONST               'py3'
             1678  STORE_MAP        
             1679  BINARY_MODULO    
             1680  STORE_FAST            9  '@py_format4'
             1683  LOAD_CONST               'assert %(py5)s'
             1686  BUILD_MAP_1           1  None
             1689  LOAD_FAST             9  '@py_format4'
             1692  LOAD_CONST               'py5'
             1695  STORE_MAP        
             1696  BINARY_MODULO    
             1697  STORE_FAST           10  '@py_format6'
             1700  LOAD_GLOBAL           6  'AssertionError'
             1703  LOAD_GLOBAL           3  '@pytest_ar'
             1706  LOAD_ATTR             7  '_format_explanation'
             1709  LOAD_FAST            10  '@py_format6'
             1712  CALL_FUNCTION_1       1  None
             1715  CALL_FUNCTION_1       1  None
             1718  RAISE_VARARGS_1       1  None
             1721  JUMP_FORWARD          0  'to 1724'
           1724_0  COME_FROM          1721  '1721'
             1724  LOAD_GLOBAL           8  'None'
             1727  DUP_TOP          
             1728  STORE_FAST            2  '@py_assert0'
             1731  STORE_FAST            4  '@py_assert2'

 L.  85      1734  LOAD_GLOBAL          22  'Tiddler'
             1737  LOAD_CONST               'cdentSetupFlag'
             1740  LOAD_CONST               'cdent_private'
             1743  CALL_FUNCTION_2       2  None
             1746  STORE_FAST           12  'tiddler'

 L.  86      1749  LOAD_GLOBAL          23  'store'
             1752  LOAD_ATTR            24  'put'
             1755  LOAD_FAST            12  'tiddler'
             1758  CALL_FUNCTION_1       1  None
             1761  POP_TOP          

 L.  87      1762  LOAD_GLOBAL           0  'http'
             1765  LOAD_ATTR             1  'request'
             1768  LOAD_CONST               'http://cdent.0.0.0.0:8080/'
             1771  LOAD_CONST               'method'

 L.  88      1774  LOAD_CONST               'GET'
             1777  LOAD_CONST               'headers'

 L.  89      1780  BUILD_MAP_2           2  None
             1783  LOAD_CONST               'application/json'
             1786  LOAD_CONST               'Accept'
             1789  STORE_MAP        

 L.  90      1790  LOAD_CONST               'tiddlyweb_user="%s"'
             1793  LOAD_GLOBAL          13  'AUTH_COOKIE'
             1796  BINARY_MODULO    
             1797  LOAD_CONST               'Cookie'
             1800  STORE_MAP        
             1801  CALL_FUNCTION_513   513  None
             1804  UNPACK_SEQUENCE_2     2 
             1807  STORE_FAST            0  'response'
             1810  STORE_FAST            1  'content'

 L.  92      1813  LOAD_FAST             0  'response'
             1816  LOAD_CONST               'status'
             1819  BINARY_SUBSCR    
             1820  LOAD_CONST               '200'
             1823  COMPARE_OP            2  ==
             1826  POP_JUMP_IF_TRUE   1838  'to 1838'
             1829  LOAD_ASSERT              AssertionError
             1832  LOAD_FAST             1  'content'
             1835  RAISE_VARARGS_2       2  None

 L.  93      1838  LOAD_GLOBAL          17  'simplejson'
             1841  LOAD_ATTR            18  'loads'
             1844  LOAD_FAST             1  'content'
             1847  CALL_FUNCTION_1       1  None
             1850  STORE_FAST           11  'tiddlers'

 L.  94      1853  BUILD_LIST_0          0 
             1856  LOAD_FAST            11  'tiddlers'
             1859  GET_ITER         
             1860  FOR_ITER             26  'to 1889'
             1863  STORE_FAST           12  'tiddler'
             1866  LOAD_FAST            12  'tiddler'
             1869  LOAD_CONST               'title'
             1872  BINARY_SUBSCR    
             1873  LOAD_FAST            12  'tiddler'
             1876  LOAD_CONST               'bag'
             1879  BINARY_SUBSCR    
             1880  BUILD_TUPLE_2         2 
             1883  LIST_APPEND           2  None
             1886  JUMP_BACK          1860  'to 1860'
             1889  STORE_FAST           13  'tiddlers_info'

 L.  95      1892  LOAD_GLOBAL          19  'set'
             1895  LOAD_GENEXPR             '<code_object <genexpr>>'
             1898  MAKE_FUNCTION_0       0  None
             1901  LOAD_FAST            13  'tiddlers_info'
             1904  GET_ITER         
             1905  CALL_FUNCTION_1       1  None
             1908  CALL_FUNCTION_1       1  None
             1911  STORE_FAST           14  'bags'

 L.  96      1914  LOAD_GLOBAL          20  'list'
             1917  LOAD_FAST            14  'bags'
             1920  CALL_FUNCTION_1       1  None
             1923  STORE_FAST            3  '@py_assert3'
             1926  LOAD_GLOBAL          21  'sorted'
             1929  LOAD_FAST             3  '@py_assert3'
             1932  CALL_FUNCTION_1       1  None
             1935  STORE_FAST           15  '@py_assert5'
             1938  LOAD_CONST               'cdent_private'
             1941  LOAD_CONST               'cdent_public'
             1944  LOAD_CONST               'system'
             1947  LOAD_CONST               'system-images_public'
             1950  LOAD_CONST               'system-info_public'
             1953  LOAD_CONST               'system-plugins_public'
             1956  LOAD_CONST               'system-theme_public'
             1959  LOAD_CONST               'tiddlyspace'
             1962  BUILD_LIST_8          8 
             1965  STORE_FAST           16  '@py_assert8'
             1968  LOAD_FAST            15  '@py_assert5'
             1971  LOAD_FAST            16  '@py_assert8'
             1974  COMPARE_OP            2  ==
             1977  STORE_FAST           17  '@py_assert7'
             1980  LOAD_FAST            17  '@py_assert7'
             1983  UNARY_NOT        
             1984  POP_JUMP_IF_FALSE  2284  'to 2284'
             1987  LOAD_GLOBAL           3  '@pytest_ar'
             1990  LOAD_ATTR             4  '_call_reprcompare'
             1993  LOAD_CONST               '=='
             1996  BUILD_TUPLE_1         1 
             1999  LOAD_FAST            17  '@py_assert7'
             2002  BUILD_TUPLE_1         1 
             2005  LOAD_CONST               '%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s'
             2008  BUILD_TUPLE_1         1 
             2011  LOAD_FAST            15  '@py_assert5'
             2014  LOAD_FAST            16  '@py_assert8'
             2017  BUILD_TUPLE_2         2 
             2020  CALL_FUNCTION_4       4  None
             2023  BUILD_MAP_6           6  None
             2026  LOAD_GLOBAL           3  '@pytest_ar'
             2029  LOAD_ATTR             5  '_saferepr'
             2032  LOAD_FAST            16  '@py_assert8'
             2035  CALL_FUNCTION_1       1  None
             2038  LOAD_CONST               'py9'
             2041  STORE_MAP        
             2042  LOAD_CONST               'sorted'
             2045  LOAD_GLOBAL          14  '@py_builtins'
             2048  LOAD_ATTR            15  'locals'
             2051  CALL_FUNCTION_0       0  None
             2054  COMPARE_OP            6  in
             2057  JUMP_IF_TRUE_OR_POP  2072  'to 2072'
             2060  LOAD_GLOBAL           3  '@pytest_ar'
             2063  LOAD_ATTR            16  '_should_repr_global_name'
             2066  LOAD_GLOBAL          21  'sorted'
             2069  CALL_FUNCTION_1       1  None
           2072_0  COME_FROM          2057  '2057'
             2072  POP_JUMP_IF_FALSE  2090  'to 2090'
             2075  LOAD_GLOBAL           3  '@pytest_ar'
             2078  LOAD_ATTR             5  '_saferepr'
             2081  LOAD_GLOBAL          21  'sorted'
             2084  CALL_FUNCTION_1       1  None
             2087  JUMP_FORWARD          3  'to 2093'
             2090  LOAD_CONST               'sorted'
           2093_0  COME_FROM          2087  '2087'
             2093  LOAD_CONST               'py0'
             2096  STORE_MAP        
             2097  LOAD_CONST               'list'
             2100  LOAD_GLOBAL          14  '@py_builtins'
             2103  LOAD_ATTR            15  'locals'
             2106  CALL_FUNCTION_0       0  None
             2109  COMPARE_OP            6  in
             2112  JUMP_IF_TRUE_OR_POP  2127  'to 2127'
             2115  LOAD_GLOBAL           3  '@pytest_ar'
             2118  LOAD_ATTR            16  '_should_repr_global_name'
             2121  LOAD_GLOBAL          20  'list'
             2124  CALL_FUNCTION_1       1  None
           2127_0  COME_FROM          2112  '2112'
             2127  POP_JUMP_IF_FALSE  2145  'to 2145'
             2130  LOAD_GLOBAL           3  '@pytest_ar'
             2133  LOAD_ATTR             5  '_saferepr'
             2136  LOAD_GLOBAL          20  'list'
             2139  CALL_FUNCTION_1       1  None
             2142  JUMP_FORWARD          3  'to 2148'
             2145  LOAD_CONST               'list'
           2148_0  COME_FROM          2142  '2142'
             2148  LOAD_CONST               'py1'
             2151  STORE_MAP        
             2152  LOAD_CONST               'bags'
             2155  LOAD_GLOBAL          14  '@py_builtins'
             2158  LOAD_ATTR            15  'locals'
             2161  CALL_FUNCTION_0       0  None
             2164  COMPARE_OP            6  in
             2167  JUMP_IF_TRUE_OR_POP  2182  'to 2182'
             2170  LOAD_GLOBAL           3  '@pytest_ar'
             2173  LOAD_ATTR            16  '_should_repr_global_name'
             2176  LOAD_FAST            14  'bags'
             2179  CALL_FUNCTION_1       1  None
           2182_0  COME_FROM          2167  '2167'
             2182  POP_JUMP_IF_FALSE  2200  'to 2200'
             2185  LOAD_GLOBAL           3  '@pytest_ar'
             2188  LOAD_ATTR             5  '_saferepr'
             2191  LOAD_FAST            14  'bags'
             2194  CALL_FUNCTION_1       1  None
             2197  JUMP_FORWARD          3  'to 2203'
             2200  LOAD_CONST               'bags'
           2203_0  COME_FROM          2197  '2197'
             2203  LOAD_CONST               'py2'
             2206  STORE_MAP        
             2207  LOAD_GLOBAL           3  '@pytest_ar'
             2210  LOAD_ATTR             5  '_saferepr'
             2213  LOAD_FAST             3  '@py_assert3'
             2216  CALL_FUNCTION_1       1  None
             2219  LOAD_CONST               'py4'
             2222  STORE_MAP        
             2223  LOAD_GLOBAL           3  '@pytest_ar'
             2226  LOAD_ATTR             5  '_saferepr'
             2229  LOAD_FAST            15  '@py_assert5'
             2232  CALL_FUNCTION_1       1  None
             2235  LOAD_CONST               'py6'
             2238  STORE_MAP        
             2239  BINARY_MODULO    
             2240  STORE_FAST           18  '@py_format10'
             2243  LOAD_CONST               'assert %(py11)s'
             2246  BUILD_MAP_1           1  None
             2249  LOAD_FAST            18  '@py_format10'
             2252  LOAD_CONST               'py11'
             2255  STORE_MAP        
             2256  BINARY_MODULO    
             2257  STORE_FAST           19  '@py_format12'
             2260  LOAD_GLOBAL           6  'AssertionError'
             2263  LOAD_GLOBAL           3  '@pytest_ar'
             2266  LOAD_ATTR             7  '_format_explanation'
             2269  LOAD_FAST            19  '@py_format12'
             2272  CALL_FUNCTION_1       1  None
             2275  CALL_FUNCTION_1       1  None
             2278  RAISE_VARARGS_1       1  None
             2281  JUMP_FORWARD          0  'to 2284'
           2284_0  COME_FROM          2281  '2281'
             2284  LOAD_GLOBAL           8  'None'
             2287  DUP_TOP          
             2288  STORE_FAST            3  '@py_assert3'
             2291  DUP_TOP          
             2292  STORE_FAST           15  '@py_assert5'
             2295  DUP_TOP          
             2296  STORE_FAST           17  '@py_assert7'
             2299  STORE_FAST           16  '@py_assert8'

 L. 100      2302  LOAD_CONST               'TiddlyWebAdaptor'
             2305  LOAD_CONST               'system'
             2308  BUILD_TUPLE_2         2 
             2311  STORE_FAST            2  '@py_assert0'
             2314  LOAD_FAST             2  '@py_assert0'
             2317  LOAD_FAST            13  'tiddlers_info'
             2320  COMPARE_OP            6  in
             2323  STORE_FAST            4  '@py_assert2'
             2326  LOAD_FAST             4  '@py_assert2'
             2329  UNARY_NOT        
             2330  POP_JUMP_IF_FALSE  2488  'to 2488'
             2333  LOAD_GLOBAL           3  '@pytest_ar'
             2336  LOAD_ATTR             4  '_call_reprcompare'
             2339  LOAD_CONST               'in'
             2342  BUILD_TUPLE_1         1 
             2345  LOAD_FAST             4  '@py_assert2'
             2348  BUILD_TUPLE_1         1 
             2351  LOAD_CONST               '%(py1)s in %(py3)s'
             2354  BUILD_TUPLE_1         1 
             2357  LOAD_FAST             2  '@py_assert0'
             2360  LOAD_FAST            13  'tiddlers_info'
             2363  BUILD_TUPLE_2         2 
             2366  CALL_FUNCTION_4       4  None
             2369  BUILD_MAP_2           2  None
             2372  LOAD_GLOBAL           3  '@pytest_ar'
             2375  LOAD_ATTR             5  '_saferepr'
             2378  LOAD_FAST             2  '@py_assert0'
             2381  CALL_FUNCTION_1       1  None
             2384  LOAD_CONST               'py1'
             2387  STORE_MAP        
             2388  LOAD_CONST               'tiddlers_info'
             2391  LOAD_GLOBAL          14  '@py_builtins'
             2394  LOAD_ATTR            15  'locals'
             2397  CALL_FUNCTION_0       0  None
             2400  COMPARE_OP            6  in
             2403  JUMP_IF_TRUE_OR_POP  2418  'to 2418'
             2406  LOAD_GLOBAL           3  '@pytest_ar'
             2409  LOAD_ATTR            16  '_should_repr_global_name'
             2412  LOAD_FAST            13  'tiddlers_info'
             2415  CALL_FUNCTION_1       1  None
           2418_0  COME_FROM          2403  '2403'
             2418  POP_JUMP_IF_FALSE  2436  'to 2436'
             2421  LOAD_GLOBAL           3  '@pytest_ar'
             2424  LOAD_ATTR             5  '_saferepr'
             2427  LOAD_FAST            13  'tiddlers_info'
             2430  CALL_FUNCTION_1       1  None
             2433  JUMP_FORWARD          3  'to 2439'
             2436  LOAD_CONST               'tiddlers_info'
           2439_0  COME_FROM          2433  '2433'
             2439  LOAD_CONST               'py3'
             2442  STORE_MAP        
             2443  BINARY_MODULO    
             2444  STORE_FAST            9  '@py_format4'
             2447  LOAD_CONST               'assert %(py5)s'
             2450  BUILD_MAP_1           1  None
             2453  LOAD_FAST             9  '@py_format4'
             2456  LOAD_CONST               'py5'
             2459  STORE_MAP        
             2460  BINARY_MODULO    
             2461  STORE_FAST           10  '@py_format6'
             2464  LOAD_GLOBAL           6  'AssertionError'
             2467  LOAD_GLOBAL           3  '@pytest_ar'
             2470  LOAD_ATTR             7  '_format_explanation'
             2473  LOAD_FAST            10  '@py_format6'
             2476  CALL_FUNCTION_1       1  None
             2479  CALL_FUNCTION_1       1  None
             2482  RAISE_VARARGS_1       1  None
             2485  JUMP_FORWARD          0  'to 2488'
           2488_0  COME_FROM          2485  '2485'
             2488  LOAD_GLOBAL           8  'None'
             2491  DUP_TOP          
             2492  STORE_FAST            2  '@py_assert0'
             2495  STORE_FAST            4  '@py_assert2'
             2498  LOAD_CONST               None
             2501  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 2498


def test_safe_mode_deletes_bad():
    global AUTH_COOKIE
    tiddler = {'text': 'oh hai', 'tags': ['fun', 'systemConfig']}
    body = simplejson.dumps(tiddler)
    response, content = http.request('http://cdent.0.0.0.0:8080/recipes/cdent_private/tiddlers/TiddlyWebAdaptor', method='PUT', body=body, headers={'Content-Type': 'application/json', 'Cookie': 'tiddlyweb_user="%s"' % AUTH_COOKIE})
    @py_assert0 = response['status']
    @py_assert3 = '204'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://cdent.0.0.0.0:8080/recipes/cdent_private/tiddlers/helloplugin', method='PUT', body=body, headers={'Content-Type': 'application/json', 'Cookie': 'tiddlyweb_user="%s"' % AUTH_COOKIE})
    @py_assert0 = response['status']
    @py_assert3 = '204'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://cdent.0.0.0.0:8080/', method='GET', headers={'Accept': 'application/json', 'Cookie': 'tiddlyweb_user="%s"' % AUTH_COOKIE})
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    tiddlers = simplejson.loads(content)
    tiddlers_info = [ (tiddler['title'], tiddler['bag']) for tiddler in tiddlers ]
    bags = set(bag for title, bag in tiddlers_info)
    @py_assert3 = list(bags)
    @py_assert5 = sorted(@py_assert3)
    @py_assert8 = ['cdent_private', 'cdent_public', 'system', 'system-images_public', 'system-info_public', 'system-plugins_public', 'system-theme_public', 'tiddlyspace']
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py2': @pytest_ar._saferepr(bags) if 'bags' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bags) else 'bags', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert0 = (
     'TiddlyWebAdaptor', 'cdent_private')
    @py_assert2 = @py_assert0 in tiddlers_info
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in',), (@py_assert2,), ('%(py1)s in %(py3)s',), (@py_assert0, tiddlers_info)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddlers_info) if 'tiddlers_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers_info) else 'tiddlers_info'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = (
     'helloplugin', 'cdent_private')
    @py_assert2 = @py_assert0 in tiddlers_info
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in',), (@py_assert2,), ('%(py1)s in %(py3)s',), (@py_assert0, tiddlers_info)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddlers_info) if 'tiddlers_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers_info) else 'tiddlers_info'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = http.request('http://cdent.0.0.0.0:8080/_safe', method='POST', headers={'Content-Type': 'application/json', 'Cookie': 'tiddlyweb_user="%s"' % AUTH_COOKIE})
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    tiddlers = simplejson.loads(content)
    tiddlers_info = [ (tiddler['title'], tiddler['bag']) for tiddler in tiddlers ]
    bags = set(bag for title, bag in tiddlers_info)
    @py_assert3 = list(bags)
    @py_assert5 = sorted(@py_assert3)
    @py_assert8 = ['cdent_private', 'cdent_public', 'system', 'system-images_public', 'system-info_public', 'system-plugins_public', 'system-theme_public', 'tiddlyspace']
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py2': @pytest_ar._saferepr(bags) if 'bags' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bags) else 'bags', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert0 = (
     'TiddlyWebAdaptor', 'system')
    @py_assert2 = @py_assert0 in tiddlers_info
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in',), (@py_assert2,), ('%(py1)s in %(py3)s',), (@py_assert0, tiddlers_info)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddlers_info) if 'tiddlers_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers_info) else 'tiddlers_info'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = (
     'helloplugin', 'cdent_private')
    @py_assert2 = @py_assert0 in tiddlers_info
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in',), (@py_assert2,), ('%(py1)s in %(py3)s',), (@py_assert0, tiddlers_info)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddlers_info) if 'tiddlers_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers_info) else 'tiddlers_info'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    our_tiddler = [ tiddler for tiddler in tiddlers if tiddler['title'] == 'helloplugin' ][0]
    @py_assert1 = our_tiddler['tags']
    @py_assert3 = sorted(@py_assert1)
    @py_assert6 = ['fun', 'systemConfig', 'systemConfigDisable']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    return