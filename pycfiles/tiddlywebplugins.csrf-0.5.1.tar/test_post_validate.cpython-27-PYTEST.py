# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.csrf/test/test_post_validate.py
# Compiled at: 2014-05-06 15:53:35
"""
Tests to ensure that POST requests all come from the same domain.

i.e. tests that ensure we are not vulnerable to CSRF
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from wsgi_intercept import httplib2_intercept
import wsgi_intercept, httplib2, Cookie, os, shutil
from datetime import datetime, timedelta
from tiddlywebplugins.utils import get_store
from tiddlyweb.config import config
from tiddlyweb.fixups import quote
from tiddlyweb.web.serve import load_app
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.user import User
from tiddlyweb.util import sha
from tiddlyweb.web.util import encode_name
from tiddlywebplugins.csrf import CSRFProtector, InvalidNonceError
BAD_MATCH_MESSAGE = 'CSRF token does not match'

def setup_module(module):
    if os.path.exists('store'):
        shutil.rmtree('store')
    if CSRFProtector not in config['server_request_filters']:
        config['server_request_filters'].append(CSRFProtector)
    app = load_app()

    def app_fn():
        return app

    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)
    wsgi_intercept.add_wsgi_intercept('foo.0.0.0.0', 8080, app_fn)
    module.http = httplib2.Http()


def test_validator_no_nonce():
    """
    test the validator directly
    ensure that it fails when the nonce is not present
    """
    try:
        csrf = CSRFProtector({})
        csrf.check_csrf({}, None)
        raise AssertionError('check_csrf succeeded when no csrf_token supplied')
    except InvalidNonceError as exc:
        @py_assert1 = exc.message
        @py_assert4 = 'No csrf_token supplied'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.message\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(exc) if 'exc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exc) else 'exc', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    return


def test_validator_nonce_success():
    """
    test the validator directly
    ensure that it succeeds when the nonce passed in is correct
    """
    username = 'föo'
    hostname = 'foo.0.0.0.0:8080'
    secret = '12345'
    timestamp = datetime.utcnow().strftime('%Y%m%d%H')
    nonce = '%s:%s:%s' % (timestamp, username,
     sha('%s:%s:%s:%s' % (username, timestamp, hostname,
      secret)).hexdigest())
    environ = {'tiddlyweb.usersign': {'name': username}, 'tiddlyweb.config': {'secret': secret, 
                            'server_host': {'host': '0.0.0.0', 
                                            'port': '8080'}}, 
       'HTTP_HOST': 'foo.0.0.0.0:8080'}
    csrf = CSRFProtector({})
    result = csrf.check_csrf(environ, nonce)
    @py_assert1 = result is True
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (result, True)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result', 'py2': @pytest_ar._saferepr(True) if 'True' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(True) else 'True'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


def test_validator_nonce_fail():
    """
    test the validator directly
    ensure that it fails when the nonce doesn't match
    """
    nonce = 'dwaoiju277218ywdhdnakas72'
    username = 'föo'
    secret = '12345'
    environ = {'tiddlyweb.usersign': {'name': username}, 'tiddlyweb.config': {'secret': secret, 
                            'server_host': {'host': '0.0.0.0', 
                                            'port': '8080'}}, 
       'HTTP_HOST': 'foo.0.0.0.0:8080'}
    try:
        csrf = CSRFProtector({})
        csrf.check_csrf(environ, nonce)
        raise AssertionError("check_csrf succeeded when nonce didn't match")
    except InvalidNonceError as exc:
        @py_assert1 = exc.message
        @py_assert3 = @py_assert1 == BAD_MATCH_MESSAGE
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.message\n} == %(py4)s', ), (@py_assert1, BAD_MATCH_MESSAGE)) % {'py0': @pytest_ar._saferepr(exc) if 'exc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exc) else 'exc', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(BAD_MATCH_MESSAGE) if 'BAD_MATCH_MESSAGE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BAD_MATCH_MESSAGE) else 'BAD_MATCH_MESSAGE'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None

    return


def test_validator_nonce_hash_fail():
    """
    test the validator directly
    ensure that it fails when the hash section of the nonce is incorrect
    """
    username = 'föo'
    hostname = 'foo.0.0.0.0:8080'
    secret = '12345'
    timestamp = datetime.utcnow().strftime('%Y%m%d%H')
    nonce = '%s:%s:dwaoiju277218ywdhdnakas72' % (timestamp, username)
    environ = {'tiddlyweb.usersign': {'name': username}, 'tiddlyweb.config': {'secret': secret, 
                            'server_host': {'host': '0.0.0.0', 
                                            'port': '8080'}}, 
       'HTTP_HOST': hostname}
    try:
        csrf = CSRFProtector({})
        csrf.check_csrf(environ, nonce)
        raise AssertionError("check_csrf succeeded when nonce didn't match")
    except InvalidNonceError as exc:
        @py_assert1 = exc.message
        @py_assert3 = @py_assert1 == BAD_MATCH_MESSAGE
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.message\n} == %(py4)s', ), (@py_assert1, BAD_MATCH_MESSAGE)) % {'py0': @pytest_ar._saferepr(exc) if 'exc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exc) else 'exc', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(BAD_MATCH_MESSAGE) if 'BAD_MATCH_MESSAGE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BAD_MATCH_MESSAGE) else 'BAD_MATCH_MESSAGE'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None

    return


def test_post_data_form_urlencoded--- This code section failed: ---

 L. 158         0  LOAD_GLOBAL           0  'get_store'
                3  LOAD_GLOBAL           1  'config'
                6  CALL_FUNCTION_1       1  None
                9  STORE_FAST            0  'store'

 L. 159        12  LOAD_CONST               'foo.0.0.0.0:8080'
               15  STORE_FAST            1  'hostname'

 L. 160        18  LOAD_GLOBAL           2  'User'
               21  LOAD_CONST               'föo'
               24  CALL_FUNCTION_1       1  None
               27  STORE_FAST            2  'user'

 L. 161        30  LOAD_FAST             2  'user'
               33  LOAD_ATTR             3  'set_password'
               36  LOAD_CONST               'foobar'
               39  CALL_FUNCTION_1       1  None
               42  POP_TOP          

 L. 162        43  LOAD_FAST             0  'store'
               46  LOAD_ATTR             4  'put'
               49  LOAD_FAST             2  'user'
               52  CALL_FUNCTION_1       1  None
               55  POP_TOP          

 L. 163        56  LOAD_FAST             0  'store'
               59  LOAD_ATTR             4  'put'
               62  LOAD_GLOBAL           5  'Bag'
               65  LOAD_CONST               'foo_public'
               68  CALL_FUNCTION_1       1  None
               71  CALL_FUNCTION_1       1  None
               74  POP_TOP          

 L. 164        75  LOAD_GLOBAL           6  'datetime'
               78  LOAD_ATTR             7  'utcnow'
               81  CALL_FUNCTION_0       0  None
               84  LOAD_ATTR             8  'strftime'
               87  LOAD_CONST               '%Y%m%d%H'
               90  CALL_FUNCTION_1       1  None
               93  STORE_FAST            3  'timestamp'

 L. 165        96  LOAD_GLOBAL           1  'config'
               99  LOAD_CONST               'secret'
              102  BINARY_SUBSCR    
              103  STORE_FAST            4  'secret'

 L. 166       106  LOAD_CONST               '%s:%s:%s'
              109  LOAD_FAST             3  'timestamp'
              112  LOAD_FAST             2  'user'
              115  LOAD_ATTR             9  'usersign'

 L. 167       118  LOAD_GLOBAL          10  'sha'
              121  LOAD_CONST               '%s:%s:%s:%s'
              124  LOAD_FAST             2  'user'
              127  LOAD_ATTR             9  'usersign'
              130  LOAD_FAST             3  'timestamp'
              133  LOAD_FAST             1  'hostname'

 L. 168       136  LOAD_FAST             4  'secret'
              139  BUILD_TUPLE_4         4 
              142  BINARY_MODULO    
              143  CALL_FUNCTION_1       1  None
              146  LOAD_ATTR            11  'hexdigest'
              149  CALL_FUNCTION_0       0  None
              152  BUILD_TUPLE_3         3 
              155  BINARY_MODULO    
              156  STORE_FAST            5  'nonce'

 L. 170       159  LOAD_GLOBAL          12  'get_auth'
              162  LOAD_CONST               'föo'
              165  LOAD_CONST               'foobar'
              168  CALL_FUNCTION_2       2  None
              171  STORE_FAST            6  'user_cookie'

 L. 171       174  LOAD_CONST               'csrf_token="%s"'
              177  LOAD_GLOBAL          13  'quote'
              180  LOAD_FAST             5  'nonce'
              183  LOAD_ATTR            14  'encode'
              186  LOAD_CONST               'utf-8'
              189  CALL_FUNCTION_1       1  None
              192  LOAD_CONST               'safe'

 L. 172       195  LOAD_CONST               ".!~*'():"
              198  CALL_FUNCTION_257   257  None
              201  BINARY_MODULO    
              202  STORE_FAST            7  'csrf_token'

 L. 173       205  LOAD_CONST               'title=foobar&text=hello%20world'
              208  STORE_FAST            8  'data'

 L. 175       211  LOAD_CONST               'nc'
              214  PRINT_ITEM       
              215  LOAD_FAST             5  'nonce'
              218  PRINT_ITEM_CONT  
              219  LOAD_FAST             7  'csrf_token'
              222  PRINT_ITEM_CONT  
              223  PRINT_NEWLINE_CONT

 L. 177       224  LOAD_GLOBAL          15  'http'
              227  LOAD_ATTR            16  'request'

 L. 178       230  LOAD_CONST               'http://foo.0.0.0.0:8080/bags/foo_public/tiddlers'
              233  LOAD_CONST               'method'

 L. 179       236  LOAD_CONST               'POST'
              239  LOAD_CONST               'headers'

 L. 180       242  BUILD_MAP_2           2  None

 L. 181       245  LOAD_CONST               'application/x-www-form-urlencoded'
              248  LOAD_CONST               'Content-type'
              251  STORE_MAP        

 L. 182       252  LOAD_CONST               'tiddlyweb_user="%s"; %s'
              255  LOAD_FAST             6  'user_cookie'
              258  LOAD_FAST             7  'csrf_token'
              261  BUILD_TUPLE_2         2 
              264  BINARY_MODULO    
              265  LOAD_CONST               'Cookie'
              268  STORE_MAP        
              269  LOAD_CONST               'body'

 L. 184       272  LOAD_CONST               '%s&csrf_token=%s'
              275  LOAD_FAST             8  'data'
              278  LOAD_GLOBAL          17  'encode_name'
              281  LOAD_FAST             5  'nonce'
              284  CALL_FUNCTION_1       1  None
              287  BUILD_TUPLE_2         2 
              290  BINARY_MODULO    
              291  CALL_FUNCTION_769   769  None
              294  UNPACK_SEQUENCE_2     2 
              297  STORE_FAST            9  'response'
              300  STORE_FAST           10  'content'

 L. 185       303  LOAD_FAST             9  'response'
              306  LOAD_CONST               'status'
              309  BINARY_SUBSCR    
              310  LOAD_CONST               '204'
              313  COMPARE_OP            2  ==
              316  POP_JUMP_IF_TRUE    328  'to 328'
              319  LOAD_ASSERT              AssertionError
              322  LOAD_FAST            10  'content'
              325  RAISE_VARARGS_2       2  None

 L. 188       328  LOAD_GLOBAL          15  'http'
              331  LOAD_ATTR            16  'request'

 L. 189       334  LOAD_CONST               'http://0.0.0.0:8080/bags/foo_public/tiddlers'
              337  LOAD_CONST               'method'

 L. 190       340  LOAD_CONST               'POST'
              343  LOAD_CONST               'headers'

 L. 191       346  BUILD_MAP_2           2  None

 L. 192       349  LOAD_CONST               'application/x-www-form-urlencoded'
              352  LOAD_CONST               'Content-type'
              355  STORE_MAP        

 L. 193       356  LOAD_CONST               'tiddlyweb_user="%s"'
              359  LOAD_FAST             6  'user_cookie'
              362  BINARY_MODULO    
              363  LOAD_CONST               'Cookie'
              366  STORE_MAP        
              367  LOAD_CONST               'body'

 L. 195       370  LOAD_CONST               '%s'
              373  LOAD_FAST             8  'data'
              376  BINARY_MODULO    
              377  CALL_FUNCTION_769   769  None
              380  UNPACK_SEQUENCE_2     2 
              383  STORE_FAST            9  'response'
              386  STORE_FAST           10  'content'

 L. 196       389  LOAD_FAST             9  'response'
              392  LOAD_CONST               'status'
              395  BINARY_SUBSCR    
              396  LOAD_CONST               '400'
              399  COMPARE_OP            2  ==
              402  POP_JUMP_IF_TRUE    414  'to 414'
              405  LOAD_ASSERT              AssertionError
              408  LOAD_FAST            10  'content'
              411  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_FAST' instruction at offset 408


def test_post_data_multipart_form():
    """
    test that a form POST requires a nonce
    test using multipart/form-data
    """
    store = get_store(config)
    hostname = 'foo.0.0.0.0:8080'
    user = User('föo')
    user.set_password('foobar')
    store.put(user)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H')
    secret = config['secret']
    nonce = '%s:%s:%s' % (timestamp, user.usersign,
     sha('%s:%s:%s:%s' % (user.usersign, timestamp, hostname,
      secret)).hexdigest())
    user_cookie = get_auth('föo', 'foobar')
    csrf_token = 'csrf_token=%s' % nonce
    data = '---------------------------168072824752491622650073\nContent-Disposition: form-data; name="title"\n\nfoobar\n---------------------------168072824752491622650073\nContent-Disposition: form-data; name="text"\n\nHello World\n---------------------------168072824752491622650073--'
    uri = 'http://foo.0.0.0.0:8080/bags/foo_public/tiddlers?%s' % csrf_token
    response, content = http.request(uri, method='POST', headers={'Content-Type': 'multipart/form-data; boundary=---------------------------168072824752491622650073', 
       'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Content-Length': '390'}, body=data)
    if not response['status'] == '204':
        raise AssertionError, content
        response, _ = http.request('http://foo.0.0.0.0:8080/bags/foo_public/tiddlers', method='POST', headers={'Content-Type': 'multipart/form-data; boundary=---------------------------168072824752491622650073', 
           'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
           'Content-Length': '267'}, body=data)
        @py_assert0 = response['status']
        @py_assert3 = '400'
        @py_assert2 = @py_assert0 == @py_assert3
        @py_format5 = @py_assert2 or @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_nonce_not_left_over():
    """
    Test that the nonce is not left over in the tiddler after a POST
    i.e. check that it is removed before the request continues
    """
    store = get_store(config)
    hostname = 'foo.0.0.0.0:8080'
    user = User('föo')
    user.set_password('foobar')
    store.put(user)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H')
    secret = config['secret']
    nonce = '%s:%s:%s' % (timestamp, user.usersign,
     sha('%s:%s:%s:%s' % (user.usersign, timestamp, hostname,
      secret)).hexdigest())
    user_cookie = get_auth('föo', 'foobar')
    data = 'title=foobar&text=hello%20world&extra_field=baz'
    nonce = quote(nonce.encode('utf-8'), safe=".!~*'():")
    response, _ = http.request('http://foo.0.0.0.0:8080/bags/foo_public/tiddlers', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded', 
       'Cookie': 'tiddlyweb_user="%s"' % user_cookie}, body='%s&csrf_token=%s' % (data, nonce))
    @py_assert0 = response['status']
    @py_assert3 = '204'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    new_tiddler = Tiddler('foobar')
    new_tiddler.bag = 'foo_public'
    new_tiddler = store.get(new_tiddler)
    @py_assert1 = new_tiddler.title
    @py_assert4 = 'foobar'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(new_tiddler) if 'new_tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_tiddler) else 'new_tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = new_tiddler.text
    @py_assert4 = 'hello world'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(new_tiddler) if 'new_tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_tiddler) else 'new_tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = new_tiddler.fields
    @py_assert3 = @py_assert1.get
    @py_assert5 = 'extra_field'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert10 = 'baz'
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.fields\n}.get\n}(%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(new_tiddler) if 'new_tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_tiddler) else 'new_tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = new_tiddler.fields
    @py_assert3 = @py_assert1.get
    @py_assert5 = 'nonce'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7 is None
    if not @py_assert9:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.fields\n}.get\n}(%(py6)s)\n} is %(py10)s', ), (@py_assert7, None)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(new_tiddler) if 'new_tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_tiddler) else 'new_tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py10': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(None) else 'None'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    return


def test_cookie_set():
    """
    test that we get a cookie relating to the space we are in
    """
    store = get_store(config)
    hostname = 'foo.0.0.0.0:8080'
    user = User('föo')
    user.set_password('foobar')
    store.put(user)
    user_cookie = get_auth('föo', 'foobar')
    response, content = http.request('http://foo.0.0.0.0:8080/', method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie})
    if not response['status'] == '200':
        raise AssertionError, content
        time = datetime.utcnow().strftime('%Y%m%d%H')
        cookie = 'csrf_token=%s:%s:%s' % (time, user.usersign,
         sha('%s:%s:%s:%s' % (user.usersign,
          time, hostname, config['secret'])).hexdigest())
        @py_assert0 = response['set-cookie']
        @py_assert5 = cookie.encode
        @py_assert7 = 'utf-8'
        @py_assert9 = @py_assert5(@py_assert7)
        @py_assert11 = ".!~*'():="
        @py_assert13 = quote(@py_assert9, safe=@py_assert11)
        @py_assert2 = @py_assert0 == @py_assert13
        @py_format15 = @py_assert2 or @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py14)s\n{%(py14)s = %(py3)s(%(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s.encode\n}(%(py8)s)\n}, safe=%(py12)s)\n}', ), (@py_assert0, @py_assert13)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py12': @pytest_ar._saferepr(@py_assert11), 'py1': @pytest_ar._saferepr(@py_assert0), 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(quote) if 'quote' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(quote) else 'quote', 'py4': @pytest_ar._saferepr(cookie) if 'cookie' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cookie) else 'cookie', 'py6': @pytest_ar._saferepr(@py_assert5), 'py14': @pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    return


def test_guest_no_cookie_set():
    """
    Test that we don't get a cookie if we are a guest
    """
    response, _ = http.request('http://0.0.0.0:8080/', method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    cookie = response.get('set-cookie')
    if cookie:
        @py_assert0 = 'csrf_token'
        @py_assert2 = @py_assert0 not in cookie
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, cookie)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(cookie) if 'cookie' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cookie) else 'cookie'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
    return


def test_no_cookie_sent():
    """
    Test no cookie is sent if one is already present
    """
    store = get_store(config)
    hostname = 'foo.0.0.0.0:8080'
    user = User('föo')
    user.set_password('foobar')
    store.put(user)
    user_cookie = get_auth('föo', 'foobar')
    time = datetime.utcnow().strftime('%Y%m%d%H')
    token_cookie = 'csrf_token=%s:%s:%s' % (time, encode_name(user.usersign),
     sha('%s:%s:%s:%s' % (encode_name(user.usersign), time, hostname,
      config['secret'])).hexdigest())
    response, _ = http.request('http://foo.0.0.0.0:8080/status', method='GET', headers={'Cookie': 'tiddlyweb_user="%s"; %s' % (user_cookie, token_cookie)})
    cookie = response.get('set-cookie')
    if cookie:
        @py_assert0 = 'csrf_token'
        @py_assert2 = @py_assert0 not in cookie
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, cookie)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(cookie) if 'cookie' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cookie) else 'cookie'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
    response, _ = http.request('http://foo.0.0.0.0:8080/status', method='GET', headers={'User-Agent': 'MSIE', 
       'Cookie': '%s' % token_cookie})
    cookie = response.get('set-cookie')
    @py_assert0 = 'csrf_token'
    @py_assert2 = @py_assert0 in cookie
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, cookie)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(cookie) if 'cookie' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cookie) else 'cookie'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'Expires='
    @py_assert2 = @py_assert0 in cookie
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, cookie)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(cookie) if 'cookie' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cookie) else 'cookie'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_invalid_cookie():
    """
    Test that an invalid/old cookie causes a new cookie to be sent
    """
    store = get_store(config)
    hostname = 'foo.0.0.0.0:8080'
    user = User('föo')
    user.set_password('foobar')
    store.put(user)
    user_cookie = get_auth('föo', 'foobar')
    time = datetime.utcnow() - timedelta(hours=3)
    time = time.strftime('%Y%m%d%H')
    cookie = 'csrf_token=%s:%s:%s' % (time, encode_name(user.usersign),
     sha('%s:%s:%s:%s' % (encode_name(user.usersign),
      time, hostname, config['secret'])).hexdigest())
    response, _ = http.request('http://foo.0.0.0.0:8080/status', method='GET', headers={'Cookie': 'tiddlyweb_user="%s"; %s' % (user_cookie, cookie)})
    @py_assert0 = 'csrf_token'
    @py_assert3 = response['set-cookie']
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    cookie = 'csrf_token=adiudh9389wefnf98'
    response, _ = http.request('http://foo.0.0.0.0:8080/status', method='GET', headers={'Cookie': 'tiddlyweb_user="%s"; %s' % (user_cookie, cookie)})
    @py_assert0 = 'csrf_token'
    @py_assert3 = response['set-cookie']
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    user2 = User('bar')
    user2.set_password('foobar')
    store.put(user2)
    user2_cookie = get_auth('bar', 'foobar')
    response, _ = http.request('http://foo.0.0.0.0:8080/status', method='GET', headers={'Cookie': 'tiddlyweb_user="%s"; %s' % (user2_cookie, cookie)})
    @py_assert0 = 'csrf_token'
    @py_assert4 = response.get
    @py_assert6 = 'set-cookie'
    @py_assert8 = ''
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert2 = @py_assert0 in @py_assert10
    if not @py_assert2:
        @py_format12 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.get\n}(%(py7)s, %(py9)s)\n}', ), (@py_assert0, @py_assert10)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py1': @pytest_ar._saferepr(@py_assert0), 'py11': @pytest_ar._saferepr(@py_assert10), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    return


def get_auth(username, password):
    response, _ = http.request('http://0.0.0.0:8080/challenge/cookie_form', body='user=%s&password=%s' % (encode_name(username),
     encode_name(password)), method='POST', headers={'Content-Type': 'application/x-www-form-urlencoded'})
    @py_assert0 = response.previous['status']
    @py_assert3 = '303'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    user_cookie = response.previous['set-cookie']
    cookie = Cookie.SimpleCookie()
    cookie.load(user_cookie)
    return cookie['tiddlyweb_user'].value