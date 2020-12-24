# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/g2_select.py
# Compiled at: 2010-06-22 06:59:49
import math
from gmisclib import die
from gmisclib import avio
try:
    from gmisclib import load_mod
except ImportError:
    pass

def filterlist(s, d, verbose=False):
    """This filters a list of dictionaries, passing ones where
        the X{selector} returns true.
        @param s: the selector -- a little snippet of python
        @type s: L{str}
        @param d: the list of dictionaries.
                Each dictionary is temporarily used as the local variable
                space and the selector is evaluated.
        @type d: C{ list(dict(str:value)) }
        @return: a subset of the input list, whichever dictionaries cause
                C{s} to return True when evaluated.
        @rtype: C{ list(dict(str: value)) }
        """
    return list(filter_iter(s, d, verbose=verbose))


def filter_iter(s, d, verbose=False):
    """This filters a list of lines, passing ones where
        the selector returns true.
        S is the selector -- a little snippet of python,
        and d is the list of data : a list of {k:v} mappings.
        """
    nok = 0
    nne = 0
    x = None
    cs = _compile(s)
    for t in d:
        try:
            tmp = cs.eval(t)
            if tmp:
                if verbose:
                    die.info('filter_iter: %s -> %s' % (str(t), str(tmp)))
                nok += 1
                yield t
        except NameError as x:
            nne += 1
            if verbose:
                die.info('filter_iter: %s exception: %s' % (str(t), str(x)))

    if nne > 0 and nok == 0:
        die.warn('Name Error (%s) on each of the %d data.' % (str(x), nne))
    return


def _compact(s):
    if len(s) > 15:
        return s[:12] + '...'
    return s


class selector_c(object):

    def __init__(self, code, global_values=None):
        """Code = a string containing python code.
                Global_values = a dictionary containing values to be used by
                that python code.  Note that the dictionary is not copied,
                so that it is shared and changes will be noticed.
                """
        self.code = None
        self.set_code(code)
        if global_values is None:
            self.g = {'math': math}
            try:
                self.g['load_mod'] = load_mod
            except NameError:
                pass

        else:
            self.g = global_values
        self.traptuple = ()
        self.trapmap = []
        return

    def set_code(self, code):
        self.cc = compile(code, '<g2_select: %s>' % _compact(code), 'eval')
        self.code = code

    def set_trap(self, exc, result):
        """This adds to a list of exceptions.    If any of those exceptions
                happen later, when you run C{self.eval()}, then they will be
                caught and turned into the specified result.

                For instance, if you call C{set_trap(ValueError, False)}, and
                when you execute C{self.cc} in C{self.eval} a C{ValueError} is
                raised, then C{self.eval()} will return C{False}.   You have
                mapped a C{ValueError} exception into a returned value of C{False}.
                """
        self.traptuple = self.traptuple + (exc,)
        self.trapmap.append((exc, result))

    def eval(self, locals):
        try:
            return eval(self.cc, self.g, locals)
        except self.traptuple as x:
            for e, r in self.trapmap:
                if isinstance(x, e):
                    return r

            raise

    def globals(self, s):
        exec s in self.g


CCSZ = 100
_ccache = {}

def _compile(s):
    try:
        selector = _ccache[s]
    except KeyError:
        if len(_ccache) > CCSZ:
            _ccache.pop()
        _ccache[s] = selector_c(s)
        selector = _ccache[s]

    return selector


def accept(s, d):
    """This checks a single dictionary, and returns
        the result of the selector.   Errors in the evaluation
        are trapped and cause accept() to return False.
        S is the selector -- a little snippet of python,
        and d is the data : a {k:v} mapping.
        """
    try:
        return evaluate(s, d)
    except NameError as x:
        die.warn('Name Error: %s on %s in %s' % (str(x), avio.concoct(d), s))

    return False


def whynot(s, d):
    """Returns an explanation of why d was not accepted, given s, or None of d was accepted."""
    try:
        if _compile(s).eval(d):
            return
        else:
            return 'Sorry, not implemented yet.'

    except NameError as x:
        return 'data does not contain attribute=%s (d=%s) (selector=%s)' % (x.args[0],
         _compact(avio.concoct(d)),
         _compact(s))

    return


def why(s, d):
    """Returns an explanation of why d was accepted, given s, or None if d was not accepted."""
    if not accept(s, d):
        return None
    else:
        return 'Sorry, not implemented yet.'


def evaluate(s, d):
    """This checks a single dictionary, and returns
        the result of the selector.
        S is the selector -- a little snippet of python,
        and d is the data : a {k:v} mapping.
        """
    return _compile(s).eval(d)


