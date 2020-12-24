# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\komparse\scanner.py
# Compiled at: 2020-03-13 17:41:12
# Size of source mod 2**32: 9647 bytes
from collections import namedtuple
from .char_stream import CharStream
Token = namedtuple('Token', 'types value')

class Scanner(object):

    def __init__(self, char_stream, grammar):
        self._char_stream = char_stream
        self._grammar = grammar
        self._remaining = []
        self._consumption = [[]]
        self._reader = StdReader(char_stream, self._grammar, self)

    def has_next(self):
        self._fill_buffer()
        return bool(self._remaining)

    def peek(self):
        self._fill_buffer()
        return self._remaining[(-1)]

    def advance(self):
        self._fill_buffer()
        if self._remaining:
            ret = self._remaining.pop()
            self._consumption[(-1)].append(ret)
            return ret
        return

    def open_transaction(self):
        self._consumption.append([])

    def commit(self):
        if len(self._consumption) == 1:
            raise Exception('Commit not allowed')
        self._consumption[(-1)] += self._consumption.pop()

    def undo(self):
        if len(self._consumption) == 1:
            raise Exception('Cannot be undone')
        else:
            consumed = self._consumption.pop()
            while True:
                if consumed:
                    self._remaining.append(consumed.pop())

    def _fill_buffer(self):
        if not self._remaining:
            tokens = []
            while True:
                new_tokens = self._reader.next_tokens()
                if new_tokens is None:
                    break
                tokens += new_tokens
                if tokens:
                    break

            if tokens is not None:
                tokens.reverse()
                for token in tokens:
                    self._remaining.append(token)


class TokenReader(object):

    def __init__(self, char_stream, grammar, scanner):
        self._char_stream = char_stream
        self._grammar = grammar
        self._scanner = scanner
        self._chars = ''

    def next_tokens(self):
        raise NotImplementedError()

    def _init_chars(self, chars):
        self._chars = chars

    def _peek_next_char(self):
        if self._char_stream.has_next():
            return self._char_stream.peek()
        return

    def _advance_char(self):
        self._chars += self._char_stream.advance()

    def _remove_tail(self, tail):
        self._chars = self._chars[:len(self._chars) - len(tail)]

    def _ends_with(self, tail):
        return self._chars[-len(tail):] == tail


class StdReader(TokenReader):

    def __init__(self, char_stream, grammar, scanner):
        TokenReader.__init__(self, char_stream, grammar, scanner)
        self._wspace = self._grammar.get_whitespace_chars()

    def next_tokens(self):
        while True:
            ch = self._peek_next_char()
            if ch is None:
                if self._chars:
                    tokens = self._create_tokens()
                    self._chars = ''
                    return tokens
                return
            if ch in self._wspace:
                tokens = self._create_tokens()
                self._scanner._reader = WSpaceReader(self._char_stream, self._grammar, self._scanner)
                return tokens
            self._advance_char()
            starts_comment, start, end, nestable = self._is_comment_start()
            if starts_comment:
                self._remove_tail(start)
                tokens = self._create_tokens()
                reader = CommentReader(self._char_stream, self._grammar, self._scanner)
                reader.set_delimiters(start, end, nestable)
                reader._init_chars(start)
                self._scanner._reader = reader
                return tokens
            starts_string, name, start, end, esc = self._is_string_start()
            if starts_string:
                self._remove_tail(start)
                tokens = self._create_tokens()
                reader = StringReader(self._char_stream, self._grammar, self._scanner)
                reader.set_name(name)
                reader.set_delimiters(start, end, esc)
                self._scanner._reader = reader
                return tokens

    def _create_tokens--- This code section failed: ---

 L. 134         0  BUILD_LIST_0          0 
                2  STORE_FAST               'tokens'

 L. 135         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _chars
                8  STORE_FAST               'remaining'

 L. 136        10  LOAD_FAST                'remaining'
               12  POP_JUMP_IF_FALSE    78  'to 78'

 L. 137        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _find_next_token
               18  LOAD_FAST                'remaining'
               20  CALL_METHOD_1         1  ''
               22  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST               'token_types'
               26  STORE_FAST               'text'

 L. 138        28  LOAD_FAST                'text'
               30  LOAD_CONST               None
               32  COMPARE_OP               is-not
               34  POP_JUMP_IF_FALSE    78  'to 78'

 L. 139        36  LOAD_FAST                'token_types'
               38  POP_JUMP_IF_FALSE    56  'to 56'

 L. 140        40  LOAD_FAST                'tokens'
               42  LOAD_METHOD              append
               44  LOAD_GLOBAL              Token
               46  LOAD_FAST                'token_types'
               48  LOAD_FAST                'text'
               50  CALL_FUNCTION_2       2  ''
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L. 141        56  LOAD_FAST                'remaining'
               58  LOAD_GLOBAL              len
               60  LOAD_FAST                'text'
               62  CALL_FUNCTION_1       1  ''
               64  LOAD_CONST               None
               66  BUILD_SLICE_2         2 
               68  BINARY_SUBSCR    
               70  STORE_FAST               'remaining'
               72  JUMP_BACK            10  'to 10'

 L. 143        74  BREAK_LOOP           78  'to 78'
               76  JUMP_BACK            10  'to 10'
             78_0  COME_FROM            34  '34'
             78_1  COME_FROM            12  '12'

 L. 144        78  LOAD_FAST                'remaining'
               80  POP_JUMP_IF_FALSE    96  'to 96'

 L. 145        82  LOAD_GLOBAL              Exception
               84  LOAD_STR                 'Code could not be resolved: {}'
               86  LOAD_METHOD              format
               88  LOAD_FAST                'remaining'
               90  CALL_METHOD_1         1  ''
               92  CALL_FUNCTION_1       1  ''
               94  RAISE_VARARGS_1       1  'exception instance'
             96_0  COME_FROM            80  '80'

 L. 146        96  LOAD_FAST                'tokens'
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 98

    def _find_next_token(self, s):
        matches = []
        for name, regex in self._grammar.get_token_patterns():
            m = regex.match(s)
            if m:
                text = m.group(1)
                matches.append((name, text))
            return self._max_munch(sorted(matches, key=(lambda it: len(it[1])), reverse=True))

    def _max_munch(self, sorted_matches):
        token_types = []
        max_len = None
        max_text = None
        for name, text in sorted_matches:
            if max_len is None:
                max_len = len(text)
                max_text = text
            if len(text) == max_len:
                if not self._grammar.multiple_types_per_token_enabled():
                    token_types or token_types.append(name)
                else:
                    break
            else:
                return (
                 token_types, max_text)

    def _is_comment_start(self):
        comment_delims = self._grammar.get_comments()
        for start, end, nestable in comment_delims:
            if self._ends_with(start):
                return (
                 True, start, end, nestable)
            return (False, None, None, False)

    def _is_string_start(self):
        string_delims = self._grammar.get_strings()
        for name, start, end, esc in string_delims:
            if self._ends_with(start):
                return (
                 True, name, start, end, esc)
            return (False, None, None, None, None)


