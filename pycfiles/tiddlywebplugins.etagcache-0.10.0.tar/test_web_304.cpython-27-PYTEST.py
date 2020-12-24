# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.etagcache/test/test_web_304.py
# Compiled at: 2013-06-04 09:10:34
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, httplib2
from wsgi_intercept import httplib2_intercept
import wsgi_intercept
from tiddlyweb.web.serve import load_app
from tiddlyweb.config import config
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler
from tiddlywebplugins.utils import get_store
import random, shutil, string, threading
RELEVANT_HEADERS = [
 'cache-control', 'etag', 'vary', 'last-modified']

def setup_module(module):
    try:
        shutil.rmtree('store')
    except OSError:
        pass

    app = load_app()

    def app_fn():
        return app

    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('our_test_domain', 8001, app_fn)
    module.store = get_store(config)
    module.http = httplib2.Http()


def _random_name(length=5):
    return ('').join(random.choice(string.lowercase) for i in range(length))


def test_single_tiddler():
    bag = Bag(_random_name())
    store.put(bag)
    tiddler = Tiddler(_random_name(), bag.name)
    tiddler.text = _random_name(10)
    store.put(tiddler)
    uri = 'http://our_test_domain:8001/bags/%s/tiddlers/%s' % (
     tiddler.bag, tiddler.title)
    _get_entity(uri)


class RequestThread(threading.Thread):
    """
    Simple thread to test data concurrency.
    """

    def __init__(self, uri, pause=30):
        threading.Thread.__init__(self)
        self.uri = uri
        self.pause = pause
        self.response = None
        self.content = None
        return

    def run(self):
        response, content = http.request(self.uri)
        self.response = response
        self.content = content


