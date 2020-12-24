# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/__init__.py
# Compiled at: 2019-10-05 08:06:47
# Size of source mod 2**32: 39079 bytes
"""
parsr is a library for building parsers based on `parsing expression grammars or
PEGs <http://bford.info/pub/lang/peg.pdf>`_.

You build a parser by making subparsers to match simple building blocks like
numbers, strings, symbols, etc. and then composing them to reflect the higher
level structure of your language.

Some means of combination are like those of regular expressions: sequences,
alternatives, repetition, optional matching, etc. However, matching is always
greedy. parsr also allows recursive definitions and the ability to transform
the match of any subparser with a function. The parser can recognize and
interpret its input at the same time.

Here's an example that evaluates arithmetic expressions.

    .. code-block:: python

        from parsr import EOF, Forward, InSet, Many, Number, WS

        def op(args):
            ans, rest = args
            for op, arg in rest:
                if op == "+":
                    ans += arg
                elif op == "-":
                    ans -= arg
                elif op == "*":
                    ans *= arg
                else:
                    ans /= arg
            return ans

        LP = Char("(")
        RP = Char(")")

        expr = Forward()  # Forward declarations allow recursive structure
        factor = WS >> (Number | (LP >> expr << RP)) << WS
        term = (factor + Many(InSet("*/") + factor)).map(op)

        # Notice the funny assignment of Forward definitions.
        expr <= (term + Many(InSet("+-") + term)).map(op)

        evaluate = expr << EOF
"""
from __future__ import print_function
import functools, logging, string
from bisect import bisect_left
from six import StringIO, with_metaclass
log = logging.getLogger(__name__)

class Node(object):
    __doc__ = "\n    Node is the base class of all parsers. It's a generic tree structure with\n    each instance containing a list of its children. Its main purpose is to\n    simplify pretty printing.\n    "

    def __init__(self):
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        return self

    def set_children(self, children):
        self.children = []
        for c in children:
            self.add_child(c)

        return self

    def __repr__(self):
        return self.__class__.__name__


def text_format(tree):
    """
    Converts a PEG into a pretty printed string.
    """
    out = StringIO()
    tab = '  '
    seen = set()

    def inner(cur, prefix):
        print((prefix + str(cur)), file=out)
        if cur in seen:
            return
        seen.add(cur)
        next_prefix = prefix + tab
        for c in cur.children:
            inner(c, next_prefix)

    inner(tree, '')
    out.seek(0)
    return out.read()


def render(tree):
    """
    Pretty prints a PEG.
    """
    print(text_format(tree))


def _debug_hook(func):
    """
    _debug_hook wraps the process function of every parser. It maintains a
    stack of active parsers during evaluation to help with error reporting and
    prints diagnostic messages for parsers with debug enabled.
    """

    @functools.wraps(func)
    def inner(self, pos, data, ctx):
        ctx.parser_stack.append(self)
        if self._debug:
            line = ctx.line(pos) + 1
            col = ctx.col(pos) + 1
            log.debug('Trying {} at line {} col {}'.format(self, line, col))
        try:
            try:
                res = func(self, pos, data, ctx)
                if self._debug:
                    log.debug('Result: {}'.format(res[1]))
                return res
            except:
                if self._debug:
                    ps = '-> '.join([str(p) for p in ctx.parser_stack])
                    log.debug('Failed: {}'.format(ps))
                raise

        finally:
            ctx.parser_stack.pop()

    return inner


class Context(object):
    __doc__ = '\n    An instance of Context is threaded through the process call to every\n    parser. It stores an indention stack to track hanging indents, a tag stack\n    for grammars like xml or apache configuration, the active parser stack for\n    error reporting, and accumulated errors for the farthest position reached.\n    '

    def __init__(self, lines, src=None):
        self.pos = -1
        self.indents = []
        self.tags = []
        self.src = src
        self.lines = [i for i, x in enumerate(lines) if x == '\n']
        self.parser_stack = []
        self.errors = []

    def set(self, pos, msg):
        """
        Every parser that encounters an error calls set with the current
        position and a message. If the error is at the farthest position
        reached by any other parser, the active parser stack and message are
        accumulated onto a list of errors for that position. If the position is
        beyond any previous errors, the error list is cleared before the active
        stack and new error are recorded. This is the "farthest failure
        heurstic."
        """
        if pos > self.pos:
            self.errors = []
        if pos >= self.pos:
            self.pos = pos
            self.errors.append((list(self.parser_stack), msg))

    def line(self, pos):
        return bisect_left(self.lines, pos)

    def col(self, pos):
        p = self.line(pos)
        if p == 0:
            return pos
        else:
            return pos - self.lines[(p - 1)] - 1


