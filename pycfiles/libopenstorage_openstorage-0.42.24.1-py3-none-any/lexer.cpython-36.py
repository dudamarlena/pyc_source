# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexer.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 31698 bytes
"""
    pygments.lexer
    ~~~~~~~~~~~~~~

    Base lexer classes.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from __future__ import print_function
import re, sys, time
from pygments.filter import apply_filters, Filter
from pygments.filters import get_filter_by_name
from pygments.token import Error, Text, Other, _TokenType
from pygments.util import get_bool_opt, get_int_opt, get_list_opt, make_analysator, text_type, add_metaclass, iteritems, Future, guess_decode
from pygments.regexopt import regex_opt
__all__ = [
 'Lexer', 'RegexLexer', 'ExtendedRegexLexer', 'DelegatingLexer',
 'LexerContext', 'include', 'inherit', 'bygroups', 'using', 'this',
 'default', 'words']
_encoding_map = [
 (b'\xef\xbb\xbf', 'utf-8'),
 (b'\xff\xfe\x00\x00', 'utf-32'),
 (b'\x00\x00\xfe\xff', 'utf-32be'),
 (b'\xff\xfe', 'utf-16'),
 (b'\xfe\xff', 'utf-16be')]
_default_analyse = staticmethod(lambda x: 0.0)

class LexerMeta(type):
    __doc__ = '\n    This metaclass automagically converts ``analyse_text`` methods into\n    static methods which always return float values.\n    '

    def __new__(mcs, name, bases, d):
        if 'analyse_text' in d:
            d['analyse_text'] = make_analysator(d['analyse_text'])
        return type.__new__(mcs, name, bases, d)


@add_metaclass(LexerMeta)
class Lexer(object):
    __doc__ = "\n    Lexer for a specific language.\n\n    Basic options recognized:\n    ``stripnl``\n        Strip leading and trailing newlines from the input (default: True).\n    ``stripall``\n        Strip all leading and trailing whitespace from the input\n        (default: False).\n    ``ensurenl``\n        Make sure that the input ends with a newline (default: True).  This\n        is required for some lexers that consume input linewise.\n\n        .. versionadded:: 1.3\n\n    ``tabsize``\n        If given and greater than 0, expand tabs in the input (default: 0).\n    ``encoding``\n        If given, must be an encoding name. This encoding will be used to\n        convert the input string to Unicode, if it is not already a Unicode\n        string (default: ``'guess'``, which uses a simple UTF-8 / Locale /\n        Latin1 detection.  Can also be ``'chardet'`` to use the chardet\n        library, if it is installed.\n    ``inencoding``\n        Overrides the ``encoding`` if given.\n    "
    name = None
    aliases = []
    filenames = []
    alias_filenames = []
    mimetypes = []
    priority = 0

    def __init__(self, **options):
        self.options = options
        self.stripnl = get_bool_opt(options, 'stripnl', True)
        self.stripall = get_bool_opt(options, 'stripall', False)
        self.ensurenl = get_bool_opt(options, 'ensurenl', True)
        self.tabsize = get_int_opt(options, 'tabsize', 0)
        self.encoding = options.get('encoding', 'guess')
        self.encoding = options.get('inencoding') or self.encoding
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
        if not isinstance(text, text_type):
            if self.encoding == 'guess':
                text, _ = guess_decode(text)
            else:
                if self.encoding == 'chardet':
                    try:
                        import chardet
                    except ImportError:
                        raise ImportError('To enable chardet encoding guessing, please install the chardet library from http://chardet.feedparser.org/')

                    decoded = None
                    for bom, encoding in _encoding_map:
                        if text.startswith(bom):
                            decoded = text[len(bom):].decode(encoding, 'replace')
                            break

                    if decoded is None:
                        enc = chardet.detect(text[:1024])
                        decoded = text.decode(enc.get('encoding') or 'utf-8', 'replace')
                    text = decoded
                else:
                    text = text.decode(self.encoding)
                    if text.startswith('\ufeff'):
                        text = text[len('\ufeff'):]
        else:
            if text.startswith('\ufeff'):
                text = text[len('\ufeff'):]
            else:
                text = text.replace('\r\n', '\n')
                text = text.replace('\r', '\n')
                if self.stripall:
                    text = text.strip()
                else:
                    if self.stripnl:
                        text = text.strip('\n')
                if self.tabsize > 0:
                    text = text.expandtabs(self.tabsize)
                if self.ensurenl:
                    if not text.endswith('\n'):
                        text += '\n'

                def streamer():
                    for _, t, v in self.get_tokens_unprocessed(text):
                        yield (
                         t, v)

                stream = streamer()
                stream = unfiltered or apply_filters(stream, self.filters, self)
            return stream

    def get_tokens_unprocessed(self, text):
        """
        Return an iterable of (index, tokentype, value) pairs where "index"
        is the starting position of the token within the input text.

        In subclasses, implement this method as a generator to
        maximize effectiveness.
        """
        raise NotImplementedError


class DelegatingLexer(Lexer):
    __doc__ = '\n    This lexer takes two lexer as arguments. A root lexer and\n    a language lexer. First everything is scanned using the language\n    lexer, afterwards all ``Other`` tokens are lexed using the root\n    lexer.\n\n    The lexers from the ``template`` lexer package use this base lexer.\n    '

    def __init__(self, _root_lexer, _language_lexer, _needle=Other, **options):
        self.root_lexer = _root_lexer(**options)
        self.language_lexer = _language_lexer(**options)
        self.needle = _needle
        (Lexer.__init__)(self, **options)

    def get_tokens_unprocessed(self, text):
        buffered = ''
        insertions = []
        lng_buffer = []
        for i, t, v in self.language_lexer.get_tokens_unprocessed(text):
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
    __doc__ = '\n    Indicates that a state should include rules from another state.\n    '


class _inherit(object):
    __doc__ = '\n    Indicates the a state should inherit from its superclass.\n    '

    def __repr__(self):
        return 'inherit'


inherit = _inherit()

class combined(tuple):
    __doc__ = '\n    Indicates a state combined from multiple states.\n    '

    def __new__(cls, *args):
        return tuple.__new__(cls, args)

    def __init__(self, *args):
        pass


class _PseudoMatch(object):
    __doc__ = '\n    A pseudo match object constructed from a string.\n    '

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
        for i, action in enumerate(args):
            if action is None:
                continue
            else:
                if type(action) is _TokenType:
                    data = match.group(i + 1)
                    if data:
                        yield (
                         match.start(i + 1), action, data)
                    else:
                        data = match.group(i + 1)
                        if data is not None:
                            if ctx:
                                ctx.pos = match.start(i + 1)
                            for item in action(lexer, _PseudoMatch(match.start(i + 1), data), ctx):
                                if item:
                                    yield item

        if ctx:
            ctx.pos = match.end()

    return callback


class _This(object):
    __doc__ = '\n    Special singleton used for indicating the caller class.\n    Used by ``using``.\n    '


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
    else:
        if _other is this:

            def callback(lexer, match, ctx=None):
                if kwargs:
                    kwargs.update(lexer.options)
                    lx = (lexer.__class__)(**kwargs)
                else:
                    lx = lexer
                s = match.start()
                for i, t, v in (lx.get_tokens_unprocessed)((match.group()), **gt_kwargs):
                    yield (
                     i + s, t, v)

                if ctx:
                    ctx.pos = match.end()

        else:

            def callback(lexer, match, ctx=None):
                kwargs.update(lexer.options)
                lx = _other(**kwargs)
                s = match.start()
                for i, t, v in (lx.get_tokens_unprocessed)((match.group()), **gt_kwargs):
                    yield (
                     i + s, t, v)

                if ctx:
                    ctx.pos = match.end()

    return callback


class default:
    __doc__ = "\n    Indicates a state or state action (e.g. #pop) to apply.\n    For example default('#pop') is equivalent to ('', Token, '#pop')\n    Note that state tuples may be used as well.\n\n    .. versionadded:: 2.0\n    "

    def __init__(self, state):
        self.state = state


class words(Future):
    __doc__ = '\n    Indicates a list of literal words that is transformed into an optimized\n    regex that matches any of the words.\n\n    .. versionadded:: 2.0\n    '

    def __init__(self, words, prefix='', suffix=''):
        self.words = words
        self.prefix = prefix
        self.suffix = suffix

    def get(self):
        return regex_opt((self.words), prefix=(self.prefix), suffix=(self.suffix))


class RegexLexerMeta(LexerMeta):
    __doc__ = '\n    Metaclass for RegexLexer, creates the self._tokens attribute from\n    self.tokens on the first instantiation.\n    '

    def _process_regex(cls, regex, rflags, state):
        """Preprocess the regular expression component of a token definition."""
        if isinstance(regex, Future):
            regex = regex.get()
        return re.compile(regex, rflags).match

    def _process_token(cls, token):
        """Preprocess the token component of a token definition."""
        if not type(token) is _TokenType:
            if not callable(token):
                raise AssertionError('token type must be simple type or callable, not %r' % (token,))
        return token

    def _process_new_state(cls, new_state, unprocessed, processed):
        """Preprocess the state transition action of a token definition."""
        if isinstance(new_state, str):
            if new_state == '#pop':
                return -1
            else:
                if new_state in unprocessed:
                    return (
                     new_state,)
                if new_state == '#push':
                    return new_state
                if new_state[:5] == '#pop:':
                    return -int(new_state[5:])
            if not False:
                raise AssertionError('unknown new state %r' % new_state)
        else:
            if isinstance(new_state, combined):
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
                if not istate in unprocessed:
                    assert istate in ('#pop', '#push'), 'unknown new state ' + istate

            return new_state
        assert False, 'unknown new state def %r' % new_state

    def _process_state(cls, unprocessed, processed, state):
        """Preprocess a single state definition."""
        if not type(state) is str:
            raise AssertionError('wrong state name %r' % state)
        elif not state[0] != '#':
            raise AssertionError('invalid state name %r' % state)
        if state in processed:
            return processed[state]
        else:
            tokens = processed[state] = []
            rflags = cls.flags
            for tdef in unprocessed[state]:
                if isinstance(tdef, include):
                    assert tdef != state, 'circular state reference %r' % state
                    tokens.extend(cls._process_state(unprocessed, processed, str(tdef)))
                else:
                    if isinstance(tdef, _inherit):
                        continue
                    if isinstance(tdef, default):
                        new_state = cls._process_new_state(tdef.state, unprocessed, processed)
                        tokens.append((re.compile('').match, None, new_state))
                    else:
                        if not type(tdef) is tuple:
                            raise AssertionError('wrong rule def %r' % tdef)
                        else:
                            try:
                                rex = cls._process_regex(tdef[0], rflags, state)
                            except Exception as err:
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
        for state in list(tokendefs):
            cls._process_state(tokendefs, processed, state)

        return processed

    def get_tokendefs(cls):
        """
        Merge tokens from superclasses in MRO order, returning a single tokendef
        dictionary.

        Any state that is not defined by a subclass will be inherited
        automatically.  States that *are* defined by subclasses will, by
        default, override that state in the superclass.  If a subclass wishes to
        inherit definitions from a superclass, it can use the special value
        "inherit", which will cause the superclass' state definition to be
        included at that point in the state.
        """
        tokens = {}
        inheritable = {}
        for c in cls.__mro__:
            toks = c.__dict__.get('tokens', {})
            for state, items in iteritems(toks):
                curitems = tokens.get(state)
                if curitems is None:
                    tokens[state] = items
                    try:
                        inherit_ndx = items.index(inherit)
                    except ValueError:
                        continue

                    inheritable[state] = inherit_ndx
                else:
                    inherit_ndx = inheritable.pop(state, None)
                    if inherit_ndx is None:
                        pass
                    else:
                        curitems[inherit_ndx:inherit_ndx + 1] = items
                        try:
                            new_inh_ndx = items.index(inherit)
                        except ValueError:
                            pass

                    inheritable[state] = inherit_ndx + new_inh_ndx

        return tokens

    def __call__(cls, *args, **kwds):
        """Instantiate cls after preprocessing its token definitions."""
        if '_tokens' not in cls.__dict__:
            cls._all_tokens = {}
            cls._tmpname = 0
            if hasattr(cls, 'token_variants'):
                if cls.token_variants:
                    pass
            else:
                cls._tokens = cls.process_tokendef('', cls.get_tokendefs())
        return (type.__call__)(cls, *args, **kwds)


@add_metaclass(RegexLexerMeta)
class RegexLexer(Lexer):
    __doc__ = '\n    Base for simple stateful regular expression-based lexers.\n    Simplifies the lexing process so that you need only\n    provide a list of states and regular expressions.\n    '
    flags = re.MULTILINE
    tokens = {}

    def get_tokens_unprocessed(self, text, stack=('root',)):
        """
        Split ``text`` into (tokentype, text) pairs.

        ``stack`` is the inital stack (default: ``['root']``)
        """
        pos = 0
        tokendefs = self._tokens
        statestack = list(stack)
        statetokens = tokendefs[statestack[(-1)]]
        while True:
            for rexmatch, action, new_state in statetokens:
                m = rexmatch(text, pos)
                if m:
                    if action is not None:
                        if type(action) is _TokenType:
                            yield (
                             pos, action, m.group())
                        else:
                            for item in action(self, m):
                                yield item

                    pos = m.end()
                    if new_state is not None:
                        if isinstance(new_state, tuple):
                            for state in new_state:
                                if state == '#pop':
                                    if len(statestack) > 1:
                                        statestack.pop()
                                else:
                                    if state == '#push':
                                        statestack.append(statestack[(-1)])
                                    else:
                                        statestack.append(state)

                        else:
                            if isinstance(new_state, int):
                                if abs(new_state) >= len(statestack):
                                    del statestack[1:]
                                else:
                                    del statestack[new_state:]
                            else:
                                if new_state == '#push':
                                    statestack.append(statestack[(-1)])
                                else:
                                    assert False, 'wrong state def: %r' % new_state
                        statetokens = tokendefs[statestack[(-1)]]
                    break
            else:
                try:
                    if text[pos] == '\n':
                        statestack = ['root']
                        statetokens = tokendefs['root']
                        yield (pos, Text, '\n')
                        pos += 1
                        continue
                    yield (
                     pos, Error, text[pos])
                    pos += 1
                except IndexError:
                    break


class LexerContext(object):
    __doc__ = '\n    A helper object that holds lexer position data.\n    '

    def __init__(self, text, pos, stack=None, end=None):
        self.text = text
        self.pos = pos
        self.end = end or len(text)
        self.stack = stack or ['root']

    def __repr__(self):
        return 'LexerContext(%r, %r, %r)' % (
         self.text, self.pos, self.stack)


class ExtendedRegexLexer(RegexLexer):
    __doc__ = '\n    A RegexLexer that uses a context object to store its state.\n    '

    def get_tokens_unprocessed(self, text=None, context=None):
        """
        Split ``text`` into (tokentype, text) pairs.
        If ``context`` is given, use this lexer context instead.
        """
        tokendefs = self._tokens
        if not context:
            ctx = LexerContext(text, 0)
            statetokens = tokendefs['root']
        else:
            ctx = context
            statetokens = tokendefs[ctx.stack[(-1)]]
            text = ctx.text
        while True:
            for rexmatch, action, new_state in statetokens:
                m = rexmatch(text, ctx.pos, ctx.end)
                if m:
                    if action is not None:
                        if type(action) is _TokenType:
                            yield (
                             ctx.pos, action, m.group())
                            ctx.pos = m.end()
                        else:
                            for item in action(self, m, ctx):
                                yield item

                            if not new_state:
                                statetokens = tokendefs[ctx.stack[(-1)]]
                    if new_state is not None:
                        if isinstance(new_state, tuple):
                            for state in new_state:
                                if state == '#pop':
                                    if len(ctx.stack) > 1:
                                        ctx.stack.pop()
                                else:
                                    if state == '#push':
                                        ctx.stack.append(ctx.stack[(-1)])
                                    else:
                                        ctx.stack.append(state)

                        else:
                            if isinstance(new_state, int):
                                if abs(new_state) >= len(ctx.stack):
                                    del ctx.state[1:]
                                else:
                                    del ctx.stack[new_state:]
                            else:
                                if new_state == '#push':
                                    ctx.stack.append(ctx.stack[(-1)])
                                else:
                                    assert False, 'wrong state def: %r' % new_state
                        statetokens = tokendefs[ctx.stack[(-1)]]
                    break
            else:
                try:
                    if ctx.pos >= ctx.end:
                        break
                    if text[ctx.pos] == '\n':
                        ctx.stack = ['root']
                        statetokens = tokendefs['root']
                        yield (ctx.pos, Text, '\n')
                        ctx.pos += 1
                        continue
                    yield (
                     ctx.pos, Error, text[ctx.pos])
                    ctx.pos += 1
                except IndexError:
                    break


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
        index, itokens = next(insertions)
    except StopIteration:
        for item in tokens:
            yield item

        return
    else:
        realpos = None
        insleft = True
        for i, t, v in tokens:
            if realpos is None:
                realpos = i
            oldi = 0
            while insleft and i + len(v) >= index:
                tmpval = v[oldi:index - i]
                yield (realpos, t, tmpval)
                realpos += len(tmpval)
                for it_index, it_token, it_value in itokens:
                    yield (
                     realpos, it_token, it_value)
                    realpos += len(it_value)

                oldi = index - i
                try:
                    index, itokens = next(insertions)
                except StopIteration:
                    insleft = False
                    break

            yield (
             realpos, t, v[oldi:])
            realpos += len(v) - oldi

        while insleft:
            realpos = realpos or 0
            for p, t, v in itokens:
                yield (
                 realpos, t, v)
                realpos += len(v)

            try:
                index, itokens = next(insertions)
            except StopIteration:
                insleft = False
                break


class ProfilingRegexLexerMeta(RegexLexerMeta):
    __doc__ = 'Metaclass for ProfilingRegexLexer, collects regex timing info.'

    def _process_regex(cls, regex, rflags, state):
        if isinstance(regex, words):
            rex = regex_opt((regex.words), prefix=(regex.prefix), suffix=(regex.suffix))
        else:
            rex = regex
        compiled = re.compile(rex, rflags)

        def match_func(text, pos, endpos=sys.maxsize):
            info = cls._prof_data[(-1)].setdefault((state, rex), [0, 0.0])
            t0 = time.time()
            res = compiled.match(text, pos, endpos)
            t1 = time.time()
            info[0] += 1
            info[1] += t1 - t0
            return res

        return match_func


@add_metaclass(ProfilingRegexLexerMeta)
class ProfilingRegexLexer(RegexLexer):
    __doc__ = 'Drop-in replacement for RegexLexer that does profiling of its regexes.'
    _prof_data = []
    _prof_sort_index = 4

    def get_tokens_unprocessed(self, text, stack=('root',)):
        self.__class__._prof_data.append({})
        for tok in RegexLexer.get_tokens_unprocessed(self, text, stack):
            yield tok

        rawdata = self.__class__._prof_data.pop()
        data = sorted(((s, repr(r).strip("u'").replace('\\\\', '\\')[:65], n, 1000 * t, 1000 * t / n) for (s, r), (n, t) in rawdata.items()),
          key=(lambda x: x[self._prof_sort_index]),
          reverse=True)
        sum_total = sum(x[3] for x in data)
        print()
        print('Profiling result for %s lexing %d chars in %.3f ms' % (
         self.__class__.__name__, len(text), sum_total))
        print('=' * 110)
        print('%-20s %-64s ncalls  tottime  percall' % ('state', 'regex'))
        print('-' * 110)
        for d in data:
            print('%-20s %-65s %5d %8.4f %8.4f' % d)

        print('=' * 110)