class WSpaceReader(TokenReader):

    def __init__(self, char_stream, grammar, scanner):
        TokenReader.__init__(self, char_stream, grammar, scanner)
        self._wspace = self._grammar.get_whitespace_chars()

    def next_tokens(self):
        while True:
            ch = self._peek_next_char()
            if ch is None or ch not in self._wspace:
                self._scanner._reader = StdReader(self._char_stream, self._grammar, self._scanner)
                return []
            self._advance_char()


class CommentReader(TokenReader):

    def __init__(self, char_stream, grammar, scanner):
        TokenReader.__init__(self, char_stream, grammar, scanner)
        self._start = ''
        self._end = ''
        self._nestable = False

    def set_delimiters(self, start, end, nestable):
        self._start = start
        self._end = end
        self._nestable = nestable

    def next_tokens(self):
        nest_level = 1
        while self._peek_next_char() is None:
            self._scanner._reader = StdReader(self._char_stream, self._grammar, self._scanner)
            return []
            self._advance_char()
            if self._ends_with(self._end):
                nest_level -= 1
                if nest_level == 0:
                    self._scanner._reader = StdReader(self._char_stream, self._grammar, self._scanner)
                    return []
            elif self._nestable:
                if self._ends_with(self._start):
                    nest_level += 1


class StringReader(TokenReader):

    def __init__(self, char_stream, grammar, scanner):
        TokenReader.__init__(self, char_stream, grammar, scanner)
        self._start = ''
        self._end = ''
        self._esc = ''
        self._name = 'STRING'
        self._immut_len = 0

    def _ends_with(self, tail):
        mut_tail = self._chars[self._immut_len:]
        return mut_tail[-len(tail):] == tail

    def set_delimiters(self, start, end, esc):
        self._start = start
        self._end = end
        self._esc = esc

    def set_name(self, name):
        self._name = name

    def next_tokens(self):
        escaped_end = self._esc + self._end
        escaped_esc = 2 * self._esc
        while True:
            if self._peek_next_char() is None:
                return
            self._advance_char()
            if self._esc and self._escape(self._end) or self._escape(self._esc):
                pass
            elif self._ends_with(self._end):
                self._remove_tail(self._end)
                self._scanner._reader = StdReader(self._char_stream, self._grammar, self._scanner)
                return [Token(types=[self._name], value=(self._chars))]

    def _escape(self, ch):
        escaped = self._esc + ch
        if not self._ends_with(escaped):
            return False
        self._remove_tail(escaped)
        self._chars += ch
        self._immut_len = len(self._chars)
        return True