class _ParserMeta(type):
    __doc__ = "\n    ParserMeta wraps every parser subclass's process function with the\n    ``_debug_hook`` decorator.\n    "

    def __init__(cls, name, bases, clsdict):
        orig = getattr(cls, 'process')
        setattr(cls, 'process', _debug_hook(orig))


class Parser(with_metaclass(_ParserMeta, Node)):
    __doc__ = '\n    Parser is the common base class of all Parsers.\n    '

    def __init__(self):
        super(Parser, self).__init__()
        self.name = None
        self._debug = False

    def debug(self, d=True):
        """
        Set to ``True`` to enable diagnostic messages before and after the
        parser is invoked.
        """
        self._debug = d
        return self

    @staticmethod
    def _accumulate(first, rest):
        results = [first] if first else []
        if rest:
            results.extend(rest)
        return results

    def sep_by(self, sep):
        """
        Return a parser that matches zero or more instances of the current
        parser separated by instances of the parser sep.
        """
        return Lift(self._accumulate) * Opt(self) * Many(sep >> self)

    def until(self, pred):
        """
        Return an :py:class:`Until` parser that matches zero or more instances
        of the current parser until the pred parser succeeds.
        """
        return Until(self, pred)

    def map(self, func):
        """
        Return a :py:class:`Map` parser that transforms the results of the
        current parser with the function func.
        """
        return Map(self, func)

    def __add__(self, other):
        """
        Return a :py:class:`Sequence` that requires the current parser to be
        followed by the other parser. Additional calls to ``+`` on the returned
        parser will cause it to accumulate "other" onto itself instead of
        creating new Sequences. This has the desirable effect of causing
        sequence matches to be represented as flat lists instead of trees, but
        it can also have unintended consequences if a sequence is used in
        multiple parts of a grammar as the initial element of another sequence.

        :py:class:`Choice`s also accumulate and can lead to similar surprises.
        """
        return Sequence([self, other])

    def __or__(self, other):
        """
        Return a :py:class:`Choice` that requires the current parser or the
        other parser to match. Additional calls to ``|`` on the returned parser
        will cause it to accumulate "other" onto itself instead of creating new
        Choices. This has the desirable effect of making choices more
        efficient, but it can also have unintended consequences if a choice is
        used in multiple parts of a grammar as the initial element of another
        :py:class:`Choice`.
        """
        return Choice([self, other])

    def __lshift__(self, other):
        """
        Return a parser that requires the current parser and the other parser
        but ignores the other parser's result. Both parsers consume input.
        """
        return KeepLeft(self, other)

    def __rshift__(self, other):
        """
        Return a parser that requires the current parser and the other parser
        but ignores the current parser's result. Both parsers consume input.
        """
        return KeepRight(self, other)

    def __and__(self, other):
        """
        Return a parser that requires the current parser and the other parser
        but ignores the current parser's result. Only the current parser
        consumes input.
        """
        return FollowedBy(self, other)

    def __truediv__(self, other):
        """
        Return a parser that requires the current parser but requires the other
        parser to fail. Only the current parser consumes input.
        """
        return NotFollowedBy(self, other)

    def __mod__(self, name):
        """
        Gives the current parser a human friendly name for display in error
        messages and PEG rendering.
        """
        self.name = name
        return self

    def process(self, pos, data, ctx):
        raise NotImplementedError()

    def __call__(self, data, src=None, Ctx=Context):
        """
        Invoke the parser like a function on a regular string of characters.

        Optinally provide an arbitrary external object that will be made available to
        the Context instance. You also can provide a Context subclass if your
        parsers have particular needs not covered by the default
        implementation that provides significant indent and tag stacks.
        """
        data = list(data)
        data.append(None)
        ctx = Ctx(data, src=src)
        try:
            _, ret = self.process(0, data, ctx)
            return ret
        except Exception:
            pass

        err = StringIO()
        lineno = ctx.line(ctx.pos) + 1
        colno = ctx.col(ctx.pos) + 1
        msg = 'At line {} column {}:'
        print((msg.format(lineno, colno, ctx.lines)), file=err)
        for parsers, msg in ctx.errors:
            ps = '-> '.join([str(p) for p in parsers])
            print(('{}: Got {!r}. {}'.format(ps, data[ctx.pos], msg)), file=err)

        err.seek(0)
        raise Exception(err.read())

    def __repr__(self):
        return self.name or self.__class__.__name__


