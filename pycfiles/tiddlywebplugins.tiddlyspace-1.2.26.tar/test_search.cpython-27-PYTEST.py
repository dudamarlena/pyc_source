# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyspace/test/test_search.py
# Compiled at: 2013-08-20 13:22:51
"""
Test the search interface.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from test.fixtures import make_test_env, make_fake_space
from wsgi_intercept import httplib2_intercept
import wsgi_intercept, httplib2, simplejson
from tiddlyweb.model.user import User
from tiddlyweb.model.tiddler import Tiddler

def setup_module(module):
    make_test_env(module, hsearch=True)
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)
    wsgi_intercept.add_wsgi_intercept('cdent.0.0.0.0', 8080, app_fn)
    wsgi_intercept.add_wsgi_intercept('fnd.0.0.0.0', 8080, app_fn)
    make_fake_space(module.store, 'cdent')
    make_fake_space(module.store, 'fnd')
    user = User('cdent')
    user.set_password('cow')
    module.store.put(user)
    module.http = httplib2.Http()


def test_basic_search():
    response, content = http.request('http://0.0.0.0:8080/search.json?q=title:TiddlyWebAdaptor')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    info = simplejson.loads(content)
    @py_assert0 = info[0]['title']
    @py_assert3 = 'TiddlyWebAdaptor'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_wildcard_search():
    response, content = http.request('http://0.0.0.0:8080/search.json?q=ftitle:TiddlyWebA*')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    info = simplejson.loads(content)
    @py_assert0 = info[0]['title']
    @py_assert3 = 'TiddlyWebAdaptor'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_multiword_phrase_search--- This code section failed: ---

 L.  44         0  LOAD_GLOBAL           0  'Tiddler'
                3  LOAD_CONST               'one'
                6  LOAD_CONST               'cdent_public'
                9  CALL_FUNCTION_2       2  None
               12  STORE_FAST            0  'tiddler'

 L.  45        15  LOAD_CONST               'monkeys are fun!'
               18  LOAD_FAST             0  'tiddler'
               21  STORE_ATTR            1  'text'

 L.  46        24  LOAD_GLOBAL           2  'store'
               27  LOAD_ATTR             3  'put'
               30  LOAD_FAST             0  'tiddler'
               33  CALL_FUNCTION_1       1  None
               36  POP_TOP          

 L.  47        37  LOAD_GLOBAL           0  'Tiddler'
               40  LOAD_CONST               'one two'
               43  LOAD_CONST               'cdent_public'
               46  CALL_FUNCTION_2       2  None
               49  STORE_FAST            0  'tiddler'

 L.  48        52  LOAD_CONST               'monkeys are fun!'
               55  LOAD_FAST             0  'tiddler'
               58  STORE_ATTR            1  'text'

 L.  49        61  LOAD_GLOBAL           2  'store'
               64  LOAD_ATTR             3  'put'
               67  LOAD_FAST             0  'tiddler'
               70  CALL_FUNCTION_1       1  None
               73  POP_TOP          

 L.  50        74  LOAD_GLOBAL           0  'Tiddler'
               77  LOAD_CONST               'one two three'
               80  LOAD_CONST               'cdent_public'
               83  CALL_FUNCTION_2       2  None
               86  STORE_FAST            0  'tiddler'

 L.  51        89  LOAD_CONST               'monkeys are fun!'
               92  LOAD_FAST             0  'tiddler'
               95  STORE_ATTR            1  'text'

 L.  52        98  LOAD_GLOBAL           2  'store'
              101  LOAD_ATTR             3  'put'
              104  LOAD_FAST             0  'tiddler'
              107  CALL_FUNCTION_1       1  None
              110  POP_TOP          

 L.  53       111  LOAD_GLOBAL           0  'Tiddler'
              114  LOAD_CONST               'three two one'
              117  LOAD_CONST               'cdent_public'
              120  CALL_FUNCTION_2       2  None
              123  STORE_FAST            0  'tiddler'

 L.  54       126  LOAD_CONST               'monkeys are fun!'
              129  LOAD_FAST             0  'tiddler'
              132  STORE_ATTR            1  'text'

 L.  55       135  LOAD_GLOBAL           2  'store'
              138  LOAD_ATTR             3  'put'
              141  LOAD_FAST             0  'tiddler'
              144  CALL_FUNCTION_1       1  None
              147  POP_TOP          

 L.  57       148  LOAD_GLOBAL           4  'http'
              151  LOAD_ATTR             5  'request'

 L.  58       154  LOAD_CONST               'http://0.0.0.0:8080/search.json?q=ftitle:one'
              157  CALL_FUNCTION_1       1  None
              160  UNPACK_SEQUENCE_2     2 
              163  STORE_FAST            1  'response'
              166  STORE_FAST            2  'content'

 L.  59       169  LOAD_FAST             1  'response'
              172  LOAD_CONST               'status'
              175  BINARY_SUBSCR    
              176  STORE_FAST            3  '@py_assert0'
              179  LOAD_CONST               '200'
              182  STORE_FAST            4  '@py_assert3'
              185  LOAD_FAST             3  '@py_assert0'
              188  LOAD_FAST             4  '@py_assert3'
              191  COMPARE_OP            2  ==
              194  STORE_FAST            5  '@py_assert2'
              197  LOAD_FAST             5  '@py_assert2'
              200  POP_JUMP_IF_TRUE    313  'to 313'
              203  LOAD_GLOBAL           6  '@pytest_ar'
              206  LOAD_ATTR             7  '_call_reprcompare'
              209  LOAD_CONST               ('==',)
              212  LOAD_FAST             5  '@py_assert2'
              215  BUILD_TUPLE_1         1 
              218  LOAD_CONST               ('%(py1)s == %(py4)s',)
              221  LOAD_FAST             3  '@py_assert0'
              224  LOAD_FAST             4  '@py_assert3'
              227  BUILD_TUPLE_2         2 
              230  CALL_FUNCTION_4       4  None
              233  BUILD_MAP_2           2  None
              236  LOAD_GLOBAL           6  '@pytest_ar'
              239  LOAD_ATTR             8  '_saferepr'
              242  LOAD_FAST             3  '@py_assert0'
              245  CALL_FUNCTION_1       1  None
              248  LOAD_CONST               'py1'
              251  STORE_MAP        
              252  LOAD_GLOBAL           6  '@pytest_ar'
              255  LOAD_ATTR             8  '_saferepr'
              258  LOAD_FAST             4  '@py_assert3'
              261  CALL_FUNCTION_1       1  None
              264  LOAD_CONST               'py4'
              267  STORE_MAP        
              268  BINARY_MODULO    
              269  STORE_FAST            6  '@py_format5'
              272  LOAD_CONST               'assert %(py6)s'
              275  BUILD_MAP_1           1  None
              278  LOAD_FAST             6  '@py_format5'
              281  LOAD_CONST               'py6'
              284  STORE_MAP        
              285  BINARY_MODULO    
              286  STORE_FAST            7  '@py_format7'
              289  LOAD_GLOBAL           9  'AssertionError'
              292  LOAD_GLOBAL           6  '@pytest_ar'
              295  LOAD_ATTR            10  '_format_explanation'
              298  LOAD_FAST             7  '@py_format7'
              301  CALL_FUNCTION_1       1  None
              304  CALL_FUNCTION_1       1  None
              307  RAISE_VARARGS_1       1  None
              310  JUMP_FORWARD          0  'to 313'
            313_0  COME_FROM           310  '310'
              313  LOAD_CONST               None
              316  DUP_TOP          
              317  STORE_FAST            3  '@py_assert0'
              320  DUP_TOP          
              321  STORE_FAST            5  '@py_assert2'
              324  STORE_FAST            4  '@py_assert3'

 L.  60       327  LOAD_GLOBAL          12  'simplejson'
              330  LOAD_ATTR            13  'loads'
              333  LOAD_FAST             2  'content'
              336  CALL_FUNCTION_1       1  None
              339  STORE_FAST            8  'info'

 L.  61       342  LOAD_GLOBAL          14  'len'
              345  LOAD_FAST             8  'info'
              348  CALL_FUNCTION_1       1  None
              351  LOAD_CONST               1
              354  COMPARE_OP            2  ==
              357  POP_JUMP_IF_TRUE    369  'to 369'
              360  LOAD_ASSERT              AssertionError
              363  LOAD_FAST             8  'info'
              366  RAISE_VARARGS_2       2  None

 L.  63       369  LOAD_GLOBAL           4  'http'
              372  LOAD_ATTR             5  'request'

 L.  64       375  LOAD_CONST               'http://0.0.0.0:8080/search.json?q=ftitle:one%20two'
              378  CALL_FUNCTION_1       1  None
              381  UNPACK_SEQUENCE_2     2 
              384  STORE_FAST            1  'response'
              387  STORE_FAST            2  'content'

 L.  65       390  LOAD_FAST             1  'response'
              393  LOAD_CONST               'status'
              396  BINARY_SUBSCR    
              397  STORE_FAST            3  '@py_assert0'
              400  LOAD_CONST               '200'
              403  STORE_FAST            4  '@py_assert3'
              406  LOAD_FAST             3  '@py_assert0'
              409  LOAD_FAST             4  '@py_assert3'
              412  COMPARE_OP            2  ==
              415  STORE_FAST            5  '@py_assert2'
              418  LOAD_FAST             5  '@py_assert2'
              421  POP_JUMP_IF_TRUE    534  'to 534'
              424  LOAD_GLOBAL           6  '@pytest_ar'
              427  LOAD_ATTR             7  '_call_reprcompare'
              430  LOAD_CONST               ('==',)
              433  LOAD_FAST             5  '@py_assert2'
              436  BUILD_TUPLE_1         1 
              439  LOAD_CONST               ('%(py1)s == %(py4)s',)
              442  LOAD_FAST             3  '@py_assert0'
              445  LOAD_FAST             4  '@py_assert3'
              448  BUILD_TUPLE_2         2 
              451  CALL_FUNCTION_4       4  None
              454  BUILD_MAP_2           2  None
              457  LOAD_GLOBAL           6  '@pytest_ar'
              460  LOAD_ATTR             8  '_saferepr'
              463  LOAD_FAST             3  '@py_assert0'
              466  CALL_FUNCTION_1       1  None
              469  LOAD_CONST               'py1'
              472  STORE_MAP        
              473  LOAD_GLOBAL           6  '@pytest_ar'
              476  LOAD_ATTR             8  '_saferepr'
              479  LOAD_FAST             4  '@py_assert3'
              482  CALL_FUNCTION_1       1  None
              485  LOAD_CONST               'py4'
              488  STORE_MAP        
              489  BINARY_MODULO    
              490  STORE_FAST            6  '@py_format5'
              493  LOAD_CONST               'assert %(py6)s'
              496  BUILD_MAP_1           1  None
              499  LOAD_FAST             6  '@py_format5'
              502  LOAD_CONST               'py6'
              505  STORE_MAP        
              506  BINARY_MODULO    
              507  STORE_FAST            7  '@py_format7'
              510  LOAD_GLOBAL           9  'AssertionError'
              513  LOAD_GLOBAL           6  '@pytest_ar'
              516  LOAD_ATTR            10  '_format_explanation'
              519  LOAD_FAST             7  '@py_format7'
              522  CALL_FUNCTION_1       1  None
              525  CALL_FUNCTION_1       1  None
              528  RAISE_VARARGS_1       1  None
              531  JUMP_FORWARD          0  'to 534'
            534_0  COME_FROM           531  '531'
              534  LOAD_CONST               None
              537  DUP_TOP          
              538  STORE_FAST            3  '@py_assert0'
              541  DUP_TOP          
              542  STORE_FAST            5  '@py_assert2'
              545  STORE_FAST            4  '@py_assert3'

 L.  66       548  LOAD_GLOBAL          12  'simplejson'
              551  LOAD_ATTR            13  'loads'
              554  LOAD_FAST             2  'content'
              557  CALL_FUNCTION_1       1  None
              560  STORE_FAST            8  'info'

 L.  67       563  LOAD_GLOBAL          14  'len'
              566  LOAD_FAST             8  'info'
              569  CALL_FUNCTION_1       1  None
              572  LOAD_CONST               0
              575  COMPARE_OP            2  ==
              578  POP_JUMP_IF_TRUE    590  'to 590'
              581  LOAD_ASSERT              AssertionError
              584  LOAD_FAST             8  'info'
              587  RAISE_VARARGS_2       2  None

 L.  69       590  LOAD_GLOBAL           4  'http'
              593  LOAD_ATTR             5  'request'

 L.  70       596  LOAD_CONST               'http://0.0.0.0:8080/search.json?q=ftitle:one%20two%20three'
              599  CALL_FUNCTION_1       1  None
              602  UNPACK_SEQUENCE_2     2 
              605  STORE_FAST            1  'response'
              608  STORE_FAST            2  'content'

 L.  71       611  LOAD_FAST             1  'response'
              614  LOAD_CONST               'status'
              617  BINARY_SUBSCR    
              618  STORE_FAST            3  '@py_assert0'
              621  LOAD_CONST               '200'
              624  STORE_FAST            4  '@py_assert3'
              627  LOAD_FAST             3  '@py_assert0'
              630  LOAD_FAST             4  '@py_assert3'
              633  COMPARE_OP            2  ==
              636  STORE_FAST            5  '@py_assert2'
              639  LOAD_FAST             5  '@py_assert2'
              642  POP_JUMP_IF_TRUE    755  'to 755'
              645  LOAD_GLOBAL           6  '@pytest_ar'
              648  LOAD_ATTR             7  '_call_reprcompare'
              651  LOAD_CONST               ('==',)
              654  LOAD_FAST             5  '@py_assert2'
              657  BUILD_TUPLE_1         1 
              660  LOAD_CONST               ('%(py1)s == %(py4)s',)
              663  LOAD_FAST             3  '@py_assert0'
              666  LOAD_FAST             4  '@py_assert3'
              669  BUILD_TUPLE_2         2 
              672  CALL_FUNCTION_4       4  None
              675  BUILD_MAP_2           2  None
              678  LOAD_GLOBAL           6  '@pytest_ar'
              681  LOAD_ATTR             8  '_saferepr'
              684  LOAD_FAST             3  '@py_assert0'
              687  CALL_FUNCTION_1       1  None
              690  LOAD_CONST               'py1'
              693  STORE_MAP        
              694  LOAD_GLOBAL           6  '@pytest_ar'
              697  LOAD_ATTR             8  '_saferepr'
              700  LOAD_FAST             4  '@py_assert3'
              703  CALL_FUNCTION_1       1  None
              706  LOAD_CONST               'py4'
              709  STORE_MAP        
              710  BINARY_MODULO    
              711  STORE_FAST            6  '@py_format5'
              714  LOAD_CONST               'assert %(py6)s'
              717  BUILD_MAP_1           1  None
              720  LOAD_FAST             6  '@py_format5'
              723  LOAD_CONST               'py6'
              726  STORE_MAP        
              727  BINARY_MODULO    
              728  STORE_FAST            7  '@py_format7'
              731  LOAD_GLOBAL           9  'AssertionError'
              734  LOAD_GLOBAL           6  '@pytest_ar'
              737  LOAD_ATTR            10  '_format_explanation'
              740  LOAD_FAST             7  '@py_format7'
              743  CALL_FUNCTION_1       1  None
              746  CALL_FUNCTION_1       1  None
              749  RAISE_VARARGS_1       1  None
              752  JUMP_FORWARD          0  'to 755'
            755_0  COME_FROM           752  '752'
              755  LOAD_CONST               None
              758  DUP_TOP          
              759  STORE_FAST            3  '@py_assert0'
              762  DUP_TOP          
              763  STORE_FAST            5  '@py_assert2'
              766  STORE_FAST            4  '@py_assert3'

 L.  72       769  LOAD_GLOBAL          12  'simplejson'
              772  LOAD_ATTR            13  'loads'
              775  LOAD_FAST             2  'content'
              778  CALL_FUNCTION_1       1  None
              781  STORE_FAST            8  'info'

 L.  73       784  LOAD_GLOBAL          14  'len'
              787  LOAD_FAST             8  'info'
              790  CALL_FUNCTION_1       1  None
              793  LOAD_CONST               0
              796  COMPARE_OP            2  ==
              799  POP_JUMP_IF_TRUE    811  'to 811'
              802  LOAD_ASSERT              AssertionError
              805  LOAD_FAST             8  'info'
              808  RAISE_VARARGS_2       2  None

 L.  75       811  LOAD_GLOBAL           4  'http'
              814  LOAD_ATTR             5  'request'

 L.  76       817  LOAD_CONST               'http://0.0.0.0:8080/search.json?q=ftitle:%22one%20two%20three%22'
              820  CALL_FUNCTION_1       1  None
              823  UNPACK_SEQUENCE_2     2 
              826  STORE_FAST            1  'response'
              829  STORE_FAST            2  'content'

 L.  77       832  LOAD_FAST             1  'response'
              835  LOAD_CONST               'status'
              838  BINARY_SUBSCR    
              839  STORE_FAST            3  '@py_assert0'
              842  LOAD_CONST               '200'
              845  STORE_FAST            4  '@py_assert3'
              848  LOAD_FAST             3  '@py_assert0'
              851  LOAD_FAST             4  '@py_assert3'
              854  COMPARE_OP            2  ==
              857  STORE_FAST            5  '@py_assert2'
              860  LOAD_FAST             5  '@py_assert2'
              863  POP_JUMP_IF_TRUE    976  'to 976'
              866  LOAD_GLOBAL           6  '@pytest_ar'
              869  LOAD_ATTR             7  '_call_reprcompare'
              872  LOAD_CONST               ('==',)
              875  LOAD_FAST             5  '@py_assert2'
              878  BUILD_TUPLE_1         1 
              881  LOAD_CONST               ('%(py1)s == %(py4)s',)
              884  LOAD_FAST             3  '@py_assert0'
              887  LOAD_FAST             4  '@py_assert3'
              890  BUILD_TUPLE_2         2 
              893  CALL_FUNCTION_4       4  None
              896  BUILD_MAP_2           2  None
              899  LOAD_GLOBAL           6  '@pytest_ar'
              902  LOAD_ATTR             8  '_saferepr'
              905  LOAD_FAST             3  '@py_assert0'
              908  CALL_FUNCTION_1       1  None
              911  LOAD_CONST               'py1'
              914  STORE_MAP        
              915  LOAD_GLOBAL           6  '@pytest_ar'
              918  LOAD_ATTR             8  '_saferepr'
              921  LOAD_FAST             4  '@py_assert3'
              924  CALL_FUNCTION_1       1  None
              927  LOAD_CONST               'py4'
              930  STORE_MAP        
              931  BINARY_MODULO    
              932  STORE_FAST            6  '@py_format5'
              935  LOAD_CONST               'assert %(py6)s'
              938  BUILD_MAP_1           1  None
              941  LOAD_FAST             6  '@py_format5'
              944  LOAD_CONST               'py6'
              947  STORE_MAP        
              948  BINARY_MODULO    
              949  STORE_FAST            7  '@py_format7'
              952  LOAD_GLOBAL           9  'AssertionError'
              955  LOAD_GLOBAL           6  '@pytest_ar'
              958  LOAD_ATTR            10  '_format_explanation'
              961  LOAD_FAST             7  '@py_format7'
              964  CALL_FUNCTION_1       1  None
              967  CALL_FUNCTION_1       1  None
              970  RAISE_VARARGS_1       1  None
              973  JUMP_FORWARD          0  'to 976'
            976_0  COME_FROM           973  '973'
              976  LOAD_CONST               None
              979  DUP_TOP          
              980  STORE_FAST            3  '@py_assert0'
              983  DUP_TOP          
              984  STORE_FAST            5  '@py_assert2'
              987  STORE_FAST            4  '@py_assert3'

 L.  78       990  LOAD_GLOBAL          12  'simplejson'
              993  LOAD_ATTR            13  'loads'
              996  LOAD_FAST             2  'content'
              999  CALL_FUNCTION_1       1  None
             1002  STORE_FAST            8  'info'

 L.  79      1005  LOAD_GLOBAL          14  'len'
             1008  LOAD_FAST             8  'info'
             1011  CALL_FUNCTION_1       1  None
             1014  LOAD_CONST               1
             1017  COMPARE_OP            2  ==
             1020  POP_JUMP_IF_TRUE   1032  'to 1032'
             1023  LOAD_ASSERT              AssertionError
             1026  LOAD_FAST             8  'info'
             1029  RAISE_VARARGS_2       2  None
             1032  LOAD_CONST               None
             1035  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 1032


def test_multibag_search--- This code section failed: ---

 L.  82         0  LOAD_GLOBAL           0  'Tiddler'
                3  LOAD_CONST               'one two'
                6  LOAD_CONST               'fnd_public'
                9  CALL_FUNCTION_2       2  None
               12  STORE_FAST            0  'tiddler'

 L.  83        15  LOAD_CONST               'monkeys are not fun!'
               18  LOAD_FAST             0  'tiddler'
               21  STORE_ATTR            1  'text'

 L.  84        24  LOAD_GLOBAL           2  'store'
               27  LOAD_ATTR             3  'put'
               30  LOAD_FAST             0  'tiddler'
               33  CALL_FUNCTION_1       1  None
               36  POP_TOP          

 L.  86        37  LOAD_GLOBAL           4  'http'
               40  LOAD_ATTR             5  'request'

 L.  87        43  LOAD_CONST               'http://0.0.0.0:8080/search.json?q=ftitle:%22one%20two%22%20fbag:cdent_public'
               46  CALL_FUNCTION_1       1  None
               49  UNPACK_SEQUENCE_2     2 
               52  STORE_FAST            1  'response'
               55  STORE_FAST            2  'content'

 L.  88        58  LOAD_GLOBAL           6  'simplejson'
               61  LOAD_ATTR             7  'loads'
               64  LOAD_FAST             2  'content'
               67  CALL_FUNCTION_1       1  None
               70  STORE_FAST            3  'info'

 L.  89        73  LOAD_GLOBAL           8  'len'
               76  LOAD_FAST             3  'info'
               79  CALL_FUNCTION_1       1  None
               82  LOAD_CONST               1
               85  COMPARE_OP            2  ==
               88  POP_JUMP_IF_TRUE    100  'to 100'
               91  LOAD_ASSERT              AssertionError
               94  LOAD_FAST             3  'info'
               97  RAISE_VARARGS_2       2  None

 L.  90       100  LOAD_FAST             3  'info'
              103  LOAD_CONST               0
              106  BINARY_SUBSCR    
              107  LOAD_CONST               'bag'
              110  BINARY_SUBSCR    
              111  LOAD_CONST               'cdent_public'
              114  COMPARE_OP            2  ==
              117  POP_JUMP_IF_TRUE    129  'to 129'
              120  LOAD_ASSERT              AssertionError
              123  LOAD_FAST             3  'info'
              126  RAISE_VARARGS_2       2  None

 L.  92       129  LOAD_GLOBAL           4  'http'
              132  LOAD_ATTR             5  'request'

 L.  93       135  LOAD_CONST               'http://0.0.0.0:8080/search.json?q=ftitle:%22one%20two%22%20(fbag:cdent_public%20OR%20fbag:fnd_public)'
              138  CALL_FUNCTION_1       1  None
              141  UNPACK_SEQUENCE_2     2 
              144  STORE_FAST            1  'response'
              147  STORE_FAST            2  'content'

 L.  94       150  LOAD_GLOBAL           6  'simplejson'
              153  LOAD_ATTR             7  'loads'
              156  LOAD_FAST             2  'content'
              159  CALL_FUNCTION_1       1  None
              162  STORE_FAST            3  'info'

 L.  95       165  LOAD_GLOBAL           8  'len'
              168  LOAD_FAST             3  'info'
              171  CALL_FUNCTION_1       1  None
              174  LOAD_CONST               2
              177  COMPARE_OP            2  ==
              180  POP_JUMP_IF_TRUE    192  'to 192'
              183  LOAD_ASSERT              AssertionError
              186  LOAD_FAST             3  'info'
              189  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_FAST' instruction at offset 186


def test_cased_search--- This code section failed: ---

 L.  98         0  LOAD_GLOBAL           0  'Tiddler'
                3  LOAD_CONST               'One Two'
                6  LOAD_CONST               'fnd_public'
                9  CALL_FUNCTION_2       2  None
               12  STORE_FAST            0  'tiddler'

 L.  99        15  LOAD_CONST               'monkeys are not fun!'
               18  LOAD_FAST             0  'tiddler'
               21  STORE_ATTR            1  'text'

 L. 100        24  LOAD_GLOBAL           2  'store'
               27  LOAD_ATTR             3  'put'
               30  LOAD_FAST             0  'tiddler'
               33  CALL_FUNCTION_1       1  None
               36  POP_TOP          

 L. 102        37  LOAD_GLOBAL           4  'http'
               40  LOAD_ATTR             5  'request'

 L. 103        43  LOAD_CONST               'http://0.0.0.0:8080/search.json?q=ftitle:%22one%20two%22%20fbag:fnd_public'
               46  CALL_FUNCTION_1       1  None
               49  UNPACK_SEQUENCE_2     2 
               52  STORE_FAST            1  'response'
               55  STORE_FAST            2  'content'

 L. 104        58  LOAD_GLOBAL           6  'simplejson'
               61  LOAD_ATTR             7  'loads'
               64  LOAD_FAST             2  'content'
               67  CALL_FUNCTION_1       1  None
               70  STORE_FAST            3  'info'

 L. 105        73  LOAD_GLOBAL           8  'len'
               76  LOAD_FAST             3  'info'
               79  CALL_FUNCTION_1       1  None
               82  LOAD_CONST               1
               85  COMPARE_OP            2  ==
               88  POP_JUMP_IF_TRUE    100  'to 100'
               91  LOAD_ASSERT              AssertionError
               94  LOAD_FAST             3  'info'
               97  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_FAST' instruction at offset 94


def test_search_no_args():
    """a no args search is like recent changes, this test confirms
    controlview"""
    response, content = http.request('http://0.0.0.0:8080/search.json')
    @py_assert0 = response['status']
    @py_assert3 = '400'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://0.0.0.0:8080/search.json?q=_limit:999')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    allinfo = simplejson.loads(content)
    @py_assert2 = len(allinfo)
    @py_assert5 = 171
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(allinfo) if 'allinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(allinfo) else 'allinfo', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    response, content = http.request('http://fnd.0.0.0.0:8080/search.json')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    fndinfo = simplejson.loads(content)
    @py_assert2 = len(fndinfo)
    @py_assert5 = 20
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(fndinfo) if 'fndinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fndinfo) else 'fndinfo', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    response, content = http.request('http://fnd.0.0.0.0:8080/search.json?q=_limit:999')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    fndinfo = simplejson.loads(content)
    @py_assert2 = len(fndinfo)
    @py_assert5 = 150
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(fndinfo) if 'fndinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fndinfo) else 'fndinfo', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = len(allinfo)
    @py_assert7 = len(fndinfo)
    @py_assert4 = @py_assert2 > @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('>',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} > %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}',), (@py_assert2, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(allinfo) if 'allinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(allinfo) else 'allinfo', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py6': @pytest_ar._saferepr(fndinfo) if 'fndinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fndinfo) else 'fndinfo'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    return


def test_hsearch--- This code section failed: ---

 L. 132         0  LOAD_GLOBAL           0  'http'
                3  LOAD_ATTR             1  'request'
                6  LOAD_CONST               'http://0.0.0.0:8080/hsearch.json?q=monkeys'
                9  CALL_FUNCTION_1       1  None
               12  UNPACK_SEQUENCE_2     2 
               15  STORE_FAST            0  'response'
               18  STORE_FAST            1  'content'

 L. 134        21  LOAD_FAST             0  'response'
               24  LOAD_CONST               'status'
               27  BINARY_SUBSCR    
               28  STORE_FAST            2  '@py_assert0'
               31  LOAD_CONST               '200'
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

 L. 135       179  LOAD_GLOBAL           8  'simplejson'
              182  LOAD_ATTR             9  'loads'
              185  LOAD_FAST             1  'content'
              188  CALL_FUNCTION_1       1  None
              191  STORE_FAST            7  'info'

 L. 136       194  LOAD_GLOBAL          10  'len'
              197  LOAD_FAST             7  'info'
              200  CALL_FUNCTION_1       1  None
              203  LOAD_CONST               6
              206  COMPARE_OP            2  ==
              209  POP_JUMP_IF_TRUE    227  'to 227'
              212  LOAD_ASSERT              AssertionError
              215  LOAD_GLOBAL          10  'len'
              218  LOAD_FAST             7  'info'
              221  CALL_FUNCTION_1       1  None
              224  RAISE_VARARGS_2       2  None

 L. 138       227  LOAD_GLOBAL           0  'http'
              230  LOAD_ATTR             1  'request'
              233  LOAD_CONST               'http://0.0.0.0:8080/hsearch.json?q=bag:cdent_public%20monkeys'
              236  CALL_FUNCTION_1       1  None
              239  UNPACK_SEQUENCE_2     2 
              242  STORE_FAST            0  'response'
              245  STORE_FAST            1  'content'

 L. 140       248  LOAD_FAST             0  'response'
              251  LOAD_CONST               'status'
              254  BINARY_SUBSCR    
              255  STORE_FAST            2  '@py_assert0'
              258  LOAD_CONST               '200'
              261  STORE_FAST            3  '@py_assert3'
              264  LOAD_FAST             2  '@py_assert0'
              267  LOAD_FAST             3  '@py_assert3'
              270  COMPARE_OP            2  ==
              273  STORE_FAST            4  '@py_assert2'
              276  LOAD_FAST             4  '@py_assert2'
              279  POP_JUMP_IF_TRUE    392  'to 392'
              282  LOAD_GLOBAL           2  '@pytest_ar'
              285  LOAD_ATTR             3  '_call_reprcompare'
              288  LOAD_CONST               ('==',)
              291  LOAD_FAST             4  '@py_assert2'
              294  BUILD_TUPLE_1         1 
              297  LOAD_CONST               ('%(py1)s == %(py4)s',)
              300  LOAD_FAST             2  '@py_assert0'
              303  LOAD_FAST             3  '@py_assert3'
              306  BUILD_TUPLE_2         2 
              309  CALL_FUNCTION_4       4  None
              312  BUILD_MAP_2           2  None
              315  LOAD_GLOBAL           2  '@pytest_ar'
              318  LOAD_ATTR             4  '_saferepr'
              321  LOAD_FAST             2  '@py_assert0'
              324  CALL_FUNCTION_1       1  None
              327  LOAD_CONST               'py1'
              330  STORE_MAP        
              331  LOAD_GLOBAL           2  '@pytest_ar'
              334  LOAD_ATTR             4  '_saferepr'
              337  LOAD_FAST             3  '@py_assert3'
              340  CALL_FUNCTION_1       1  None
              343  LOAD_CONST               'py4'
              346  STORE_MAP        
              347  BINARY_MODULO    
              348  STORE_FAST            5  '@py_format5'
              351  LOAD_CONST               'assert %(py6)s'
              354  BUILD_MAP_1           1  None
              357  LOAD_FAST             5  '@py_format5'
              360  LOAD_CONST               'py6'
              363  STORE_MAP        
              364  BINARY_MODULO    
              365  STORE_FAST            6  '@py_format7'
              368  LOAD_GLOBAL           5  'AssertionError'
              371  LOAD_GLOBAL           2  '@pytest_ar'
              374  LOAD_ATTR             6  '_format_explanation'
              377  LOAD_FAST             6  '@py_format7'
              380  CALL_FUNCTION_1       1  None
              383  CALL_FUNCTION_1       1  None
              386  RAISE_VARARGS_1       1  None
              389  JUMP_FORWARD          0  'to 392'
            392_0  COME_FROM           389  '389'
              392  LOAD_CONST               None
              395  DUP_TOP          
              396  STORE_FAST            2  '@py_assert0'
              399  DUP_TOP          
              400  STORE_FAST            4  '@py_assert2'
              403  STORE_FAST            3  '@py_assert3'

 L. 141       406  LOAD_GLOBAL           8  'simplejson'
              409  LOAD_ATTR             9  'loads'
              412  LOAD_FAST             1  'content'
              415  CALL_FUNCTION_1       1  None
              418  STORE_FAST            7  'info'

 L. 142       421  LOAD_GLOBAL          10  'len'
              424  LOAD_FAST             7  'info'
              427  CALL_FUNCTION_1       1  None
              430  LOAD_CONST               4
              433  COMPARE_OP            2  ==
              436  POP_JUMP_IF_TRUE    454  'to 454'
              439  LOAD_ASSERT              AssertionError
              442  LOAD_GLOBAL          10  'len'
              445  LOAD_FAST             7  'info'
              448  CALL_FUNCTION_1       1  None
              451  RAISE_VARARGS_2       2  None
              454  LOAD_CONST               None
              457  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 454


def test_search_html():
    response, content = http.request('http://0.0.0.0:8080/search?q=monkeys')
    if not response['status'] == '200':
        raise AssertionError, content
        @py_assert0 = 'http://fnd.0.0.0.0:8080/One%20Two'
        @py_assert2 = @py_assert0 in content
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'http://cdent.0.0.0.0:8080/three%20two%20one'
        @py_assert2 = @py_assert0 in content
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = '<a class="space" href="http://fnd.0.0.0.0:8080/">'
        @py_assert2 = @py_assert0 in content
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = '<img alt="space icon" src="http://fnd.0.0.0.0:8080/SiteIcon"/>'
        @py_assert2 = @py_assert0 in content
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        tiddler = store.get(Tiddler('One Two', 'fnd_public'))
        tiddler.modifier = 'cowboy'
        store.put(tiddler)
        response, content = http.request('http://0.0.0.0:8080/search?q=monkeys')
        if not response['status'] == '200':
            raise AssertionError, content
            @py_assert0 = '<a class="modifier" href="http://fnd.0.0.0.0:8080/">'
            @py_assert2 = @py_assert0 not in content
            @py_format4 = @py_assert2 or @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = '<a class="modifier" href="http://cowboy.0.0.0.0:8080/">'
        @py_assert2 = @py_assert0 in content
        @py_format4 = @py_assert2 or @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    tiddler = Tiddler('commoner', 'common')
    tiddler.text = 'I want to live like common people.'
    store.put(tiddler)
    response, content = http.request('http://0.0.0.0:8080/search?q=title:commoner')
    if not response['status'] == '200':
        raise AssertionError, content
        @py_assert0 = '<img alt="space icon" src="http://0.0.0.0:8080/SiteIcon"/>'
        @py_assert2 = @py_assert0 in content
        @py_format4 = @py_assert2 or @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return