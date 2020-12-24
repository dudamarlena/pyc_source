# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/urilib/tests.py
# Compiled at: 2011-09-06 23:52:31
import re, unittest, urilib

def assert_queries_eq--- This code section failed: ---

 L.   6         0  LOAD_GLOBAL           0  'len'
                3  LOAD_FAST             0  'q1'
                6  LOAD_ATTR             1  'keys'
                9  CALL_FUNCTION_0       0  None
               12  CALL_FUNCTION_1       1  None
               15  LOAD_GLOBAL           0  'len'
               18  LOAD_FAST             1  'q2'
               21  LOAD_ATTR             1  'keys'
               24  CALL_FUNCTION_0       0  None
               27  CALL_FUNCTION_1       1  None
               30  COMPARE_OP            2  ==
               33  POP_JUMP_IF_TRUE     79  'to 79'
               36  LOAD_ASSERT              AssertionError

 L.   7        39  LOAD_CONST               'Expected %d params, Got %d.'
               42  LOAD_GLOBAL           0  'len'
               45  LOAD_FAST             1  'q2'
               48  LOAD_ATTR             1  'keys'
               51  CALL_FUNCTION_0       0  None
               54  CALL_FUNCTION_1       1  None
               57  LOAD_GLOBAL           0  'len'
               60  LOAD_FAST             0  'q1'
               63  LOAD_ATTR             1  'keys'
               66  CALL_FUNCTION_0       0  None
               69  CALL_FUNCTION_1       1  None
               72  BUILD_TUPLE_2         2 
               75  BINARY_MODULO    
               76  RAISE_VARARGS_2       2  None

 L.   8        79  SETUP_LOOP           72  'to 154'
               82  LOAD_FAST             0  'q1'
               85  LOAD_ATTR             3  'iteritems'
               88  CALL_FUNCTION_0       0  None
               91  GET_ITER         
               92  FOR_ITER             58  'to 153'
               95  UNPACK_SEQUENCE_2     2 
               98  STORE_FAST            2  'k'
              101  STORE_FAST            3  'v'

 L.   9       104  LOAD_FAST             2  'k'
              107  LOAD_FAST             1  'q2'
              110  COMPARE_OP            6  in
              113  POP_JUMP_IF_TRUE    129  'to 129'
              116  LOAD_ASSERT              AssertionError
              119  LOAD_CONST               'Got unexpected param: %s'
              122  LOAD_FAST             2  'k'
              125  BINARY_MODULO    
              126  RAISE_VARARGS_2       2  None

 L.  10       129  LOAD_GLOBAL           4  'assert_lists_eq'
              132  LOAD_FAST             0  'q1'
              135  LOAD_FAST             2  'k'
              138  BINARY_SUBSCR    
              139  LOAD_FAST             1  'q2'
              142  LOAD_FAST             2  'k'
              145  BINARY_SUBSCR    
              146  CALL_FUNCTION_2       2  None
              149  POP_TOP          
              150  JUMP_BACK            92  'to 92'
              153  POP_BLOCK        
            154_0  COME_FROM            79  '79'