class AnyChar(Parser):

    def process(self, pos, data, ctx):
        c = data[pos]
        if c is not None:
            return (
             pos + 1, c)
        msg = 'Expected any character.'
        ctx.set(pos, msg)
        raise Exception(msg)


class Char(Parser):
    __doc__ = '\n    Char matches a single character.\n\n        .. code-block:: python\n\n            a = Char("a")     # parses a single "a"\n            val = a("a")      # produces an "a" from the data.\n            val = a("b")      # raises an exception\n\n    '

    def __init__(self, char):
        super(Char, self).__init__()
        self.char = char

    def process(self, pos, data, ctx):
        if data[pos] == self.char:
            return (
             pos + 1, self.char)
        msg = 'Expected {!r}.'.format(self.char)
        ctx.set(pos, msg)
        raise Exception(msg)

    def __repr__(self):
        return 'Char({!r})'.format(self.char)


class InSet(Parser):
    __doc__ = '\n    InSet matches any single character from a set.\n\n        .. code-block:: python\n\n            vowel = InSet("aeiou")  # or InSet(set("aeiou"))\n            val = vowel("a")  # okay\n            val = vowel("e")  # okay\n            val = vowel("i")  # okay\n            val = vowel("o")  # okay\n            val = vowel("u")  # okay\n            val = vowel("y")  # raises an exception\n\n    '

    def __init__(self, s, name=None):
        super(InSet, self).__init__()
        self.values = set(s)
        self.name = name

    def process(self, pos, data, ctx):
        c = data[pos]
        if c in self.values:
            return (
             pos + 1, c)
        msg = 'Expected {}.'.format(self)
        ctx.set(pos, msg)
        raise Exception(msg)

    def __repr__(self):
        if not self.name:
            return 'InSet({!r})'.format(sorted(self.values))
        else:
            return super(InSet, self).__repr__()


class String(Parser):
    __doc__ = '\n    Match one or more characters in a set. Matching is greedy.\n\n        .. code-block:: python\n\n            vowels = String("aeiou")\n            val = vowels("a")            # returns "a"\n            val = vowels("u")            # returns "u"\n            val = vowels("aaeiouuoui")   # returns "aaeiouuoui"\n            val = vowels("uoiea")        # returns "uoiea"\n            val = vowels("oouieaaea")    # returns "oouieaaea"\n            val = vowels("ga")           # raises an exception\n\n    '

    def __init__(self, chars, echars=None, min_length=1):
        super(String, self).__init__()
        self.chars = set(chars)
        self.echars = set(echars) if echars else set()
        self.min_length = min_length

    def process(self, pos, data, ctx):
        results = []
        p = data[pos]
        old = pos
        while p in self.chars or p == '\\':
            if p == '\\':
                if data[(pos + 1)] in self.echars:
                    results.append(data[(pos + 1)])
                    pos += 2
            else:
                if p in self.chars:
                    results.append(p)
                    pos += 1
                else:
                    break
            p = data[pos]

        if len(results) < self.min_length:
            msg = 'Expected {} of {}.'.format(self.min_length, sorted(self.chars))
            ctx.set(old, msg)
            raise Exception(msg)
        return (
         pos, ''.join(results))


class Literal(Parser):
    __doc__ = '\n    Match a literal string. The ``value`` keyword lets you return a python\n    value instead of the matched input. The ``ignore_case`` keyword makes the\n    match case insensitive.\n\n        .. code-block:: python\n\n            lit = Literal("true")\n            val = lit("true")  # returns "true"\n            val = lit("True")  # raises an exception\n            val = lit("one")   # raises an exception\n\n            lit = Literal("true", ignore_case=True)\n            val = lit("true")  # returns "true"\n            val = lit("TRUE")  # returns "TRUE"\n            val = lit("one")   # raises an exception\n\n            t = Literal("true", value=True)\n            f = Literal("false", value=False)\n            val = t("true")  # returns the boolean True\n            val = t("True")  # raises an exception\n\n            val = f("false") # returns the boolean False\n            val = f("False") # raises and exception\n\n            t = Literal("true", value=True, ignore_case=True)\n            f = Literal("false", value=False, ignore_case=True)\n            val = t("true")  # returns the boolean True\n            val = t("True")  # returns the boolean True\n\n            val = f("false") # returns the boolean False\n            val = f("False") # returns the boolean False\n    '
    _NULL = object()

    def __init__(self, chars, value=_NULL, ignore_case=False):
        super(Literal, self).__init__()
        self.chars = chars if not ignore_case else chars.lower()
        self.value = value
        self.ignore_case = ignore_case

    def process(self, pos, data, ctx):
        old = pos
        if not self.ignore_case:
            for c in self.chars:
                if data[pos] == c:
                    pos += 1
                else:
                    msg = 'Expected {!r}.'.format(self.chars)
                    ctx.set(old, msg)
                    raise Exception(msg)

            return (
             pos, self.chars if self.value is self._NULL else self.value)
        else:
            result = []
            for c in self.chars:
                if data[pos].lower() == c:
                    result.append(data[pos])
                    pos += 1
                else:
                    msg = 'Expected case insensitive {!r}.'.format(self.chars)
                    ctx.set(old, msg)
                    raise Exception(msg)

            return (
             pos, ''.join(result) if self.value is self._NULL else self.value)


