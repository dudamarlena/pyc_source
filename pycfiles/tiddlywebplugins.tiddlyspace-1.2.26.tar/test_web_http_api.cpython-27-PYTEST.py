# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyspace/test/test_web_http_api.py
# Compiled at: 2013-11-01 16:22:24
"""
Run through the socialusers API testing what's there.

Read the TESTS variable as document of
the capabilities of the API.

If you run this test file by itself, instead
of as a test it will produce a list of test
requests and some associated information.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from test.fixtures import make_test_env
from wsgi_intercept import httplib2_intercept
import wsgi_intercept, httplib2, yaml
base_url = 'http://0.0.0.0:8080'
TESTS = {}

def setup_module(module):
    global TESTS
    make_test_env(module)
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)
    module.http = httplib2.Http()
    TESTS = yaml.load(open('../test/httptest.yaml'))


def test_assert_response():
    """
    Make sure our assertion tester is valid.
    """
    response = {'status': '200', 
       'location': 'http://example.com'}
    content = 'Hello World\n'
    status = '200'
    headers = {'location': 'http://example.com'}
    expected = [
     'Hello']
    assert_response(response, content, status, headers, expected)


EMPTY_TEST = {'name': '', 
   'desc': '', 
   'method': 'GET', 
   'url': '', 
   'status': '200', 
   'request_headers': {}, 'response_headers': {}, 'expected': [], 'data': ''}

def test_the_TESTS():
    """
    Run the entire TEST.
    """
    for test_data in TESTS:
        test = dict(EMPTY_TEST)
        test.update(test_data)
        yield (test['name'], _run_test, test)


def _run_test(test):
    full_url = base_url + test['url']
    if test['method'] == 'GET' or test['method'] == 'DELETE':
        response, content = http.request(full_url, method=test['method'], headers=test['request_headers'])
    else:
        response, content = http.request(full_url, method=test['method'], headers=test['request_headers'], body=test['data'].encode('UTF-8'))
    assert_response(response, content, test['status'], headers=test['response_headers'], expected=test['expected'])


def assert_response--- This code section failed: ---

 L.  84         0  LOAD_FAST             0  'response'
                3  LOAD_CONST               'status'
                6  BINARY_SUBSCR    
                7  LOAD_CONST               '500'
               10  COMPARE_OP            2  ==
               13  POP_JUMP_IF_FALSE    24  'to 24'
               16  LOAD_FAST             1  'content'
               19  PRINT_ITEM       
               20  PRINT_NEWLINE_CONT
               21  JUMP_FORWARD          0  'to 24'
             24_0  COME_FROM            21  '21'

 L.  85        24  LOAD_FAST             0  'response'
               27  LOAD_CONST               'status'
               30  BINARY_SUBSCR    
               31  LOAD_CONST               '%s'
               34  LOAD_FAST             2  'status'
               37  BINARY_MODULO    
               38  COMPARE_OP            2  ==
               41  POP_JUMP_IF_TRUE     59  'to 59'
               44  LOAD_ASSERT              AssertionError
               47  LOAD_FAST             0  'response'
               50  LOAD_FAST             1  'content'
               53  BUILD_TUPLE_2         2 
               56  RAISE_VARARGS_2       2  None

 L.  87        59  LOAD_FAST             3  'headers'
               62  POP_JUMP_IF_FALSE   247  'to 247'

 L.  88        65  SETUP_LOOP          179  'to 247'
               68  LOAD_FAST             3  'headers'
               71  GET_ITER         
               72  FOR_ITER            168  'to 243'
               75  STORE_FAST            5  'header'

 L.  89        78  LOAD_FAST             0  'response'
               81  LOAD_FAST             5  'header'
               84  BINARY_SUBSCR    
               85  STORE_FAST            6  '@py_assert0'
               88  LOAD_FAST             3  'headers'
               91  LOAD_FAST             5  'header'
               94  BINARY_SUBSCR    
               95  STORE_FAST            7  '@py_assert3'
               98  LOAD_FAST             6  '@py_assert0'
              101  LOAD_FAST             7  '@py_assert3'
              104  COMPARE_OP            2  ==
              107  STORE_FAST            8  '@py_assert2'
              110  LOAD_FAST             8  '@py_assert2'
              113  POP_JUMP_IF_TRUE    226  'to 226'
              116  LOAD_GLOBAL           1  '@pytest_ar'
              119  LOAD_ATTR             2  '_call_reprcompare'
              122  LOAD_CONST               ('==',)
              125  LOAD_FAST             8  '@py_assert2'
              128  BUILD_TUPLE_1         1 
              131  LOAD_CONST               ('%(py1)s == %(py4)s',)
              134  LOAD_FAST             6  '@py_assert0'
              137  LOAD_FAST             7  '@py_assert3'
              140  BUILD_TUPLE_2         2 
              143  CALL_FUNCTION_4       4  None
              146  BUILD_MAP_2           2  None
              149  LOAD_GLOBAL           1  '@pytest_ar'
              152  LOAD_ATTR             3  '_saferepr'
              155  LOAD_FAST             6  '@py_assert0'
              158  CALL_FUNCTION_1       1  None
              161  LOAD_CONST               'py1'
              164  STORE_MAP        
              165  LOAD_GLOBAL           1  '@pytest_ar'
              168  LOAD_ATTR             3  '_saferepr'
              171  LOAD_FAST             7  '@py_assert3'
              174  CALL_FUNCTION_1       1  None
              177  LOAD_CONST               'py4'
              180  STORE_MAP        
              181  BINARY_MODULO    
              182  STORE_FAST            9  '@py_format5'
              185  LOAD_CONST               'assert %(py6)s'
              188  BUILD_MAP_1           1  None
              191  LOAD_FAST             9  '@py_format5'
              194  LOAD_CONST               'py6'
              197  STORE_MAP        
              198  BINARY_MODULO    
              199  STORE_FAST           10  '@py_format7'
              202  LOAD_GLOBAL           0  'AssertionError'
              205  LOAD_GLOBAL           1  '@pytest_ar'
              208  LOAD_ATTR             4  '_format_explanation'
              211  LOAD_FAST            10  '@py_format7'
              214  CALL_FUNCTION_1       1  None
              217  CALL_FUNCTION_1       1  None
              220  RAISE_VARARGS_1       1  None
              223  JUMP_FORWARD          0  'to 226'
            226_0  COME_FROM           223  '223'
              226  LOAD_CONST               None
              229  DUP_TOP          
              230  STORE_FAST            6  '@py_assert0'
              233  DUP_TOP          
              234  STORE_FAST            8  '@py_assert2'
              237  STORE_FAST            7  '@py_assert3'
              240  JUMP_BACK            72  'to 72'
              243  POP_BLOCK        
            244_0  COME_FROM            65  '65'
              244  JUMP_FORWARD          0  'to 247'
            247_0  COME_FROM            65  '65'

 L.  91       247  LOAD_FAST             4  'expected'
              250  POP_JUMP_IF_FALSE   572  'to 572'

 L.  92       253  SETUP_LOOP          316  'to 572'
              256  LOAD_FAST             4  'expected'
              259  GET_ITER         
              260  FOR_ITER            305  'to 568'
              263  STORE_FAST           11  'expect'

 L.  93       266  LOAD_FAST            11  'expect'
              269  LOAD_ATTR             6  'encode'
              272  STORE_FAST           12  '@py_assert1'
              275  LOAD_CONST               'UTF-8'
              278  STORE_FAST            7  '@py_assert3'
              281  LOAD_FAST            12  '@py_assert1'
              284  LOAD_FAST             7  '@py_assert3'
              287  CALL_FUNCTION_1       1  None
              290  STORE_FAST           13  '@py_assert5'
              293  LOAD_FAST            13  '@py_assert5'
              296  LOAD_FAST             1  'content'
              299  COMPARE_OP            6  in
              302  STORE_FAST           14  '@py_assert7'
              305  LOAD_FAST            14  '@py_assert7'
              308  POP_JUMP_IF_TRUE    547  'to 547'
              311  LOAD_GLOBAL           1  '@pytest_ar'
              314  LOAD_ATTR             2  '_call_reprcompare'
              317  LOAD_CONST               ('in',)
              320  LOAD_FAST            14  '@py_assert7'
              323  BUILD_TUPLE_1         1 
              326  LOAD_CONST               ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.encode\n}(%(py4)s)\n} in %(py8)s',)
              329  LOAD_FAST            13  '@py_assert5'
              332  LOAD_FAST             1  'content'
              335  BUILD_TUPLE_2         2 
              338  CALL_FUNCTION_4       4  None
              341  BUILD_MAP_5           5  None
              344  LOAD_CONST               'expect'
              347  LOAD_GLOBAL           7  '@py_builtins'
              350  LOAD_ATTR             8  'locals'
              353  CALL_FUNCTION_0       0  None
              356  COMPARE_OP            6  in
              359  POP_JUMP_IF_TRUE    377  'to 377'
              362  LOAD_GLOBAL           1  '@pytest_ar'
              365  LOAD_ATTR             9  '_should_repr_global_name'
              368  LOAD_FAST            11  'expect'
              371  CALL_FUNCTION_1       1  None
            374_0  COME_FROM           359  '359'
              374  POP_JUMP_IF_FALSE   392  'to 392'
              377  LOAD_GLOBAL           1  '@pytest_ar'
              380  LOAD_ATTR             3  '_saferepr'
              383  LOAD_FAST            11  'expect'
              386  CALL_FUNCTION_1       1  None
              389  JUMP_FORWARD          3  'to 395'
              392  LOAD_CONST               'expect'
            395_0  COME_FROM           389  '389'
              395  LOAD_CONST               'py0'
              398  STORE_MAP        
              399  LOAD_CONST               'content'
              402  LOAD_GLOBAL           7  '@py_builtins'
              405  LOAD_ATTR             8  'locals'
              408  CALL_FUNCTION_0       0  None
              411  COMPARE_OP            6  in
              414  POP_JUMP_IF_TRUE    432  'to 432'
              417  LOAD_GLOBAL           1  '@pytest_ar'
              420  LOAD_ATTR             9  '_should_repr_global_name'
              423  LOAD_FAST             1  'content'
              426  CALL_FUNCTION_1       1  None
            429_0  COME_FROM           414  '414'
              429  POP_JUMP_IF_FALSE   447  'to 447'
              432  LOAD_GLOBAL           1  '@pytest_ar'
              435  LOAD_ATTR             3  '_saferepr'
              438  LOAD_FAST             1  'content'
              441  CALL_FUNCTION_1       1  None
              444  JUMP_FORWARD          3  'to 450'
              447  LOAD_CONST               'content'
            450_0  COME_FROM           444  '444'
              450  LOAD_CONST               'py8'
              453  STORE_MAP        
              454  LOAD_GLOBAL           1  '@pytest_ar'
              457  LOAD_ATTR             3  '_saferepr'
              460  LOAD_FAST            12  '@py_assert1'
              463  CALL_FUNCTION_1       1  None
              466  LOAD_CONST               'py2'
              469  STORE_MAP        
              470  LOAD_GLOBAL           1  '@pytest_ar'
              473  LOAD_ATTR             3  '_saferepr'
              476  LOAD_FAST             7  '@py_assert3'
              479  CALL_FUNCTION_1       1  None
              482  LOAD_CONST               'py4'
              485  STORE_MAP        
              486  LOAD_GLOBAL           1  '@pytest_ar'
              489  LOAD_ATTR             3  '_saferepr'
              492  LOAD_FAST            13  '@py_assert5'
              495  CALL_FUNCTION_1       1  None
              498  LOAD_CONST               'py6'
              501  STORE_MAP        
              502  BINARY_MODULO    
              503  STORE_FAST           15  '@py_format9'
              506  LOAD_CONST               'assert %(py10)s'
              509  BUILD_MAP_1           1  None
              512  LOAD_FAST            15  '@py_format9'
              515  LOAD_CONST               'py10'
              518  STORE_MAP        
              519  BINARY_MODULO    
              520  STORE_FAST           16  '@py_format11'
              523  LOAD_GLOBAL           0  'AssertionError'
              526  LOAD_GLOBAL           1  '@pytest_ar'
              529  LOAD_ATTR             4  '_format_explanation'
              532  LOAD_FAST            16  '@py_format11'
              535  CALL_FUNCTION_1       1  None
              538  CALL_FUNCTION_1       1  None
              541  RAISE_VARARGS_1       1  None
              544  JUMP_FORWARD          0  'to 547'
            547_0  COME_FROM           544  '544'
              547  LOAD_CONST               None
              550  DUP_TOP          
              551  STORE_FAST           12  '@py_assert1'
              554  DUP_TOP          
              555  STORE_FAST            7  '@py_assert3'
              558  DUP_TOP          
              559  STORE_FAST           13  '@py_assert5'
              562  STORE_FAST           14  '@py_assert7'
              565  JUMP_BACK           260  'to 260'
              568  POP_BLOCK        
            569_0  COME_FROM           253  '253'
              569  JUMP_FORWARD          0  'to 572'
            572_0  COME_FROM           253  '253'
              572  LOAD_CONST               None
              575  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 572


if __name__ == '__main__':
    for test_data in TESTS:
        test = dict(EMPTY_TEST)
        test.update(test_data)
        full_url = base_url + test['url']
        print test['name']
        print '%s %s' % (test['method'], full_url)
        print