def test--- This code section failed: ---

 L. 171         0  LOAD_GLOBAL           0  'selector_c'
                3  LOAD_CONST               'y'
                6  CALL_FUNCTION_1       1  None
                9  STORE_FAST            0  'x'

 L. 172        12  LOAD_FAST             0  'x'
               15  LOAD_ATTR             1  'eval'
               18  BUILD_MAP_1           1  None
               21  LOAD_CONST               1
               24  LOAD_CONST               'y'
               27  STORE_MAP        
               28  CALL_FUNCTION_1       1  None
               31  LOAD_CONST               1
               34  COMPARE_OP            2  ==
               37  POP_JUMP_IF_TRUE     46  'to 46'
               40  LOAD_ASSERT              AssertionError
               43  RAISE_VARARGS_1       1  None

 L. 173        46  SETUP_EXCEPT         17  'to 66'

 L. 174        49  LOAD_FAST             0  'x'
               52  LOAD_ATTR             1  'eval'
               55  BUILD_MAP_0           0  None
               58  CALL_FUNCTION_1       1  None
               61  POP_TOP          
               62  POP_BLOCK        
               63  JUMP_FORWARD         17  'to 83'
             66_0  COME_FROM            46  '46'

 L. 175        66  DUP_TOP          
               67  LOAD_GLOBAL           3  'NameError'
               70  COMPARE_OP           10  exception-match
               73  POP_JUMP_IF_FALSE    82  'to 82'
               76  POP_TOP          
               77  POP_TOP          
               78  POP_TOP          

 L. 176        79  JUMP_FORWARD         16  'to 98'
               82  END_FINALLY      
             83_0  COME_FROM            63  '63'

 L. 178        83  LOAD_CONST               0
               86  POP_JUMP_IF_TRUE     98  'to 98'
               89  LOAD_ASSERT              AssertionError
               92  LOAD_CONST               'Whoops! no exception when one was expected.'
               95  RAISE_VARARGS_2       2  None
             98_0  COME_FROM            82  '82'

 L. 179        98  LOAD_GLOBAL           0  'selector_c'
              101  LOAD_CONST               'y+w'
              104  BUILD_MAP_1           1  None
              107  LOAD_CONST               1
              110  LOAD_CONST               'w'
              113  STORE_MAP        
              114  CALL_FUNCTION_2       2  None
              117  STORE_FAST            1  'z'

 L. 180       120  LOAD_FAST             1  'z'
              123  LOAD_ATTR             1  'eval'
              126  BUILD_MAP_1           1  None
              129  LOAD_CONST               1
              132  LOAD_CONST               'y'
              135  STORE_MAP        
              136  CALL_FUNCTION_1       1  None
              139  LOAD_CONST               2
              142  COMPARE_OP            2  ==
              145  POP_JUMP_IF_TRUE    154  'to 154'
              148  LOAD_ASSERT              AssertionError
              151  RAISE_VARARGS_1       1  None

 L. 181       154  LOAD_FAST             1  'z'
              157  LOAD_ATTR             4  'globals'
              160  LOAD_CONST               'w=2'
              163  CALL_FUNCTION_1       1  None
              166  POP_TOP          

 L. 182       167  LOAD_FAST             1  'z'
              170  LOAD_ATTR             1  'eval'
              173  BUILD_MAP_1           1  None
              176  LOAD_CONST               1
              179  LOAD_CONST               'y'
              182  STORE_MAP        
              183  CALL_FUNCTION_1       1  None
              186  LOAD_CONST               3
              189  COMPARE_OP            2  ==
              192  POP_JUMP_IF_TRUE    201  'to 201'
              195  LOAD_ASSERT              AssertionError
              198  RAISE_VARARGS_1       1  None

 L. 183       201  LOAD_GLOBAL           0  'selector_c'
              204  LOAD_CONST               'y'
              207  CALL_FUNCTION_1       1  None
              210  STORE_FAST            0  'x'

 L. 184       213  LOAD_FAST             0  'x'
              216  LOAD_ATTR             5  'set_trap'
              219  LOAD_GLOBAL           3  'NameError'
              222  LOAD_CONST               44
              225  CALL_FUNCTION_2       2  None
              228  POP_TOP          

 L. 185       229  LOAD_FAST             0  'x'
              232  LOAD_ATTR             1  'eval'
              235  BUILD_MAP_0           0  None
              238  CALL_FUNCTION_1       1  None
              241  LOAD_CONST               44
              244  COMPARE_OP            2  ==
              247  POP_JUMP_IF_TRUE    256  'to 256'
              250  LOAD_ASSERT              AssertionError
              253  RAISE_VARARGS_1       1  None

Parse error at or near `LOAD_GLOBAL' instruction at offset 98


if __name__ == '__main__':
    test()