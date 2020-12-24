# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/substrate/data/local/substrate/lib/webtest/lint3.py
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
from __future__ import unicode_literals
import re, sys, warnings
from webtest.compat import to_string
header_re = re.compile(b'^[a-zA-Z][a-zA-Z0-9\\-_]*$')
bad_header_value_re = re.compile(b'[\\000-\\037]')
valid_methods = ('GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'DELETE', 'TRACE', 'PATCH')
METADATA_TYPE = (
 str, bytes)

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

 L. 150         0  LOAD_GLOBAL           0  'len'
                3  LOAD_FAST             0  'args'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_CONST               2
               12  COMPARE_OP            2  ==
               15  POP_JUMP_IF_TRUE     27  'to 27'
               18  LOAD_ASSERT              AssertionError
               21  LOAD_CONST               'Two arguments required'
               24  RAISE_VARARGS_2       2  None

 L. 151        27  LOAD_FAST             1  'kw'
               30  UNARY_NOT        
               31  POP_JUMP_IF_TRUE     43  'to 43'
               34  LOAD_ASSERT              AssertionError
               37  LOAD_CONST               'No keyword arguments allowed'
               40  RAISE_VARARGS_2       2  None

 L. 152        43  LOAD_FAST             0  'args'
               46  UNPACK_SEQUENCE_2     2 
               49  STORE_FAST            2  'environ'
               52  STORE_DEREF           0  'start_response'

 L. 154        55  LOAD_GLOBAL           2  'check_environ'
               58  LOAD_FAST             2  'environ'
               61  CALL_FUNCTION_1       1  None
               64  POP_TOP          

 L. 158        65  BUILD_LIST_0          0 
               68  STORE_DEREF           1  'start_response_started'

 L. 160        71  LOAD_CLOSURE          0  'start_response'
               74  LOAD_CLOSURE          1  'start_response_started'
               80  LOAD_CODE                <code_object start_response_wrapper>
               83  MAKE_CLOSURE_0        0  None
               86  STORE_FAST            3  'start_response_wrapper'

 L. 179        89  LOAD_GLOBAL           3  'InputWrapper'
               92  LOAD_FAST             2  'environ'
               95  LOAD_CONST               'wsgi.input'
               98  BINARY_SUBSCR    
               99  CALL_FUNCTION_1       1  None
              102  LOAD_FAST             2  'environ'
              105  LOAD_CONST               'wsgi.input'
              108  STORE_SUBSCR     

 L. 180       109  LOAD_GLOBAL           4  'ErrorWrapper'
              112  LOAD_FAST             2  'environ'
              115  LOAD_CONST               'wsgi.errors'
              118  BINARY_SUBSCR    
              119  CALL_FUNCTION_1       1  None
              122  LOAD_FAST             2  'environ'
              125  LOAD_CONST               'wsgi.errors'
              128  STORE_SUBSCR     

 L. 182       129  LOAD_DEREF            2  'application'
              132  LOAD_FAST             2  'environ'
              135  LOAD_FAST             3  'start_response_wrapper'
              138  CALL_FUNCTION_2       2  None
              141  STORE_FAST            4  'iterator'

 L. 183       144  LOAD_FAST             4  'iterator'
              147  LOAD_CONST               None
              150  COMPARE_OP            9  is-not
              153  POP_JUMP_IF_FALSE   168  'to 168'
              156  LOAD_FAST             4  'iterator'
              159  LOAD_GLOBAL           6  'False'
              162  COMPARE_OP            3  !=
            165_0  COME_FROM           153  '153'
              165  POP_JUMP_IF_TRUE    177  'to 177'
              168  LOAD_ASSERT              AssertionError

 L. 184       171  LOAD_CONST               'The application must return an iterator, if only an empty list'
              174  RAISE_VARARGS_2       2  None

 L. 186       177  LOAD_GLOBAL           7  'check_iterator'
              180  LOAD_FAST             4  'iterator'
              183  CALL_FUNCTION_1       1  None
              186  POP_TOP          

 L. 188       187  LOAD_GLOBAL           8  'IteratorWrapper'
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
        assert type(v) is bytes
        return v

    def readline(self, *args):
        v = self.input.readline(*args)
        assert type(v) is bytes
        return v

    def readlines(self, *args):
        assert len(args) <= 1
        lines = self.input.readlines(*args)
        assert type(lines) is type([])
        for line in lines:
            assert type(line) is bytes

        return lines

    def __iter__(self):
        while 1:
            line = self.readline()
            if not line:
                return
            yield line

    def close--- This code section failed: ---

 L. 225         0  LOAD_CONST               0
                3  POP_JUMP_IF_TRUE     15  'to 15'
                6  LOAD_ASSERT              AssertionError
                9  LOAD_CONST               'input.close() must not be called'
               12  RAISE_VARARGS_2       2  None

Parse error at or near `None' instruction at offset -1


class ErrorWrapper(object):

    def __init__(self, wsgi_errors):
        self.errors = wsgi_errors

    def write(self, s):
        assert type(s) is bytes
        self.errors.write(s)

    def flush(self):
        self.errors.flush()

    def writelines(self, seq):
        for line in seq:
            self.write(line)

    def close--- This code section failed: ---

 L. 245         0  LOAD_CONST               0
                3  POP_JUMP_IF_TRUE     15  'to 15'
                6  LOAD_ASSERT              AssertionError
                9  LOAD_CONST               'errors.close() must not be called'
               12  RAISE_VARARGS_2       2  None

Parse error at or near `None' instruction at offset -1


class WriteWrapper(object):

    def __init__(self, wsgi_writer):
        self.writer = wsgi_writer

    def __call__(self, s):
        assert type(s) is bytes
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

 L. 280         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'closed'
                6  UNARY_NOT        
                7  POP_JUMP_IF_TRUE     19  'to 19'
               10  LOAD_ASSERT              AssertionError

 L. 281        13  LOAD_CONST               'Iterator read after closed'
               16  RAISE_VARARGS_2       2  None

 L. 282        19  LOAD_GLOBAL           2  'next'
               22  LOAD_FAST             0  'self'
               25  LOAD_ATTR             3  'iterator'
               28  CALL_FUNCTION_1       1  None
               31  STORE_FAST            1  'v'

 L. 283        34  LOAD_FAST             0  'self'
               37  LOAD_ATTR             4  'check_start_response'
               40  LOAD_CONST               None
               43  COMPARE_OP            9  is-not
               46  POP_JUMP_IF_FALSE    79  'to 79'

 L. 284        49  LOAD_FAST             0  'self'
               52  LOAD_ATTR             4  'check_start_response'
               55  POP_JUMP_IF_TRUE     67  'to 67'
               58  LOAD_ASSERT              AssertionError

 L. 285        61  LOAD_CONST               'The application returns and we started iterating over its body, but start_response has not yet been called'
               64  RAISE_VARARGS_2       2  None

 L. 287        67  LOAD_CONST               None
               70  LOAD_FAST             0  'self'
               73  STORE_ATTR            4  'check_start_response'
               76  JUMP_FORWARD          0  'to 79'
             79_0  COME_FROM            76  '76'

 L. 288        79  LOAD_GLOBAL           6  'isinstance'
               82  LOAD_FAST             1  'v'
               85  LOAD_GLOBAL           7  'bytes'
               88  CALL_FUNCTION_2       2  None
               91  POP_JUMP_IF_TRUE    119  'to 119'
               94  LOAD_ASSERT              AssertionError

 L. 289        97  LOAD_CONST               'Iterator %r returned a non-%r object: %r'

 L. 290       100  LOAD_FAST             0  'self'
              103  LOAD_ATTR             3  'iterator'
              106  LOAD_GLOBAL           7  'bytes'
              109  LOAD_FAST             1  'v'
              112  BUILD_TUPLE_3         3 
              115  BINARY_MODULO    
              116  RAISE_VARARGS_2       2  None

 L. 291       119  LOAD_FAST             1  'v'
              122  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 119

    __next__ = next

    def close(self):
        self.closed = True
        if hasattr(self.original_iterator, b'close'):
            self.original_iterator.close()

    def __del__--- This code section failed: ---

 L. 301         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'closed'
                6  POP_JUMP_IF_TRUE     28  'to 28'

 L. 302         9  LOAD_GLOBAL           1  'sys'
               12  LOAD_ATTR             2  'stderr'
               15  LOAD_ATTR             3  'write'

 L. 303        18  LOAD_CONST               'Iterator garbage collected without being closed'
               21  CALL_FUNCTION_1       1  None
               24  POP_TOP          
               25  JUMP_FORWARD          0  'to 28'
             28_0  COME_FROM            25  '25'

 L. 304        28  LOAD_FAST             0  'self'
               31  LOAD_ATTR             0  'closed'
               34  POP_JUMP_IF_TRUE     46  'to 46'
               37  LOAD_ASSERT              AssertionError

 L. 305        40  LOAD_CONST               'Iterator garbage collected without being closed'
               43  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_CONST' instruction at offset 40


def check_environ--- This code section failed: ---

 L. 309         0  LOAD_GLOBAL           0  'type'
                3  LOAD_FAST             0  'environ'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_GLOBAL           1  'dict'
               12  COMPARE_OP            8  is
               15  POP_JUMP_IF_TRUE     43  'to 43'
               18  LOAD_ASSERT              AssertionError

 L. 310        21  LOAD_CONST               'Environment is not of the right type: %r (environment: %r)'

 L. 311        24  LOAD_GLOBAL           0  'type'
               27  LOAD_FAST             0  'environ'
               30  CALL_FUNCTION_1       1  None
               33  LOAD_FAST             0  'environ'
               36  BUILD_TUPLE_2         2 
               39  BINARY_MODULO    
               40  RAISE_VARARGS_2       2  None

 L. 313        43  SETUP_LOOP           66  'to 112'
               46  LOAD_CONST               'REQUEST_METHOD'
               49  LOAD_CONST               'SERVER_NAME'
               52  LOAD_CONST               'SERVER_PORT'

 L. 314        55  LOAD_CONST               'wsgi.version'
               58  LOAD_CONST               'wsgi.input'
               61  LOAD_CONST               'wsgi.errors'

 L. 315        64  LOAD_CONST               'wsgi.multithread'
               67  LOAD_CONST               'wsgi.multiprocess'

 L. 316        70  LOAD_CONST               'wsgi.run_once'
               73  BUILD_LIST_9          9 
               76  GET_ITER         
               77  FOR_ITER             31  'to 111'
               80  STORE_FAST            1  'key'

 L. 317        83  LOAD_FAST             1  'key'
               86  LOAD_FAST             0  'environ'
               89  COMPARE_OP            6  in
               92  POP_JUMP_IF_TRUE     77  'to 77'
               95  LOAD_ASSERT              AssertionError

 L. 318        98  LOAD_CONST               'Environment missing required key: %r'
              101  LOAD_FAST             1  'key'
              104  BINARY_MODULO    
              105  RAISE_VARARGS_2       2  None
              108  JUMP_BACK            77  'to 77'
              111  POP_BLOCK        
            112_0  COME_FROM            43  '43'

 L. 320       112  SETUP_LOOP           55  'to 170'
              115  LOAD_CONST               'HTTP_CONTENT_TYPE'
              118  LOAD_CONST               'HTTP_CONTENT_LENGTH'
              121  BUILD_LIST_2          2 
              124  GET_ITER         
              125  FOR_ITER             41  'to 169'
              128  STORE_FAST            1  'key'

 L. 321       131  LOAD_FAST             1  'key'
              134  LOAD_FAST             0  'environ'
              137  COMPARE_OP            7  not-in
              140  POP_JUMP_IF_TRUE    125  'to 125'
              143  LOAD_ASSERT              AssertionError

 L. 322       146  LOAD_CONST               'Environment should not have the key: %s (use %s instead)'

 L. 323       149  LOAD_FAST             1  'key'
              152  LOAD_FAST             1  'key'
              155  LOAD_CONST               5
              158  SLICE+1          
              159  BUILD_TUPLE_2         2 
              162  BINARY_MODULO    
              163  RAISE_VARARGS_2       2  None
              166  JUMP_BACK           125  'to 125'
              169  POP_BLOCK        
            170_0  COME_FROM           112  '112'

 L. 325       170  LOAD_CONST               'QUERY_STRING'
              173  LOAD_FAST             0  'environ'
              176  COMPARE_OP            7  not-in
              179  POP_JUMP_IF_FALSE   201  'to 201'

 L. 326       182  LOAD_GLOBAL           3  'warnings'
              185  LOAD_ATTR             4  'warn'

 L. 327       188  LOAD_CONST               'QUERY_STRING is not in the WSGI environment; the cgi module will use sys.argv when this variable is missing, so application errors are more likely'

 L. 330       191  LOAD_GLOBAL           5  'WSGIWarning'
              194  CALL_FUNCTION_2       2  None
              197  POP_TOP          
              198  JUMP_FORWARD          0  'to 201'
            201_0  COME_FROM           198  '198'

 L. 332       201  SETUP_LOOP           90  'to 294'
              204  LOAD_FAST             0  'environ'
              207  GET_ITER         
              208  FOR_ITER             82  'to 293'
              211  STORE_FAST            1  'key'

 L. 333       214  LOAD_CONST               '.'
              217  LOAD_FAST             1  'key'
              220  COMPARE_OP            6  in
              223  POP_JUMP_IF_FALSE   232  'to 232'

 L. 335       226  CONTINUE            208  'to 208'
              229  JUMP_FORWARD          0  'to 232'
            232_0  COME_FROM           229  '229'

 L. 336       232  LOAD_GLOBAL           0  'type'
              235  LOAD_FAST             0  'environ'
              238  LOAD_FAST             1  'key'
              241  BINARY_SUBSCR    
              242  CALL_FUNCTION_1       1  None
              245  LOAD_GLOBAL           6  'METADATA_TYPE'
              248  COMPARE_OP            6  in
              251  POP_JUMP_IF_TRUE    208  'to 208'
              254  LOAD_ASSERT              AssertionError

 L. 337       257  LOAD_CONST               'Environmental variable %s is not a string: %r (value: %r)'

 L. 338       260  LOAD_FAST             1  'key'
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

 L. 340       294  LOAD_GLOBAL           0  'type'
              297  LOAD_FAST             0  'environ'
              300  LOAD_CONST               'wsgi.version'
              303  BINARY_SUBSCR    
              304  CALL_FUNCTION_1       1  None
              307  LOAD_GLOBAL           7  'tuple'
              310  COMPARE_OP            8  is
              313  POP_JUMP_IF_TRUE    333  'to 333'
              316  LOAD_ASSERT              AssertionError

 L. 341       319  LOAD_CONST               'wsgi.version should be a tuple (%r)'
              322  LOAD_FAST             0  'environ'
              325  LOAD_CONST               'wsgi.version'
              328  BINARY_SUBSCR    
              329  BINARY_MODULO    
              330  RAISE_VARARGS_2       2  None

 L. 342       333  LOAD_FAST             0  'environ'
              336  LOAD_CONST               'wsgi.url_scheme'
              339  BINARY_SUBSCR    
              340  LOAD_CONST               ('http', 'https')
              343  COMPARE_OP            6  in
              346  POP_JUMP_IF_TRUE    366  'to 366'
              349  LOAD_ASSERT              AssertionError

 L. 343       352  LOAD_CONST               'wsgi.url_scheme unknown: %r'
              355  LOAD_FAST             0  'environ'
              358  LOAD_CONST               'wsgi.url_scheme'
              361  BINARY_SUBSCR    
              362  BINARY_MODULO    
              363  RAISE_VARARGS_2       2  None

 L. 345       366  LOAD_GLOBAL           8  'check_input'
              369  LOAD_FAST             0  'environ'
              372  LOAD_CONST               'wsgi.input'
              375  BINARY_SUBSCR    
              376  CALL_FUNCTION_1       1  None
              379  POP_TOP          

 L. 346       380  LOAD_GLOBAL           9  'check_errors'
              383  LOAD_FAST             0  'environ'
              386  LOAD_CONST               'wsgi.errors'
              389  BINARY_SUBSCR    
              390  CALL_FUNCTION_1       1  None
              393  POP_TOP          

 L. 349       394  LOAD_FAST             0  'environ'
              397  LOAD_CONST               'REQUEST_METHOD'
              400  BINARY_SUBSCR    
              401  LOAD_GLOBAL          10  'valid_methods'
              404  COMPARE_OP            7  not-in
              407  POP_JUMP_IF_FALSE   437  'to 437'

 L. 350       410  LOAD_GLOBAL           3  'warnings'
              413  LOAD_ATTR             4  'warn'

 L. 351       416  LOAD_CONST               'Unknown REQUEST_METHOD: %r'
              419  LOAD_FAST             0  'environ'
              422  LOAD_CONST               'REQUEST_METHOD'
              425  BINARY_SUBSCR    
              426  BINARY_MODULO    

 L. 352       427  LOAD_GLOBAL           5  'WSGIWarning'
              430  CALL_FUNCTION_2       2  None
              433  POP_TOP          
              434  JUMP_FORWARD          0  'to 437'
            437_0  COME_FROM           434  '434'

 L. 354       437  LOAD_FAST             0  'environ'
              440  LOAD_ATTR            11  'get'
              443  LOAD_CONST               'SCRIPT_NAME'
              446  CALL_FUNCTION_1       1  None
              449  UNARY_NOT        
              450  POP_JUMP_IF_TRUE    489  'to 489'

 L. 355       453  LOAD_FAST             0  'environ'
              456  LOAD_CONST               'SCRIPT_NAME'
              459  BINARY_SUBSCR    
              460  LOAD_ATTR            12  'startswith'
              463  LOAD_CONST               '/'
              466  CALL_FUNCTION_1       1  None
              469  POP_JUMP_IF_TRUE    489  'to 489'
              472  LOAD_ASSERT              AssertionError

 L. 356       475  LOAD_CONST               "SCRIPT_NAME doesn't start with /: %r"
              478  LOAD_FAST             0  'environ'
              481  LOAD_CONST               'SCRIPT_NAME'
              484  BINARY_SUBSCR    
              485  BINARY_MODULO    
              486  RAISE_VARARGS_2       2  None

 L. 357       489  LOAD_FAST             0  'environ'
              492  LOAD_ATTR            11  'get'
              495  LOAD_CONST               'PATH_INFO'
              498  CALL_FUNCTION_1       1  None
              501  UNARY_NOT        
              502  POP_JUMP_IF_TRUE    541  'to 541'

 L. 358       505  LOAD_FAST             0  'environ'
              508  LOAD_CONST               'PATH_INFO'
              511  BINARY_SUBSCR    
              512  LOAD_ATTR            12  'startswith'
              515  LOAD_CONST               '/'
              518  CALL_FUNCTION_1       1  None
              521  POP_JUMP_IF_TRUE    541  'to 541'
              524  LOAD_ASSERT              AssertionError

 L. 359       527  LOAD_CONST               "PATH_INFO doesn't start with /: %r"
              530  LOAD_FAST             0  'environ'
              533  LOAD_CONST               'PATH_INFO'
              536  BINARY_SUBSCR    
              537  BINARY_MODULO    
              538  RAISE_VARARGS_2       2  None

 L. 360       541  LOAD_FAST             0  'environ'
              544  LOAD_ATTR            11  'get'
              547  LOAD_CONST               'CONTENT_LENGTH'
              550  CALL_FUNCTION_1       1  None
              553  POP_JUMP_IF_FALSE   598  'to 598'

 L. 361       556  LOAD_GLOBAL          13  'int'
              559  LOAD_FAST             0  'environ'
              562  LOAD_CONST               'CONTENT_LENGTH'
              565  BINARY_SUBSCR    
              566  CALL_FUNCTION_1       1  None
              569  LOAD_CONST               0
              572  COMPARE_OP            5  >=
              575  POP_JUMP_IF_TRUE    598  'to 598'
              578  LOAD_ASSERT              AssertionError

 L. 362       581  LOAD_CONST               'Invalid CONTENT_LENGTH: %r'
              584  LOAD_FAST             0  'environ'
              587  LOAD_CONST               'CONTENT_LENGTH'
              590  BINARY_SUBSCR    
              591  BINARY_MODULO    
              592  RAISE_VARARGS_2       2  None
              595  JUMP_FORWARD          0  'to 598'
            598_0  COME_FROM           595  '595'

 L. 364       598  LOAD_FAST             0  'environ'
              601  LOAD_ATTR            11  'get'
              604  LOAD_CONST               'SCRIPT_NAME'
              607  CALL_FUNCTION_1       1  None
              610  POP_JUMP_IF_TRUE    637  'to 637'

 L. 365       613  LOAD_CONST               'PATH_INFO'
              616  LOAD_FAST             0  'environ'
              619  COMPARE_OP            6  in
              622  POP_JUMP_IF_TRUE    637  'to 637'
              625  LOAD_ASSERT              AssertionError

 L. 366       628  LOAD_CONST               "One of SCRIPT_NAME or PATH_INFO are required (PATH_INFO should at least be '/' if SCRIPT_NAME is empty)"
              631  RAISE_VARARGS_2       2  None
              634  JUMP_FORWARD          0  'to 637'
            637_0  COME_FROM           634  '634'

 L. 368       637  LOAD_FAST             0  'environ'
              640  LOAD_ATTR            11  'get'
              643  LOAD_CONST               'SCRIPT_NAME'
              646  CALL_FUNCTION_1       1  None
              649  LOAD_CONST               '/'
              652  COMPARE_OP            3  !=
              655  POP_JUMP_IF_TRUE    667  'to 667'
              658  LOAD_ASSERT              AssertionError

 L. 369       661  LOAD_CONST               "SCRIPT_NAME cannot be '/'; it should instead be '', and PATH_INFO should be '/'"
              664  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_CONST' instruction at offset 661


def check_input(wsgi_input):
    for attr in [b'read', b'readline', b'readlines', b'__iter__']:
        if not hasattr(wsgi_input, attr):
            raise AssertionError, b"wsgi.input (%r) doesn't have the attribute %s" % (
             wsgi_input, attr)


def check_errors(wsgi_errors):
    for attr in [b'flush', b'write', b'writelines']:
        if not hasattr(wsgi_errors, attr):
            raise AssertionError, b"wsgi.errors (%r) doesn't have the attribute %s" % (
             wsgi_errors, attr)


def check_status--- This code section failed: ---

 L. 388         0  LOAD_GLOBAL           0  'type'
                3  LOAD_FAST             0  'status'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_GLOBAL           1  'METADATA_TYPE'
               12  COMPARE_OP            6  in
               15  POP_JUMP_IF_TRUE     37  'to 37'
               18  LOAD_ASSERT              AssertionError

 L. 389        21  LOAD_CONST               'Status must be a %s (not %r)'
               24  LOAD_GLOBAL           1  'METADATA_TYPE'
               27  LOAD_FAST             0  'status'
               30  BUILD_TUPLE_2         2 
               33  BINARY_MODULO    
               34  RAISE_VARARGS_2       2  None

 L. 391        37  LOAD_FAST             0  'status'
               40  LOAD_ATTR             3  'split'
               43  LOAD_CONST               None
               46  LOAD_CONST               1
               49  CALL_FUNCTION_2       2  None
               52  LOAD_CONST               0
               55  BINARY_SUBSCR    
               56  STORE_FAST            1  'status_code'

 L. 392        59  LOAD_GLOBAL           5  'len'
               62  LOAD_FAST             1  'status_code'
               65  CALL_FUNCTION_1       1  None
               68  LOAD_CONST               3
               71  COMPARE_OP            2  ==
               74  POP_JUMP_IF_TRUE     90  'to 90'
               77  LOAD_ASSERT              AssertionError

 L. 393        80  LOAD_CONST               'Status codes must be three characters: %r'
               83  LOAD_FAST             1  'status_code'
               86  BINARY_MODULO    
               87  RAISE_VARARGS_2       2  None

 L. 394        90  LOAD_GLOBAL           6  'int'
               93  LOAD_FAST             1  'status_code'
               96  CALL_FUNCTION_1       1  None
               99  STORE_FAST            2  'status_int'

 L. 395       102  LOAD_FAST             2  'status_int'
              105  LOAD_CONST               100
              108  COMPARE_OP            5  >=
              111  POP_JUMP_IF_TRUE    127  'to 127'
              114  LOAD_ASSERT              AssertionError
              117  LOAD_CONST               'Status code is invalid: %r'
              120  LOAD_FAST             2  'status_int'
              123  BINARY_MODULO    
              124  RAISE_VARARGS_2       2  None

 L. 396       127  LOAD_GLOBAL           5  'len'
              130  LOAD_FAST             0  'status'
              133  CALL_FUNCTION_1       1  None
              136  LOAD_CONST               4
              139  COMPARE_OP            0  <
              142  POP_JUMP_IF_TRUE    161  'to 161'
              145  LOAD_FAST             0  'status'
              148  LOAD_CONST               3
              151  BINARY_SUBSCR    
              152  LOAD_CONST               ' '
              155  COMPARE_OP            3  !=
            158_0  COME_FROM           142  '142'
              158  POP_JUMP_IF_FALSE   184  'to 184'

 L. 397       161  LOAD_GLOBAL           7  'warnings'
              164  LOAD_ATTR             8  'warn'

 L. 398       167  LOAD_CONST               'The status string (%r) should be a three-digit integer followed by a single space and a status explanation'

 L. 400       170  LOAD_FAST             0  'status'
              173  BINARY_MODULO    
              174  LOAD_GLOBAL           9  'WSGIWarning'
              177  CALL_FUNCTION_2       2  None
              180  POP_TOP          
              181  JUMP_FORWARD          0  'to 184'
            184_0  COME_FROM           181  '181'
              184  LOAD_CONST               None
              187  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 184


def check_headers--- This code section failed: ---

 L. 404         0  LOAD_GLOBAL           0  'type'
                3  LOAD_FAST             0  'headers'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_GLOBAL           1  'list'
               12  COMPARE_OP            8  is
               15  POP_JUMP_IF_TRUE     43  'to 43'
               18  LOAD_ASSERT              AssertionError

 L. 405        21  LOAD_CONST               'Headers (%r) must be of type list: %r'

 L. 406        24  LOAD_FAST             0  'headers'
               27  LOAD_GLOBAL           0  'type'
               30  LOAD_FAST             0  'headers'
               33  CALL_FUNCTION_1       1  None
               36  BUILD_TUPLE_2         2 
               39  BINARY_MODULO    
               40  RAISE_VARARGS_2       2  None

 L. 407        43  SETUP_LOOP          465  'to 511'
               46  LOAD_FAST             0  'headers'
               49  GET_ITER         
               50  FOR_ITER            457  'to 510'
               53  STORE_FAST            1  'item'

 L. 408        56  LOAD_GLOBAL           0  'type'
               59  LOAD_FAST             1  'item'
               62  CALL_FUNCTION_1       1  None
               65  LOAD_GLOBAL           3  'tuple'
               68  COMPARE_OP            8  is
               71  POP_JUMP_IF_TRUE     99  'to 99'
               74  LOAD_ASSERT              AssertionError

 L. 409        77  LOAD_CONST               'Individual headers (%r) must be of type tuple: %r'

 L. 410        80  LOAD_FAST             1  'item'
               83  LOAD_GLOBAL           0  'type'
               86  LOAD_FAST             1  'item'
               89  CALL_FUNCTION_1       1  None
               92  BUILD_TUPLE_2         2 
               95  BINARY_MODULO    
               96  RAISE_VARARGS_2       2  None

 L. 411        99  LOAD_GLOBAL           4  'len'
              102  LOAD_FAST             1  'item'
              105  CALL_FUNCTION_1       1  None
              108  LOAD_CONST               2
              111  COMPARE_OP            2  ==
              114  POP_JUMP_IF_TRUE    123  'to 123'
              117  LOAD_ASSERT              AssertionError
              120  RAISE_VARARGS_1       1  None

 L. 412       123  LOAD_FAST             1  'item'
              126  UNPACK_SEQUENCE_2     2 
              129  STORE_FAST            2  'name'
              132  STORE_FAST            3  'value'

 L. 413       135  LOAD_GLOBAL           0  'type'
              138  LOAD_FAST             2  'name'
              141  CALL_FUNCTION_1       1  None
              144  LOAD_GLOBAL           5  'str'
              147  COMPARE_OP            8  is
              150  POP_JUMP_IF_FALSE   212  'to 212'

 L. 414       153  SETUP_EXCEPT         17  'to 173'

 L. 415       156  LOAD_FAST             2  'name'
              159  LOAD_ATTR             6  'encode'
              162  LOAD_CONST               'latin1'
              165  CALL_FUNCTION_1       1  None
              168  POP_TOP          
              169  POP_BLOCK        
              170  JUMP_ABSOLUTE       212  'to 212'
            173_0  COME_FROM           153  '153'

 L. 416       173  DUP_TOP          
              174  LOAD_GLOBAL           7  'UnicodeEncodeError'
              177  COMPARE_OP           10  exception-match
              180  POP_JUMP_IF_FALSE   208  'to 208'
              183  POP_TOP          
              184  POP_TOP          
              185  POP_TOP          

 L. 417       186  LOAD_GLOBAL           2  'AssertionError'

 L. 418       189  LOAD_CONST               'Headers name must be latin1 string or bytes.%r is not a valid latin1 string'

 L. 419       192  LOAD_FAST             2  'name'
              195  BUILD_TUPLE_1         1 
              198  BINARY_MODULO    
              199  CALL_FUNCTION_1       1  None
              202  RAISE_VARARGS_1       1  None
              205  JUMP_ABSOLUTE       212  'to 212'
              208  END_FINALLY      
            209_0  COME_FROM           208  '208'
              209  JUMP_FORWARD          0  'to 212'
            212_0  COME_FROM           209  '209'

 L. 420       212  LOAD_GLOBAL           8  'to_string'
              215  LOAD_FAST             2  'name'
              218  CALL_FUNCTION_1       1  None
              221  STORE_FAST            4  'str_name'

 L. 421       224  LOAD_FAST             4  'str_name'
              227  LOAD_ATTR             9  'lower'
              230  CALL_FUNCTION_0       0  None
              233  LOAD_CONST               'status'
              236  COMPARE_OP            3  !=
              239  POP_JUMP_IF_TRUE    255  'to 255'
              242  LOAD_ASSERT              AssertionError

 L. 422       245  LOAD_CONST               'The Status header cannot be used; it conflicts with CGI script, and HTTP status is not given through headers (value: %r).'

 L. 424       248  LOAD_FAST             3  'value'
              251  BINARY_MODULO    
              252  RAISE_VARARGS_2       2  None

 L. 425       255  LOAD_CONST               '\n'
              258  LOAD_FAST             4  'str_name'
              261  COMPARE_OP            7  not-in
              264  POP_JUMP_IF_FALSE   279  'to 279'
              267  LOAD_CONST               ':'
              270  LOAD_FAST             4  'str_name'
              273  COMPARE_OP            7  not-in
            276_0  COME_FROM           264  '264'
              276  POP_JUMP_IF_TRUE    292  'to 292'
              279  LOAD_ASSERT              AssertionError

 L. 426       282  LOAD_CONST               "Header names may not contain ':' or '\\n': %r"
              285  LOAD_FAST             2  'name'
              288  BINARY_MODULO    
              289  RAISE_VARARGS_2       2  None

 L. 427       292  LOAD_GLOBAL          10  'header_re'
              295  LOAD_ATTR            11  'search'
              298  LOAD_FAST             4  'str_name'
              301  CALL_FUNCTION_1       1  None
              304  POP_JUMP_IF_TRUE    320  'to 320'
              307  LOAD_ASSERT              AssertionError
              310  LOAD_CONST               'Bad header name: %r'
              313  LOAD_FAST             2  'name'
              316  BINARY_MODULO    
              317  RAISE_VARARGS_2       2  None

 L. 428       320  LOAD_FAST             4  'str_name'
              323  LOAD_ATTR            12  'endswith'
              326  LOAD_CONST               '-'
              329  CALL_FUNCTION_1       1  None
              332  UNARY_NOT        
              333  POP_JUMP_IF_FALSE   352  'to 352'
              336  LOAD_FAST             4  'str_name'
              339  LOAD_ATTR            12  'endswith'
              342  LOAD_CONST               '_'
              345  CALL_FUNCTION_1       1  None
              348  UNARY_NOT        
            349_0  COME_FROM           333  '333'
              349  POP_JUMP_IF_TRUE    365  'to 365'
              352  LOAD_ASSERT              AssertionError

 L. 429       355  LOAD_CONST               "Names may not end in '-' or '_': %r"
              358  LOAD_FAST             2  'name'
              361  BINARY_MODULO    
              362  RAISE_VARARGS_2       2  None

 L. 430       365  LOAD_GLOBAL           0  'type'
              368  LOAD_FAST             3  'value'
              371  CALL_FUNCTION_1       1  None
              374  LOAD_GLOBAL           5  'str'
              377  COMPARE_OP            8  is
              380  POP_JUMP_IF_FALSE   442  'to 442'

 L. 431       383  SETUP_EXCEPT         17  'to 403'

 L. 432       386  LOAD_FAST             3  'value'
              389  LOAD_ATTR             6  'encode'
              392  LOAD_CONST               'latin1'
              395  CALL_FUNCTION_1       1  None
              398  POP_TOP          
              399  POP_BLOCK        
              400  JUMP_ABSOLUTE       442  'to 442'
            403_0  COME_FROM           383  '383'

 L. 433       403  DUP_TOP          
              404  LOAD_GLOBAL           7  'UnicodeEncodeError'
              407  COMPARE_OP           10  exception-match
              410  POP_JUMP_IF_FALSE   438  'to 438'
              413  POP_TOP          
              414  POP_TOP          
              415  POP_TOP          

 L. 434       416  LOAD_GLOBAL           2  'AssertionError'

 L. 435       419  LOAD_CONST               'Headers values must be latin1 string or bytes.%r is not a valid latin1 string'

 L. 436       422  LOAD_FAST             3  'value'
              425  BUILD_TUPLE_1         1 
              428  BINARY_MODULO    
              429  CALL_FUNCTION_1       1  None
              432  RAISE_VARARGS_1       1  None
              435  JUMP_ABSOLUTE       442  'to 442'
              438  END_FINALLY      
            439_0  COME_FROM           438  '438'
              439  JUMP_FORWARD          0  'to 442'
            442_0  COME_FROM           439  '439'

 L. 437       442  LOAD_GLOBAL           8  'to_string'
              445  LOAD_FAST             3  'value'
              448  CALL_FUNCTION_1       1  None
              451  STORE_FAST            5  'str_value'

 L. 438       454  LOAD_GLOBAL          13  'bad_header_value_re'
              457  LOAD_ATTR            11  'search'
              460  LOAD_FAST             5  'str_value'
              463  CALL_FUNCTION_1       1  None
              466  UNARY_NOT        
              467  POP_JUMP_IF_TRUE     50  'to 50'
              470  LOAD_ASSERT              AssertionError

 L. 439       473  LOAD_CONST               'Bad header value: %r (bad char: %r)'

 L. 440       476  LOAD_FAST             5  'str_value'
              479  LOAD_GLOBAL          13  'bad_header_value_re'
              482  LOAD_ATTR            11  'search'
              485  LOAD_FAST             5  'str_value'
              488  CALL_FUNCTION_1       1  None
              491  LOAD_ATTR            14  'group'
              494  LOAD_CONST               0
              497  CALL_FUNCTION_1       1  None
              500  BUILD_TUPLE_2         2 
              503  BINARY_MODULO    
              504  RAISE_VARARGS_2       2  None
              507  JUMP_BACK            50  'to 50'
              510  POP_BLOCK        
            511_0  COME_FROM            43  '43'

Parse error at or near `POP_BLOCK' instruction at offset 510


def check_content_type--- This code section failed: ---

 L. 444         0  LOAD_GLOBAL           0  'int'
                3  LOAD_FAST             0  'status'
                6  LOAD_ATTR             1  'split'
                9  LOAD_CONST               None
               12  LOAD_CONST               1
               15  CALL_FUNCTION_2       2  None
               18  LOAD_CONST               0
               21  BINARY_SUBSCR    
               22  CALL_FUNCTION_1       1  None
               25  STORE_FAST            2  'code'

 L. 447        28  LOAD_CONST               (201, 204, 304)
               31  STORE_FAST            3  'NO_MESSAGE_BODY'

 L. 448        34  LOAD_CONST               (204, 304)
               37  STORE_FAST            4  'NO_MESSAGE_TYPE'

 L. 449        40  LOAD_CONST               None
               43  STORE_FAST            5  'length'

 L. 450        46  SETUP_LOOP           77  'to 126'
               49  LOAD_FAST             1  'headers'
               52  GET_ITER         
               53  FOR_ITER             69  'to 125'
               56  UNPACK_SEQUENCE_2     2 
               59  STORE_FAST            6  'name'
               62  STORE_FAST            7  'value'

 L. 451        65  LOAD_GLOBAL           3  'to_string'
               68  LOAD_FAST             6  'name'
               71  CALL_FUNCTION_1       1  None
               74  STORE_FAST            8  'str_name'

 L. 452        77  LOAD_FAST             8  'str_name'
               80  LOAD_ATTR             4  'lower'
               83  CALL_FUNCTION_0       0  None
               86  LOAD_CONST               'content-length'
               89  COMPARE_OP            2  ==
               92  POP_JUMP_IF_FALSE    53  'to 53'
               95  LOAD_FAST             7  'value'
               98  LOAD_ATTR             5  'isdigit'
              101  CALL_FUNCTION_0       0  None
            104_0  COME_FROM            92  '92'
              104  POP_JUMP_IF_FALSE    53  'to 53'

 L. 453       107  LOAD_GLOBAL           0  'int'
              110  LOAD_FAST             7  'value'
              113  CALL_FUNCTION_1       1  None
              116  STORE_FAST            5  'length'
              119  JUMP_BACK            53  'to 53'
              122  JUMP_BACK            53  'to 53'
              125  POP_BLOCK        
            126_0  COME_FROM            46  '46'

 L. 454       126  SETUP_LOOP          124  'to 253'
              129  LOAD_FAST             1  'headers'
              132  GET_ITER         
              133  FOR_ITER            116  'to 252'
              136  UNPACK_SEQUENCE_2     2 
              139  STORE_FAST            6  'name'
              142  STORE_FAST            7  'value'

 L. 455       145  LOAD_GLOBAL           3  'to_string'
              148  LOAD_FAST             6  'name'
              151  CALL_FUNCTION_1       1  None
              154  STORE_FAST            8  'str_name'

 L. 456       157  LOAD_FAST             8  'str_name'
              160  LOAD_ATTR             4  'lower'
              163  CALL_FUNCTION_0       0  None
              166  LOAD_CONST               'content-type'
              169  COMPARE_OP            2  ==
              172  POP_JUMP_IF_FALSE   133  'to 133'

 L. 457       175  LOAD_FAST             2  'code'
              178  LOAD_FAST             4  'NO_MESSAGE_TYPE'
              181  COMPARE_OP            7  not-in
              184  POP_JUMP_IF_FALSE   191  'to 191'

 L. 458       187  LOAD_CONST               None
              190  RETURN_END_IF    
            191_0  COME_FROM           184  '184'

 L. 459       191  LOAD_FAST             5  'length'
              194  LOAD_CONST               0
              197  COMPARE_OP            2  ==
              200  POP_JUMP_IF_FALSE   227  'to 227'

 L. 460       203  LOAD_GLOBAL           6  'warnings'
              206  LOAD_ATTR             7  'warn'
              209  LOAD_CONST               'Content-Type header found in a %s response, which not return content.'

 L. 461       212  LOAD_FAST             2  'code'
              215  BINARY_MODULO    

 L. 462       216  LOAD_GLOBAL           8  'WSGIWarning'
              219  CALL_FUNCTION_2       2  None
              222  POP_TOP          

 L. 463       223  LOAD_CONST               None
              226  RETURN_END_IF    
            227_0  COME_FROM           200  '200'

 L. 465       227  LOAD_CONST               0
              230  POP_JUMP_IF_TRUE    249  'to 249'
              233  LOAD_ASSERT              AssertionError
              236  LOAD_CONST               'Content-Type header found in a %s response, which must not return content.'

 L. 466       239  LOAD_FAST             2  'code'
              242  BINARY_MODULO    
              243  RAISE_VARARGS_2       2  None
              246  JUMP_BACK           133  'to 133'
              249  JUMP_BACK           133  'to 133'
              252  POP_BLOCK        
            253_0  COME_FROM           126  '126'

 L. 467       253  LOAD_FAST             2  'code'
              256  LOAD_FAST             3  'NO_MESSAGE_BODY'
              259  COMPARE_OP            7  not-in
              262  POP_JUMP_IF_FALSE   311  'to 311'
              265  LOAD_FAST             5  'length'
              268  LOAD_CONST               None
              271  COMPARE_OP            9  is-not
              274  POP_JUMP_IF_FALSE   311  'to 311'
              277  LOAD_FAST             5  'length'
              280  LOAD_CONST               0
              283  COMPARE_OP            4  >
            286_0  COME_FROM           274  '274'
            286_1  COME_FROM           262  '262'
              286  POP_JUMP_IF_FALSE   311  'to 311'

 L. 468       289  LOAD_CONST               0
              292  POP_JUMP_IF_TRUE    311  'to 311'
              295  LOAD_ASSERT              AssertionError
              298  LOAD_CONST               'No Content-Type header found in headers (%s)'
              301  LOAD_FAST             1  'headers'
              304  BINARY_MODULO    
              305  RAISE_VARARGS_2       2  None
              308  JUMP_FORWARD          0  'to 311'
            311_0  COME_FROM           308  '308'
              311  LOAD_CONST               None
              314  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 252


def check_exc_info--- This code section failed: ---

 L. 472         0  LOAD_FAST             0  'exc_info'
                3  LOAD_CONST               None
                6  COMPARE_OP            8  is
                9  POP_JUMP_IF_TRUE     55  'to 55'
               12  LOAD_GLOBAL           1  'type'
               15  LOAD_FAST             0  'exc_info'
               18  CALL_FUNCTION_1       1  None
               21  LOAD_GLOBAL           2  'tuple'
               24  COMPARE_OP            8  is
               27  POP_JUMP_IF_TRUE     55  'to 55'
               30  LOAD_ASSERT              AssertionError

 L. 473        33  LOAD_CONST               'exc_info (%r) is not a tuple: %r'
               36  LOAD_FAST             0  'exc_info'
               39  LOAD_GLOBAL           1  'type'
               42  LOAD_FAST             0  'exc_info'
               45  CALL_FUNCTION_1       1  None
               48  BUILD_TUPLE_2         2 
               51  BINARY_MODULO    
               52  RAISE_VARARGS_2       2  None
               55  LOAD_CONST               None
               58  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 55


def check_iterator--- This code section failed: ---

 L. 481         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             0  'iterator'
                6  LOAD_GLOBAL           1  'bytes'
                9  CALL_FUNCTION_2       2  None
               12  UNARY_NOT        
               13  POP_JUMP_IF_TRUE     25  'to 25'
               16  LOAD_ASSERT              AssertionError

 L. 482        19  LOAD_CONST               'You should not return a bytes as your application iterator, instead return a single-item list containing that string.'
               22  RAISE_VARARGS_2       2  None

 L. 484        25  LOAD_GLOBAL           0  'isinstance'
               28  LOAD_FAST             0  'iterator'
               31  LOAD_GLOBAL           3  'str'
               34  CALL_FUNCTION_2       2  None
               37  UNARY_NOT        
               38  POP_JUMP_IF_TRUE     50  'to 50'
               41  LOAD_ASSERT              AssertionError

 L. 485        44  LOAD_CONST               'You should not return a string as your application iterator, instead return a single-item list containing bytes.'
               47  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_CONST' instruction at offset 44


def make_middleware(application, global_conf):
    return middleware(application)


make_middleware.__doc__ = __doc__
__all__ = [
 b'middleware', b'make_middleware']