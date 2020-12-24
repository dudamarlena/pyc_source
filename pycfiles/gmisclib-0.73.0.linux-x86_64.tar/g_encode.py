# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/g_encode.py
# Compiled at: 2011-03-31 16:40:20
"""This module allows strings to be encoded into a
reduced subset.   It is designed to work for avio.py,
and to do a minimal mapping, so that the resulting
text is human-readable.   It is similar to Quoted-printable
encoding, but is not specialized to e-mail limitations and
is rather more flexible.
"""
import re, string
__version__ = '$Revision: 1.10 $'

class BadFormatError(Exception):

    def __init__(self, *x):
        Exception.__init__(self, *x)


_backdict = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, 
   '7': 7, '8': 8, '9': 9, 'a': 10, 
   'A': 10, 'b': 11, 'B': 11, 'c': 12, 
   'C': 12, 'd': 13, 'D': 13, 'e': 14, 
   'E': 14, 'f': 15, 'F': 15}
_specials = [
 ('mt', ''),
 (' ', '_'),
 ('u', '_'),
 ('p', '.'),
 ('m', ','),
 ('s', ';'),
 ('z', '='),
 ('t', '\t'),
 ('Z', '\x1b'),
 ('M', '&'),
 ('T', '%'),
 ('l', '/'),
 ('K', '\\'),
 ('k', '\x08'),
 ('R', '\r'),
 ('L', '\n'),
 ('q', '"'),
 ('Q', '?'),
 ('U', "'"),
 ('S', ' '),
 ('P', '#')]

def _expand_bdict--- This code section failed: ---

 L.  57         0  BUILD_MAP_0           0  None
                3  STORE_FAST            1  'o'

 L.  58         6  SETUP_LOOP           83  'to 92'
                9  LOAD_FAST             0  'b'
               12  LOAD_ATTR             0  'items'
               15  CALL_FUNCTION_0       0  None
               18  GET_ITER         
               19  FOR_ITER             69  'to 91'
               22  UNPACK_SEQUENCE_2     2 
               25  STORE_FAST            2  'si'
               28  STORE_FAST            3  'ni'

 L.  59        31  SETUP_LOOP           54  'to 88'
               34  LOAD_FAST             0  'b'
               37  LOAD_ATTR             0  'items'
               40  CALL_FUNCTION_0       0  None
               43  GET_ITER         
               44  FOR_ITER             40  'to 87'
               47  UNPACK_SEQUENCE_2     2 
               50  STORE_FAST            4  'sj'
               53  STORE_FAST            5  'nj'

 L.  60        56  LOAD_GLOBAL           1  'chr'
               59  LOAD_CONST               16
               62  LOAD_FAST             3  'ni'
               65  BINARY_MULTIPLY  
               66  LOAD_FAST             5  'nj'
               69  BINARY_ADD       
               70  CALL_FUNCTION_1       1  None
               73  LOAD_FAST             1  'o'
               76  LOAD_FAST             2  'si'
               79  LOAD_FAST             4  'sj'
               82  BINARY_ADD       
               83  STORE_SUBSCR     
               84  JUMP_BACK            44  'to 44'
               87  POP_BLOCK        
             88_0  COME_FROM            31  '31'
               88  JUMP_BACK            19  'to 19'
               91  POP_BLOCK        
             92_0  COME_FROM             6  '6'

 L.  61        92  SETUP_LOOP           88  'to 183'
               95  LOAD_GLOBAL           2  '_specials'
               98  GET_ITER         
               99  FOR_ITER             80  'to 182'
              102  UNPACK_SEQUENCE_2     2 
              105  STORE_FAST            6  'k'
              108  STORE_FAST            7  'v'

 L.  62       111  LOAD_GLOBAL           3  '_backdict'
              114  LOAD_ATTR             4  'has_key'
              117  LOAD_FAST             6  'k'
              120  CALL_FUNCTION_1       1  None
              123  UNARY_NOT        
              124  POP_JUMP_IF_TRUE    140  'to 140'
              127  LOAD_ASSERT              AssertionError
              130  LOAD_CONST               'Special (%s) collides with hex.'
              133  LOAD_FAST             6  'k'
              136  BINARY_MODULO    
              137  RAISE_VARARGS_2       2  None

 L.  63       140  LOAD_FAST             1  'o'
              143  LOAD_ATTR             4  'has_key'
              146  LOAD_FAST             6  'k'
              149  CALL_FUNCTION_1       1  None
              152  UNARY_NOT        
              153  POP_JUMP_IF_TRUE    169  'to 169'
              156  LOAD_ASSERT              AssertionError
              159  LOAD_CONST               'Special (%s) collides with hex or special.'
              162  LOAD_FAST             6  'k'
              165  BINARY_MODULO    
              166  RAISE_VARARGS_2       2  None

 L.  64       169  LOAD_FAST             7  'v'
              172  LOAD_FAST             1  'o'
              175  LOAD_FAST             6  'k'
              178  STORE_SUBSCR     
              179  JUMP_BACK            99  'to 99'
              182  POP_BLOCK        
            183_0  COME_FROM            92  '92'

 L.  65       183  LOAD_FAST             1  'o'
              186  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 182