class Wrapper(Parser):
    __doc__ = '\n    Parser that wraps another parser. This can be used to prevent sequences and\n    choices from accidentally accumulating other parsers when used in multiple\n    parts of a grammar.\n    '

    def __init__(self, parser):
        super(Wrapper, self).__init__()
        self.add_child(parser)

    def process(self, pos, data, ctx):
        return self.children[0].process(pos, data, ctx)


class Mark(object):
    __doc__ = '\n    An object created by :py:class:`PosMarker` to capture a value at a position\n    in the input. Marks can give more context to a value transformed by mapped\n    functions.\n    '

    def __init__(self, lineno, col, value):
        self.lineno = lineno
        self.col = col
        self.value = value


class PosMarker(Wrapper):
    __doc__ = '\n    Save the line number and column of a subparser by wrapping it in a\n    PosMarker. The value of the parser that handled the input as well as the\n    initial input position will be returned as a :py:class:`Mark`.\n    '

    def process(self, pos, data, ctx):
        lineno = ctx.line(pos) + 1
        col = ctx.col(pos) + 1
        pos, result = super(PosMarker, self).process(pos, data, ctx)
        return (pos, Mark(lineno, col, result))


class Sequence(Parser):
    __doc__ = '\n    A Sequence requires all of its children to succeed. It returns a list of\n    the values they matched.\n\n    Additional uses of ``+`` on the parser will cause it to accumulate parsers\n    onto itself instead of creating new Sequences. This has the desirable\n    effect of causing sequence results to be represented as flat lists instead\n    of trees, but it can also have unintended consequences if a sequence is\n    used in multiple parts of a grammar as the initial element of another\n    sequence. Use a :py:class:`Wrapper` to prevent that from happening.\n\n        .. code-block :: python\n\n            a = Char("a")     # parses a single "a"\n            b = Char("b")     # parses a single "b"\n            c = Char("c")     # parses a single "c"\n\n            ab = a + b        # parses a single "a" followed by a single "b"\n                              # (a + b) creates a "Sequence" object. Using `ab`\n                              # as an element in a later sequence would modify\n                              # its original definition.\n\n            abc = a + b + c   # parses "abc"\n                              # (a + b) creates a "Sequence" object to which c\n                              # is appended\n\n            val = ab("ab")    # produces a list ["a", "b"]\n            val = ab("a")     # raises an exception\n            val = ab("b")     # raises an exception\n            val = ab("ac")    # raises an exception\n            val = ab("cb")    # raises an exception\n\n            val = abc("abc")  # produces ["a", "b", "c"]\n    '

    def __init__(self, children):
        super(Sequence, self).__init__()
        self.set_children(children)

    def __add__(self, other):
        return self.add_child(other)

    def process(self, pos, data, ctx):
        results = []
        for p in self.children:
            pos, res = p.process(pos, data, ctx)
            results.append(res)

        return (
         pos, results)


class Choice(Parser):
    __doc__ = '\n    A Choice requires at least one of its children to succeed, and it returns\n    the value of the one that matched. Alternatives in a choice are tried left\n    to right, so they have a definite priority. This a feature of PEGs over\n    context free grammars.\n\n    Additional uses of ``|`` on the parser will cause it to accumulate parsers\n    onto itself instead of creating new Choices. This has the desirable effect\n    of increasing efficiency, but it can also have unintended consequences if a\n    choice is used in multiple parts of a grammar as the initial element of\n    another choice. Use a :py:class:`Wrapper` to prevent that from happening.\n\n        .. code-block:: python\n\n            abc = a | b | c   # alternation or choice.\n            val = abc("a")    # parses a single "a"\n            val = abc("b")    # parses a single "b"\n            val = abc("c")    # parses a single "c"\n            val = abc("d")    # raises an exception\n    '

    def __init__(self, children):
        super(Choice, self).__init__()
        self.set_children(children)

    def __or__(self, other):
        return self.add_child(other)

    def process(self, pos, data, ctx):
        for c in self.children:
            try:
                return c.process(pos, data, ctx)
            except:
                pass

        raise Exception()