Parse error at or near `POP_BLOCK' instruction at offset 153


def assert_lists_eq--- This code section failed: ---

 L.  13         0  LOAD_FAST             2  'strict'
                3  POP_JUMP_IF_FALSE    95  'to 95'

 L.  14         6  LOAD_GLOBAL           0  'type'
                9  LOAD_FAST             0  'l1'
               12  CALL_FUNCTION_1       1  None
               15  LOAD_GLOBAL           1  'list'
               18  COMPARE_OP            2  ==
               21  POP_JUMP_IF_TRUE     49  'to 49'
               24  LOAD_ASSERT              AssertionError
               27  LOAD_CONST               'Expected a list for arg 0, got %s.'
               30  LOAD_GLOBAL           3  'str'
               33  LOAD_GLOBAL           0  'type'
               36  LOAD_FAST             0  'l1'
               39  CALL_FUNCTION_1       1  None
               42  CALL_FUNCTION_1       1  None
               45  BINARY_MODULO    
               46  RAISE_VARARGS_2       2  None

 L.  15        49  LOAD_GLOBAL           0  'type'
               52  LOAD_FAST             1  'l2'
               55  CALL_FUNCTION_1       1  None
               58  LOAD_GLOBAL           1  'list'
               61  COMPARE_OP            2  ==
               64  POP_JUMP_IF_TRUE     95  'to 95'
               67  LOAD_ASSERT              AssertionError
               70  LOAD_CONST               'Expected a list for arg 1, got %s.'
               73  LOAD_GLOBAL           3  'str'
               76  LOAD_GLOBAL           0  'type'
               79  LOAD_FAST             1  'l2'
               82  CALL_FUNCTION_1       1  None
               85  CALL_FUNCTION_1       1  None
               88  BINARY_MODULO    
               89  RAISE_VARARGS_2       2  None
               92  JUMP_FORWARD          0  'to 95'
             95_0  COME_FROM            92  '92'

 L.  16        95  LOAD_GLOBAL           4  'len'
               98  LOAD_FAST             0  'l1'
              101  CALL_FUNCTION_1       1  None
              104  LOAD_GLOBAL           4  'len'
              107  LOAD_FAST             1  'l2'
              110  CALL_FUNCTION_1       1  None
              113  COMPARE_OP            2  ==
              116  POP_JUMP_IF_TRUE    150  'to 150'
              119  LOAD_ASSERT              AssertionError
              122  LOAD_CONST               'Expected %d elements, Got %d elements'
              125  LOAD_GLOBAL           4  'len'
              128  LOAD_FAST             1  'l2'
              131  CALL_FUNCTION_1       1  None
              134  LOAD_GLOBAL           4  'len'
              137  LOAD_FAST             0  'l1'
              140  CALL_FUNCTION_1       1  None
              143  BUILD_TUPLE_2         2 
              146  BINARY_MODULO    
              147  RAISE_VARARGS_2       2  None

 L.  17       150  SETUP_LOOP           68  'to 221'
              153  LOAD_GLOBAL           5  'enumerate'
              156  LOAD_FAST             0  'l1'
              159  CALL_FUNCTION_1       1  None
              162  GET_ITER         
              163  FOR_ITER             54  'to 220'
              166  UNPACK_SEQUENCE_2     2 
              169  STORE_FAST            3  'i'
              172  STORE_FAST            4  'element'

 L.  18       175  LOAD_FAST             4  'element'
              178  LOAD_FAST             1  'l2'
              181  LOAD_FAST             3  'i'
              184  BINARY_SUBSCR    
              185  COMPARE_OP            2  ==
              188  POP_JUMP_IF_TRUE    163  'to 163'
              191  LOAD_ASSERT              AssertionError
              194  LOAD_CONST               "At index %d, Expected '%s', Got '%s'"
              197  LOAD_FAST             3  'i'
              200  LOAD_FAST             1  'l2'
              203  LOAD_FAST             3  'i'
              206  BINARY_SUBSCR    
              207  LOAD_FAST             4  'element'
              210  BUILD_TUPLE_3         3 
              213  BINARY_MODULO    
              214  RAISE_VARARGS_2       2  None
              217  JUMP_BACK           163  'to 163'
              220  POP_BLOCK        
            221_0  COME_FROM           150  '150'

Parse error at or near `POP_BLOCK' instruction at offset 220


