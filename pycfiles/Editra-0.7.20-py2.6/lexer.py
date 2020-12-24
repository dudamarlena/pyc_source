# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/pygments/lexer.py
# Compiled at: 2011-04-22 17:53:28
"""
    pygments.lexer
    ~~~~~~~~~~~~~~

    Base lexer classes.

    :copyright: Copyright 2006-2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.filter import apply_filters, Filter
from pygments.filters import get_filter_by_name
from pygments.token import Error, Text, Other, _TokenType
from pygments.util import get_bool_opt, get_int_opt, get_list_opt, make_analysator
__all__ = [
 'Lexer', 'RegexLexer', 'ExtendedRegexLexer', 'DelegatingLexer',
 'LexerContext', 'include', 'bygroups', 'using', 'this']
_default_analyse = staticmethod(lambda x: 0.0)

class LexerMeta(type):
    """
    This metaclass automagically converts ``analyse_text`` methods into
    static methods which always return float values.
    """

    def __new__(cls, name, bases, d):
        if 'analyse_text' in d:
            d['analyse_text'] = make_analysator(d['analyse_text'])
        return type.__new__(cls, name, bases, d)


class Lexer(object):
    """
    Lexer for a specific language.

    Basic options recognized:
    ``stripnl``
        Strip leading and trailing newlines from the input (default: True).
    ``stripall``
        Strip all leading and trailing whitespace from the input
        (default: False).
    ``ensurenl``
        Make sure that the input ends with a newline (default: True).  This
        is required for some lexers that consume input linewise.
        *New in Pygments 1.3.*
    ``tabsize``
        If given and greater than 0, expand tabs in the input (default: 0).
    ``encoding``
        If given, must be an encoding name. This encoding will be used to
        convert the input string to Unicode, if it is not already a Unicode
        string (default: ``'latin1'``).
        Can also be ``'guess'`` to use a simple UTF-8 / Latin1 detection, or
        ``'chardet'`` to use the chardet library, if it is installed.
    """
    name = None
    aliases = []
    filenames = []
    alias_filenames = []
    mimetypes = []
    __metaclass__ = LexerMeta

    def __init__(self, **options):
        self.options = options
        self.stripnl = get_bool_opt(options, 'stripnl', True)
        self.stripall = get_bool_opt(options, 'stripall', False)
        self.ensurenl = get_bool_opt(options, 'ensurenl', True)
        self.tabsize = get_int_opt(options, 'tabsize', 0)
        self.encoding = options.get('encoding', 'latin1')
        self.filters = []
        for filter_ in get_list_opt(options, 'filters', ()):
            self.add_filter(filter_)

    def __repr__(self):
        if self.options:
            return '<pygments.lexers.%s with %r>' % (self.__class__.__name__,
             self.options)
        else:
            return '<pygments.lexers.%s>' % self.__class__.__name__

    def add_filter(self, filter_, **options):
        """
        Add a new stream filter to this lexer.
        """
        if not isinstance(filter_, Filter):
            filter_ = get_filter_by_name(filter_, **options)
        self.filters.append(filter_)

    def analyse_text(text):
        """
        Has to return a float between ``0`` and ``1`` that indicates
        if a lexer wants to highlight this text. Used by ``guess_lexer``.
        If this method returns ``0`` it won't highlight it in any case, if
        it returns ``1`` highlighting with this lexer is guaranteed.

        The `LexerMeta` metaclass automatically wraps this function so
        that it works like a static method (no ``self`` or ``cls``
        parameter) and the return value is automatically converted to
        `float`. If the return value is an object that is boolean `False`
        it's the same as if the return values was ``0.0``.
        """
        pass

    def get_tokens(self, text, unfiltered=False):
        """
        Return an iterable of (tokentype, value) pairs generated from
        `text`. If `unfiltered` is set to `True`, the filtering mechanism
        is bypassed even if filters are defined.

        Also preprocess the text, i.e. expand tabs and strip it if
        wanted and applies registered filters.
        """
        if not isinstance(text, unicode):
            if self.encoding == 'guess':
                try:
                    text = text.decode('utf-8')
                    if text.startswith('\ufeff'):
                        text = text[len('\ufeff'):]
                except UnicodeDecodeError:
                    text = text.decode('latin1')

            elif self.encoding == 'chardet':
                try:
                    import chardet
                except ImportError:
                    raise ImportError('To enable chardet encoding guessing, please install the chardet library from http://chardet.feedparser.org/')
                else:
                    enc = chardet.detect(text)
                    text = text.decode(enc['encoding'])
            else:
                text = text.decode(self.encoding)
        text = text.replace('\r\n', '\n')
        text = text.replace('\r', '\n')
        if self.stripall:
            text = text.strip()
        elif self.stripnl:
            text = text.strip('\n')
        if self.tabsize > 0:
            text = text.expandtabs(self.tabsize)
        if self.ensurenl and not text.endswith('\n'):
            text += '\n'

        def streamer():
            for (i, t, v) in self.get_tokens_unprocessed(text):
                yield (
                 t, v)

        stream = streamer()
        if not unfiltered:
            stream = apply_filters(stream, self.filters, self)
        return stream

    def get_tokens_unprocessed(self, text):
        """
        Return an iterable of (tokentype, value) pairs.
        In subclasses, implement this method as a generator to
        maximize effectiveness.
        """
        raise NotImplementedError


class DelegatingLexer(Lexer):
    """
    This lexer takes two lexer as arguments. A root lexer and
    a language lexer. First everything is scanned using the language
    lexer, afterwards all ``Other`` tokens are lexed using the root
    lexer.

    The lexers from the ``template`` lexer package use this base lexer.
    """

    def __init__(self, _root_lexer, _language_lexer, _needle=Other, **options):
        self.root_lexer = _root_lexer(**options)
        self.language_lexer = _language_lexer(**options)
        self.needle = _needle
        Lexer.__init__(self, **options)

    def get_tokens_unprocessed(self, text):
        buffered = ''
        insertions = []
        lng_buffer = []
        for (i, t, v) in self.language_lexer.get_tokens_unprocessed(text):
            if t is self.needle:
                if lng_buffer:
                    insertions.append((len(buffered), lng_buffer))
                    lng_buffer = []
                buffered += v
            else:
                lng_buffer.append((i, t, v))

        if lng_buffer:
            insertions.append((len(buffered), lng_buffer))
        return do_insertions(insertions, self.root_lexer.get_tokens_unprocessed(buffered))


class include(str):
    """
    Indicates that a state should include rules from another state.
    """
    pass


class combined(tuple):
    """
    Indicates a state combined from multiple states.
    """

    def __new__(cls, *args):
        return tuple.__new__(cls, args)

    def __init__(self, *args):
        pass


class _PseudoMatch(object):
    """
    A pseudo match object constructed from a string.
    """

    def __init__(self, start, text):
        self._text = text
        self._start = start

    def start(self, arg=None):
        return self._start

    def end(self, arg=None):
        return self._start + len(self._text)

    def group(self, arg=None):
        if arg:
            raise IndexError('No such group')
        return self._text

    def groups(self):
        return (
         self._text,)

    def groupdict(self):
        return {}


def bygroups(*args):
    """
    Callback that yields multiple actions for each group in the match.
    """

    def callback(lexer, match, ctx=None):
        for (i, action) in enumerate(args):
            if action is None:
                continue
            elif type(action) is _TokenType:
                data = match.group(i + 1)
                if data:
                    yield (
                     match.start(i + 1), action, data)
            else:
                if ctx:
                    ctx.pos = match.start(i + 1)
                for item in action(lexer, _PseudoMatch(match.start(i + 1), match.group(i + 1)), ctx):
                    if item:
                        yield item

        if ctx:
            ctx.pos = match.end()
        return

    return callback


class _This(object):
    """
    Special singleton used for indicating the caller class.
    Used by ``using``.
    """
    pass


this = _This()

def using(_other, **kwargs):
    """
    Callback that processes the match with a different lexer.

    The keyword arguments are forwarded to the lexer, except `state` which
    is handled separately.

    `state` specifies the state that the new lexer will start in, and can
    be an enumerable such as ('root', 'inline', 'string') or a simple
    string which is assumed to be on top of the root state.

    Note: For that to work, `_other` must not be an `ExtendedRegexLexer`.
    """
    gt_kwargs = {}
    if 'state' in kwargs:
        s = kwargs.pop('state')
        if isinstance(s, (list, tuple)):
            gt_kwargs['stack'] = s
        else:
            gt_kwargs['stack'] = (
             'root', s)
    if _other is this:

        def callback(lexer, match, ctx=None):
            if kwargs:
                kwargs.update(lexer.options)
                lx = lexer.__class__(**kwargs)
            else:
                lx = lexer
            s = match.start()
            for (i, t, v) in lx.get_tokens_unprocessed(match.group(), **gt_kwargs):
                yield (
                 i + s, t, v)

            if ctx:
                ctx.pos = match.end()

    else:

        def callback(lexer, match, ctx=None):
            kwargs.update(lexer.options)
            lx = _other(**kwargs)
            s = match.start()
            for (i, t, v) in lx.get_tokens_unprocessed(match.group(), **gt_kwargs):
                yield (
                 i + s, t, v)

            if ctx:
                ctx.pos = match.end()

    return callback


class RegexLexerMeta(LexerMeta):
    """
    Metaclass for RegexLexer, creates the self._tokens attribute from
    self.tokens on the first instantiation.
    """

    def _process_regex(cls, regex, rflags):
        """Preprocess the regular expression component of a token definition."""
        return re.compile(regex, rflags).match

    def _process_token(cls, token):
        """Preprocess the token component of a token definition."""
        assert type(token) is _TokenType or callable(token), 'token type must be simple type or callable, not %r' % (token,)
        return token

    def _process_new_state(cls, new_state, unprocessed, processed):
        """Preprocess the state transition action of a token definition."""
        if isinstance(new_state, str):
            if new_state == '#pop':
                pass
            else:
                return -1
                if new_state in unprocessed:
                    return (new_state,)
                if new_state == '#push':
                    return new_state
                if new_state[:5] == '#pop:':
                    return -int(new_state[5:])
                raise False or AssertionError, 'unknown new state %r' % new_state
        elif isinstance(new_state, combined):
            pass
        else:
            tmp_state = '_tmp_%d' % cls._tmpname
            cls._tmpname += 1
            itokens = []
            for istate in new_state:
                assert istate != new_state, 'circular state ref %r' % istate
                itokens.extend(cls._process_state(unprocessed, processed, istate))

            processed[tmp_state] = itokens
            return (tmp_state,)
            if isinstance(new_state, tuple):
                for istate in new_state:
                    assert istate in unprocessed or istate in ('#pop', '#push'), 'unknown new state ' + istate

                return new_state
            raise False or AssertionError, 'unknown new state def %r' % new_state

    def _process_state(cls, unprocessed, processed, state):
        """Preprocess a single state definition."""
        assert type(state) is str, 'wrong state name %r' % state
        assert state[0] != '#', 'invalid state name %r' % state
        if state in processed:
            return processed[state]
        else:
            tokens = processed[state] = []
            rflags = cls.flags
            for tdef in unprocessed[state]:
                if isinstance(tdef, include):
                    assert tdef != state, 'circular state reference %r' % state
                    tokens.extend(cls._process_state(unprocessed, processed, str(tdef)))
                    continue
                assert type(tdef) is tuple, 'wrong rule def %r' % tdef
                try:
                    rex = cls._process_regex(tdef[0], rflags)
                except Exception, err:
                    raise ValueError('uncompilable regex %r in state %r of %r: %s' % (
                     tdef[0], state, cls, err))

                token = cls._process_token(tdef[1])
                if len(tdef) == 2:
                    new_state = None
                else:
                    new_state = cls._process_new_state(tdef[2], unprocessed, processed)
                tokens.append((rex, token, new_state))

            return tokens

    def process_tokendef(cls, name, tokendefs=None):
        """Preprocess a dictionary of token definitions."""
        processed = cls._all_tokens[name] = {}
        tokendefs = tokendefs or cls.tokens[name]
        for state in tokendefs.keys():
            cls._process_state(tokendefs, processed, state)

        return processed

    def __call__(cls, *args, **kwds):
        """Instantiate cls after preprocessing its token definitions."""
        if not hasattr(cls, '_tokens'):
            cls._all_tokens = {}
            cls._tmpname = 0
            if hasattr(cls, 'token_variants') and cls.token_variants:
                pass
            else:
                cls._tokens = cls.process_tokendef('', cls.tokens)
        return type.__call__(cls, *args, **kwds)


class RegexLexer(Lexer):
    """
    Base for simple stateful regular expression-based lexers.
    Simplifies the lexing process so that you need only
    provide a list of states and regular expressions.
    """
    __metaclass__ = RegexLexerMeta
    flags = re.MULTILINE
    tokens = {}

    def get_tokens_unprocessed--- This code section failed: ---

 L. 491         0  LOAD_CONST               0
                3  STORE_FAST            3  'pos'

 L. 492         6  LOAD_FAST             0  'self'
                9  LOAD_ATTR             0  '_tokens'
               12  STORE_FAST            4  'tokendefs'

 L. 493        15  LOAD_GLOBAL           1  'list'
               18  LOAD_FAST             2  'stack'
               21  CALL_FUNCTION_1       1  None
               24  STORE_FAST            5  'statestack'

 L. 494        27  LOAD_FAST             4  'tokendefs'
               30  LOAD_FAST             5  'statestack'
               33  LOAD_CONST               -1
               36  BINARY_SUBSCR    
               37  BINARY_SUBSCR    
               38  STORE_FAST            6  'statetokens'

 L. 495        41  SETUP_LOOP          488  'to 532'

 L. 496        44  SETUP_LOOP          482  'to 529'
               47  LOAD_FAST             6  'statetokens'
               50  GET_ITER         
               51  FOR_ITER            352  'to 406'
               54  UNPACK_SEQUENCE_3     3 
               57  STORE_FAST            7  'rexmatch'
               60  STORE_FAST            8  'action'
               63  STORE_FAST            9  'new_state'

 L. 497        66  LOAD_FAST             7  'rexmatch'
               69  LOAD_FAST             1  'text'
               72  LOAD_FAST             3  'pos'
               75  CALL_FUNCTION_2       2  None
               78  STORE_FAST           10  'm'

 L. 498        81  LOAD_FAST            10  'm'
               84  JUMP_IF_FALSE       315  'to 402'
               87  POP_TOP          

 L. 499        88  LOAD_GLOBAL           2  'type'
               91  LOAD_FAST             8  'action'
               94  CALL_FUNCTION_1       1  None
               97  LOAD_GLOBAL           3  '_TokenType'
              100  COMPARE_OP            8  is
              103  JUMP_IF_FALSE        24  'to 130'
              106  POP_TOP          

 L. 500       107  LOAD_FAST             3  'pos'
              110  LOAD_FAST             8  'action'
              113  LOAD_FAST            10  'm'
              116  LOAD_ATTR             4  'group'
              119  CALL_FUNCTION_0       0  None
              122  BUILD_TUPLE_3         3 
              125  YIELD_VALUE      
              126  POP_TOP          
              127  JUMP_FORWARD         32  'to 162'
            130_0  COME_FROM           103  '103'
              130  POP_TOP          

 L. 502       131  SETUP_LOOP           28  'to 162'
              134  LOAD_FAST             8  'action'
              137  LOAD_FAST             0  'self'
              140  LOAD_FAST            10  'm'
              143  CALL_FUNCTION_2       2  None
              146  GET_ITER         
              147  FOR_ITER             11  'to 161'
              150  STORE_FAST           11  'item'

 L. 503       153  LOAD_FAST            11  'item'
              156  YIELD_VALUE      
              157  POP_TOP          
              158  JUMP_BACK           147  'to 147'
              161  POP_BLOCK        
            162_0  COME_FROM           131  '131'
            162_1  COME_FROM           127  '127'

 L. 504       162  LOAD_FAST            10  'm'
              165  LOAD_ATTR             5  'end'
              168  CALL_FUNCTION_0       0  None
              171  STORE_FAST            3  'pos'

 L. 505       174  LOAD_FAST             9  'new_state'
              177  LOAD_CONST               None
              180  COMPARE_OP            9  is-not
              183  JUMP_IF_FALSE       211  'to 397'
            186_0  THEN                     398
              186  POP_TOP          

 L. 507       187  LOAD_GLOBAL           7  'isinstance'
              190  LOAD_FAST             9  'new_state'
              193  LOAD_GLOBAL           8  'tuple'
              196  CALL_FUNCTION_2       2  None
              199  JUMP_IF_FALSE        95  'to 297'
              202  POP_TOP          

 L. 508       203  SETUP_LOOP          174  'to 380'
              206  LOAD_FAST             9  'new_state'
              209  GET_ITER         
              210  FOR_ITER             80  'to 293'
              213  STORE_FAST           12  'state'

 L. 509       216  LOAD_FAST            12  'state'
              219  LOAD_CONST               '#pop'
              222  COMPARE_OP            2  ==
              225  JUMP_IF_FALSE        14  'to 242'
              228  POP_TOP          

 L. 510       229  LOAD_FAST             5  'statestack'
              232  LOAD_ATTR             9  'pop'
              235  CALL_FUNCTION_0       0  None
              238  POP_TOP          
              239  JUMP_BACK           210  'to 210'
            242_0  COME_FROM           225  '225'
              242  POP_TOP          

 L. 511       243  LOAD_FAST            12  'state'
              246  LOAD_CONST               '#push'
              249  COMPARE_OP            2  ==
              252  JUMP_IF_FALSE        21  'to 276'
              255  POP_TOP          

 L. 512       256  LOAD_FAST             5  'statestack'
              259  LOAD_ATTR            10  'append'
              262  LOAD_FAST             5  'statestack'
              265  LOAD_CONST               -1
              268  BINARY_SUBSCR    
              269  CALL_FUNCTION_1       1  None
              272  POP_TOP          
              273  JUMP_BACK           210  'to 210'
            276_0  COME_FROM           252  '252'
              276  POP_TOP          

 L. 514       277  LOAD_FAST             5  'statestack'
              280  LOAD_ATTR            10  'append'
              283  LOAD_FAST            12  'state'
              286  CALL_FUNCTION_1       1  None
              289  POP_TOP          
              290  JUMP_BACK           210  'to 210'
              293  POP_BLOCK        
              294  JUMP_FORWARD         83  'to 380'
            297_0  COME_FROM           199  '199'
              297  POP_TOP          

 L. 515       298  LOAD_GLOBAL           7  'isinstance'
              301  LOAD_FAST             9  'new_state'
              304  LOAD_GLOBAL          11  'int'
              307  CALL_FUNCTION_2       2  None
              310  JUMP_IF_FALSE        11  'to 324'
              313  POP_TOP          

 L. 517       314  LOAD_FAST             5  'statestack'
              317  LOAD_FAST             9  'new_state'
              320  DELETE_SLICE+1   
              321  JUMP_FORWARD         56  'to 380'
            324_0  COME_FROM           310  '310'
              324  POP_TOP          

 L. 518       325  LOAD_FAST             9  'new_state'
              328  LOAD_CONST               '#push'
              331  COMPARE_OP            2  ==
              334  JUMP_IF_FALSE        21  'to 358'
              337  POP_TOP          

 L. 519       338  LOAD_FAST             5  'statestack'
              341  LOAD_ATTR            10  'append'
              344  LOAD_FAST             5  'statestack'
              347  LOAD_CONST               -1
              350  BINARY_SUBSCR    
              351  CALL_FUNCTION_1       1  None
              354  POP_TOP          
              355  JUMP_FORWARD         22  'to 380'
            358_0  COME_FROM           334  '334'
              358  POP_TOP          

 L. 521       359  LOAD_GLOBAL          12  'False'
              362  JUMP_IF_TRUE         14  'to 379'
              365  POP_TOP          
              366  LOAD_ASSERT              AssertionError
              369  LOAD_CONST               'wrong state def: %r'
              372  LOAD_FAST             9  'new_state'
              375  BINARY_MODULO    
              376  RAISE_VARARGS_2       2  None
            379_0  COME_FROM           362  '362'
              379  POP_TOP          
            380_0  COME_FROM           203  '203'

 L. 522       380  LOAD_FAST             4  'tokendefs'
              383  LOAD_FAST             5  'statestack'
              386  LOAD_CONST               -1
              389  BINARY_SUBSCR    
              390  BINARY_SUBSCR    
              391  STORE_FAST            6  'statetokens'
              394  JUMP_FORWARD          1  'to 398'
            397_0  COME_FROM           183  '183'
              397  POP_TOP          
            398_0  COME_FROM           394  '394'

 L. 523       398  BREAK_LOOP       
              399  JUMP_BACK            51  'to 51'
            402_0  COME_FROM            84  '84'
              402  POP_TOP          
              403  JUMP_BACK            51  'to 51'
              406  POP_BLOCK        

 L. 525       407  SETUP_EXCEPT         99  'to 509'

 L. 526       410  LOAD_FAST             1  'text'
              413  LOAD_FAST             3  'pos'
              416  BINARY_SUBSCR    
              417  LOAD_CONST               '\n'
              420  COMPARE_OP            2  ==
              423  JUMP_IF_FALSE        50  'to 476'
            426_0  THEN                     477
              426  POP_TOP          

 L. 528       427  LOAD_FAST             3  'pos'
              430  LOAD_CONST               1
              433  INPLACE_ADD      
              434  STORE_FAST            3  'pos'

 L. 529       437  LOAD_CONST               'root'
              440  BUILD_LIST_1          1 
              443  STORE_FAST            5  'statestack'

 L. 530       446  LOAD_FAST             4  'tokendefs'
              449  LOAD_CONST               'root'
              452  BINARY_SUBSCR    
              453  STORE_FAST            6  'statetokens'

 L. 531       456  LOAD_FAST             3  'pos'
              459  LOAD_GLOBAL          14  'Text'
              462  LOAD_CONST               '\n'
              465  BUILD_TUPLE_3         3 
              468  YIELD_VALUE      
              469  POP_TOP          

 L. 532       470  CONTINUE_LOOP        44  'to 44'
              473  JUMP_FORWARD          1  'to 477'
            476_0  COME_FROM           423  '423'
              476  POP_TOP          
            477_0  COME_FROM           473  '473'

 L. 533       477  LOAD_FAST             3  'pos'
              480  LOAD_GLOBAL          15  'Error'
              483  LOAD_FAST             1  'text'
              486  LOAD_FAST             3  'pos'
              489  BINARY_SUBSCR    
              490  BUILD_TUPLE_3         3 
              493  YIELD_VALUE      
              494  POP_TOP          

 L. 534       495  LOAD_FAST             3  'pos'
              498  LOAD_CONST               1
              501  INPLACE_ADD      
              502  STORE_FAST            3  'pos'
              505  POP_BLOCK        
              506  JUMP_BACK            44  'to 44'
            509_0  COME_FROM           407  '407'

 L. 535       509  DUP_TOP          
              510  LOAD_GLOBAL          16  'IndexError'
              513  COMPARE_OP           10  exception-match
              516  JUMP_IF_FALSE         8  'to 527'
              519  POP_TOP          
              520  POP_TOP          
              521  POP_TOP          
              522  POP_TOP          

 L. 536       523  BREAK_LOOP       
              524  JUMP_BACK            44  'to 44'
              527  POP_TOP          
              528  END_FINALLY      
            529_0  COME_FROM            44  '44'
              529  JUMP_BACK            44  'to 44'
            532_0  COME_FROM            41  '41'
              532  LOAD_CONST               None
              535  RETURN_VALUE     

Parse error at or near `JUMP_BACK' instruction at offset 529


class LexerContext(object):
    """
    A helper object that holds lexer position data.
    """

    def __init__(self, text, pos, stack=None, end=None):
        self.text = text
        self.pos = pos
        self.end = end or len(text)
        self.stack = stack or ['root']

    def __repr__(self):
        return 'LexerContext(%r, %r, %r)' % (
         self.text, self.pos, self.stack)


class ExtendedRegexLexer(RegexLexer):
    """
    A RegexLexer that uses a context object to store its state.
    """

    def get_tokens_unprocessed--- This code section failed: ---

 L. 565         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  '_tokens'
                6  STORE_FAST            3  'tokendefs'

 L. 566         9  LOAD_FAST             2  'context'
               12  JUMP_IF_TRUE         29  'to 44'
               15  POP_TOP          

 L. 567        16  LOAD_GLOBAL           1  'LexerContext'
               19  LOAD_FAST             1  'text'
               22  LOAD_CONST               0
               25  CALL_FUNCTION_2       2  None
               28  STORE_FAST            4  'ctx'

 L. 568        31  LOAD_FAST             3  'tokendefs'
               34  LOAD_CONST               'root'
               37  BINARY_SUBSCR    
               38  STORE_FAST            5  'statetokens'
               41  JUMP_FORWARD         33  'to 77'
             44_0  COME_FROM            12  '12'
               44  POP_TOP          

 L. 570        45  LOAD_FAST             2  'context'
               48  STORE_FAST            4  'ctx'

 L. 571        51  LOAD_FAST             3  'tokendefs'
               54  LOAD_FAST             4  'ctx'
               57  LOAD_ATTR             2  'stack'
               60  LOAD_CONST               -1
               63  BINARY_SUBSCR    
               64  BINARY_SUBSCR    
               65  STORE_FAST            5  'statetokens'

 L. 572        68  LOAD_FAST             4  'ctx'
               71  LOAD_ATTR             3  'text'
               74  STORE_FAST            1  'text'
             77_0  COME_FROM            41  '41'

 L. 573        77  SETUP_LOOP          520  'to 600'

 L. 574        80  SETUP_LOOP          514  'to 597'
               83  LOAD_FAST             5  'statetokens'
               86  GET_ITER         
               87  FOR_ITER            335  'to 425'
               90  UNPACK_SEQUENCE_3     3 
               93  STORE_FAST            6  'rexmatch'
               96  STORE_FAST            7  'action'
               99  STORE_FAST            8  'new_state'

 L. 575       102  LOAD_FAST             6  'rexmatch'
              105  LOAD_FAST             1  'text'
              108  LOAD_FAST             4  'ctx'
              111  LOAD_ATTR             4  'pos'
              114  LOAD_FAST             4  'ctx'
              117  LOAD_ATTR             5  'end'
              120  CALL_FUNCTION_3       3  None
              123  STORE_FAST            9  'm'

 L. 576       126  LOAD_FAST             9  'm'
              129  JUMP_IF_FALSE       289  'to 421'
              132  POP_TOP          

 L. 577       133  LOAD_GLOBAL           6  'type'
              136  LOAD_FAST             7  'action'
              139  CALL_FUNCTION_1       1  None
              142  LOAD_GLOBAL           7  '_TokenType'
              145  COMPARE_OP            8  is
              148  JUMP_IF_FALSE        42  'to 193'
              151  POP_TOP          

 L. 578       152  LOAD_FAST             4  'ctx'
              155  LOAD_ATTR             4  'pos'
              158  LOAD_FAST             7  'action'
              161  LOAD_FAST             9  'm'
              164  LOAD_ATTR             8  'group'
              167  CALL_FUNCTION_0       0  None
              170  BUILD_TUPLE_3         3 
              173  YIELD_VALUE      
              174  POP_TOP          

 L. 579       175  LOAD_FAST             9  'm'
              178  LOAD_ATTR             5  'end'
              181  CALL_FUNCTION_0       0  None
              184  LOAD_FAST             4  'ctx'
              187  STORE_ATTR            4  'pos'
              190  JUMP_FORWARD         63  'to 256'
            193_0  COME_FROM           148  '148'
              193  POP_TOP          

 L. 581       194  SETUP_LOOP           31  'to 228'
              197  LOAD_FAST             7  'action'
              200  LOAD_FAST             0  'self'
              203  LOAD_FAST             9  'm'
              206  LOAD_FAST             4  'ctx'
              209  CALL_FUNCTION_3       3  None
              212  GET_ITER         
              213  FOR_ITER             11  'to 227'
              216  STORE_FAST           10  'item'

 L. 582       219  LOAD_FAST            10  'item'
              222  YIELD_VALUE      
              223  POP_TOP          
              224  JUMP_BACK           213  'to 213'
              227  POP_BLOCK        
            228_0  COME_FROM           194  '194'

 L. 583       228  LOAD_FAST             8  'new_state'
              231  JUMP_IF_TRUE         21  'to 255'
            234_0  THEN                     256
              234  POP_TOP          

 L. 585       235  LOAD_FAST             3  'tokendefs'
              238  LOAD_FAST             4  'ctx'
              241  LOAD_ATTR             2  'stack'
              244  LOAD_CONST               -1
              247  BINARY_SUBSCR    
              248  BINARY_SUBSCR    
              249  STORE_FAST            5  'statetokens'
              252  JUMP_FORWARD          1  'to 256'
            255_0  COME_FROM           231  '231'
              255  POP_TOP          
            256_0  COME_FROM           252  '252'
            256_1  COME_FROM           190  '190'

 L. 587       256  LOAD_FAST             8  'new_state'
              259  LOAD_CONST               None
              262  COMPARE_OP            9  is-not
              265  JUMP_IF_FALSE       148  'to 416'
            268_0  THEN                     417
              268  POP_TOP          

 L. 589       269  LOAD_GLOBAL          10  'isinstance'
              272  LOAD_FAST             8  'new_state'
              275  LOAD_GLOBAL          11  'tuple'
              278  CALL_FUNCTION_2       2  None
              281  JUMP_IF_FALSE        20  'to 304'
              284  POP_TOP          

 L. 590       285  LOAD_FAST             4  'ctx'
              288  LOAD_ATTR             2  'stack'
              291  LOAD_ATTR            12  'extend'
              294  LOAD_FAST             8  'new_state'
              297  CALL_FUNCTION_1       1  None
              300  POP_TOP          
              301  JUMP_FORWARD         92  'to 396'
            304_0  COME_FROM           281  '281'
              304  POP_TOP          

 L. 591       305  LOAD_GLOBAL          10  'isinstance'
              308  LOAD_FAST             8  'new_state'
              311  LOAD_GLOBAL          13  'int'
              314  CALL_FUNCTION_2       2  None
              317  JUMP_IF_FALSE        14  'to 334'
              320  POP_TOP          

 L. 593       321  LOAD_FAST             4  'ctx'
              324  LOAD_ATTR             2  'stack'
              327  LOAD_FAST             8  'new_state'
              330  DELETE_SLICE+1   
              331  JUMP_FORWARD         62  'to 396'
            334_0  COME_FROM           317  '317'
              334  POP_TOP          

 L. 594       335  LOAD_FAST             8  'new_state'
              338  LOAD_CONST               '#push'
              341  COMPARE_OP            2  ==
              344  JUMP_IF_FALSE        27  'to 374'
              347  POP_TOP          

 L. 595       348  LOAD_FAST             4  'ctx'
              351  LOAD_ATTR             2  'stack'
              354  LOAD_ATTR            14  'append'
              357  LOAD_FAST             4  'ctx'
              360  LOAD_ATTR             2  'stack'
              363  LOAD_CONST               -1
              366  BINARY_SUBSCR    
              367  CALL_FUNCTION_1       1  None
              370  POP_TOP          
              371  JUMP_FORWARD         22  'to 396'
            374_0  COME_FROM           344  '344'
              374  POP_TOP          

 L. 597       375  LOAD_GLOBAL          15  'False'
              378  JUMP_IF_TRUE         14  'to 395'
              381  POP_TOP          
              382  LOAD_ASSERT              AssertionError
              385  LOAD_CONST               'wrong state def: %r'
              388  LOAD_FAST             8  'new_state'
              391  BINARY_MODULO    
              392  RAISE_VARARGS_2       2  None
            395_0  COME_FROM           378  '378'
              395  POP_TOP          
            396_0  COME_FROM           371  '371'
            396_1  COME_FROM           331  '331'
            396_2  COME_FROM           301  '301'

 L. 598       396  LOAD_FAST             3  'tokendefs'
              399  LOAD_FAST             4  'ctx'
              402  LOAD_ATTR             2  'stack'
              405  LOAD_CONST               -1
              408  BINARY_SUBSCR    
              409  BINARY_SUBSCR    
              410  STORE_FAST            5  'statetokens'
              413  JUMP_FORWARD          1  'to 417'
            416_0  COME_FROM           265  '265'
              416  POP_TOP          
            417_0  COME_FROM           413  '413'

 L. 599       417  BREAK_LOOP       
              418  JUMP_BACK            87  'to 87'
            421_0  COME_FROM           129  '129'
              421  POP_TOP          
              422  JUMP_BACK            87  'to 87'
              425  POP_BLOCK        

 L. 601       426  SETUP_EXCEPT        148  'to 577'

 L. 602       429  LOAD_FAST             4  'ctx'
              432  LOAD_ATTR             4  'pos'
              435  LOAD_FAST             4  'ctx'
              438  LOAD_ATTR             5  'end'
              441  COMPARE_OP            5  >=
              444  JUMP_IF_FALSE         5  'to 452'
            447_0  THEN                     453
              447  POP_TOP          

 L. 603       448  BREAK_LOOP       
              449  JUMP_FORWARD          1  'to 453'
            452_0  COME_FROM           444  '444'
              452  POP_TOP          
            453_0  COME_FROM           449  '449'

 L. 604       453  LOAD_FAST             1  'text'
              456  LOAD_FAST             4  'ctx'
              459  LOAD_ATTR             4  'pos'
              462  BINARY_SUBSCR    
              463  LOAD_CONST               '\n'
              466  COMPARE_OP            2  ==
              469  JUMP_IF_FALSE        61  'to 533'
            472_0  THEN                     534
              472  POP_TOP          

 L. 606       473  LOAD_FAST             4  'ctx'
              476  DUP_TOP          
              477  LOAD_ATTR             4  'pos'
              480  LOAD_CONST               1
              483  INPLACE_ADD      
              484  ROT_TWO          
              485  STORE_ATTR            4  'pos'

 L. 607       488  LOAD_CONST               'root'
              491  BUILD_LIST_1          1 
              494  LOAD_FAST             4  'ctx'
              497  STORE_ATTR            2  'stack'

 L. 608       500  LOAD_FAST             3  'tokendefs'
              503  LOAD_CONST               'root'
              506  BINARY_SUBSCR    
              507  STORE_FAST            5  'statetokens'

 L. 609       510  LOAD_FAST             4  'ctx'
              513  LOAD_ATTR             4  'pos'
              516  LOAD_GLOBAL          17  'Text'
              519  LOAD_CONST               '\n'
              522  BUILD_TUPLE_3         3 
              525  YIELD_VALUE      
              526  POP_TOP          

 L. 610       527  CONTINUE_LOOP        80  'to 80'
              530  JUMP_FORWARD          1  'to 534'
            533_0  COME_FROM           469  '469'
              533  POP_TOP          
            534_0  COME_FROM           530  '530'

 L. 611       534  LOAD_FAST             4  'ctx'
              537  LOAD_ATTR             4  'pos'
              540  LOAD_GLOBAL          18  'Error'
              543  LOAD_FAST             1  'text'
              546  LOAD_FAST             4  'ctx'
              549  LOAD_ATTR             4  'pos'
              552  BINARY_SUBSCR    
              553  BUILD_TUPLE_3         3 
              556  YIELD_VALUE      
              557  POP_TOP          

 L. 612       558  LOAD_FAST             4  'ctx'
              561  DUP_TOP          
              562  LOAD_ATTR             4  'pos'
              565  LOAD_CONST               1
              568  INPLACE_ADD      
              569  ROT_TWO          
              570  STORE_ATTR            4  'pos'
              573  POP_BLOCK        
              574  JUMP_BACK            80  'to 80'
            577_0  COME_FROM           426  '426'

 L. 613       577  DUP_TOP          
              578  LOAD_GLOBAL          19  'IndexError'
              581  COMPARE_OP           10  exception-match
              584  JUMP_IF_FALSE         8  'to 595'
              587  POP_TOP          
              588  POP_TOP          
              589  POP_TOP          
              590  POP_TOP          

 L. 614       591  BREAK_LOOP       
              592  JUMP_BACK            80  'to 80'
              595  POP_TOP          
              596  END_FINALLY      
            597_0  COME_FROM            80  '80'
              597  JUMP_BACK            80  'to 80'
            600_0  COME_FROM            77  '77'
              600  LOAD_CONST               None
              603  RETURN_VALUE     

Parse error at or near `JUMP_BACK' instruction at offset 597


def do_insertions(insertions, tokens):
    """
    Helper for lexers which must combine the results of several
    sublexers.

    ``insertions`` is a list of ``(index, itokens)`` pairs.
    Each ``itokens`` iterable should be inserted at position
    ``index`` into the token stream given by the ``tokens``
    argument.

    The result is a combined token stream.

    TODO: clean up the code here.
    """
    insertions = iter(insertions)
    try:
        (index, itokens) = insertions.next()
    except StopIteration:
        for item in tokens:
            yield item

        return
    else:
        realpos = None
        insleft = True
        for (i, t, v) in tokens:
            if realpos is None:
                realpos = i
            oldi = 0
            while insleft and i + len(v) >= index:
                tmpval = v[oldi:index - i]
                yield (realpos, t, tmpval)
                realpos += len(tmpval)
                for (it_index, it_token, it_value) in itokens:
                    yield (
                     realpos, it_token, it_value)
                    realpos += len(it_value)

                oldi = index - i
                try:
                    (index, itokens) = insertions.next()
                except StopIteration:
                    insleft = False
                    break

            yield (
             realpos, t, v[oldi:])
            realpos += len(v) - oldi

        while insleft:
            realpos = realpos or 0
            for (p, t, v) in itokens:
                yield (
                 realpos, t, v)
                realpos += len(v)

            try:
                (index, itokens) = insertions.next()
            except StopIteration:
                insleft = False
                break

    return