class Many(Parser):
    __doc__ = '\n    Many wraps another parser and requires it to match a certain number of\n    times.\n\n    When Many matches zero occurences (``lower=0``), it always succeeds. Keep\n    this in mind when using it in a list of alternatives or with\n    :py:class:`FollowedBy` or :py:class:`NotFollowedBy`.\n\n    The results are returned as a list.\n\n        .. code-block:: python\n\n            x = Char("x")\n            xs = Many(x)      # parses many (or no) x\'s in a row\n            val = xs("")      # returns []\n            val = xs("a")     # returns []\n            val = xs("x")     # returns ["x"]\n            val = xs("xxxxx") # returns ["x", "x", "x", "x", "x"]\n            val = xs("xxxxb") # returns ["x", "x", "x", "x"]\n\n            ab = Many(a + b)  # parses "abab..."\n            val = ab("")      # produces []\n            val = ab("ab")    # produces [["a", b"]]\n            val = ab("ba")    # produces []\n            val = ab("ababab")# produces [["a", b"], ["a", "b"], ["a", "b"]]\n\n            ab = Many(a | b)  # parses any combination of "a" and "b" like\n                              # "aababbaba..."\n            val = ab("aababb")# produces ["a", "a", "b", "a", "b", "b"]\n            bs = Many(Char("b"), lower=1) # requires at least one "b"\n\n    '

    def __init__(self, parser, lower=0):
        super(Many, self).__init__()
        self.add_child(parser)
        self.lower = lower

    def process(self, pos, data, ctx):
        orig = pos
        results = []
        p = self.children[0]
        while True:
            try:
                pos, res = p.process(pos, data, ctx)
                results.append(res)
            except Exception:
                break

        if len(results) < self.lower:
            child = self.children[0]
            msg = 'Expected at least {} of {}.'.format(self.lower, child)
            ctx.set(orig, msg)
            raise Exception()
        return (pos, results)

    def __repr__(self):
        if not self.name:
            return 'Many({}, lower={})'.format(self.children[0], self.lower)
        else:
            return super(Many, self).__repr__()


class Until(Parser):
    __doc__ = '\n    Until wraps a parser and a terminal parser. It accumulates matches of the\n    first parser until the terminal parser succeeds. Input for the terminal\n    parser is left unread, and the results of the first parser are returned as\n    a list.\n\n    Since Until can match zero occurences, it always succeeds. Keep this in\n    mind when using it in a list of alternatives or with :py:class:`FollowedBy`\n    or :py:class:`NotFollowedBy`.\n\n        .. code-block:: python\n\n            cs = AnyChar.until(Char("y")) # parses many (or no) characters\n                                          # until a "y" is encountered.\n\n            val = cs("")                  # returns []\n            val = cs("a")                 # returns ["a"]\n            val = cs("x")                 # returns ["x"]\n            val = cs("ccccc")             # returns ["c", "c", "c", "c", "c"]\n            val = cs("abcdycc")           # returns ["a", "b", "c", "d"]\n\n    '

    def __init__(self, parser, predicate):
        super(Until, self).__init__()
        self.set_children([parser, predicate])

    def process(self, pos, data, ctx):
        parser, pred = self.children
        results = []
        while True:
            try:
                pred.process(pos, data, ctx)
            except Exception:
                try:
                    pos, res = parser.process(pos, data, ctx)
                    results.append(res)
                except Exception:
                    break

            else:
                break

        return (
         pos, results)


class FollowedBy(Parser):
    __doc__ = '\n    FollowedBy takes a parser and a predicate parser. The initial parser\n    matches only if the predicate matches the input after it. On success, input\n    for the predicate is left unread, and the result of the first parser is\n    returned.\n\n        .. code-block:: python\n\n            ab = Char("a") & Char("b") # matches an "a" followed by a "b", but\n                                       # the "b" isn\'t consumed from the input.\n            val = ab("ab")             # returns "a" and leaves "b" to be\n                                       # consumed.\n            val = ab("ac")             # raises an exception and doesn\'t\n                                       # consume "a".\n\n    '

    def __init__(self, child, follow):
        super(FollowedBy, self).__init__()
        self.set_children([child, follow])

    def process(self, pos, data, ctx):
        left, right = self.children
        new, res = left.process(pos, data, ctx)
        right.process(new, data, ctx)
        return (new, res)


