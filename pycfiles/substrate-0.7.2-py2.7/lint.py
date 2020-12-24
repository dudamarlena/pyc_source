# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/substrate/data/local/substrate/lib/webtest/lint.py
# Compiled at: 2012-09-09 20:09:24
"""
Middleware to check for obedience to the WSGI specification.

Some of the things this checks:

* Signature of the application and start_response (including that
  keyword arguments are not used).

* Environment checks:

  - Environment is a dictionary (and not a subclass).

  - That all the required keys are in the environment: REQUEST_METHOD,
    SERVER_NAME, SERVER_PORT, wsgi.version, wsgi.input, wsgi.errors,
    wsgi.multithread, wsgi.multiprocess, wsgi.run_once

  - That HTTP_CONTENT_TYPE and HTTP_CONTENT_LENGTH are not in the
    environment (these headers should appear as CONTENT_LENGTH and
    CONTENT_TYPE).

  - Warns if QUERY_STRING is missing, as the cgi module acts
    unpredictably in that case.

  - That CGI-style variables (that don't contain a .) have
    (non-unicode) string values

  - That wsgi.version is a tuple

  - That wsgi.url_scheme is 'http' or 'https' (@@: is this too
    restrictive?)

  - Warns if the REQUEST_METHOD is not known (@@: probably too
    restrictive).

  - That SCRIPT_NAME and PATH_INFO are empty or start with /

  - That at least one of SCRIPT_NAME or PATH_INFO are set.

  - That CONTENT_LENGTH is a positive integer.

  - That SCRIPT_NAME is not '/' (it should be '', and PATH_INFO should
    be '/').

  - That wsgi.input has the methods read, readline, readlines, and
    __iter__

  - That wsgi.errors has the methods flush, write, writelines

* The status is a string, contains a space, starts with an integer,
  and that integer is in range (> 100).

* That the headers is a list (not a subclass, not another kind of
  sequence).

* That the items of the headers are tuples of strings.

* That there is no 'status' header (that is used in CGI, but not in
  WSGI).

* That the headers don't contain newlines or colons, end in _ or -, or
  contain characters codes below 037.

* That Content-Type is given if there is content (CGI often has a
  default content type, but WSGI does not).

* That no Content-Type is given when there is no content (@@: is this
  too restrictive?)

* That the exc_info argument to start_response is a tuple or None.

* That all calls to the writer are with strings, and no other methods
  on the writer are accessed.

* That wsgi.input is used properly:

  - .read() is called with zero or one argument

  - That it returns a string

  - That readline, readlines, and __iter__ return strings

  - That .close() is not called

  - No other methods are provided

* That wsgi.errors is used properly:

  - .write() and .writelines() is called with a string

  - That .close() is not called, and no other methods are provided.

* The response iterator:

  - That it is not a string (it should be a list of a single string; a
    string will work, but perform horribly).

  - That .next() returns a string

  - That the iterator is not iterated over until start_response has
    been called (that can signal either a server or application
    error).

  - That .close() is called (doesn't raise exception, only prints to
    sys.stderr, because we only know it isn't called when the object
    is garbage collected).
"""
import re, sys, warnings
from webtest.compat import next
header_re = re.compile('^[a-zA-Z][a-zA-Z0-9\\-_]*$')
bad_header_value_re = re.compile('[\\000-\\037]')
valid_methods = ('GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'DELETE', 'TRACE', 'PATCH')

class WSGIWarning(Warning):
    """
    Raised in response to WSGI-spec-related warnings
    """
    pass


def middleware(application, global_conf=None):
    """
    When applied between a WSGI server and a WSGI application, this
    middleware will check for WSGI compliancy on a number of levels.
    This middleware does not modify the request or response in any
    way, but will throw an AssertionError if anything seems off
    (except for a failure to close the application iterator, which
    will be printed to stderr -- there's no way to throw an exception
    at that point).
    """

    def lint_app--- This code section failed: ---

 L. 147         0  LOAD_GLOBAL           0  'len'
                3  LOAD_FAST             0  'args'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_CONST               2
               12  COMPARE_OP            2  ==
               15  POP_JUMP_IF_TRUE     27  'to 27'
               18  LOAD_ASSERT              AssertionError
               21  LOAD_CONST               'Two arguments required'
               24  RAISE_VARARGS_2       2  None

 L. 148        27  LOAD_FAST             1  'kw'
               30  UNARY_NOT        
               31  POP_JUMP_IF_TRUE     43  'to 43'
               34  LOAD_ASSERT              AssertionError
               37  LOAD_CONST               'No keyword arguments allowed'
               40  RAISE_VARARGS_2       2  None

 L. 149        43  LOAD_FAST             0  'args'
               46  UNPACK_SEQUENCE_2     2 
               49  STORE_FAST            2  'environ'
               52  STORE_DEREF           0  'start_response'

 L. 151        55  LOAD_GLOBAL           2  'check_environ'
               58  LOAD_FAST             2  'environ'
               61  CALL_FUNCTION_1       1  None
               64  POP_TOP          

 L. 155        65  BUILD_LIST_0          0 
               68  STORE_DEREF           1  'start_response_started'

 L. 157        71  LOAD_CLOSURE          0  'start_response'
               74  LOAD_CLOSURE          1  'start_response_started'
               80  LOAD_CODE                <code_object start_response_wrapper>
               83  MAKE_CLOSURE_0        0  None
               86  STORE_FAST            3  'start_response_wrapper'

 L. 176        89  LOAD_GLOBAL           3  'InputWrapper'
               92  LOAD_FAST             2  'environ'
               95  LOAD_CONST               'wsgi.input'
               98  BINARY_SUBSCR    
               99  CALL_FUNCTION_1       1  None
              102  LOAD_FAST             2  'environ'
              105  LOAD_CONST               'wsgi.input'
              108  STORE_SUBSCR     

 L. 177       109  LOAD_GLOBAL           4  'ErrorWrapper'
              112  LOAD_FAST             2  'environ'
              115  LOAD_CONST               'wsgi.errors'
              118  BINARY_SUBSCR    
              119  CALL_FUNCTION_1       1  None
              122  LOAD_FAST             2  'environ'
              125  LOAD_CONST               'wsgi.errors'
              128  STORE_SUBSCR     

 L. 179       129  LOAD_DEREF            2  'application'
              132  LOAD_FAST             2  'environ'
              135  LOAD_FAST             3  'start_response_wrapper'
              138  CALL_FUNCTION_2       2  None
              141  STORE_FAST            4  'iterator'

 L. 180       144  LOAD_FAST             4  'iterator'
              147  LOAD_CONST               None
              150  COMPARE_OP            9  is-not
              153  POP_JUMP_IF_FALSE   168  'to 168'
              156  LOAD_FAST             4  'iterator'
              159  LOAD_GLOBAL           6  'False'
              162  COMPARE_OP            3  !=
            165_0  COME_FROM           153  '153'
              165  POP_JUMP_IF_TRUE    177  'to 177'
              168  LOAD_ASSERT              AssertionError

 L. 181       171  LOAD_CONST               'The application must return an iterator, if only an empty list'
              174  RAISE_VARARGS_2       2  None

 L. 183       177  LOAD_GLOBAL           7  'check_iterator'
              180  LOAD_FAST             4  'iterator'
              183  CALL_FUNCTION_1       1  None
              186  POP_TOP          

 L. 185       187  LOAD_GLOBAL           8  'IteratorWrapper'
              190  LOAD_FAST             4  'iterator'
              193  LOAD_DEREF            1  'start_response_started'
              196  CALL_FUNCTION_2       2  None
              199  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 196

    return lint_app


class InputWrapper(object):

    def __init__(self, wsgi_input):
        self.input = wsgi_input

    def read(self, *args):
        assert len(args) <= 1
        v = self.input.read(*args)
        assert type(v) is type('')
        return v

    def readline(self, *args):
        v = self.input.readline(*args)
        assert type(v) is type('')
        return v

    def readlines(self, *args):
        assert len(args) <= 1
        lines = self.input.readlines(*args)
        assert type(lines) is type([])
        for line in lines:
            assert type(line) is type('')

        return lines

    def __iter__(self):
        while 1:
            line = self.readline()
            if not line:
                return
            yield line

    def close--- This code section failed: ---

 L. 222         0  LOAD_CONST               0
                3  POP_JUMP_IF_TRUE     15  'to 15'
                6  LOAD_ASSERT              AssertionError
                9  LOAD_CONST               'input.close() must not be called'
               12  RAISE_VARARGS_2       2  None

Parse error at or near `None' instruction at offset -1


class ErrorWrapper(object):

    def __init__(self, wsgi_errors):
        self.errors = wsgi_errors

    def write(self, s):
        assert type(s) is type('')
        self.errors.write(s)

    def flush(self):
        self.errors.flush()

    def writelines(self, seq):
        for line in seq:
            self.write(line)

    def close--- This code section failed: ---

 L. 242         0  LOAD_CONST               0
                3  POP_JUMP_IF_TRUE     15  'to 15'
                6  LOAD_ASSERT              AssertionError
                9  LOAD_CONST               'errors.close() must not be called'
               12  RAISE_VARARGS_2       2  None

Parse error at or near `None' instruction at offset -1


class WriteWrapper(object):

    def __init__(self, wsgi_writer):
        self.writer = wsgi_writer

    def __call__(self, s):
        assert type(s) is type('')
        self.writer(s)


class PartialIteratorWrapper(object):

    def __init__(self, wsgi_iterator):
        self.iterator = wsgi_iterator

    def __iter__(self):
        return IteratorWrapper(self.iterator)


class IteratorWrapper(object):

    def __init__(self, wsgi_iterator, check_start_response):
        self.original_iterator = wsgi_iterator
        self.iterator = iter(wsgi_iterator)
        self.closed = False
        self.check_start_response = check_start_response

    def __iter__(self):
        return self

    def next--- This code section failed: ---

 L. 277         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'closed'
                6  UNARY_NOT        
                7  POP_JUMP_IF_TRUE     19  'to 19'
               10  LOAD_ASSERT              AssertionError

 L. 278        13  LOAD_CONST               'Iterator read after closed'
               16  RAISE_VARARGS_2       2  None

 L. 279        19  LOAD_GLOBAL           2  'next'
               22  LOAD_FAST             0  'self'
               25  LOAD_ATTR             3  'iterator'
               28  CALL_FUNCTION_1       1  None
               31  STORE_FAST            1  'v'

 L. 280        34  LOAD_FAST             0  'self'
               37  LOAD_ATTR             4  'check_start_response'
               40  LOAD_CONST               None
               43  COMPARE_OP            9  is-not
               46  POP_JUMP_IF_FALSE    79  'to 79'

 L. 281        49  LOAD_FAST             0  'self'
               52  LOAD_ATTR             4  'check_start_response'
               55  POP_JUMP_IF_TRUE     67  'to 67'
               58  LOAD_ASSERT              AssertionError

 L. 282        61  LOAD_CONST               'The application returns and we started iterating over its body, but start_response has not yet been called'
               64  RAISE_VARARGS_2       2  None

 L. 284        67  LOAD_CONST               None
               70  LOAD_FAST             0  'self'
               73  STORE_ATTR            4  'check_start_response'
               76  JUMP_FORWARD          0  'to 79'
             79_0  COME_FROM            76  '76'

 L. 285        79  LOAD_GLOBAL           6  'isinstance'
               82  LOAD_FAST             1  'v'
               85  LOAD_GLOBAL           7  'str'
               88  CALL_FUNCTION_2       2  None
               91  POP_JUMP_IF_TRUE    116  'to 116'
               94  LOAD_ASSERT              AssertionError

 L. 286        97  LOAD_CONST               'Iterator %r returned a non-str object: %r'

 L. 287       100  LOAD_FAST             0  'self'
              103  LOAD_ATTR             3  'iterator'
              106  LOAD_FAST             1  'v'
              109  BUILD_TUPLE_2         2 
              112  BINARY_MODULO    
              113  RAISE_VARARGS_2       2  None

 L. 288       116  LOAD_FAST             1  'v'
              119  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 116

    __next__ = next

    def close(self):
        self.closed = True
        if hasattr(self.original_iterator, 'close'):
            self.original_iterator.close()

    def __del__--- This code section failed: ---

 L. 298         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'closed'
                6  POP_JUMP_IF_TRUE     28  'to 28'

 L. 299         9  LOAD_GLOBAL           1  'sys'
               12  LOAD_ATTR             2  'stderr'
               15  LOAD_ATTR             3  'write'

 L. 300        18  LOAD_CONST               'Iterator garbage collected without being closed'
               21  CALL_FUNCTION_1       1  None
               24  POP_TOP          
               25  JUMP_FORWARD          0  'to 28'
             28_0  COME_FROM            25  '25'

 L. 301        28  LOAD_FAST             0  'self'
               31  LOAD_ATTR             0  'closed'
               34  POP_JUMP_IF_TRUE     46  'to 46'
               37  LOAD_ASSERT              AssertionError

 L. 302        40  LOAD_CONST               'Iterator garbage collected without being closed'
               43  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_CONST' instruction at offset 40


def check_environ--- This code section failed: ---

 L. 306         0  LOAD_GLOBAL           0  'type'
                3  LOAD_FAST             0  'environ'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_GLOBAL           1  'dict'
               12  COMPARE_OP            8  is
               15  POP_JUMP_IF_TRUE     43  'to 43'
               18  LOAD_ASSERT              AssertionError

 L. 307        21  LOAD_CONST               'Environment is not of the right type: %r (environment: %r)'

 L. 308        24  LOAD_GLOBAL           0  'type'
               27  LOAD_FAST             0  'environ'
               30  CALL_FUNCTION_1       1  None
               33  LOAD_FAST             0  'environ'
               36  BUILD_TUPLE_2         2 
               39  BINARY_MODULO    
               40  RAISE_VARARGS_2       2  None

 L. 310        43  SETUP_LOOP           66  'to 112'
               46  LOAD_CONST               'REQUEST_METHOD'
               49  LOAD_CONST               'SERVER_NAME'
               52  LOAD_CONST               'SERVER_PORT'

 L. 311        55  LOAD_CONST               'wsgi.version'
               58  LOAD_CONST               'wsgi.input'
               61  LOAD_CONST               'wsgi.errors'

 L. 312        64  LOAD_CONST               'wsgi.multithread'
               67  LOAD_CONST               'wsgi.multiprocess'

 L. 313        70  LOAD_CONST               'wsgi.run_once'
               73  BUILD_LIST_9          9 
               76  GET_ITER         
               77  FOR_ITER             31  'to 111'
               80  STORE_FAST            1  'key'

 L. 314        83  LOAD_FAST             1  'key'
               86  LOAD_FAST             0  'environ'
               89  COMPARE_OP            6  in
               92  POP_JUMP_IF_TRUE     77  'to 77'
               95  LOAD_ASSERT              AssertionError

 L. 315        98  LOAD_CONST               'Environment missing required key: %r'
              101  LOAD_FAST             1  'key'
              104  BINARY_MODULO    
              105  RAISE_VARARGS_2       2  None
              108  JUMP_BACK            77  'to 77'
              111  POP_BLOCK        
            112_0  COME_FROM            43  '43'

 L. 317       112  SETUP_LOOP           55  'to 170'
              115  LOAD_CONST               'HTTP_CONTENT_TYPE'
              118  LOAD_CONST               'HTTP_CONTENT_LENGTH'
              121  BUILD_LIST_2          2 
              124  GET_ITER         
              125  FOR_ITER             41  'to 169'
              128  STORE_FAST            1  'key'

 L. 318       131  LOAD_FAST             1  'key'
              134  LOAD_FAST             0  'environ'
              137  COMPARE_OP            7  not-in
              140  POP_JUMP_IF_TRUE    125  'to 125'
              143  LOAD_ASSERT              AssertionError

 L. 319       146  LOAD_CONST               'Environment should not have the key: %s (use %s instead)'

 L. 320       149  LOAD_FAST             1  'key'
              152  LOAD_FAST             1  'key'
              155  LOAD_CONST               5
              158  SLICE+1          
              159  BUILD_TUPLE_2         2 
              162  BINARY_MODULO    
              163  RAISE_VARARGS_2       2  None
              166  JUMP_BACK           125  'to 125'
              169  POP_BLOCK        
            170_0  COME_FROM           112  '112'

 L. 322       170  LOAD_CONST               'QUERY_STRING'
              173  LOAD_FAST             0  'environ'
              176  COMPARE_OP            7  not-in
              179  POP_JUMP_IF_FALSE   201  'to 201'

 L. 323       182  LOAD_GLOBAL           3  'warnings'
              185  LOAD_ATTR             4  'warn'

 L. 324       188  LOAD_CONST               'QUERY_STRING is not in the WSGI environment; the cgi module will use sys.argv when this variable is missing, so application errors are more likely'

 L. 327       191  LOAD_GLOBAL           5  'WSGIWarning'
              194  CALL_FUNCTION_2       2  None
              197  POP_TOP          
              198  JUMP_FORWARD          0  'to 201'
            201_0  COME_FROM           198  '198'

 L. 329       201  SETUP_LOOP           90  'to 294'
              204  LOAD_FAST             0  'environ'
              207  GET_ITER         
              208  FOR_ITER             82  'to 293'
              211  STORE_FAST            1  'key'

 L. 330       214  LOAD_CONST               '.'
              217  LOAD_FAST             1  'key'
              220  COMPARE_OP            6  in
              223  POP_JUMP_IF_FALSE   232  'to 232'

 L. 332       226  CONTINUE            208  'to 208'
              229  JUMP_FORWARD          0  'to 232'
            232_0  COME_FROM           229  '229'

 L. 333       232  LOAD_GLOBAL           0  'type'
              235  LOAD_FAST             0  'environ'
              238  LOAD_FAST             1  'key'
              241  BINARY_SUBSCR    
              242  CALL_FUNCTION_1       1  None
              245  LOAD_GLOBAL           6  'str'
              248  COMPARE_OP            8  is
              251  POP_JUMP_IF_TRUE    208  'to 208'
              254  LOAD_ASSERT              AssertionError

 L. 334       257  LOAD_CONST               'Environmental variable %s is not a string: %r (value: %r)'

 L. 335       260  LOAD_FAST             1  'key'
              263  LOAD_GLOBAL           0  'type'
              266  LOAD_FAST             0  'environ'
              269  LOAD_FAST             1  'key'
              272  BINARY_SUBSCR    
              273  CALL_FUNCTION_1       1  None
              276  LOAD_FAST             0  'environ'
              279  LOAD_FAST             1  'key'
              282  BINARY_SUBSCR    
              283  BUILD_TUPLE_3         3 
              286  BINARY_MODULO    
              287  RAISE_VARARGS_2       2  None
              290  JUMP_BACK           208  'to 208'
              293  POP_BLOCK        
            294_0  COME_FROM           201  '201'

 L. 337       294  LOAD_GLOBAL           0  'type'
              297  LOAD_FAST             0  'environ'
              300  LOAD_CONST               'wsgi.version'
              303  BINARY_SUBSCR    
              304  CALL_FUNCTION_1       1  None
              307  LOAD_GLOBAL           7  'tuple'
              310  COMPARE_OP            8  is
              313  POP_JUMP_IF_TRUE    333  'to 333'
              316  LOAD_ASSERT              AssertionError

 L. 338       319  LOAD_CONST               'wsgi.version should be a tuple (%r)'
              322  LOAD_FAST             0  'environ'
              325  LOAD_CONST               'wsgi.version'
              328  BINARY_SUBSCR    
              329  BINARY_MODULO    
              330  RAISE_VARARGS_2       2  None

 L. 339       333  LOAD_FAST             0  'environ'
              336  LOAD_CONST               'wsgi.url_scheme'
              339  BINARY_SUBSCR    
              340  LOAD_CONST               ('http', 'https')
              343  COMPARE_OP            6  in
              346  POP_JUMP_IF_TRUE    366  'to 366'
              349  LOAD_ASSERT              AssertionError

 L. 340       352  LOAD_CONST               'wsgi.url_scheme unknown: %r'
              355  LOAD_FAST             0  'environ'
              358  LOAD_CONST               'wsgi.url_scheme'
              361  BINARY_SUBSCR    
              362  BINARY_MODULO    
              363  RAISE_VARARGS_2       2  None

 L. 342       366  LOAD_GLOBAL           8  'check_input'
              369  LOAD_FAST             0  'environ'
              372  LOAD_CONST               'wsgi.input'
              375  BINARY_SUBSCR    
              376  CALL_FUNCTION_1       1  None
              379  POP_TOP          

 L. 343       380  LOAD_GLOBAL           9  'check_errors'
              383  LOAD_FAST             0  'environ'
              386  LOAD_CONST               'wsgi.errors'
              389  BINARY_SUBSCR    
              390  CALL_FUNCTION_1       1  None
              393  POP_TOP          

 L. 346       394  LOAD_FAST             0  'environ'
              397  LOAD_CONST               'REQUEST_METHOD'
              400  BINARY_SUBSCR    
              401  LOAD_GLOBAL          10  'valid_methods'
              404  COMPARE_OP            7  not-in
              407  POP_JUMP_IF_FALSE   437  'to 437'

 L. 347       410  LOAD_GLOBAL           3  'warnings'
              413  LOAD_ATTR             4  'warn'

 L. 348       416  LOAD_CONST               'Unknown REQUEST_METHOD: %r'
              419  LOAD_FAST             0  'environ'
              422  LOAD_CONST               'REQUEST_METHOD'
              425  BINARY_SUBSCR    
              426  BINARY_MODULO    

 L. 349       427  LOAD_GLOBAL           5  'WSGIWarning'
              430  CALL_FUNCTION_2       2  None
              433  POP_TOP          
              434  JUMP_FORWARD          0  'to 437'
            437_0  COME_FROM           434  '434'

 L. 351       437  LOAD_FAST             0  'environ'
              440  LOAD_ATTR            11  'get'
              443  LOAD_CONST               'SCRIPT_NAME'
              446  CALL_FUNCTION_1       1  None
              449  UNARY_NOT        
              450  POP_JUMP_IF_TRUE    489  'to 489'

 L. 352       453  LOAD_FAST             0  'environ'
              456  LOAD_CONST               'SCRIPT_NAME'
              459  BINARY_SUBSCR    
              460  LOAD_ATTR            12  'startswith'
              463  LOAD_CONST               '/'
              466  CALL_FUNCTION_1       1  None
              469  POP_JUMP_IF_TRUE    489  'to 489'
              472  LOAD_ASSERT              AssertionError

 L. 353       475  LOAD_CONST               "SCRIPT_NAME doesn't start with /: %r"
              478  LOAD_FAST             0  'environ'
              481  LOAD_CONST               'SCRIPT_NAME'
              484  BINARY_SUBSCR    
              485  BINARY_MODULO    
              486  RAISE_VARARGS_2       2  None

 L. 354       489  LOAD_FAST             0  'environ'
              492  LOAD_ATTR            11  'get'
              495  LOAD_CONST               'PATH_INFO'
              498  CALL_FUNCTION_1       1  None
              501  UNARY_NOT        
              502  POP_JUMP_IF_TRUE    541  'to 541'

 L. 355       505  LOAD_FAST             0  'environ'
              508  LOAD_CONST               'PATH_INFO'
              511  BINARY_SUBSCR    
              512  LOAD_ATTR            12  'startswith'
              515  LOAD_CONST               '/'
              518  CALL_FUNCTION_1       1  None
              521  POP_JUMP_IF_TRUE    541  'to 541'
              524  LOAD_ASSERT              AssertionError

 L. 356       527  LOAD_CONST               "PATH_INFO doesn't start with /: %r"
              530  LOAD_FAST             0  'environ'
              533  LOAD_CONST               'PATH_INFO'
              536  BINARY_SUBSCR    
              537  BINARY_MODULO    
              538  RAISE_VARARGS_2       2  None

 L. 357       541  LOAD_FAST             0  'environ'
              544  LOAD_ATTR            11  'get'
              547  LOAD_CONST               'CONTENT_LENGTH'
              550  CALL_FUNCTION_1       1  None
              553  POP_JUMP_IF_FALSE   598  'to 598'

 L. 358       556  LOAD_GLOBAL          13  'int'
              559  LOAD_FAST             0  'environ'
              562  LOAD_CONST               'CONTENT_LENGTH'
              565  BINARY_SUBSCR    
              566  CALL_FUNCTION_1       1  None
              569  LOAD_CONST               0
              572  COMPARE_OP            5  >=
              575  POP_JUMP_IF_TRUE    598  'to 598'
              578  LOAD_ASSERT              AssertionError

 L. 359       581  LOAD_CONST               'Invalid CONTENT_LENGTH: %r'
              584  LOAD_FAST             0  'environ'
              587  LOAD_CONST               'CONTENT_LENGTH'
              590  BINARY_SUBSCR    
              591  BINARY_MODULO    
              592  RAISE_VARARGS_2       2  None
              595  JUMP_FORWARD          0  'to 598'
            598_0  COME_FROM           595  '595'

 L. 361       598  LOAD_FAST             0  'environ'
              601  LOAD_ATTR            11  'get'
              604  LOAD_CONST               'SCRIPT_NAME'
              607  CALL_FUNCTION_1       1  None
              610  POP_JUMP_IF_TRUE    637  'to 637'

 L. 362       613  LOAD_CONST               'PATH_INFO'
              616  LOAD_FAST             0  'environ'
              619  COMPARE_OP            6  in
              622  POP_JUMP_IF_TRUE    637  'to 637'
              625  LOAD_ASSERT              AssertionError

 L. 363       628  LOAD_CONST               "One of SCRIPT_NAME or PATH_INFO are required (PATH_INFO should at least be '/' if SCRIPT_NAME is empty)"
              631  RAISE_VARARGS_2       2  None
              634  JUMP_FORWARD          0  'to 637'
            637_0  COME_FROM           634  '634'

 L. 365       637  LOAD_FAST             0  'environ'
              640  LOAD_ATTR            11  'get'
              643  LOAD_CONST               'SCRIPT_NAME'
              646  CALL_FUNCTION_1       1  None
              649  LOAD_CONST               '/'
              652  COMPARE_OP            3  !=
              655  POP_JUMP_IF_TRUE    667  'to 667'
              658  LOAD_ASSERT              AssertionError

 L. 366       661  LOAD_CONST               "SCRIPT_NAME cannot be '/'; it should instead be '', and PATH_INFO should be '/'"
              664  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_CONST' instruction at offset 661


def check_input(wsgi_input):
    for attr in ['read', 'readline', 'readlines', '__iter__']:
        if not hasattr(wsgi_input, attr):
            raise AssertionError, "wsgi.input (%r) doesn't have the attribute %s" % (
             wsgi_input, attr)


def check_errors(wsgi_errors):
    for attr in ['flush', 'write', 'writelines']:
        if not hasattr(wsgi_errors, attr):
            raise AssertionError, "wsgi.errors (%r) doesn't have the attribute %s" % (
             wsgi_errors, attr)


def check_status--- This code section failed: ---

 L. 385         0  LOAD_GLOBAL           0  'type'
                3  LOAD_FAST             0  'status'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_GLOBAL           1  'str'
               12  COMPARE_OP            8  is
               15  POP_JUMP_IF_TRUE     31  'to 31'
               18  LOAD_ASSERT              AssertionError

 L. 386        21  LOAD_CONST               'Status must be a string (not %r)'
               24  LOAD_FAST             0  'status'
               27  BINARY_MODULO    
               28  RAISE_VARARGS_2       2  None

 L. 388        31  LOAD_FAST             0  'status'
               34  LOAD_ATTR             3  'split'
               37  LOAD_CONST               None
               40  LOAD_CONST               1
               43  CALL_FUNCTION_2       2  None
               46  LOAD_CONST               0
               49  BINARY_SUBSCR    
               50  STORE_FAST            1  'status_code'

 L. 389        53  LOAD_GLOBAL           5  'len'
               56  LOAD_FAST             1  'status_code'
               59  CALL_FUNCTION_1       1  None
               62  LOAD_CONST               3
               65  COMPARE_OP            2  ==
               68  POP_JUMP_IF_TRUE     84  'to 84'
               71  LOAD_ASSERT              AssertionError

 L. 390        74  LOAD_CONST               'Status codes must be three characters: %r'
               77  LOAD_FAST             1  'status_code'
               80  BINARY_MODULO    
               81  RAISE_VARARGS_2       2  None

 L. 391        84  LOAD_GLOBAL           6  'int'
               87  LOAD_FAST             1  'status_code'
               90  CALL_FUNCTION_1       1  None
               93  STORE_FAST            2  'status_int'

 L. 392        96  LOAD_FAST             2  'status_int'
               99  LOAD_CONST               100
              102  COMPARE_OP            5  >=
              105  POP_JUMP_IF_TRUE    121  'to 121'
              108  LOAD_ASSERT              AssertionError
              111  LOAD_CONST               'Status code is invalid: %r'
              114  LOAD_FAST             2  'status_int'
              117  BINARY_MODULO    
              118  RAISE_VARARGS_2       2  None

 L. 393       121  LOAD_GLOBAL           5  'len'
              124  LOAD_FAST             0  'status'
              127  CALL_FUNCTION_1       1  None
              130  LOAD_CONST               4
              133  COMPARE_OP            0  <
              136  POP_JUMP_IF_TRUE    155  'to 155'
              139  LOAD_FAST             0  'status'
              142  LOAD_CONST               3
              145  BINARY_SUBSCR    
              146  LOAD_CONST               ' '
              149  COMPARE_OP            3  !=
            152_0  COME_FROM           136  '136'
              152  POP_JUMP_IF_FALSE   178  'to 178'

 L. 394       155  LOAD_GLOBAL           7  'warnings'
              158  LOAD_ATTR             8  'warn'

 L. 395       161  LOAD_CONST               'The status string (%r) should be a three-digit integer followed by a single space and a status explanation'

 L. 397       164  LOAD_FAST             0  'status'
              167  BINARY_MODULO    
              168  LOAD_GLOBAL           9  'WSGIWarning'
              171  CALL_FUNCTION_2       2  None
              174  POP_TOP          
              175  JUMP_FORWARD          0  'to 178'
            178_0  COME_FROM           175  '175'
              178  LOAD_CONST               None
              181  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 178


def check_headers--- This code section failed: ---

 L. 401         0  LOAD_GLOBAL           0  'type'
                3  LOAD_FAST             0  'headers'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_GLOBAL           1  'list'
               12  COMPARE_OP            8  is
               15  POP_JUMP_IF_TRUE     43  'to 43'
               18  LOAD_ASSERT              AssertionError

 L. 402        21  LOAD_CONST               'Headers (%r) must be of type list: %r'

 L. 403        24  LOAD_FAST             0  'headers'
               27  LOAD_GLOBAL           0  'type'
               30  LOAD_FAST             0  'headers'
               33  CALL_FUNCTION_1       1  None
               36  BUILD_TUPLE_2         2 
               39  BINARY_MODULO    
               40  RAISE_VARARGS_2       2  None

 L. 404        43  BUILD_MAP_0           0  None
               46  STORE_FAST            1  'header_names'

 L. 405        49  SETUP_LOOP          303  'to 355'
               52  LOAD_FAST             0  'headers'
               55  GET_ITER         
               56  FOR_ITER            295  'to 354'
               59  STORE_FAST            2  'item'

 L. 406        62  LOAD_GLOBAL           0  'type'
               65  LOAD_FAST             2  'item'
               68  CALL_FUNCTION_1       1  None
               71  LOAD_GLOBAL           3  'tuple'
               74  COMPARE_OP            8  is
               77  POP_JUMP_IF_TRUE    105  'to 105'
               80  LOAD_ASSERT              AssertionError

 L. 407        83  LOAD_CONST               'Individual headers (%r) must be of type tuple: %r'

 L. 408        86  LOAD_FAST             2  'item'
               89  LOAD_GLOBAL           0  'type'
               92  LOAD_FAST             2  'item'
               95  CALL_FUNCTION_1       1  None
               98  BUILD_TUPLE_2         2 
              101  BINARY_MODULO    
              102  RAISE_VARARGS_2       2  None

 L. 409       105  LOAD_GLOBAL           4  'len'
              108  LOAD_FAST             2  'item'
              111  CALL_FUNCTION_1       1  None
              114  LOAD_CONST               2
              117  COMPARE_OP            2  ==
              120  POP_JUMP_IF_TRUE    129  'to 129'
              123  LOAD_ASSERT              AssertionError
              126  RAISE_VARARGS_1       1  None

 L. 410       129  LOAD_FAST             2  'item'
              132  UNPACK_SEQUENCE_2     2 
              135  STORE_FAST            3  'name'
              138  STORE_FAST            4  'value'

 L. 411       141  LOAD_FAST             3  'name'
              144  LOAD_ATTR             5  'lower'
              147  CALL_FUNCTION_0       0  None
              150  LOAD_CONST               'status'
              153  COMPARE_OP            3  !=
              156  POP_JUMP_IF_TRUE    172  'to 172'
              159  LOAD_ASSERT              AssertionError

 L. 412       162  LOAD_CONST               'The Status header cannot be used; it conflicts with CGI script, and HTTP status is not given through headers (value: %r).'

 L. 414       165  LOAD_FAST             4  'value'
              168  BINARY_MODULO    
              169  RAISE_VARARGS_2       2  None

 L. 415       172  LOAD_CONST               None
              175  LOAD_FAST             1  'header_names'
              178  LOAD_FAST             3  'name'
              181  LOAD_ATTR             5  'lower'
              184  CALL_FUNCTION_0       0  None
              187  STORE_SUBSCR     

 L. 416       188  LOAD_CONST               '\n'
              191  LOAD_FAST             3  'name'
              194  COMPARE_OP            7  not-in
              197  POP_JUMP_IF_FALSE   212  'to 212'
              200  LOAD_CONST               ':'
              203  LOAD_FAST             3  'name'
              206  COMPARE_OP            7  not-in
            209_0  COME_FROM           197  '197'
              209  POP_JUMP_IF_TRUE    225  'to 225'
              212  LOAD_ASSERT              AssertionError

 L. 417       215  LOAD_CONST               "Header names may not contain ':' or '\\n': %r"
              218  LOAD_FAST             3  'name'
              221  BINARY_MODULO    
              222  RAISE_VARARGS_2       2  None

 L. 418       225  LOAD_GLOBAL           7  'header_re'
              228  LOAD_ATTR             8  'search'
              231  LOAD_FAST             3  'name'
              234  CALL_FUNCTION_1       1  None
              237  POP_JUMP_IF_TRUE    253  'to 253'
              240  LOAD_ASSERT              AssertionError
              243  LOAD_CONST               'Bad header name: %r'
              246  LOAD_FAST             3  'name'
              249  BINARY_MODULO    
              250  RAISE_VARARGS_2       2  None

 L. 419       253  LOAD_FAST             3  'name'
              256  LOAD_ATTR             9  'endswith'
              259  LOAD_CONST               '-'
              262  CALL_FUNCTION_1       1  None
              265  UNARY_NOT        
              266  POP_JUMP_IF_FALSE   285  'to 285'
              269  LOAD_FAST             3  'name'
              272  LOAD_ATTR             9  'endswith'
              275  LOAD_CONST               '_'
              278  CALL_FUNCTION_1       1  None
              281  UNARY_NOT        
            282_0  COME_FROM           266  '266'
              282  POP_JUMP_IF_TRUE    298  'to 298'
              285  LOAD_ASSERT              AssertionError

 L. 420       288  LOAD_CONST               "Names may not end in '-' or '_': %r"
              291  LOAD_FAST             3  'name'
              294  BINARY_MODULO    
              295  RAISE_VARARGS_2       2  None

 L. 421       298  LOAD_GLOBAL          10  'bad_header_value_re'
              301  LOAD_ATTR             8  'search'
              304  LOAD_FAST             4  'value'
              307  CALL_FUNCTION_1       1  None
              310  UNARY_NOT        
              311  POP_JUMP_IF_TRUE     56  'to 56'
              314  LOAD_ASSERT              AssertionError

 L. 422       317  LOAD_CONST               'Bad header value: %r (bad char: %r)'

 L. 423       320  LOAD_FAST             4  'value'
              323  LOAD_GLOBAL          10  'bad_header_value_re'
              326  LOAD_ATTR             8  'search'
              329  LOAD_FAST             4  'value'
              332  CALL_FUNCTION_1       1  None
              335  LOAD_ATTR            11  'group'
              338  LOAD_CONST               0
              341  CALL_FUNCTION_1       1  None
              344  BUILD_TUPLE_2         2 
              347  BINARY_MODULO    
              348  RAISE_VARARGS_2       2  None
              351  JUMP_BACK            56  'to 56'
              354  POP_BLOCK        
            355_0  COME_FROM            49  '49'
              355  LOAD_CONST               None
              358  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 354


def check_content_type--- This code section failed: ---

 L. 427         0  LOAD_GLOBAL           0  'int'
                3  LOAD_FAST             0  'status'
                6  LOAD_ATTR             1  'split'
                9  LOAD_CONST               None
               12  LOAD_CONST               1
               15  CALL_FUNCTION_2       2  None
               18  LOAD_CONST               0
               21  BINARY_SUBSCR    
               22  CALL_FUNCTION_1       1  None
               25  STORE_FAST            2  'code'

 L. 430        28  LOAD_CONST               (201, 204, 304)
               31  STORE_FAST            3  'NO_MESSAGE_BODY'

 L. 431        34  LOAD_CONST               (204, 304)
               37  STORE_FAST            4  'NO_MESSAGE_TYPE'

 L. 432        40  LOAD_CONST               None
               43  STORE_FAST            5  'length'

 L. 433        46  SETUP_LOOP           65  'to 114'
               49  LOAD_FAST             1  'headers'
               52  GET_ITER         
               53  FOR_ITER             57  'to 113'
               56  UNPACK_SEQUENCE_2     2 
               59  STORE_FAST            6  'name'
               62  STORE_FAST            7  'value'

 L. 434        65  LOAD_FAST             6  'name'
               68  LOAD_ATTR             3  'lower'
               71  CALL_FUNCTION_0       0  None
               74  LOAD_CONST               'content-length'
               77  COMPARE_OP            2  ==
               80  POP_JUMP_IF_FALSE    53  'to 53'
               83  LOAD_FAST             7  'value'
               86  LOAD_ATTR             4  'isdigit'
               89  CALL_FUNCTION_0       0  None
             92_0  COME_FROM            80  '80'
               92  POP_JUMP_IF_FALSE    53  'to 53'

 L. 435        95  LOAD_GLOBAL           0  'int'
               98  LOAD_FAST             7  'value'
              101  CALL_FUNCTION_1       1  None
              104  STORE_FAST            5  'length'
              107  JUMP_BACK            53  'to 53'
              110  JUMP_BACK            53  'to 53'
              113  POP_BLOCK        
            114_0  COME_FROM            46  '46'

 L. 436       114  SETUP_LOOP          112  'to 229'
              117  LOAD_FAST             1  'headers'
              120  GET_ITER         
              121  FOR_ITER            104  'to 228'
              124  UNPACK_SEQUENCE_2     2 
              127  STORE_FAST            6  'name'
              130  STORE_FAST            7  'value'

 L. 437       133  LOAD_FAST             6  'name'
              136  LOAD_ATTR             3  'lower'
              139  CALL_FUNCTION_0       0  None
              142  LOAD_CONST               'content-type'
              145  COMPARE_OP            2  ==
              148  POP_JUMP_IF_FALSE   121  'to 121'

 L. 438       151  LOAD_FAST             2  'code'
              154  LOAD_FAST             4  'NO_MESSAGE_TYPE'
              157  COMPARE_OP            7  not-in
              160  POP_JUMP_IF_FALSE   167  'to 167'

 L. 439       163  LOAD_CONST               None
              166  RETURN_END_IF    
            167_0  COME_FROM           160  '160'

 L. 440       167  LOAD_FAST             5  'length'
              170  LOAD_CONST               0
              173  COMPARE_OP            2  ==
              176  POP_JUMP_IF_FALSE   203  'to 203'

 L. 441       179  LOAD_GLOBAL           5  'warnings'
              182  LOAD_ATTR             6  'warn'
              185  LOAD_CONST               'Content-Type header found in a %s response, which not return content.'

 L. 442       188  LOAD_FAST             2  'code'
              191  BINARY_MODULO    

 L. 443       192  LOAD_GLOBAL           7  'WSGIWarning'
              195  CALL_FUNCTION_2       2  None
              198  POP_TOP          

 L. 444       199  LOAD_CONST               None
              202  RETURN_END_IF    
            203_0  COME_FROM           176  '176'

 L. 446       203  LOAD_CONST               0
              206  POP_JUMP_IF_TRUE    225  'to 225'
              209  LOAD_ASSERT              AssertionError
              212  LOAD_CONST               'Content-Type header found in a %s response, which must not return content.'

 L. 447       215  LOAD_FAST             2  'code'
              218  BINARY_MODULO    
              219  RAISE_VARARGS_2       2  None
              222  JUMP_BACK           121  'to 121'
              225  JUMP_BACK           121  'to 121'
              228  POP_BLOCK        
            229_0  COME_FROM           114  '114'

 L. 448       229  LOAD_FAST             2  'code'
              232  LOAD_FAST             3  'NO_MESSAGE_BODY'
              235  COMPARE_OP            7  not-in
              238  POP_JUMP_IF_FALSE   287  'to 287'
              241  LOAD_FAST             5  'length'
              244  LOAD_CONST               None
              247  COMPARE_OP            9  is-not
              250  POP_JUMP_IF_FALSE   287  'to 287'
              253  LOAD_FAST             5  'length'
              256  LOAD_CONST               0
              259  COMPARE_OP            4  >
            262_0  COME_FROM           250  '250'
            262_1  COME_FROM           238  '238'
              262  POP_JUMP_IF_FALSE   287  'to 287'

 L. 449       265  LOAD_CONST               0
              268  POP_JUMP_IF_TRUE    287  'to 287'
              271  LOAD_ASSERT              AssertionError
              274  LOAD_CONST               'No Content-Type header found in headers (%s)'
              277  LOAD_FAST             1  'headers'
              280  BINARY_MODULO    
              281  RAISE_VARARGS_2       2  None
              284  JUMP_FORWARD          0  'to 287'
            287_0  COME_FROM           284  '284'
              287  LOAD_CONST               None
              290  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 228


def check_exc_info--- This code section failed: ---

 L. 453         0  LOAD_FAST             0  'exc_info'
                3  LOAD_CONST               None
                6  COMPARE_OP            8  is
                9  POP_JUMP_IF_TRUE     61  'to 61'
               12  LOAD_GLOBAL           1  'type'
               15  LOAD_FAST             0  'exc_info'
               18  CALL_FUNCTION_1       1  None
               21  LOAD_GLOBAL           1  'type'
               24  LOAD_CONST               ()
               27  CALL_FUNCTION_1       1  None
               30  COMPARE_OP            8  is
               33  POP_JUMP_IF_TRUE     61  'to 61'
               36  LOAD_ASSERT              AssertionError

 L. 454        39  LOAD_CONST               'exc_info (%r) is not a tuple: %r'
               42  LOAD_FAST             0  'exc_info'
               45  LOAD_GLOBAL           1  'type'
               48  LOAD_FAST             0  'exc_info'
               51  CALL_FUNCTION_1       1  None
               54  BUILD_TUPLE_2         2 
               57  BINARY_MODULO    
               58  RAISE_VARARGS_2       2  None
               61  LOAD_CONST               None
               64  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 61


def check_iterator--- This code section failed: ---

 L. 462         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             0  'iterator'
                6  LOAD_GLOBAL           1  'str'
                9  CALL_FUNCTION_2       2  None
               12  UNARY_NOT        
               13  POP_JUMP_IF_TRUE     25  'to 25'
               16  LOAD_ASSERT              AssertionError

 L. 463        19  LOAD_CONST               'You should not return a string as your application iterator, instead return a single-item list containing that string.'
               22  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_CONST' instruction at offset 19


def make_middleware(application, global_conf):
    return middleware(application)


make_middleware.__doc__ = __doc__
__all__ = [
 'middleware', 'make_middleware']