_bdict = _expand_bdict(_backdict)

def _fromhex(x):
    """Expands a %XX code (or the specials above) into a character."""
    q = x.group(1)
    return _bdict[q]


def _rm_nl(s):
    if s.endswith('\n'):
        return s[:-1]
    return s


def _expand_fdict(eschar):
    o = {}
    for c in range(256):
        o[chr(c)] = '%s%02x' % (eschar, c)

    for k, v in _specials:
        o[v] = '%s%s' % (eschar, k)

    return o


class encoder:

    def __init__--- This code section failed: ---

 L. 108         0  LOAD_FAST             3  'regex'
                3  LOAD_CONST               None
                6  COMPARE_OP            9  is-not
                9  LOAD_FAST             1  'allowed'
               12  LOAD_CONST               None
               15  COMPARE_OP            9  is-not
               18  BINARY_ADD       
               19  LOAD_FAST             2  'notallowed'
               22  LOAD_CONST               None
               25  COMPARE_OP            9  is-not
               28  BINARY_ADD       
               29  LOAD_CONST               1
               32  COMPARE_OP            1  <=
               35  POP_JUMP_IF_TRUE     47  'to 47'
               38  LOAD_ASSERT              AssertionError
               41  LOAD_CONST               'Specify at most one of regex, allowed, notallowed.'
               44  RAISE_VARARGS_2       2  None

 L. 109        47  LOAD_FAST             2  'notallowed'
               50  LOAD_CONST               None
               53  COMPARE_OP            9  is-not
               56  POP_JUMP_IF_FALSE   115  'to 115'

 L. 110        59  LOAD_FAST             4  'eschar'
               62  LOAD_FAST             2  'notallowed'
               65  COMPARE_OP            6  in
               68  POP_JUMP_IF_TRUE     90  'to 90'
               71  LOAD_ASSERT              AssertionError
               74  LOAD_CONST               "Sorry: notallowed must contain '%s', but it is '%s'."
               77  LOAD_FAST             4  'eschar'
               80  LOAD_FAST             2  'notallowed'
               83  BUILD_TUPLE_2         2 
               86  BINARY_MODULO    
               87  RAISE_VARARGS_2       2  None

 L. 111        90  LOAD_GLOBAL           2  're'
               93  LOAD_ATTR             3  'compile'
               96  LOAD_CONST               '(^\\s)|([%s])|(\\s$)'
               99  LOAD_FAST             2  'notallowed'
              102  BINARY_MODULO    
              103  CALL_FUNCTION_1       1  None
              106  LOAD_FAST             0  'self'
              109  STORE_ATTR            4  'ref'
              112  JUMP_FORWARD        115  'to 230'

 L. 112       115  LOAD_FAST             3  'regex'
              118  LOAD_CONST               None
              121  COMPARE_OP            9  is-not
              124  POP_JUMP_IF_FALSE   148  'to 148'

 L. 113       127  LOAD_GLOBAL           2  're'
              130  LOAD_ATTR             3  'compile'
              133  LOAD_FAST             3  'regex'
              136  CALL_FUNCTION_1       1  None
              139  LOAD_FAST             0  'self'
              142  STORE_ATTR            4  'ref'
              145  JUMP_FORWARD         82  'to 230'

 L. 115       148  LOAD_FAST             1  'allowed'
              151  LOAD_CONST               None
              154  COMPARE_OP            8  is
              157  POP_JUMP_IF_FALSE   183  'to 183'

 L. 116       160  LOAD_GLOBAL           5  'string'
              163  LOAD_ATTR             6  'letters'
              166  LOAD_GLOBAL           5  'string'
              169  LOAD_ATTR             7  'digits'
              172  BINARY_ADD       

 L. 117       173  LOAD_CONST               '_!@$^&*()+={}[\\]\\|:\'"?/>.<,\\ ~`-'
              176  BINARY_ADD       
              177  STORE_FAST            1  'allowed'
              180  JUMP_FORWARD          0  'to 183'
            183_0  COME_FROM           180  '180'

 L. 118       183  LOAD_FAST             4  'eschar'
              186  LOAD_FAST             1  'allowed'
              189  COMPARE_OP            7  not-in
              192  POP_JUMP_IF_TRUE    208  'to 208'
              195  LOAD_ASSERT              AssertionError
              198  LOAD_CONST               "Cannot allow '%s'."
              201  LOAD_FAST             4  'eschar'
              204  BINARY_MODULO    
              205  RAISE_VARARGS_2       2  None

 L. 119       208  LOAD_GLOBAL           2  're'
              211  LOAD_ATTR             3  'compile'
              214  LOAD_CONST               '(^\\s)|([^%s])|(\\s$)'
              217  LOAD_FAST             1  'allowed'
              220  BINARY_MODULO    
              221  CALL_FUNCTION_1       1  None
              224  LOAD_FAST             0  'self'
              227  STORE_ATTR            4  'ref'
            230_0  COME_FROM           145  '145'
            230_1  COME_FROM           112  '112'

 L. 121       230  LOAD_GLOBAL           2  're'
              233  LOAD_ATTR             3  'compile'

 L. 123       236  LOAD_CONST               '%s([0-9a-fA-F][0-9a-fA-F]|'
              239  LOAD_FAST             4  'eschar'
              242  BINARY_MODULO    
              243  LOAD_CONST               '|'
              246  LOAD_ATTR             8  'join'
              249  BUILD_LIST_0          0 
              252  LOAD_GLOBAL           9  '_specials'
              255  GET_ITER         
              256  FOR_ITER             16  'to 275'
              259  STORE_FAST            5  '_c'
              262  LOAD_FAST             5  '_c'
              265  LOAD_CONST               0
              268  BINARY_SUBSCR    
              269  LIST_APPEND           2  None
              272  JUMP_BACK           256  'to 256'
              275  CALL_FUNCTION_1       1  None
              278  BINARY_ADD       
              279  LOAD_CONST               ')'
              282  BINARY_ADD       
              283  CALL_FUNCTION_1       1  None
              286  LOAD_FAST             0  'self'
              289  STORE_ATTR           10  '_reb'

 L. 124       292  LOAD_GLOBAL          11  '_expand_fdict'
              295  LOAD_FAST             4  'eschar'
              298  CALL_FUNCTION_1       1  None
              301  LOAD_FAST             0  'self'
              304  STORE_ATTR           12  '_fdict'

 L. 125       307  LOAD_CONST               '%smt'
              310  LOAD_FAST             4  'eschar'
              313  BINARY_MODULO    
              314  LOAD_FAST             0  'self'
              317  STORE_ATTR           13  'empty'
              320  LOAD_CONST               None
              323  RETURN_VALUE     