def test_thread_safety():
    """
    Non asserting test to exercise threads, demonstrating
    confusion over who has written headers and status information.
    This experiment led to the creation of the Holder object,
    so leaving in for reference.
    """
    bag = Bag(_random_name())
    store.put(bag)
    threads = []
    for i in range(10):
        tiddler = Tiddler(_random_name(), bag.name)
        tiddler.text = _random_name(10)
        store.put(tiddler)
        uri = 'http://our_test_domain:8001/bags/%s/tiddlers/%s' % (
         tiddler.bag, tiddler.title)
        thread = RequestThread(uri)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def _get_entity--- This code section failed: ---

 L. 104         0  LOAD_GLOBAL           0  'http'
                3  LOAD_ATTR             1  'request'
                6  LOAD_FAST             0  'uri'
                9  LOAD_CONST               'method'
               12  LOAD_CONST               'GET'
               15  CALL_FUNCTION_257   257  None
               18  UNPACK_SEQUENCE_2     2 
               21  STORE_FAST            1  'response'
               24  STORE_FAST            2  'content'

 L. 106        27  LOAD_FAST             1  'response'
               30  LOAD_CONST               'status'
               33  BINARY_SUBSCR    
               34  LOAD_CONST               '200'
               37  COMPARE_OP            2  ==
               40  POP_JUMP_IF_TRUE     52  'to 52'
               43  LOAD_ASSERT              AssertionError
               46  LOAD_FAST             2  'content'
               49  RAISE_VARARGS_2       2  None

 L. 107        52  LOAD_FAST             1  'response'
               55  STORE_FAST            3  'response_200'

 L. 109        58  LOAD_FAST             1  'response'
               61  LOAD_CONST               'etag'
               64  BINARY_SUBSCR    
               65  STORE_FAST            4  'etag'

 L. 111        68  LOAD_GLOBAL           0  'http'
               71  LOAD_ATTR             1  'request'
               74  LOAD_FAST             0  'uri'
               77  LOAD_CONST               'method'
               80  LOAD_CONST               'GET'
               83  LOAD_CONST               'headers'

 L. 112        86  BUILD_MAP_1           1  None
               89  LOAD_FAST             4  'etag'
               92  LOAD_CONST               'If-None-Match'
               95  STORE_MAP        
               96  CALL_FUNCTION_513   513  None
               99  UNPACK_SEQUENCE_2     2 
              102  STORE_FAST            1  'response'
              105  STORE_FAST            2  'content'

 L. 114       108  LOAD_FAST             1  'response'
              111  LOAD_CONST               'status'
              114  BINARY_SUBSCR    
              115  LOAD_CONST               '304'
              118  COMPARE_OP            2  ==
              121  POP_JUMP_IF_TRUE    133  'to 133'
              124  LOAD_ASSERT              AssertionError
              127  LOAD_FAST             2  'content'
              130  RAISE_VARARGS_2       2  None

 L. 115       133  LOAD_FAST             1  'response'
              136  STORE_FAST            5  'response_304'

 L. 117       139  SETUP_LOOP          403  'to 545'
              142  LOAD_GLOBAL           3  'RELEVANT_HEADERS'
              145  GET_ITER         
              146  FOR_ITER            395  'to 544'
              149  STORE_FAST            6  'header'

 L. 118       152  LOAD_FAST             6  'header'
              155  LOAD_FAST             3  'response_200'
              158  COMPARE_OP            6  in
              161  POP_JUMP_IF_FALSE   146  'to 146'

 L. 119       164  LOAD_FAST             6  'header'
              167  LOAD_FAST             5  'response_304'
              170  COMPARE_OP            6  in
              173  STORE_FAST            7  '@py_assert1'
              176  LOAD_FAST             7  '@py_assert1'
              179  POP_JUMP_IF_TRUE    370  'to 370'
              182  LOAD_GLOBAL           4  '@pytest_ar'
              185  LOAD_ATTR             5  '_call_reprcompare'
              188  LOAD_CONST               ('in',)
              191  LOAD_FAST             7  '@py_assert1'
              194  BUILD_TUPLE_1         1 
              197  LOAD_CONST               ('%(py0)s in %(py2)s',)
              200  LOAD_FAST             6  'header'
              203  LOAD_FAST             5  'response_304'
              206  BUILD_TUPLE_2         2 
              209  CALL_FUNCTION_4       4  None
              212  BUILD_MAP_2           2  None
              215  LOAD_CONST               'header'
              218  LOAD_GLOBAL           6  '@py_builtins'
              221  LOAD_ATTR             7  'locals'
              224  CALL_FUNCTION_0       0  None
              227  COMPARE_OP            6  in
              230  POP_JUMP_IF_TRUE    248  'to 248'
              233  LOAD_GLOBAL           4  '@pytest_ar'
              236  LOAD_ATTR             8  '_should_repr_global_name'
              239  LOAD_FAST             6  'header'
              242  CALL_FUNCTION_1       1  None
            245_0  COME_FROM           230  '230'
              245  POP_JUMP_IF_FALSE   263  'to 263'
              248  LOAD_GLOBAL           4  '@pytest_ar'
              251  LOAD_ATTR             9  '_saferepr'
              254  LOAD_FAST             6  'header'
              257  CALL_FUNCTION_1       1  None
              260  JUMP_FORWARD          3  'to 266'
              263  LOAD_CONST               'header'
            266_0  COME_FROM           260  '260'
              266  LOAD_CONST               'py0'
              269  STORE_MAP        
              270  LOAD_CONST               'response_304'
              273  LOAD_GLOBAL           6  '@py_builtins'
              276  LOAD_ATTR             7  'locals'
              279  CALL_FUNCTION_0       0  None
              282  COMPARE_OP            6  in
              285  POP_JUMP_IF_TRUE    303  'to 303'
              288  LOAD_GLOBAL           4  '@pytest_ar'
              291  LOAD_ATTR             8  '_should_repr_global_name'
              294  LOAD_FAST             5  'response_304'
              297  CALL_FUNCTION_1       1  None
            300_0  COME_FROM           285  '285'
              300  POP_JUMP_IF_FALSE   318  'to 318'
              303  LOAD_GLOBAL           4  '@pytest_ar'
              306  LOAD_ATTR             9  '_saferepr'
              309  LOAD_FAST             5  'response_304'
              312  CALL_FUNCTION_1       1  None
              315  JUMP_FORWARD          3  'to 321'
              318  LOAD_CONST               'response_304'
            321_0  COME_FROM           315  '315'
              321  LOAD_CONST               'py2'
              324  STORE_MAP        
              325  BINARY_MODULO    
              326  STORE_FAST            8  '@py_format3'
              329  LOAD_CONST               'assert %(py4)s'
              332  BUILD_MAP_1           1  None
              335  LOAD_FAST             8  '@py_format3'
              338  LOAD_CONST               'py4'
              341  STORE_MAP        
              342  BINARY_MODULO    
              343  STORE_FAST            9  '@py_format5'
              346  LOAD_GLOBAL           2  'AssertionError'
              349  LOAD_GLOBAL           4  '@pytest_ar'
              352  LOAD_ATTR            10  '_format_explanation'
              355  LOAD_FAST             9  '@py_format5'
              358  CALL_FUNCTION_1       1  None
              361  CALL_FUNCTION_1       1  None
              364  RAISE_VARARGS_1       1  None
              367  JUMP_FORWARD          0  'to 370'
            370_0  COME_FROM           367  '367'
              370  LOAD_CONST               None
              373  STORE_FAST            7  '@py_assert1'

 L. 120       376  LOAD_FAST             3  'response_200'
              379  LOAD_FAST             6  'header'
              382  BINARY_SUBSCR    
              383  STORE_FAST           10  '@py_assert0'
              386  LOAD_FAST             5  'response_304'
              389  LOAD_FAST             6  'header'
              392  BINARY_SUBSCR    
              393  STORE_FAST           11  '@py_assert3'
              396  LOAD_FAST            10  '@py_assert0'
              399  LOAD_FAST            11  '@py_assert3'
              402  COMPARE_OP            2  ==
              405  STORE_FAST           12  '@py_assert2'
              408  LOAD_FAST            12  '@py_assert2'
              411  POP_JUMP_IF_TRUE    524  'to 524'
              414  LOAD_GLOBAL           4  '@pytest_ar'
              417  LOAD_ATTR             5  '_call_reprcompare'
              420  LOAD_CONST               ('==',)
              423  LOAD_FAST            12  '@py_assert2'
              426  BUILD_TUPLE_1         1 
              429  LOAD_CONST               ('%(py1)s == %(py4)s',)
              432  LOAD_FAST            10  '@py_assert0'
              435  LOAD_FAST            11  '@py_assert3'
              438  BUILD_TUPLE_2         2 
              441  CALL_FUNCTION_4       4  None
              444  BUILD_MAP_2           2  None
              447  LOAD_GLOBAL           4  '@pytest_ar'
              450  LOAD_ATTR             9  '_saferepr'
              453  LOAD_FAST            10  '@py_assert0'
              456  CALL_FUNCTION_1       1  None
              459  LOAD_CONST               'py1'
              462  STORE_MAP        
              463  LOAD_GLOBAL           4  '@pytest_ar'
              466  LOAD_ATTR             9  '_saferepr'
              469  LOAD_FAST            11  '@py_assert3'
              472  CALL_FUNCTION_1       1  None
              475  LOAD_CONST               'py4'
              478  STORE_MAP        
              479  BINARY_MODULO    
              480  STORE_FAST            9  '@py_format5'
              483  LOAD_CONST               'assert %(py6)s'
              486  BUILD_MAP_1           1  None
              489  LOAD_FAST             9  '@py_format5'
              492  LOAD_CONST               'py6'
              495  STORE_MAP        
              496  BINARY_MODULO    
              497  STORE_FAST           13  '@py_format7'
              500  LOAD_GLOBAL           2  'AssertionError'
              503  LOAD_GLOBAL           4  '@pytest_ar'
              506  LOAD_ATTR            10  '_format_explanation'
              509  LOAD_FAST            13  '@py_format7'
              512  CALL_FUNCTION_1       1  None
              515  CALL_FUNCTION_1       1  None
              518  RAISE_VARARGS_1       1  None
              521  JUMP_FORWARD          0  'to 524'
            524_0  COME_FROM           521  '521'
              524  LOAD_CONST               None
              527  DUP_TOP          
              528  STORE_FAST           10  '@py_assert0'
              531  DUP_TOP          
              532  STORE_FAST           12  '@py_assert2'
              535  STORE_FAST           11  '@py_assert3'
              538  JUMP_BACK           146  'to 146'
              541  JUMP_BACK           146  'to 146'
              544  POP_BLOCK        
            545_0  COME_FROM           139  '139'
              545  LOAD_CONST               None
              548  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 545