def assert_dicts_eq--- This code section failed: ---

 L.  21         0  LOAD_GLOBAL           0  'type'
                3  LOAD_FAST             0  'd1'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_GLOBAL           1  'dict'
               12  COMPARE_OP            2  ==
               15  POP_JUMP_IF_TRUE     27  'to 27'
               18  LOAD_ASSERT              AssertionError
               21  LOAD_CONST               'First argument is not a dict()'
               24  RAISE_VARARGS_2       2  None

 L.  22        27  LOAD_GLOBAL           0  'type'
               30  LOAD_FAST             1  'd2'
               33  CALL_FUNCTION_1       1  None
               36  LOAD_GLOBAL           1  'dict'
               39  COMPARE_OP            2  ==
               42  POP_JUMP_IF_TRUE     54  'to 54'
               45  LOAD_ASSERT              AssertionError
               48  LOAD_CONST               'Second argument is not a dict()'
               51  RAISE_VARARGS_2       2  None

 L.  23        54  LOAD_GLOBAL           3  'len'
               57  LOAD_FAST             0  'd1'
               60  LOAD_ATTR             4  'keys'
               63  CALL_FUNCTION_0       0  None
               66  CALL_FUNCTION_1       1  None
               69  LOAD_GLOBAL           3  'len'
               72  LOAD_FAST             1  'd2'
               75  LOAD_ATTR             4  'keys'
               78  CALL_FUNCTION_0       0  None
               81  CALL_FUNCTION_1       1  None
               84  COMPARE_OP            2  ==
               87  POP_JUMP_IF_TRUE    133  'to 133'
               90  LOAD_ASSERT              AssertionError

 L.  24        93  LOAD_CONST               'Got %d keys. Expected %d keys.'
               96  LOAD_GLOBAL           3  'len'
               99  LOAD_FAST             0  'd1'
              102  LOAD_ATTR             4  'keys'
              105  CALL_FUNCTION_0       0  None
              108  CALL_FUNCTION_1       1  None
              111  LOAD_GLOBAL           3  'len'
              114  LOAD_FAST             1  'd2'
              117  LOAD_ATTR             4  'keys'
              120  CALL_FUNCTION_0       0  None
              123  CALL_FUNCTION_1       1  None
              126  BUILD_TUPLE_2         2 
              129  BINARY_MODULO    
              130  RAISE_VARARGS_2       2  None

 L.  25       133  SETUP_LOOP           98  'to 234'
              136  LOAD_FAST             0  'd1'
              139  LOAD_ATTR             5  'iteritems'
              142  CALL_FUNCTION_0       0  None
              145  GET_ITER         
              146  FOR_ITER             84  'to 233'
              149  UNPACK_SEQUENCE_2     2 
              152  STORE_FAST            2  'k'
              155  STORE_FAST            3  'v'

 L.  26       158  LOAD_FAST             2  'k'
              161  LOAD_FAST             1  'd2'
              164  COMPARE_OP            6  in
              167  POP_JUMP_IF_TRUE    183  'to 183'
              170  LOAD_ASSERT              AssertionError
              173  LOAD_CONST               'Got unexpected key %s'
              176  LOAD_FAST             2  'k'
              179  BINARY_MODULO    
              180  RAISE_VARARGS_2       2  None

 L.  27       183  LOAD_FAST             0  'd1'
              186  LOAD_FAST             2  'k'
              189  BINARY_SUBSCR    
              190  LOAD_FAST             1  'd2'
              193  LOAD_FAST             2  'k'
              196  BINARY_SUBSCR    
              197  COMPARE_OP            2  ==
              200  POP_JUMP_IF_TRUE    146  'to 146'
              203  LOAD_ASSERT              AssertionError
              206  LOAD_CONST               "'%s' != '%s'"
              209  LOAD_FAST             0  'd1'
              212  LOAD_FAST             2  'k'
              215  BINARY_SUBSCR    
              216  LOAD_FAST             1  'd2'
              219  LOAD_FAST             2  'k'
              222  BINARY_SUBSCR    
              223  BUILD_TUPLE_2         2 
              226  BINARY_MODULO    
              227  RAISE_VARARGS_2       2  None
              230  JUMP_BACK           146  'to 146'
              233  POP_BLOCK        
            234_0  COME_FROM           133  '133'