Parse error at or near `COME_FROM' instruction at offset 230_0

    def back(self, x):
        """Converts back from a string containing %xx escape sequences to
                an unencoded string.
                """
        try:
            return self._reb.sub(_fromhex, x)
        except KeyError as x:
            raise BadFormatError, 'illegal escape sequence: %s' % x

    def _tohex--- This code section failed: ---

 L. 139         0  LOAD_FAST             1  'x'
                3  LOAD_ATTR             0  'string'
                6  LOAD_FAST             1  'x'
                9  LOAD_ATTR             1  'start'
               12  CALL_FUNCTION_0       0  None
               15  BINARY_SUBSCR    
               16  STORE_FAST            2  'q'

 L. 140        19  LOAD_GLOBAL           2  'len'
               22  LOAD_FAST             2  'q'
               25  CALL_FUNCTION_1       1  None
               28  LOAD_CONST               1
               31  COMPARE_OP            2  ==
               34  POP_JUMP_IF_TRUE     46  'to 46'
               37  LOAD_ASSERT              AssertionError
               40  LOAD_CONST               'tohex operates on a single character'
               43  RAISE_VARARGS_2       2  None

 L. 141        46  LOAD_FAST             0  'self'
               49  LOAD_ATTR             4  '_fdict'
               52  LOAD_FAST             2  'q'
               55  BINARY_SUBSCR    
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 56

    def fwd(self, x):
        """Escapes a string so it is suitable for a=v; form.
                Nonprinting characters, along with [;#] are converted
                to %xx escapes (hexadecimal).
                Non-strings will be converted to strings with repr(),
                and can be fed back into the python interpreter.  """
        if not isinstance(x, str):
            x = repr(x)
        if x == '':
            return self.empty
        return self.ref.sub(self._tohex, x)


def test():
    e = encoder()
    assert e.back(e.fwd('george')) == 'george'
    assert e.back(e.fwd('hello there')) == 'hello there'
    assert e.back('%sfoo') == ';foo'
    assert e.back('%Sfoo%S%P') == ' foo #'
    assert e.back('%Tfoo') == '%foo'
    assert e.back(e.fwd('%hello')) == '%hello'
    assert e.back(e.fwd(' hello there')) == ' hello there'
    assert e.back(e.fwd(' hello there\t')) == ' hello there\t'
    assert e.back(e.fwd(' hello there\t=')) == ' hello there\t='
    assert e.back(e.fwd(' hello there\t=;#')) == ' hello there\t=;#'
    assert e.back(e.fwd(' hello+_there\t=;#')) == ' hello+_there\t=;#'
    assert e.back(e.fwd('hello+_there\t=;#')) == 'hello+_there\t=;#'
    assert e.fwd('hello there') == 'hello there'
    ee = encoder('abcd')
    assert ee.fwd('cab d') == 'cab%Sd'
    assert ee.fwd('e') == '%65'
    assert ee.fwd('aaaa bbbb') == 'aaaa%Sbbbb'
    ee = encoder(notallowed=']\n\r%')
    assert '\n' not in ee.fwd('hello world\n\r')
    assert ']' not in ee.fwd('hello]% world\n\r')
    assert ee.back(ee.fwd('hello world\n\r')) == 'hello world\n\r'
    e = encoder(eschar='_', allowed='0-9a-zA-Z')
    assert e.back('_sfoo') == ';foo'
    assert e.back(e.fwd('%hello')) == '%hello'
    assert e.back(e.fwd('_hello')) == '_hello'


if __name__ == '__main__':
    test()
    print 'OK: passed tests'