class NotFollowedBy(Parser):
    __doc__ = '\n    NotFollowedBy takes a parser and a predicate parser. The initial parser\n    matches only if the predicate parser fails to match the input after it. On\n    success, input for the predicate is left unread, and the result of the\n    first parser is returned.\n\n        .. code-block:: python\n\n            anb = Char("a") / Char("b") # matches an "a" not followed by a "b".\n            val = anb("ac")             # returns "a" and leaves "c" to be\n                                        # consumed\n            val = anb("ab")             # raises an exception and doesn\'t\n                                        # consume "a".\n\n    '

    def __init__(self, child, follow):
        super(NotFollowedBy, self).__init__()
        self.set_children([child, follow])

    def process(self, pos, data, ctx):
        left, right = self.children
        new, res = left.process(pos, data, ctx)
        try:
            right.process(new, data, ctx)
        except Exception:
            return (
             new, res)
        else:
            msg = "{} can't follow {}".format(right, left)
            ctx.set(new, msg)
            raise Exception()


class KeepLeft(Parser):
    __doc__ = '\n    KeepLeft takes two parsers. It requires them both to succeed but only\n    returns results for the first one. It consumes input for both.\n\n        .. code-block:: python\n\n            a = Char("a")\n            q = Char(\'"\')\n\n            aq = a << q      # like a + q except only the result of a is\n                             # returned\n            val = aq(\'a"\')   # returns "a". Keeps the thing on the left of the\n                             # <<\n\n    '

    def __init__(self, left, right):
        super(KeepLeft, self).__init__()
        self.set_children([left, right])

    def process(self, pos, data, ctx):
        left, right = self.children
        pos, res = left.process(pos, data, ctx)
        pos, _ = right.process(pos, data, ctx)
        return (pos, res)


class KeepRight(Parser):
    __doc__ = '\n    KeepRight takes two parsers. It requires them both to succeed but only\n    returns results for the second one. It consumes input for both.\n\n        .. code-block:: python\n\n            q = Char(\'"\')\n            a = Char("a")\n\n            qa = q >> a      # like q + a except only the result of a is\n                             # returned\n            val = qa(\'"a\')   # returns "a". Keeps the thing on the right of the\n                             # >>\n\n    '

    def __init__(self, left, right):
        super(KeepRight, self).__init__()
        self.set_children([left, right])

    def process(self, pos, data, ctx):
        left, right = self.children
        pos, _ = left.process(pos, data, ctx)
        return right.process(pos, data, ctx)


class Opt(Parser):
    __doc__ = '\n    Opt wraps a single parser and returns its value if it succeeds. It returns\n    a default value otherwise. The input pointer is advanced only if the\n    wrapped parser succeeds.\n\n        .. code-block:: python\n\n            a = Char("a")\n            o = Opt(a)      # matches an "a" if its available. Still succeeds\n                            # otherwise but doesn\'t advance the read pointer.\n            val = o("a")    # returns "a"\n            val = o("b")    # returns None. Read pointer is not advanced.\n\n            o = Opt(a, default="x") # matches an "a" if its available. Returns\n                                    # "x" otherwise.\n            val = o("a")    # returns "a"\n            val = o("b")    # returns "x". Read pointer is not advanced.\n\n    '

    def __init__(self, p, default=None):
        super(Opt, self).__init__()
        self.add_child(p)
        self.default = default

    def process(self, pos, data, ctx):
        try:
            return self.children[0].process(pos, data, ctx)
        except Exception:
            return (
             pos, self.default)


class Map(Parser):
    __doc__ = '\n    Map wraps a parser and a function. It returns the result of using the\n    function to transform the wrapped parser\'s result.\n\n    Example::\n\n        .. code-block:: python\n\n            Digit = InSet("0123456789")\n            Digits = Many(Digit, lower=1)\n            Number = Digits.map(lambda x: int("".join(x)))\n\n    '

    def __init__(self, child, func):
        super(Map, self).__init__()
        self.add_child(child)
        self.func = func

    def process(self, pos, data, ctx):
        pos, res = self.children[0].process(pos, data, ctx)
        return (pos, self.func(res))

    def __repr__(self):
        if not self.name:
            return 'Map({}({}))'.format(self.func.__name__, self.children[0])
        else:
            return super(Map, self).__repr__()