Parse error at or near `POP_BLOCK' instruction at offset 233


class TestStandalones(unittest.TestCase):

    def testIsValidFragment--- This code section failed: ---

 L.  35         0  LOAD_GLOBAL           0  'urilib'
                3  LOAD_ATTR             1  'tools'
                6  LOAD_ATTR             2  'is_valid_fragment'
                9  LOAD_CONST               '#abc'
               12  CALL_FUNCTION_1       1  None
               15  LOAD_GLOBAL           3  'False'
               18  COMPARE_OP            2  ==
               21  POP_JUMP_IF_TRUE     33  'to 33'
               24  LOAD_ASSERT              AssertionError

 L.  36        27  LOAD_CONST               'Asserting that a preceeding # is invalid'
               30  RAISE_VARARGS_2       2  None

 L.  38        33  LOAD_GLOBAL           0  'urilib'
               36  LOAD_ATTR             1  'tools'
               39  LOAD_ATTR             2  'is_valid_fragment'
               42  LOAD_CONST               'abc#'
               45  CALL_FUNCTION_1       1  None
               48  LOAD_GLOBAL           3  'False'
               51  COMPARE_OP            2  ==
               54  POP_JUMP_IF_TRUE     66  'to 66'
               57  LOAD_ASSERT              AssertionError

 L.  39        60  LOAD_CONST               'Asserting that a trailing # is invalid'
               63  RAISE_VARARGS_2       2  None

 L.  41        66  LOAD_GLOBAL           0  'urilib'
               69  LOAD_ATTR             1  'tools'
               72  LOAD_ATTR             2  'is_valid_fragment'
               75  LOAD_CONST               'ab#c'
               78  CALL_FUNCTION_1       1  None
               81  LOAD_GLOBAL           3  'False'
               84  COMPARE_OP            2  ==
               87  POP_JUMP_IF_TRUE     99  'to 99'
               90  LOAD_ASSERT              AssertionError

 L.  42        93  LOAD_CONST               'Asserting that a # in the middle is invalid'
               96  RAISE_VARARGS_2       2  None

 L.  44        99  LOAD_GLOBAL           0  'urilib'
              102  LOAD_ATTR             1  'tools'
              105  LOAD_ATTR             2  'is_valid_fragment'
              108  LOAD_CONST               'abcdefg'
              111  CALL_FUNCTION_1       1  None
              114  LOAD_GLOBAL           5  'True'
              117  COMPARE_OP            2  ==
              120  POP_JUMP_IF_TRUE    132  'to 132'
              123  LOAD_ASSERT              AssertionError

 L.  45       126  LOAD_CONST               'Asserting the base case of alphabet chars'
              129  RAISE_VARARGS_2       2  None

 L.  47       132  LOAD_GLOBAL           0  'urilib'
              135  LOAD_ATTR             1  'tools'
              138  LOAD_ATTR             2  'is_valid_fragment'
              141  LOAD_CONST               "a.a_a~a!a$a&a'a(a)a*a+a,a;a=a/a?a:a@a"
              144  CALL_FUNCTION_1       1  None
              147  LOAD_GLOBAL           5  'True'
              150  COMPARE_OP            2  ==
              153  POP_JUMP_IF_TRUE    165  'to 165'
              156  LOAD_ASSERT              AssertionError

 L.  48       159  LOAD_CONST               "Asserting that '._~!$&'()*+,;=/?:@' are valid characters"
              162  RAISE_VARARGS_2       2  None

 L.  50       165  LOAD_GLOBAL           0  'urilib'
              168  LOAD_ATTR             1  'tools'
              171  LOAD_ATTR             2  'is_valid_fragment'
              174  LOAD_CONST               '%AF%20'
              177  CALL_FUNCTION_1       1  None
              180  LOAD_GLOBAL           5  'True'
              183  COMPARE_OP            2  ==
              186  POP_JUMP_IF_TRUE    198  'to 198'
              189  LOAD_ASSERT              AssertionError

 L.  51       192  LOAD_CONST               'Asserting that uri-escaped characters are valid.'
              195  RAISE_VARARGS_2       2  None

 L.  53       198  LOAD_GLOBAL           0  'urilib'
              201  LOAD_ATTR             1  'tools'
              204  LOAD_ATTR             2  'is_valid_fragment'
              207  LOAD_CONST               "a_a'%AFa(a)a*a+a,a;%AF=a/aa"
              210  CALL_FUNCTION_1       1  None
              213  LOAD_GLOBAL           5  'True'
              216  COMPARE_OP            2  ==
              219  POP_JUMP_IF_TRUE    231  'to 231'
              222  LOAD_ASSERT              AssertionError

 L.  54       225  LOAD_CONST               'Asserting that uri-escaped characters are valid mixed with other chars.'
              228  RAISE_VARARGS_2       2  None

 L.  56       231  LOAD_GLOBAL           0  'urilib'
              234  LOAD_ATTR             1  'tools'
              237  LOAD_ATTR             2  'is_valid_fragment'
              240  LOAD_CONST               '%%'
              243  CALL_FUNCTION_1       1  None
              246  LOAD_GLOBAL           3  'False'
              249  COMPARE_OP            2  ==
              252  POP_JUMP_IF_TRUE    264  'to 264'
              255  LOAD_ASSERT              AssertionError

 L.  57       258  LOAD_CONST               'Asserting that escaped % is invalid.'
              261  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_CONST' instruction at offset 258

    def testIsValidScheme(self):
        """ Testing URI.is_valid_scheme()
        returns a boolean verifying that the string passed in is valid as the
        scheme part of the URI """
        assert urilib.tools.is_valid_scheme('http') == True
        assert urilib.tools.is_valid_scheme('ftp1') == True
        assert urilib.tools.is_valid_scheme('f1tp') == True
        assert urilib.tools.is_valid_scheme('ftp2') == True
        assert urilib.tools.is_valid_scheme('0http') == False
        assert urilib.tools.is_valid_scheme('f9tp') == True
        assert urilib.tools.is_valid_scheme('http.') == True
        assert urilib.tools.is_valid_scheme('http+') == True
        assert urilib.tools.is_valid_scheme('http-') == True
        assert urilib.tools.is_valid_scheme('ht.tp') == True
        assert urilib.tools.is_valid_scheme('ht+tp') == True
        assert urilib.tools.is_valid_scheme('ht-tp') == True
        assert urilib.tools.is_valid_scheme('.http') == False
        assert urilib.tools.is_valid_scheme('-http') == False
        assert urilib.tools.is_valid_scheme('+http') == False
        assert urilib.tools.is_valid_scheme('htt_p') == False


class Query(unittest.TestCase):

    def testAlternateSeparator(self):
        """ Test non-default separator """
        query = urilib.Query('param=val1;param2=val3;param=val2', separator=';')
        assert_queries_eq(query, {'param': ['val1', 'val2'], 'param2': ['val3']})

    def testNonStringSeparator(self):
        """ Test non-string separator error-handling """
        try:
            urilib.Query(separator=dict())
        except ValueError as e:
            assert str(e) == "Expected separator to be a string, got <type 'dict'>"

    def testAddingSimpleQueryString(self):
        """ Adding a simple query string """
        query = urilib.Query('q=a&param=value')
        assert_queries_eq(query, {'q': ['a'], 'param': ['value']})

    def testCreatingMultiValuedKey(self):
        """ Creating a multi-valued key """
        query = urilib.Query('param=val1&param2=val3&param=val2')
        assert_queries_eq(query, {'param': ['val1', 'val2'], 'param2': ['val3']})

    def testClearingAParam(self):
        """ Removing all params for a specific name """
        query = urilib.Query('param=val1&param=val2&param2=val3')
        del query['param']
        assert_queries_eq(query, {'param2': ['val3']})

    def testRemovingMultipleParamsByNameAndValue(self):
        """ Removing parameters by name-value """
        query = urilib.Query('param=val1&param=val2&param2=val3&param=val4&param=val2')
        assert_queries_eq(query, {'param': ['val1', 'val2', 'val4', 'val2'], 'param2': ['val3']})
        query.del_by_name_value('param', 'val2')
        assert_queries_eq(query, {'param': ['val1', 'val4'], 'param2': ['val3']})

    def testRemovingASingleParamByNameAndValue(self):
        """ Removing a specific name-value pair """
        query = urilib.Query('param=val1&param=val2&param2=val3&param=val4&param=val2')
        assert_queries_eq(query, {'param': ['val1', 'val2', 'val4', 'val2'], 'param2': ['val3']})
        query.del_by_name_value('param', 'val2', max=1)
        assert_queries_eq(query, {'param': ['val1', 'val4', 'val2'], 'param2': ['val3']})

    def testEmptyQueryString(self):
        """ Instantiating an empty query """
        query = urilib.Query()
        assert len(query.keys()) == 0
        query = urilib.Query('')
        assert len(query.keys()) == 0


class URLQueryFunctions(unittest.TestCase):
    pass


class URIParsing(unittest.TestCase):

    def testURIBaseCase(self):
        """ Test a base case URI that has most of the parts in it """
        uri = urilib.URI('http://www.example.com/?q=test#header1')
        assert uri.scheme == 'http'
        assert uri.fragment == 'header1'
        assert uri.query == 'q=test'
        assert uri.hier_part == '//www.example.com/'
        assert uri.path == '/'
        assert uri.authority == 'www.example.com'
        assert str(uri) == 'http://www.example.com/?q=test#header1'

    def testURIWithFullyLoadedAuthority(self):
        """ Test a URI with a fully-loaded authority section """
        uri = urilib.URI('http://username:password@www.example.com:80/admin')
        assert uri.scheme == 'http'
        assert uri.fragment is None
        assert uri.query is None
        assert uri.hier_part == '//username:password@www.example.com:80/admin'
        assert uri.path == '/admin'
        assert uri.authority == 'username:password@www.example.com:80'
        assert str(uri) == 'http://username:password@www.example.com:80/admin'
        return

    def testURIBlankAuthorityFileScheme(self):
        """ Parsing a file URI with an empty authority section """
        uri = urilib.URI('file:///my/relative/file/uri')
        assert uri.scheme == 'file'
        assert uri.fragment is None
        assert uri.query is None
        assert uri.hier_part == '///my/relative/file/uri'
        assert uri.path == '/my/relative/file/uri'
        assert uri.authority == ''
        assert str(uri) == 'file:///my/relative/file/uri'
        return

    def testURINoAuthorityFileScheme(self):
        """ Test parsing a file URI with no authority section """
        uri = urilib.URI('file:my/relative/file/uri')
        assert uri.scheme == 'file'
        assert uri.fragment is None
        assert uri.query is None
        assert uri.hier_part == 'my/relative/file/uri'
        assert uri.path == 'my/relative/file/uri'
        assert uri.authority is None
        assert str(uri) == 'file:my/relative/file/uri'
        return

    def testURIOnlyPathAndScheme(self):
        """ Test a uri that only has a path and scheme """
        uri = urilib.URI('urn:example:animal:ferret:nose')
        assert uri.scheme == 'urn'
        assert uri.fragment is None
        assert uri.query is None
        assert uri.hier_part == 'example:animal:ferret:nose'
        assert uri.path == 'example:animal:ferret:nose'
        assert uri.authority is None
        assert str(uri) == 'urn:example:animal:ferret:nose'
        return

    def testURINoauthrityLoaded(self):
        """ Test a URI with no authority section but otherwise fully loaded """
        uri = urilib.URI('urn:example:animal:ferret:nose?sources=true#10')
        assert uri.scheme == 'urn'
        assert uri.fragment == '10'
        assert uri.query == 'sources=true'
        assert uri.hier_part == 'example:animal:ferret:nose'
        assert uri.path == 'example:animal:ferret:nose'
        assert uri.authority is None
        assert str(uri) == 'urn:example:animal:ferret:nose?sources=true#10'
        return