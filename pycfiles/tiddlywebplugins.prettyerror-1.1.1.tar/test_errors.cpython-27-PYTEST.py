# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.prettyerror/test/test_errors.py
# Compiled at: 2013-02-21 10:45:40
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, httplib2, wsgi_intercept, shutil, os, sys, urllib
from tiddlywebplugins.imaker import spawn
import tiddlywebplugins.prettyerror.instance as instance_module
from tiddlywebplugins.prettyerror.config import config as init_config
from tiddlywebplugins.prettyerror import init
from wsgi_intercept import httplib2_intercept
from tiddlyweb.store import Store
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler

def make_test_env():
    try:
        shutil.rmtree('test_instance')
    except OSError:
        pass

    spawn('test_instance', init_config, instance_module)
    os.chdir('test_instance')


def setup_module(module):
    make_test_env()
    from tiddlyweb.web import serve
    from tiddlyweb.config import config
    init(config)

    def app_fn():
        return serve.load_app()

    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)
    module.store = Store(config['server_store'][0], config['server_store'][1], {'tiddlyweb.config': config})
    module.http = httplib2.Http()


def test_selector_404():
    response, content = http.request('http://0.0.0.0:8080/fake', method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '404'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['content-type']
    @py_assert3 = 'text/html; charset=UTF-8'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'Path not found for "/fake"'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() is not @py_builtins.globals() else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_tiddlyweb_404():
    response, content = http.request('http://0.0.0.0:8080/bags/fake', method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '404'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['content-type']
    @py_assert3 = 'text/html; charset=UTF-8'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'Path not found for "/bags/fake"'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() is not @py_builtins.globals() else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_plain_output():
    response, content = http.request('http://0.0.0.0:8080/bags/fake', method='GET', headers={'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '404'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['content-type']
    @py_assert3 = 'text/plain; charset=UTF-8'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = '404 Not Found: fake not found'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() is not @py_builtins.globals() else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_404_with_unicode--- This code section failed: ---

 L.  75         0  LOAD_GLOBAL           0  'urllib'
                3  LOAD_ATTR             1  'unquote'
                6  LOAD_CONST               'test%C2%B7test'
                9  CALL_FUNCTION_1       1  None
               12  LOAD_ATTR             2  'decode'
               15  LOAD_CONST               'utf-8'
               18  CALL_FUNCTION_1       1  None
               21  STORE_FAST            0  'title'

 L.  76        24  LOAD_GLOBAL           3  'store'
               27  LOAD_ATTR             4  'put'
               30  LOAD_GLOBAL           5  'Bag'
               33  LOAD_CONST               'test'
               36  CALL_FUNCTION_1       1  None
               39  CALL_FUNCTION_1       1  None
               42  POP_TOP          

 L.  77        43  LOAD_GLOBAL           3  'store'
               46  LOAD_ATTR             4  'put'
               49  LOAD_GLOBAL           6  'Tiddler'
               52  LOAD_FAST             0  'title'
               55  LOAD_CONST               'test'
               58  CALL_FUNCTION_2       2  None
               61  CALL_FUNCTION_1       1  None
               64  POP_TOP          

 L.  78        65  LOAD_GLOBAL           7  'http'
               68  LOAD_ATTR             8  'request'
               71  LOAD_CONST               'http://0.0.0.0:8080/bags/test/tiddlers/test%C2%B7test'
               74  CALL_FUNCTION_1       1  None
               77  UNPACK_SEQUENCE_2     2 
               80  STORE_FAST            1  'response'
               83  STORE_FAST            2  'content'

 L.  79        86  LOAD_FAST             1  'response'
               89  LOAD_CONST               'status'
               92  BINARY_SUBSCR    
               93  STORE_FAST            3  '@py_assert0'
               96  LOAD_CONST               '200'
               99  STORE_FAST            4  '@py_assert3'
              102  LOAD_FAST             3  '@py_assert0'
              105  LOAD_FAST             4  '@py_assert3'
              108  COMPARE_OP            2  ==
              111  STORE_FAST            5  '@py_assert2'
              114  LOAD_FAST             5  '@py_assert2'
              117  POP_JUMP_IF_TRUE    230  'to 230'
              120  LOAD_GLOBAL           9  '@pytest_ar'
              123  LOAD_ATTR            10  '_call_reprcompare'
              126  LOAD_CONST               ('==',)
              129  LOAD_FAST             5  '@py_assert2'
              132  BUILD_TUPLE_1         1 
              135  LOAD_CONST               ('%(py1)s == %(py4)s',)
              138  LOAD_FAST             3  '@py_assert0'
              141  LOAD_FAST             4  '@py_assert3'
              144  BUILD_TUPLE_2         2 
              147  CALL_FUNCTION_4       4  None
              150  BUILD_MAP_2           2  None
              153  LOAD_GLOBAL           9  '@pytest_ar'
              156  LOAD_ATTR            11  '_saferepr'
              159  LOAD_FAST             3  '@py_assert0'
              162  CALL_FUNCTION_1       1  None
              165  LOAD_CONST               'py1'
              168  STORE_MAP        
              169  LOAD_GLOBAL           9  '@pytest_ar'
              172  LOAD_ATTR            11  '_saferepr'
              175  LOAD_FAST             4  '@py_assert3'
              178  CALL_FUNCTION_1       1  None
              181  LOAD_CONST               'py4'
              184  STORE_MAP        
              185  BINARY_MODULO    
              186  STORE_FAST            6  '@py_format5'
              189  LOAD_CONST               'assert %(py6)s'
              192  BUILD_MAP_1           1  None
              195  LOAD_FAST             6  '@py_format5'
              198  LOAD_CONST               'py6'
              201  STORE_MAP        
              202  BINARY_MODULO    
              203  STORE_FAST            7  '@py_format7'
              206  LOAD_GLOBAL          12  'AssertionError'
              209  LOAD_GLOBAL           9  '@pytest_ar'
              212  LOAD_ATTR            13  '_format_explanation'
              215  LOAD_FAST             7  '@py_format7'
              218  CALL_FUNCTION_1       1  None
              221  CALL_FUNCTION_1       1  None
              224  RAISE_VARARGS_1       1  None
              227  JUMP_FORWARD          0  'to 230'
            230_0  COME_FROM           227  '227'
              230  LOAD_CONST               None
              233  DUP_TOP          
              234  STORE_FAST            3  '@py_assert0'
              237  DUP_TOP          
              238  STORE_FAST            5  '@py_assert2'
              241  STORE_FAST            4  '@py_assert3'

 L.  80       244  LOAD_GLOBAL           7  'http'
              247  LOAD_ATTR             8  'request'
              250  LOAD_CONST               'http://0.0.0.0:8080/bags/test/tiddlers/test%C2%B7test/revisions/24'
              253  CALL_FUNCTION_1       1  None
              256  UNPACK_SEQUENCE_2     2 
              259  STORE_FAST            1  'response'
              262  STORE_FAST            2  'content'

 L.  81       265  LOAD_FAST             1  'response'
              268  LOAD_CONST               'status'
              271  BINARY_SUBSCR    
              272  LOAD_CONST               '404'
              275  COMPARE_OP            2  ==
              278  POP_JUMP_IF_TRUE    290  'to 290'
              281  LOAD_ASSERT              AssertionError
              284  LOAD_FAST             2  'content'
              287  RAISE_VARARGS_2       2  None

 L.  84       290  LOAD_FAST             0  'title'
              293  LOAD_GLOBAL           3  'store'
              296  LOAD_ATTR            15  'environ'
              299  LOAD_CONST               'silly.code'
              302  STORE_SUBSCR     

 L.  85       303  LOAD_GLOBAL           7  'http'
              306  LOAD_ATTR             8  'request'
              309  LOAD_CONST               'http://0.0.0.0:8080/bags/test/tiddlers/test%C2%B7test/revisions/24'
              312  CALL_FUNCTION_1       1  None
              315  UNPACK_SEQUENCE_2     2 
              318  STORE_FAST            1  'response'
              321  STORE_FAST            2  'content'

 L.  86       324  LOAD_FAST             1  'response'
              327  LOAD_CONST               'status'
              330  BINARY_SUBSCR    
              331  LOAD_CONST               '404'
              334  COMPARE_OP            2  ==
              337  POP_JUMP_IF_TRUE    349  'to 349'
              340  LOAD_ASSERT              AssertionError
              343  LOAD_FAST             2  'content'
              346  RAISE_VARARGS_2       2  None
              349  LOAD_CONST               None
              352  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 349


def test_explict_accept():
    response, content = http.request('http://0.0.0.0:8080/bags/test/test.js', headers={'Accept': 'text/javascript'})
    if not response['status'] == '404':
        raise AssertionError, content
        @py_assert0 = 'text/plain'
        @py_assert3 = response['content-type']
        @py_assert2 = @py_assert0 in @py_assert3
        @py_format5 = @py_assert2 or @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return