class Lift(Parser):
    __doc__ = '\n    Lift wraps a function of multiple arguments. Use it with the multiplication\n    operator on as many parsers as function arguments, and the results of those\n    parsers will be passed to the function. The result of a Lift parser is the\n    result of the wrapped function.\n\n    Example::\n\n        .. code-block:: python\n\n            def comb(a, b, c):\n                return "".join([a, b, c])\n\n            # You\'d normally invoke comb like comb("x", "y", "z"), but you can\n            # "lift" it for use with parsers like this:\n\n            x = Char("x")\n            y = Char("y")\n            z = Char("z")\n            p = Lift(comb) * x * y * z\n\n            # The * operator separates parsers whose results will go into the\n            # arguments of the lifted function. I\'ve used Char above, but x, y,\n            # and z can be arbitrarily complex.\n\n            val = p("xyz")  # would return "xyz"\n            val = p("xyx")  # raises an exception. nothing would be consumed\n\n    '

    def __init__(self, func):
        super(Lift, self).__init__()
        self.func = func

    def __mul__(self, other):
        return self.add_child(other)

    def process(self, pos, data, ctx):
        results = []
        for c in self.children:
            pos, res = c.process(pos, data, ctx)
            results.append(res)

        try:
            return (
             pos, (self.func)(*results))
        except Exception as e:
            ctx.set(pos, str(e))
            raise


class Forward(Parser):
    __doc__ = "\n    Forward allows recursive grammars where a nonterminal's definition includes\n    itself directly or indirectly. You initially create a Forward nonterminal\n    with regular assignment.\n\n        .. code-block:: python\n\n            expr = Forward()\n\n    You later give it its real definition with the ``<=`` operator.\n\n        .. code-block:: python\n\n            expr <= (term + Many(LowOps + term)).map(op)\n\n    "

    def __init__(self):
        super(Forward, self).__init__()
        self.delegate = None

    def __le__(self, delegate):
        self.set_children([delegate])

    def process(self, pos, data, ctx):
        return self.children[0].process(pos, data, ctx)


class EOF(Parser):
    __doc__ = "\n    EOF marks the end of input. This parser doesn't need to be created\n    directly. An instance is provided in this module.\n\n        .. code-block:: python\n\n            # Top executes an Expr and ensures no input is left over.\n            Top = Expr << EOF\n\n    "

    def process(self, pos, data, ctx):
        if data[pos] is None:
            return (
             pos, None)
        msg = 'Expected end of input.'
        ctx.set(pos, msg)
        raise Exception(msg)


class EnclosedComment(Parser):
    __doc__ = '\n    EnclosedComment matches a start literal, an end literal, and all characters\n    between. It returns the content between the start and end.\n\n        .. code-block:: python\n\n            Comment = EnclosedComment("/*", "*/")\n\n    '

    def __init__(self, s, e):
        super(EnclosedComment, self).__init__()
        Start = Literal(s)
        End = Literal(e)
        p = Start >> AnyChar.until(End).map(lambda x: ''.join(x)) << End
        self.add_child(p)

    def process(self, pos, data, ctx):
        return self.children[0].process(pos, data, ctx)


class OneLineComment(Parser):
    __doc__ = '\n    OneLineComment matches everything from a literal to the end of a line,\n    excluding the end of line characters themselves. It returns the content\n    between the start literal and the end of the line.\n\n        .. code-block:: python\n\n            Comment = OneLineComment("#") | OneLineComment("//")\n\n    '

    def __init__(self, s):
        super(OneLineComment, self).__init__()
        p = Literal(s) >> Opt(AnyChar.until(InSet('\r\n')), '')
        self.add_child(p)

    def process(self, pos, data, ctx):
        return self.children[0].process(pos, data, ctx)


class WithIndent(Wrapper):
    __doc__ = '\n    Consumes whitespace until a non-whitespace character is encountered, pushes\n    the column position onto an indentation stack in the :py:class:`Context`,\n    and then calls the parser it\'s wrapping. The wrapped parser and any\n    of its children can make use of the saved indentation. Returns the value of\n    the wrapped parser.\n\n    WithIndent allows :py:class:`HangingString` to work by giving a way to mark\n    how indented following lines must be to count as continuations.\n\n        .. code-block:: python\n\n            Key = WS >> PosMarker(String(key_chars)) << WS\n            Sep = InSet(sep_chars, "Sep")\n            Value = WS >> (Boolean | HangingString(value_chars))\n            KVPair = WithIndent(Key + Opt(Sep >> Value))\n\n    '

    def process(self, pos, data, ctx):
        new, _ = WS.process(pos, data, ctx)
        try:
            ctx.indents.append(ctx.col(new))
            return self.children[0].process(new, data, ctx)
        finally:
            ctx.indents.pop()


