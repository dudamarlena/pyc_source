# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/contrib/regular_languages/regex_parser.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 7266 bytes
__doc__ = "\nParser for parsing a regular expression.\nTake a string representing a regular expression and return the root node of its\nparse tree.\n\nusage::\n\n    root_node = parse_regex('(hello|world)')\n\nRemarks:\n- The regex parser processes multiline, it ignores all whitespace and supports\n  multiple named groups with the same name and #-style comments.\n\nLimitations:\n- Lookahead is not supported.\n"
from __future__ import unicode_literals
import re
__all__ = ('Repeat', 'Variable', 'Regex', 'Lookahead', 'tokenize_regex', 'parse_regex')

class Node(object):
    """Node"""

    def __add__(self, other_node):
        return Sequence([self, other_node])

    def __or__(self, other_node):
        return Any([self, other_node])


class Any(Node):
    """Any"""

    def __init__(self, children):
        self.children = children

    def __or__(self, other_node):
        return Any(self.children + [other_node])

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.children)


class Sequence(Node):
    """Sequence"""

    def __init__(self, children):
        self.children = children

    def __add__(self, other_node):
        return Sequence(self.children + [other_node])

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.children)


class Regex(Node):
    """Regex"""

    def __init__(self, regex):
        re.compile(regex)
        self.regex = regex

    def __repr__(self):
        return '%s(/%s/)' % (self.__class__.__name__, self.regex)


class Lookahead(Node):
    """Lookahead"""

    def __init__(self, childnode, negative=False):
        self.childnode = childnode
        self.negative = negative

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.childnode)


class Variable(Node):
    """Variable"""

    def __init__(self, childnode, varname=None):
        self.childnode = childnode
        self.varname = varname

    def __repr__(self):
        return '%s(childnode=%r, varname=%r)' % (
         self.__class__.__name__, self.childnode, self.varname)


class Repeat(Node):

    def __init__(self, childnode, min_repeat=0, max_repeat=None, greedy=True):
        self.childnode = childnode
        self.min_repeat = min_repeat
        self.max_repeat = max_repeat
        self.greedy = greedy

    def __repr__(self):
        return '%s(childnode=%r)' % (self.__class__.__name__, self.childnode)


def tokenize_regex(input):
    """
    Takes a string, representing a regular expression as input, and tokenizes
    it.

    :param input: string, representing a regular expression.
    :returns: List of tokens.
    """
    p = re.compile('^(\n        \\(\\?P\\<[a-zA-Z0-9_-]+\\>  | # Start of named group.\n        \\(\\?#[^)]*\\)             | # Comment\n        \\(\\?=                    | # Start of lookahead assertion\n        \\(\\?!                    | # Start of negative lookahead assertion\n        \\(\\?<=                   | # If preceded by.\n        \\(\\?<                    | # If not preceded by.\n        \\(?:                     | # Start of group. (non capturing.)\n        \\(                       | # Start of group.\n        \\(?[iLmsux]              | # Flags.\n        \\(?P=[a-zA-Z]+\\)         | # Back reference to named group\n        \\)                       | # End of group.\n        \\{[^{}]*\\}               | # Repetition\n        \\*\\? | \\+\\? | \\?\\?\\      | # Non greedy repetition.\n        \\* | \\+ | \\?             | # Repetition\n        \\#.*\\n                   | # Comment\n        \\\\. |\n\n        # Character group.\n        \\[\n            ( [^\\]\\\\]  |  \\\\.)*\n        \\]                  |\n\n        [^(){}]             |\n        .\n    )', re.VERBOSE)
    tokens = []
    while input:
        m = p.match(input)
        if m:
            token, input = input[:m.end()], input[m.end():]
            if not token.isspace():
                tokens.append(token)
        else:
            raise Exception('Could not tokenize input regex.')

    return tokens


def parse_regex(regex_tokens):
    """
    Takes a list of tokens from the tokenizer, and returns a parse tree.
    """
    tokens = [
     ')'] + regex_tokens[::-1]

    def wrap(lst):
        """ Turn list into sequence when it contains several items. """
        if len(lst) == 1:
            return lst[0]
        else:
            return Sequence(lst)

    def _parse():
        or_list = []
        result = []

        def wrapped_result():
            if or_list == []:
                return wrap(result)
            else:
                or_list.append(result)
                return Any([wrap(i) for i in or_list])

        while tokens:
            t = tokens.pop()
            if t.startswith('(?P<'):
                variable = Variable((_parse()), varname=(t[4:-1]))
                result.append(variable)
            elif t in ('*', '*?'):
                greedy = t == '*'
                result[-1] = Repeat((result[(-1)]), greedy=greedy)
            elif t in ('+', '+?'):
                greedy = t == '+'
                result[-1] = Repeat((result[(-1)]), min_repeat=1, greedy=greedy)
            elif t in ('?', '??'):
                if result == []:
                    raise Exception('Nothing to repeat.' + repr(tokens))
                else:
                    greedy = t == '?'
                    result[-1] = Repeat((result[(-1)]), min_repeat=0, max_repeat=1, greedy=greedy)
            elif t == '|':
                or_list.append(result)
                result = []
            elif t in ('(', '(?:'):
                result.append(_parse())
            elif t == '(?!':
                result.append(Lookahead((_parse()), negative=True))
            elif t == '(?=':
                result.append(Lookahead((_parse()), negative=False))
            else:
                if t == ')':
                    return wrapped_result()
                if t.startswith('#'):
                    pass
                elif t.startswith('{'):
                    raise Exception('{}-style repitition not yet supported' % t)
                elif t.startswith('(?'):
                    raise Exception('%r not supported' % t)
                elif t.isspace():
                    pass
                else:
                    result.append(Regex(t))

        raise Exception("Expecting ')' token")

    result = _parse()
    if len(tokens) != 0:
        raise Exception('Unmatched parantheses.')
    else:
        return result