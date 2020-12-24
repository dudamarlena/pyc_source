# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/context/dataindex.py
# Compiled at: 2017-01-15 13:25:40
from __future__ import unicode_literals
from __future__ import print_function
from ..compat import implements_to_string, text_type, string_types, implements_bool
from operator import truth

@implements_bool
@implements_to_string
class ParseResult(object):
    """An immutable list like object that stores the results of a parsed index"""
    __slots__ = [
     b'tokens', b'from_root', b'index']

    def __init__(self, tokens, from_root):
        self.tokens = tokens
        self.from_root = from_root
        self.index = None
        return

    def __str__(self):
        if self.index is None:
            if self.from_root:
                self.index = b'.' + build(self.tokens)
            else:
                self.index = build(self.tokens)
        return self.index

    def __repr__(self):
        return b'ParseResult(%r)' % text_type(self)

    @property
    def top_tail(self):
        return (self.tokens[0], self.tokens[1:])

    def __moyarepr__(self, context):
        return text_type(self)

    def get(self, index, default=None):
        return self.tokens.get(index, default)

    def as_list(self):
        return self.tokens[:]

    def __iter__(self):
        return iter(self.tokens)

    def __len__(self):
        return len(self.tokens)

    def __getitem__(self, i):
        return self.tokens[i]

    def __eq__(self, other):
        return self.tokens == other

    def __ne__(self, other):
        return self.tokens != other

    def __bool__(self):
        return truth(self.tokens)


def parse(s, parse_cache={}):
    """Parse a string containing a dotted notation data index in to a list of indices"""
    if isinstance(s, ParseResult):
        return s
    else:
        cached_result = parse_cache.get(s, None)
        if cached_result is not None:
            return cached_result
        from_root = s.startswith(b'.')
        iter_chars = iter(s)
        tokens = []
        token = []
        append_token = tokens.append
        append_char = token.append

        def pop():
            c = next(iter_chars, None)
            if c is None:
                return (None, None)
            else:
                if c == b'\\':
                    c = next(iter_chars, None)
                    if c is None:
                        return (None, None)
                    return (True, c)
                else:
                    if c == b'.':
                        return (True, None)
                    return (False, c)

                return

        def pop2():
            c = next(iter_chars, None)
            if c is None:
                return (None, None)
            else:
                return (
                 False, c)

        def asint(s):
            if s.isdigit():
                return int(s)
            return s

        join = (b'').join
        while 1:
            literal, c = pop()
            if literal is None:
                break
            if c is None:
                continue
            if not literal and c == b'"':
                while 1:
                    literal, c = pop2()
                    if c is None:
                        break
                    elif not literal and c == b'"':
                        append_token(join(token))
                        del token[:]
                        break
                    else:
                        append_char(c)

            else:
                append_char(c)
                while 1:
                    literal, c = pop()
                    if c is None:
                        append_token(asint(join(token)))
                        del token[:]
                        break
                    else:
                        append_char(c)

        if token:
            append_token(asint(join(token)))
        tokens = ParseResult(tokens, from_root)
        parse_cache[s] = tokens
        return tokens


def build(indices, absolute=False):
    """Combines a sequence of indices in to a data index string"""
    if isinstance(indices, string_types):
        return indices
    else:

        def escape(s):
            if isinstance(s, string_types):
                if b' ' in s or b'.' in s:
                    s = b'"%s"' % s.replace(b'"', b'\\"')
                return s
            return text_type(s)

        if absolute:
            return b'.' + (b'.').join(escape(s) for s in indices)
        return (b'.').join(escape(s) for s in indices)


def is_from_root(indices):
    """Test a string index is from the root"""
    if hasattr(indices, b'from_root'):
        return indices.from_root
    return indices.startswith(b'.')


def normalise(s):
    """Normalizes a data index"""
    return build(parse(s))


normalize = normalise

def iter_index(index):
    index_accumulator = []
    push = index_accumulator.append
    join = (b'.').join
    for name in parse(index):
        push(name)
        yield (name, join(text_type(s) for s in index_accumulator))


def join(*indices):
    """Joins 2 or more inidices in to one"""
    absolute = False
    joined = []
    append = joined.append
    for index in indices:
        if isinstance(index, string_types):
            if index.startswith(b'.'):
                absolute = True
                del joined[:]
                append(parse(index[1:]))
            else:
                append(parse(index))
        else:
            if getattr(index, b'from_root', False):
                absolute = True
                del joined[:]
            append(index)

    new_indices = []
    for index in joined:
        new_indices.extend(index)

    return build(new_indices, absolute)


indexjoin = join

def makeindex(*subindices):
    """Make an index from sub indexes"""
    return (b'.').join(text_type(i) for i in subindices)


def join_parsed(*indices):
    absolute = False
    joined = []
    append = joined.append
    for index in indices:
        if isinstance(index, string_types):
            if index.startswith(b'.'):
                absolute = True
                del joined[:]
                append(parse(index[1:]))
            else:
                append(parse(index))
        else:
            if getattr(index, b'from_root', False):
                absolute = True
                del joined[:]
            append(index)

    new_indices = []
    for index in joined:
        new_indices.extend(index)

    return ParseResult(new_indices, absolute)


def make_absolute(index):
    """Make an index absolute (preceded by a '.')"""
    if not isinstance(index, string_types):
        index = build(index)
    return b'.' + text_type(index).lstrip(b'.')


if __name__ == b'__main__':
    test = b'foo.1.2."3"."sdsd.sdsd".1:2.1:.2:.file\\.txt.3'
    print(test)
    print(parse(test))
    print(normalize(test))
    print(parse(normalize(test)))
    print(join(b'call', b'param1', ('a', 'b', 'c')))
    print(join([b'callstack', 1], b'foo'))