class HangingString(Parser):
    __doc__ = '\n    HangingString matches lines with indented continuations like in ini files.\n\n        .. code-block:: python\n\n            Key = WS >> PosMarker(String(key_chars)) << WS\n            Sep = InSet(sep_chars, "Sep")\n            Value = WS >> (Boolean | HangingString(value_chars))\n            KVPair = WithIndent(Key + Opt(Sep >> Value))\n\n    '

    def __init__(self, chars, echars=None, min_length=1):
        super(HangingString, self).__init__()
        p = String(chars, echars=echars, min_length=min_length)
        self.add_child(p << (EOL | EOF))

    def process(self, pos, data, ctx):
        old = pos
        results = []
        while True:
            try:
                if ctx.col(pos) > ctx.indents[(-1)]:
                    pos, res = self.children[0].process(pos, data, ctx)
                    results.append(res.rstrip(' \\'))
                else:
                    pos = old
                    break
                old = pos
                pos, _ = WS.process(pos, data, ctx)
            except Exception:
                break

        ret = ' '.join(results)
        return (pos, ret)


class StartTagName(Wrapper):
    __doc__ = '\n    Wraps a parser that represents a starting tag for grammars like xml, html,\n    etc. The tag result is captured and put onto a tag stack in the\n    :py:class:`Context` object.\n    '

    def process(self, pos, data, ctx):
        pos, res = self.children[0].process(pos, data, ctx)
        ctx.tags.append(res)
        return (pos, res)


class EndTagName(Wrapper):
    __doc__ = '\n    Wraps a parser that represents an end tag for grammars like xml, html, etc.\n    The result is captured and compared to the last tag on the tag stack in the\n    :py:class:`Context` object. The tags must match for the parse to be\n    successful.\n    '

    def __init__(self, parser, ignore_case=False):
        super(EndTagName, self).__init__(parser)
        self.ignore_case = ignore_case

    def process(self, pos, data, ctx):
        pos, res = self.children[0].process(pos, data, ctx)
        expect = ctx.tags.pop()
        r, e = res, expect
        if self.ignore_case:
            r = res.lower()
            e = expect.lower()
        if r != e:
            msg = 'Expected {!r}. Got {!r}.'.format(expect, res)
            ctx.set(pos, msg)
            raise Exception(msg)
        return (
         pos, res)


def _make_number(sign, int_part, frac_part):
    tmp = sign + int_part + (''.join(frac_part) if frac_part else '')
    if '.' in tmp:
        return float(tmp)
    else:
        return int(tmp)


def skip_none(x):
    """
    Filters ``None`` values from a list. Often used with map.
    """
    return [i for i in x if i is not None]


EOF = EOF()
EOL = InSet('\n\r') % 'EOL'
LineEnd = Wrapper(EOL | EOF) % 'LineEnd'
EQ = Char('=')
LT = Char('<')
GT = Char('>')
FS = Char('/')
LeftCurly = Char('{')
RightCurly = Char('}')
LeftBracket = Char('[')
RightBracket = Char(']')
LeftParen = Char('(')
RightParen = Char(')')
Colon = Char(':')
SemiColon = Char(';')
Comma = Char(',')
AnyChar = AnyChar()
NonZeroDigit = InSet(set(string.digits) - set('0'))
Digit = InSet(string.digits) % 'Digit'
Digits = String(string.digits) % 'Digits'
Letter = InSet(string.ascii_letters)
Letters = String(string.ascii_letters)
WSChar = InSet(set(string.whitespace) - set('\n\r')) % 'Whitespace w/o EOL'
WS = Many(InSet(string.whitespace) % 'WS') % 'Whitespace'
Number = Lift(_make_number) * Opt(Char('-'), '') * Digits * Opt(Char('.') + Digits) % 'Number'
SingleQuotedString = Char("'") >> String(set(string.printable) - set("'"), "'") << Char("'")
DoubleQuotedString = Char('"') >> String(set(string.printable) - set('"'), '"') << Char('"')
QuotedString = Wrapper(DoubleQuotedString | SingleQuotedString) % 'Quoted String'