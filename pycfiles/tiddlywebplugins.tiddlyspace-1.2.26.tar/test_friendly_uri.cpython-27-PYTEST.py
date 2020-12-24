# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyspace/test/test_friendly_uri.py
# Compiled at: 2013-11-11 13:48:50
"""
Test so-called "friendly" uris: links to tiddlers
in the current space from the root.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from test.fixtures import make_test_env, make_fake_space
from wsgi_intercept import httplib2_intercept
import wsgi_intercept, httplib2, simplejson
from tiddlyweb.model.tiddler import Tiddler

def setup_module(module):
    make_test_env(module)
    make_fake_space(module.store, 'cdent')
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)
    wsgi_intercept.add_wsgi_intercept('cdent.0.0.0.0', 8080, app_fn)


def test_friendly--- This code section failed: ---

 L.  28         0  LOAD_GLOBAL           0  'Tiddler'
                3  LOAD_CONST               'HouseHold'
                6  LOAD_CONST               'cdent_public'
                9  CALL_FUNCTION_2       2  None
               12  STORE_FAST            0  'tiddler'

 L.  29        15  LOAD_GLOBAL           1  'store'
               18  LOAD_ATTR             2  'put'
               21  LOAD_FAST             0  'tiddler'
               24  CALL_FUNCTION_1       1  None
               27  POP_TOP          

 L.  30        28  LOAD_GLOBAL           3  'httplib2'
               31  LOAD_ATTR             4  'Http'
               34  CALL_FUNCTION_0       0  None
               37  STORE_FAST            1  'http'

 L.  31        40  LOAD_FAST             1  'http'
               43  LOAD_ATTR             5  'request'

 L.  32        46  LOAD_CONST               'http://cdent.0.0.0.0:8080/recipes/cdent_public/tiddlers/HouseHold'
               49  LOAD_CONST               'method'

 L.  33        52  LOAD_CONST               'GET'
               55  CALL_FUNCTION_257   257  None
               58  UNPACK_SEQUENCE_2     2 
               61  STORE_FAST            2  'response'
               64  STORE_FAST            3  'content_core'

 L.  35        67  LOAD_FAST             2  'response'
               70  LOAD_CONST               'status'
               73  BINARY_SUBSCR    
               74  LOAD_CONST               '200'
               77  COMPARE_OP            2  ==
               80  POP_JUMP_IF_TRUE     92  'to 92'
               83  LOAD_ASSERT              AssertionError
               86  LOAD_FAST             3  'content_core'
               89  RAISE_VARARGS_2       2  None

 L.  37        92  LOAD_FAST             1  'http'
               95  LOAD_ATTR             5  'request'

 L.  38        98  LOAD_CONST               'http://cdent.0.0.0.0:8080/HouseHold'
              101  LOAD_CONST               'method'

 L.  39       104  LOAD_CONST               'GET'
              107  CALL_FUNCTION_257   257  None
              110  UNPACK_SEQUENCE_2     2 
              113  STORE_FAST            2  'response'
              116  STORE_FAST            4  'content_friendly'

 L.  40       119  LOAD_FAST             2  'response'
              122  LOAD_CONST               'status'
              125  BINARY_SUBSCR    
              126  LOAD_CONST               '200'
              129  COMPARE_OP            2  ==
              132  POP_JUMP_IF_TRUE    144  'to 144'
              135  LOAD_ASSERT              AssertionError
              138  LOAD_FAST             4  'content_friendly'
              141  RAISE_VARARGS_2       2  None

 L.  41       144  LOAD_CONST               'text/html'
              147  STORE_FAST            5  '@py_assert0'
              150  LOAD_FAST             2  'response'
              153  LOAD_CONST               'content-type'
              156  BINARY_SUBSCR    
              157  STORE_FAST            6  '@py_assert3'
              160  LOAD_FAST             5  '@py_assert0'
              163  LOAD_FAST             6  '@py_assert3'
              166  COMPARE_OP            6  in
              169  STORE_FAST            7  '@py_assert2'
              172  LOAD_FAST             7  '@py_assert2'
              175  POP_JUMP_IF_TRUE    288  'to 288'
              178  LOAD_GLOBAL           7  '@pytest_ar'
              181  LOAD_ATTR             8  '_call_reprcompare'
              184  LOAD_CONST               ('in',)
              187  LOAD_FAST             7  '@py_assert2'
              190  BUILD_TUPLE_1         1 
              193  LOAD_CONST               ('%(py1)s in %(py4)s',)
              196  LOAD_FAST             5  '@py_assert0'
              199  LOAD_FAST             6  '@py_assert3'
              202  BUILD_TUPLE_2         2 
              205  CALL_FUNCTION_4       4  None
              208  BUILD_MAP_2           2  None
              211  LOAD_GLOBAL           7  '@pytest_ar'
              214  LOAD_ATTR             9  '_saferepr'
              217  LOAD_FAST             5  '@py_assert0'
              220  CALL_FUNCTION_1       1  None
              223  LOAD_CONST               'py1'
              226  STORE_MAP        
              227  LOAD_GLOBAL           7  '@pytest_ar'
              230  LOAD_ATTR             9  '_saferepr'
              233  LOAD_FAST             6  '@py_assert3'
              236  CALL_FUNCTION_1       1  None
              239  LOAD_CONST               'py4'
              242  STORE_MAP        
              243  BINARY_MODULO    
              244  STORE_FAST            8  '@py_format5'
              247  LOAD_CONST               'assert %(py6)s'
              250  BUILD_MAP_1           1  None
              253  LOAD_FAST             8  '@py_format5'
              256  LOAD_CONST               'py6'
              259  STORE_MAP        
              260  BINARY_MODULO    
              261  STORE_FAST            9  '@py_format7'
              264  LOAD_GLOBAL           6  'AssertionError'
              267  LOAD_GLOBAL           7  '@pytest_ar'
              270  LOAD_ATTR            10  '_format_explanation'
              273  LOAD_FAST             9  '@py_format7'
              276  CALL_FUNCTION_1       1  None
              279  CALL_FUNCTION_1       1  None
              282  RAISE_VARARGS_1       1  None
              285  JUMP_FORWARD          0  'to 288'
            288_0  COME_FROM           285  '285'
              288  LOAD_CONST               None
              291  DUP_TOP          
              292  STORE_FAST            5  '@py_assert0'
              295  DUP_TOP          
              296  STORE_FAST            7  '@py_assert2'
              299  STORE_FAST            6  '@py_assert3'

 L.  42       302  LOAD_CONST               'href="/#%5B%5BHouseHold%5D%5D"'
              305  STORE_FAST            5  '@py_assert0'
              308  LOAD_FAST             5  '@py_assert0'
              311  LOAD_FAST             4  'content_friendly'
              314  COMPARE_OP            6  in
              317  STORE_FAST            7  '@py_assert2'
              320  LOAD_FAST             7  '@py_assert2'
              323  POP_JUMP_IF_TRUE    475  'to 475'
              326  LOAD_GLOBAL           7  '@pytest_ar'
              329  LOAD_ATTR             8  '_call_reprcompare'
              332  LOAD_CONST               ('in',)
              335  LOAD_FAST             7  '@py_assert2'
              338  BUILD_TUPLE_1         1 
              341  LOAD_CONST               ('%(py1)s in %(py3)s',)
              344  LOAD_FAST             5  '@py_assert0'
              347  LOAD_FAST             4  'content_friendly'
              350  BUILD_TUPLE_2         2 
              353  CALL_FUNCTION_4       4  None
              356  BUILD_MAP_2           2  None
              359  LOAD_GLOBAL           7  '@pytest_ar'
              362  LOAD_ATTR             9  '_saferepr'
              365  LOAD_FAST             5  '@py_assert0'
              368  CALL_FUNCTION_1       1  None
              371  LOAD_CONST               'py1'
              374  STORE_MAP        
              375  LOAD_CONST               'content_friendly'
              378  LOAD_GLOBAL          12  '@py_builtins'
              381  LOAD_ATTR            13  'locals'
              384  CALL_FUNCTION_0       0  None
              387  COMPARE_OP            6  in
              390  POP_JUMP_IF_TRUE    408  'to 408'
              393  LOAD_GLOBAL           7  '@pytest_ar'
              396  LOAD_ATTR            14  '_should_repr_global_name'
              399  LOAD_FAST             4  'content_friendly'
              402  CALL_FUNCTION_1       1  None
            405_0  COME_FROM           390  '390'
              405  POP_JUMP_IF_FALSE   423  'to 423'
              408  LOAD_GLOBAL           7  '@pytest_ar'
              411  LOAD_ATTR             9  '_saferepr'
              414  LOAD_FAST             4  'content_friendly'
              417  CALL_FUNCTION_1       1  None
              420  JUMP_FORWARD          3  'to 426'
              423  LOAD_CONST               'content_friendly'
            426_0  COME_FROM           420  '420'
              426  LOAD_CONST               'py3'
              429  STORE_MAP        
              430  BINARY_MODULO    
              431  STORE_FAST           10  '@py_format4'
              434  LOAD_CONST               'assert %(py5)s'
              437  BUILD_MAP_1           1  None
              440  LOAD_FAST            10  '@py_format4'
              443  LOAD_CONST               'py5'
              446  STORE_MAP        
              447  BINARY_MODULO    
              448  STORE_FAST           11  '@py_format6'
              451  LOAD_GLOBAL           6  'AssertionError'
              454  LOAD_GLOBAL           7  '@pytest_ar'
              457  LOAD_ATTR            10  '_format_explanation'
              460  LOAD_FAST            11  '@py_format6'
              463  CALL_FUNCTION_1       1  None
              466  CALL_FUNCTION_1       1  None
              469  RAISE_VARARGS_1       1  None
              472  JUMP_FORWARD          0  'to 475'
            475_0  COME_FROM           472  '472'
              475  LOAD_CONST               None
              478  DUP_TOP          
              479  STORE_FAST            5  '@py_assert0'
              482  STORE_FAST            7  '@py_assert2'

 L.  44       485  LOAD_FAST             1  'http'
              488  LOAD_ATTR             5  'request'

 L.  45       491  LOAD_CONST               'http://0.0.0.0:8080/HouseHold'
              494  LOAD_CONST               'method'

 L.  46       497  LOAD_CONST               'GET'
              500  CALL_FUNCTION_257   257  None
              503  UNPACK_SEQUENCE_2     2 
              506  STORE_FAST            2  'response'
              509  STORE_FAST            4  'content_friendly'

 L.  47       512  LOAD_FAST             2  'response'
              515  LOAD_CONST               'status'
              518  BINARY_SUBSCR    
              519  LOAD_CONST               '404'
              522  COMPARE_OP            2  ==
              525  POP_JUMP_IF_TRUE    537  'to 537'
              528  LOAD_ASSERT              AssertionError
              531  LOAD_FAST             4  'content_friendly'
              534  RAISE_VARARGS_2       2  None
              537  LOAD_CONST               None
              540  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 537


def test_friendly_encoded():
    tiddler = Tiddler('House Hold', 'cdent_public')
    store.put(tiddler)
    http = httplib2.Http()
    response, content_friendly = http.request('http://cdent.0.0.0.0:8080/House%20Hold', method='GET')
    if not response['status'] == '200':
        raise AssertionError, content_friendly
        @py_assert0 = 'text/html'
        @py_assert3 = response['content-type']
        @py_assert2 = @py_assert0 in @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = 'href="/#%5B%5BHouse%20Hold%5D%5D"'
        @py_assert2 = @py_assert0 in content_friendly
        @py_format4 = @py_assert2 or @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content_friendly)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content_friendly) if 'content_friendly' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content_friendly) else 'content_friendly'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_markdown_support():
    tiddler = Tiddler('Markdown Test', 'cdent_public')
    tiddler.text = '_No Way_'
    tiddler.type = 'text/x-markdown'
    store.put(tiddler)
    http = httplib2.Http()
    response, content = http.request('http://cdent.0.0.0.0:8080/Markdown%20Test', method='GET')
    if not response['status'] == '200':
        raise AssertionError, content
        @py_assert0 = 'text/html'
        @py_assert3 = response['content-type']
        @py_assert2 = @py_assert0 in @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = '<em>No Way</em>'
        @py_assert2 = @py_assert0 in content
        @py_format4 = @py_assert2 or @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_tiddlywikitext_support():
    tiddler = Tiddler('TiddlyWiki Test', 'cdent_public')
    tiddler.text = '//No Way//'
    store.put(tiddler)
    http = httplib2.Http()
    response, content = http.request('http://cdent.0.0.0.0:8080/TiddlyWiki%20Test', method='GET')
    if not response['status'] == '200':
        raise AssertionError, content
        @py_assert0 = 'text/html'
        @py_assert3 = response['content-type']
        @py_assert2 = @py_assert0 in @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = '<i class="">No Way</i>'
        @py_assert2 = @py_assert0 in content
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        tiddler = Tiddler('TiddlyWiki Test', 'cdent_public')
        tiddler.text = '//No Way//'
        tiddler.type = 'text/x-tiddlywiki'
        store.put(tiddler)
        http = httplib2.Http()
        response, content = http.request('http://cdent.0.0.0.0:8080/TiddlyWiki%20Test', method='GET')
        if not response['status'] == '200':
            raise AssertionError, content
            @py_assert0 = 'text/html'
            @py_assert3 = response['content-type']
            @py_assert2 = @py_assert0 in @py_assert3
            @py_format5 = @py_assert2 or @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = '<i class="">No Way</i>'
        @py_assert2 = @py_assert0 in content
        @py_format4 = @py_assert2 or @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_root_tiddlers--- This code section failed: ---

 L.  99         0  LOAD_GLOBAL           0  'httplib2'
                3  LOAD_ATTR             1  'Http'
                6  CALL_FUNCTION_0       0  None
                9  STORE_FAST            0  'http'

 L. 100        12  LOAD_FAST             0  'http'
               15  LOAD_ATTR             2  'request'

 L. 101        18  LOAD_CONST               'http://cdent.0.0.0.0:8080/tiddlers.wiki'
               21  LOAD_CONST               'method'

 L. 102        24  LOAD_CONST               'GET'
               27  CALL_FUNCTION_257   257  None
               30  UNPACK_SEQUENCE_2     2 
               33  STORE_FAST            1  'response'
               36  STORE_FAST            2  'content'

 L. 103        39  LOAD_FAST             1  'response'
               42  LOAD_CONST               'status'
               45  BINARY_SUBSCR    
               46  LOAD_CONST               '200'
               49  COMPARE_OP            2  ==
               52  POP_JUMP_IF_TRUE     64  'to 64'
               55  LOAD_ASSERT              AssertionError
               58  LOAD_FAST             2  'content'
               61  RAISE_VARARGS_2       2  None

 L. 104        64  LOAD_CONST               'Jeremy Ruston'
               67  STORE_FAST            3  '@py_assert0'
               70  LOAD_FAST             3  '@py_assert0'
               73  LOAD_FAST             2  'content'
               76  COMPARE_OP            6  in
               79  STORE_FAST            4  '@py_assert2'
               82  LOAD_FAST             4  '@py_assert2'
               85  POP_JUMP_IF_TRUE    237  'to 237'
               88  LOAD_GLOBAL           4  '@pytest_ar'
               91  LOAD_ATTR             5  '_call_reprcompare'
               94  LOAD_CONST               ('in',)
               97  LOAD_FAST             4  '@py_assert2'
              100  BUILD_TUPLE_1         1 
              103  LOAD_CONST               ('%(py1)s in %(py3)s',)
              106  LOAD_FAST             3  '@py_assert0'
              109  LOAD_FAST             2  'content'
              112  BUILD_TUPLE_2         2 
              115  CALL_FUNCTION_4       4  None
              118  BUILD_MAP_2           2  None
              121  LOAD_GLOBAL           4  '@pytest_ar'
              124  LOAD_ATTR             6  '_saferepr'
              127  LOAD_FAST             3  '@py_assert0'
              130  CALL_FUNCTION_1       1  None
              133  LOAD_CONST               'py1'
              136  STORE_MAP        
              137  LOAD_CONST               'content'
              140  LOAD_GLOBAL           7  '@py_builtins'
              143  LOAD_ATTR             8  'locals'
              146  CALL_FUNCTION_0       0  None
              149  COMPARE_OP            6  in
              152  POP_JUMP_IF_TRUE    170  'to 170'
              155  LOAD_GLOBAL           4  '@pytest_ar'
              158  LOAD_ATTR             9  '_should_repr_global_name'
              161  LOAD_FAST             2  'content'
              164  CALL_FUNCTION_1       1  None
            167_0  COME_FROM           152  '152'
              167  POP_JUMP_IF_FALSE   185  'to 185'
              170  LOAD_GLOBAL           4  '@pytest_ar'
              173  LOAD_ATTR             6  '_saferepr'
              176  LOAD_FAST             2  'content'
              179  CALL_FUNCTION_1       1  None
              182  JUMP_FORWARD          3  'to 188'
              185  LOAD_CONST               'content'
            188_0  COME_FROM           182  '182'
              188  LOAD_CONST               'py3'
              191  STORE_MAP        
              192  BINARY_MODULO    
              193  STORE_FAST            5  '@py_format4'
              196  LOAD_CONST               'assert %(py5)s'
              199  BUILD_MAP_1           1  None
              202  LOAD_FAST             5  '@py_format4'
              205  LOAD_CONST               'py5'
              208  STORE_MAP        
              209  BINARY_MODULO    
              210  STORE_FAST            6  '@py_format6'
              213  LOAD_GLOBAL           3  'AssertionError'
              216  LOAD_GLOBAL           4  '@pytest_ar'
              219  LOAD_ATTR            10  '_format_explanation'
              222  LOAD_FAST             6  '@py_format6'
              225  CALL_FUNCTION_1       1  None
              228  CALL_FUNCTION_1       1  None
              231  RAISE_VARARGS_1       1  None
              234  JUMP_FORWARD          0  'to 237'
            237_0  COME_FROM           234  '234'
              237  LOAD_CONST               None
              240  DUP_TOP          
              241  STORE_FAST            3  '@py_assert0'
              244  STORE_FAST            4  '@py_assert2'

 L. 106       247  LOAD_FAST             0  'http'
              250  LOAD_ATTR             2  'request'

 L. 107       253  LOAD_CONST               'http://cdent.0.0.0.0:8080/tiddlers'
              256  LOAD_CONST               'method'

 L. 108       259  LOAD_CONST               'GET'
              262  CALL_FUNCTION_257   257  None
              265  UNPACK_SEQUENCE_2     2 
              268  STORE_FAST            1  'response'
              271  STORE_FAST            2  'content'

 L. 109       274  LOAD_FAST             1  'response'
              277  LOAD_CONST               'status'
              280  BINARY_SUBSCR    
              281  LOAD_CONST               '200'
              284  COMPARE_OP            2  ==
              287  POP_JUMP_IF_TRUE    299  'to 299'
              290  LOAD_ASSERT              AssertionError
              293  LOAD_FAST             2  'content'
              296  RAISE_VARARGS_2       2  None

 L. 110       299  LOAD_CONST               '/HouseHold">HouseHold'
              302  LOAD_FAST             2  'content'
              305  COMPARE_OP            6  in
              308  POP_JUMP_IF_TRUE    320  'to 320'
              311  LOAD_ASSERT              AssertionError
              314  LOAD_FAST             2  'content'
              317  RAISE_VARARGS_2       2  None

 L. 111       320  LOAD_CONST               '/BinaryTiddlersPlugin">BinaryTiddlersPlugin'
              323  STORE_FAST            3  '@py_assert0'
              326  LOAD_FAST             3  '@py_assert0'
              329  LOAD_FAST             2  'content'
              332  COMPARE_OP            7  not-in
              335  STORE_FAST            4  '@py_assert2'
              338  LOAD_FAST             4  '@py_assert2'
              341  POP_JUMP_IF_TRUE    493  'to 493'
              344  LOAD_GLOBAL           4  '@pytest_ar'
              347  LOAD_ATTR             5  '_call_reprcompare'
              350  LOAD_CONST               ('not in',)
              353  LOAD_FAST             4  '@py_assert2'
              356  BUILD_TUPLE_1         1 
              359  LOAD_CONST               ('%(py1)s not in %(py3)s',)
              362  LOAD_FAST             3  '@py_assert0'
              365  LOAD_FAST             2  'content'
              368  BUILD_TUPLE_2         2 
              371  CALL_FUNCTION_4       4  None
              374  BUILD_MAP_2           2  None
              377  LOAD_GLOBAL           4  '@pytest_ar'
              380  LOAD_ATTR             6  '_saferepr'
              383  LOAD_FAST             3  '@py_assert0'
              386  CALL_FUNCTION_1       1  None
              389  LOAD_CONST               'py1'
              392  STORE_MAP        
              393  LOAD_CONST               'content'
              396  LOAD_GLOBAL           7  '@py_builtins'
              399  LOAD_ATTR             8  'locals'
              402  CALL_FUNCTION_0       0  None
              405  COMPARE_OP            6  in
              408  POP_JUMP_IF_TRUE    426  'to 426'
              411  LOAD_GLOBAL           4  '@pytest_ar'
              414  LOAD_ATTR             9  '_should_repr_global_name'
              417  LOAD_FAST             2  'content'
              420  CALL_FUNCTION_1       1  None
            423_0  COME_FROM           408  '408'
              423  POP_JUMP_IF_FALSE   441  'to 441'
              426  LOAD_GLOBAL           4  '@pytest_ar'
              429  LOAD_ATTR             6  '_saferepr'
              432  LOAD_FAST             2  'content'
              435  CALL_FUNCTION_1       1  None
              438  JUMP_FORWARD          3  'to 444'
              441  LOAD_CONST               'content'
            444_0  COME_FROM           438  '438'
              444  LOAD_CONST               'py3'
              447  STORE_MAP        
              448  BINARY_MODULO    
              449  STORE_FAST            5  '@py_format4'
              452  LOAD_CONST               'assert %(py5)s'
              455  BUILD_MAP_1           1  None
              458  LOAD_FAST             5  '@py_format4'
              461  LOAD_CONST               'py5'
              464  STORE_MAP        
              465  BINARY_MODULO    
              466  STORE_FAST            6  '@py_format6'
              469  LOAD_GLOBAL           3  'AssertionError'
              472  LOAD_GLOBAL           4  '@pytest_ar'
              475  LOAD_ATTR            10  '_format_explanation'
              478  LOAD_FAST             6  '@py_format6'
              481  CALL_FUNCTION_1       1  None
              484  CALL_FUNCTION_1       1  None
              487  RAISE_VARARGS_1       1  None
              490  JUMP_FORWARD          0  'to 493'
            493_0  COME_FROM           490  '490'
              493  LOAD_CONST               None
              496  DUP_TOP          
              497  STORE_FAST            3  '@py_assert0'
              500  STORE_FAST            4  '@py_assert2'
              503  LOAD_CONST               None
              506  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 503


def test_root_tiddlers_filter--- This code section failed: ---

 L. 124         0  LOAD_GLOBAL           0  'httplib2'
                3  LOAD_ATTR             1  'Http'
                6  CALL_FUNCTION_0       0  None
                9  STORE_FAST            0  'http'

 L. 126        12  LOAD_FAST             0  'http'
               15  LOAD_ATTR             2  'request'

 L. 127        18  LOAD_CONST               'http://cdent.0.0.0.0:8080/tiddlers.json'
               21  LOAD_CONST               'method'

 L. 128        24  LOAD_CONST               'GET'
               27  CALL_FUNCTION_257   257  None
               30  UNPACK_SEQUENCE_2     2 
               33  STORE_FAST            1  'response'
               36  STORE_FAST            2  'content'

 L. 129        39  LOAD_FAST             1  'response'
               42  LOAD_CONST               'status'
               45  BINARY_SUBSCR    
               46  LOAD_CONST               '200'
               49  COMPARE_OP            2  ==
               52  POP_JUMP_IF_TRUE     64  'to 64'
               55  LOAD_ASSERT              AssertionError
               58  LOAD_FAST             2  'content'
               61  RAISE_VARARGS_2       2  None

 L. 130        64  LOAD_GLOBAL           4  'simplejson'
               67  LOAD_ATTR             5  'loads'
               70  LOAD_FAST             2  'content'
               73  CALL_FUNCTION_1       1  None
               76  STORE_FAST            3  'tiddlers'

 L. 131        79  LOAD_GLOBAL           6  'len'
               82  LOAD_FAST             3  'tiddlers'
               85  CALL_FUNCTION_1       1  None
               88  LOAD_CONST               6
               91  COMPARE_OP            2  ==
               94  POP_JUMP_IF_TRUE    106  'to 106'
               97  LOAD_ASSERT              AssertionError
              100  LOAD_FAST             3  'tiddlers'
              103  RAISE_VARARGS_2       2  None

 L. 133       106  LOAD_FAST             0  'http'
              109  LOAD_ATTR             2  'request'

 L. 134       112  LOAD_CONST               'http://cdent.0.0.0.0:8080/tiddlers.json?limit=4'
              115  LOAD_CONST               'method'

 L. 135       118  LOAD_CONST               'GET'
              121  CALL_FUNCTION_257   257  None
              124  UNPACK_SEQUENCE_2     2 
              127  STORE_FAST            1  'response'
              130  STORE_FAST            2  'content'

 L. 136       133  LOAD_FAST             1  'response'
              136  LOAD_CONST               'status'
              139  BINARY_SUBSCR    
              140  LOAD_CONST               '200'
              143  COMPARE_OP            2  ==
              146  POP_JUMP_IF_TRUE    158  'to 158'
              149  LOAD_ASSERT              AssertionError
              152  LOAD_FAST             2  'content'
              155  RAISE_VARARGS_2       2  None

 L. 137       158  LOAD_GLOBAL           4  'simplejson'
              161  LOAD_ATTR             5  'loads'
              164  LOAD_FAST             2  'content'
              167  CALL_FUNCTION_1       1  None
              170  STORE_FAST            3  'tiddlers'

 L. 138       173  LOAD_GLOBAL           6  'len'
              176  LOAD_FAST             3  'tiddlers'
              179  CALL_FUNCTION_1       1  None
              182  LOAD_CONST               4
              185  COMPARE_OP            2  ==
              188  POP_JUMP_IF_TRUE    200  'to 200'
              191  LOAD_ASSERT              AssertionError
              194  LOAD_FAST             3  'tiddlers'
              197  RAISE_VARARGS_2       2  None

 L. 140       200  LOAD_FAST             0  'http'
              203  LOAD_ATTR             2  'request'

 L. 141       206  LOAD_CONST               'http://cdent.0.0.0.0:8080/tiddlers.json'
              209  LOAD_CONST               'method'

 L. 142       212  LOAD_CONST               'GET'
              215  CALL_FUNCTION_257   257  None
              218  UNPACK_SEQUENCE_2     2 
              221  STORE_FAST            1  'response'
              224  STORE_FAST            2  'content'

 L. 143       227  LOAD_FAST             1  'response'
              230  LOAD_CONST               'status'
              233  BINARY_SUBSCR    
              234  LOAD_CONST               '200'
              237  COMPARE_OP            2  ==
              240  POP_JUMP_IF_TRUE    252  'to 252'
              243  LOAD_ASSERT              AssertionError
              246  LOAD_FAST             2  'content'
              249  RAISE_VARARGS_2       2  None

 L. 144       252  LOAD_GLOBAL           4  'simplejson'
              255  LOAD_ATTR             5  'loads'
              258  LOAD_FAST             2  'content'
              261  CALL_FUNCTION_1       1  None
              264  STORE_FAST            3  'tiddlers'

 L. 145       267  LOAD_FAST             3  'tiddlers'
              270  LOAD_CONST               -1
              273  BINARY_SUBSCR    
              274  STORE_FAST            4  'last_tiddler'

 L. 147       277  LOAD_FAST             0  'http'
              280  LOAD_ATTR             2  'request'

 L. 148       283  LOAD_CONST               'http://cdent.0.0.0.0:8080/tiddlers.json?sort=modified'
              286  LOAD_CONST               'method'

 L. 149       289  LOAD_CONST               'GET'
              292  CALL_FUNCTION_257   257  None
              295  UNPACK_SEQUENCE_2     2 
              298  STORE_FAST            1  'response'
              301  STORE_FAST            2  'content'

 L. 150       304  LOAD_FAST             1  'response'
              307  LOAD_CONST               'status'
              310  BINARY_SUBSCR    
              311  LOAD_CONST               '200'
              314  COMPARE_OP            2  ==
              317  POP_JUMP_IF_TRUE    329  'to 329'
              320  LOAD_ASSERT              AssertionError
              323  LOAD_FAST             2  'content'
              326  RAISE_VARARGS_2       2  None

 L. 151       329  LOAD_GLOBAL           4  'simplejson'
              332  LOAD_ATTR             5  'loads'
              335  LOAD_FAST             2  'content'
              338  CALL_FUNCTION_1       1  None
              341  STORE_FAST            3  'tiddlers'

 L. 152       344  LOAD_FAST             3  'tiddlers'
              347  LOAD_CONST               0
              350  BINARY_SUBSCR    
              351  STORE_FAST            5  'first_tiddler'

 L. 154       354  LOAD_FAST             5  'first_tiddler'
              357  LOAD_CONST               'title'
              360  BINARY_SUBSCR    
              361  STORE_FAST            6  '@py_assert0'
              364  LOAD_FAST             4  'last_tiddler'
              367  LOAD_CONST               'title'
              370  BINARY_SUBSCR    
              371  STORE_FAST            7  '@py_assert3'
              374  LOAD_FAST             6  '@py_assert0'
              377  LOAD_FAST             7  '@py_assert3'
              380  COMPARE_OP            2  ==
              383  STORE_FAST            8  '@py_assert2'
              386  LOAD_FAST             8  '@py_assert2'
              389  POP_JUMP_IF_TRUE    502  'to 502'
              392  LOAD_GLOBAL           7  '@pytest_ar'
              395  LOAD_ATTR             8  '_call_reprcompare'
              398  LOAD_CONST               ('==',)
              401  LOAD_FAST             8  '@py_assert2'
              404  BUILD_TUPLE_1         1 
              407  LOAD_CONST               ('%(py1)s == %(py4)s',)
              410  LOAD_FAST             6  '@py_assert0'
              413  LOAD_FAST             7  '@py_assert3'
              416  BUILD_TUPLE_2         2 
              419  CALL_FUNCTION_4       4  None
              422  BUILD_MAP_2           2  None
              425  LOAD_GLOBAL           7  '@pytest_ar'
              428  LOAD_ATTR             9  '_saferepr'
              431  LOAD_FAST             6  '@py_assert0'
              434  CALL_FUNCTION_1       1  None
              437  LOAD_CONST               'py1'
              440  STORE_MAP        
              441  LOAD_GLOBAL           7  '@pytest_ar'
              444  LOAD_ATTR             9  '_saferepr'
              447  LOAD_FAST             7  '@py_assert3'
              450  CALL_FUNCTION_1       1  None
              453  LOAD_CONST               'py4'
              456  STORE_MAP        
              457  BINARY_MODULO    
              458  STORE_FAST            9  '@py_format5'
              461  LOAD_CONST               'assert %(py6)s'
              464  BUILD_MAP_1           1  None
              467  LOAD_FAST             9  '@py_format5'
              470  LOAD_CONST               'py6'
              473  STORE_MAP        
              474  BINARY_MODULO    
              475  STORE_FAST           10  '@py_format7'
              478  LOAD_GLOBAL           3  'AssertionError'
              481  LOAD_GLOBAL           7  '@pytest_ar'
              484  LOAD_ATTR            10  '_format_explanation'
              487  LOAD_FAST            10  '@py_format7'
              490  CALL_FUNCTION_1       1  None
              493  CALL_FUNCTION_1       1  None
              496  RAISE_VARARGS_1       1  None
              499  JUMP_FORWARD          0  'to 502'
            502_0  COME_FROM           499  '499'
              502  LOAD_CONST               None
              505  DUP_TOP          
              506  STORE_FAST            6  '@py_assert0'
              509  DUP_TOP          
              510  STORE_FAST            8  '@py_assert2'
              513  STORE_FAST            7  '@py_assert3'
              516  LOAD_CONST               None
              519  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 516


def test_open_graph():
    """
    Make sure the open graph stuff is present in the right places.
    """
    http = httplib2.Http()
    tiddler = Tiddler('Open Graph', 'cdent_public')
    tiddler.text = 'I am the text'
    tiddler.modifier = 'cdent'
    tiddler.tags = ['alpha', 'beta', 'cat dog']
    store.put(tiddler)
    response, content = http.request('http://cdent.0.0.0.0:8080/Open%20Graph')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = '<html prefix="og: http://ogp.me/ns#'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<meta property="og:title" content="Open Graph" />'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<meta property="og:url" content="http://cdent.0.0.0.0:8080/Open%20Graph" />'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<meta property="og:image" content="http://cdent.0.0.0.0:8080/SiteIcon" />'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<meta property="article:tag" content="alpha" />'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<meta property="article:modified_time"'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<meta property="article:published_time"'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<meta property="article:author"'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<meta property="og:site_name" content="TiddlySpace" />'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = http.request('http://cdent.0.0.0.0:8080/bags/cdent_public/tiddlers/Open%20Graph')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = '<html>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<html prefix>'
    @py_assert2 = @py_assert0 not in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    tiddler = Tiddler('ServerSettings', 'cdent_public')
    tiddler.text = 'htmltemplate: clean1\n'
    store.put(tiddler)
    response, content = http.request('http://cdent.0.0.0.0:8080/Open%20Graph')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = '<html prefix="og: http://ogp.me/ns#'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return