# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-target-g7omgaxk/lib/python/yaml/scanner.py
# Compiled at: 2019-02-27 21:17:00
# Size of source mod 2**32: 51277 bytes
__all__ = [
 'Scanner', 'ScannerError']
from .error import MarkedYAMLError
from .tokens import *

class ScannerError(MarkedYAMLError):
    pass


class SimpleKey:

    def __init__(self, token_number, required, index, line, column, mark):
        self.token_number = token_number
        self.required = required
        self.index = index
        self.line = line
        self.column = column
        self.mark = mark


class Scanner:

    def __init__(self):
        """Initialize the scanner."""
        self.done = False
        self.flow_level = 0
        self.tokens = []
        self.fetch_stream_start()
        self.tokens_taken = 0
        self.indent = -1
        self.indents = []
        self.allow_simple_key = True
        self.possible_simple_keys = {}

    def check_token(self, *choices):
        while self.need_more_tokens():
            self.fetch_more_tokens()

        if self.tokens:
            if not choices:
                return True
            for choice in choices:
                if isinstance(self.tokens[0], choice):
                    return True

        return False

    def peek_token(self):
        while self.need_more_tokens():
            self.fetch_more_tokens()

        if self.tokens:
            return self.tokens[0]
        return

    def get_token(self):
        while self.need_more_tokens():
            self.fetch_more_tokens()

        if self.tokens:
            self.tokens_taken += 1
            return self.tokens.pop(0)

    def need_more_tokens(self):
        if self.done:
            return False
        else:
            return self.tokens or True
        self.stale_possible_simple_keys()
        if self.next_possible_simple_key() == self.tokens_taken:
            return True

    def fetch_more_tokens(self):
        self.scan_to_next_token()
        self.stale_possible_simple_keys()
        self.unwind_indent(self.column)
        ch = self.peek()
        if ch == '\x00':
            return self.fetch_stream_end()
        if ch == '%':
            if self.check_directive():
                return self.fetch_directive()
        if ch == '-':
            if self.check_document_start():
                return self.fetch_document_start()
        if ch == '.':
            if self.check_document_end():
                return self.fetch_document_end()
        if ch == '[':
            return self.fetch_flow_sequence_start()
        if ch == '{':
            return self.fetch_flow_mapping_start()
        if ch == ']':
            return self.fetch_flow_sequence_end()
        if ch == '}':
            return self.fetch_flow_mapping_end()
        if ch == ',':
            return self.fetch_flow_entry()
        if ch == '-':
            if self.check_block_entry():
                return self.fetch_block_entry()
        if ch == '?':
            if self.check_key():
                return self.fetch_key()
        if ch == ':':
            if self.check_value():
                return self.fetch_value()
        if ch == '*':
            return self.fetch_alias()
        if ch == '&':
            return self.fetch_anchor()
        if ch == '!':
            return self.fetch_tag()
        if ch == '|':
            if not self.flow_level:
                return self.fetch_literal()
        if ch == '>':
            if not self.flow_level:
                return self.fetch_folded()
        if ch == "'":
            return self.fetch_single()
        if ch == '"':
            return self.fetch_double()
        if self.check_plain():
            return self.fetch_plain()
        raise ScannerError('while scanning for the next token', None, 'found character %r that cannot start any token' % ch, self.get_mark())

    def next_possible_simple_key(self):
        min_token_number = None
        for level in self.possible_simple_keys:
            key = self.possible_simple_keys[level]
            if min_token_number is None or key.token_number < min_token_number:
                min_token_number = key.token_number

        return min_token_number

    def stale_possible_simple_keys(self):
        for level in list(self.possible_simple_keys):
            key = self.possible_simple_keys[level]
            if not key.line != self.line:
                if self.index - key.index > 1024:
                    if key.required:
                        raise ScannerError('while scanning a simple key', key.mark, "could not find expected ':'", self.get_mark())
                del self.possible_simple_keys[level]

    def save_possible_simple_key(self):
        required = not self.flow_level and self.indent == self.column
        if self.allow_simple_key:
            self.remove_possible_simple_key()
            token_number = self.tokens_taken + len(self.tokens)
            key = SimpleKey(token_number, required, self.index, self.line, self.column, self.get_mark())
            self.possible_simple_keys[self.flow_level] = key

    def remove_possible_simple_key(self):
        if self.flow_level in self.possible_simple_keys:
            key = self.possible_simple_keys[self.flow_level]
            if key.required:
                raise ScannerError('while scanning a simple key', key.mark, "could not find expected ':'", self.get_mark())
            del self.possible_simple_keys[self.flow_level]

    def unwind_indent(self, column):
        if self.flow_level:
            return
        while self.indent > column:
            mark = self.get_mark()
            self.indent = self.indents.pop()
            self.tokens.append(BlockEndToken(mark, mark))

    def add_indent(self, column):
        if self.indent < column:
            self.indents.append(self.indent)
            self.indent = column
            return True
        return False

    def fetch_stream_start(self):
        mark = self.get_mark()
        self.tokens.append(StreamStartToken(mark, mark, encoding=(self.encoding)))

    def fetch_stream_end(self):
        self.unwind_indent(-1)
        self.remove_possible_simple_key()
        self.allow_simple_key = False
        self.possible_simple_keys = {}
        mark = self.get_mark()
        self.tokens.append(StreamEndToken(mark, mark))
        self.done = True

    def fetch_directive(self):
        self.unwind_indent(-1)
        self.remove_possible_simple_key()
        self.allow_simple_key = False
        self.tokens.append(self.scan_directive())

    def fetch_document_start(self):
        self.fetch_document_indicator(DocumentStartToken)

    def fetch_document_end(self):
        self.fetch_document_indicator(DocumentEndToken)

    def fetch_document_indicator(self, TokenClass):
        self.unwind_indent(-1)
        self.remove_possible_simple_key()
        self.allow_simple_key = False
        start_mark = self.get_mark()
        self.forward(3)
        end_mark = self.get_mark()
        self.tokens.append(TokenClass(start_mark, end_mark))

    def fetch_flow_sequence_start(self):
        self.fetch_flow_collection_start(FlowSequenceStartToken)

    def fetch_flow_mapping_start(self):
        self.fetch_flow_collection_start(FlowMappingStartToken)

    def fetch_flow_collection_start(self, TokenClass):
        self.save_possible_simple_key()
        self.flow_level += 1
        self.allow_simple_key = True
        start_mark = self.get_mark()
        self.forward()
        end_mark = self.get_mark()
        self.tokens.append(TokenClass(start_mark, end_mark))

    def fetch_flow_sequence_end(self):
        self.fetch_flow_collection_end(FlowSequenceEndToken)

    def fetch_flow_mapping_end(self):
        self.fetch_flow_collection_end(FlowMappingEndToken)

    def fetch_flow_collection_end(self, TokenClass):
        self.remove_possible_simple_key()
        self.flow_level -= 1
        self.allow_simple_key = False
        start_mark = self.get_mark()
        self.forward()
        end_mark = self.get_mark()
        self.tokens.append(TokenClass(start_mark, end_mark))

    def fetch_flow_entry(self):
        self.allow_simple_key = True
        self.remove_possible_simple_key()
        start_mark = self.get_mark()
        self.forward()
        end_mark = self.get_mark()
        self.tokens.append(FlowEntryToken(start_mark, end_mark))

    def fetch_block_entry(self):
        if not self.flow_level:
            if not self.allow_simple_key:
                raise ScannerError(None, None, 'sequence entries are not allowed here', self.get_mark())
            if self.add_indent(self.column):
                mark = self.get_mark()
                self.tokens.append(BlockSequenceStartToken(mark, mark))
        self.allow_simple_key = True
        self.remove_possible_simple_key()
        start_mark = self.get_mark()
        self.forward()
        end_mark = self.get_mark()
        self.tokens.append(BlockEntryToken(start_mark, end_mark))

    def fetch_key(self):
        if not self.flow_level:
            if not self.allow_simple_key:
                raise ScannerError(None, None, 'mapping keys are not allowed here', self.get_mark())
            if self.add_indent(self.column):
                mark = self.get_mark()
                self.tokens.append(BlockMappingStartToken(mark, mark))
        self.allow_simple_key = not self.flow_level
        self.remove_possible_simple_key()
        start_mark = self.get_mark()
        self.forward()
        end_mark = self.get_mark()
        self.tokens.append(KeyToken(start_mark, end_mark))

    def fetch_value(self):
        if self.flow_level in self.possible_simple_keys:
            key = self.possible_simple_keys[self.flow_level]
            del self.possible_simple_keys[self.flow_level]
            self.tokens.insert(key.token_number - self.tokens_taken, KeyToken(key.mark, key.mark))
            if not self.flow_level:
                if self.add_indent(key.column):
                    self.tokens.insert(key.token_number - self.tokens_taken, BlockMappingStartToken(key.mark, key.mark))
            self.allow_simple_key = False
        else:
            if not self.flow_level:
                if not self.allow_simple_key:
                    raise ScannerError(None, None, 'mapping values are not allowed here', self.get_mark())
            if not self.flow_level:
                if self.add_indent(self.column):
                    mark = self.get_mark()
                    self.tokens.append(BlockMappingStartToken(mark, mark))
            self.allow_simple_key = not self.flow_level
            self.remove_possible_simple_key()
        start_mark = self.get_mark()
        self.forward()
        end_mark = self.get_mark()
        self.tokens.append(ValueToken(start_mark, end_mark))

    def fetch_alias(self):
        self.save_possible_simple_key()
        self.allow_simple_key = False
        self.tokens.append(self.scan_anchor(AliasToken))

    def fetch_anchor(self):
        self.save_possible_simple_key()
        self.allow_simple_key = False
        self.tokens.append(self.scan_anchor(AnchorToken))

    def fetch_tag(self):
        self.save_possible_simple_key()
        self.allow_simple_key = False
        self.tokens.append(self.scan_tag())

    def fetch_literal(self):
        self.fetch_block_scalar(style='|')

    def fetch_folded(self):
        self.fetch_block_scalar(style='>')

    def fetch_block_scalar(self, style):
        self.allow_simple_key = True
        self.remove_possible_simple_key()
        self.tokens.append(self.scan_block_scalar(style))

    def fetch_single(self):
        self.fetch_flow_scalar(style="'")

    def fetch_double(self):
        self.fetch_flow_scalar(style='"')

    def fetch_flow_scalar(self, style):
        self.save_possible_simple_key()
        self.allow_simple_key = False
        self.tokens.append(self.scan_flow_scalar(style))

    def fetch_plain(self):
        self.save_possible_simple_key()
        self.allow_simple_key = False
        self.tokens.append(self.scan_plain())

    def check_directive(self):
        if self.column == 0:
            return True

    def check_document_start(self):
        if self.column == 0:
            if self.prefix(3) == '---':
                if self.peek(3) in '\x00 \t\r\n\x85\u2028\u2029':
                    return True

    def check_document_end(self):
        if self.column == 0:
            if self.prefix(3) == '...':
                if self.peek(3) in '\x00 \t\r\n\x85\u2028\u2029':
                    return True

    def check_block_entry(self):
        return self.peek(1) in '\x00 \t\r\n\x85\u2028\u2029'

    def check_key(self):
        if self.flow_level:
            return True
        return self.peek(1) in '\x00 \t\r\n\x85\u2028\u2029'

    def check_value(self):
        if self.flow_level:
            return True
        return self.peek(1) in '\x00 \t\r\n\x85\u2028\u2029'

    def check_plain(self):
        ch = self.peek()
        return ch not in '\x00 \t\r\n\x85\u2028\u2029-?:,[]{}#&*!|>\'"%@`' or 

    def scan_to_next_token(self):
        if self.index == 0:
            if self.peek() == '\ufeff':
                self.forward()
        found = False
        while not found:
            while self.peek() == ' ':
                self.forward()

            if self.peek() == '#':
                while self.peek() not in '\x00\r\n\x85\u2028\u2029':
                    self.forward()

            if self.scan_line_break():
                if not self.flow_level:
                    self.allow_simple_key = True
            else:
                found = True

    def scan_directive(self):
        start_mark = self.get_mark()
        self.forward()
        name = self.scan_directive_name(start_mark)
        value = None
        if name == 'YAML':
            value = self.scan_yaml_directive_value(start_mark)
            end_mark = self.get_mark()
        elif name == 'TAG':
            value = self.scan_tag_directive_value(start_mark)
            end_mark = self.get_mark()
        else:
            end_mark = self.get_mark()
            while self.peek() not in '\x00\r\n\x85\u2028\u2029':
                self.forward()

        self.scan_directive_ignored_line(start_mark)
        return DirectiveToken(name, value, start_mark, end_mark)

    def scan_directive_name--- This code section failed: ---

 L. 808         0  LOAD_CONST               0
                2  STORE_FAST               'length'

 L. 809         4  LOAD_FAST                'self'
                6  LOAD_METHOD              peek
                8  LOAD_FAST                'length'
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'ch'

 L. 810        14  SETUP_LOOP          112  'to 112'
               16  LOAD_STR                 '0'
               18  LOAD_FAST                'ch'
               20  DUP_TOP          
               22  ROT_THREE        
               24  COMPARE_OP               <=
               26  POP_JUMP_IF_FALSE    36  'to 36'
               28  LOAD_STR                 '9'
               30  COMPARE_OP               <=
               32  POP_JUMP_IF_TRUE     90  'to 90'
               34  JUMP_FORWARD         38  'to 38'
             36_0  COME_FROM            26  '26'
               36  POP_TOP          
             38_0  COME_FROM            34  '34'
               38  LOAD_STR                 'A'
               40  LOAD_FAST                'ch'
               42  DUP_TOP          
               44  ROT_THREE        
               46  COMPARE_OP               <=
               48  POP_JUMP_IF_FALSE    58  'to 58'
               50  LOAD_STR                 'Z'
               52  COMPARE_OP               <=
               54  POP_JUMP_IF_TRUE     90  'to 90'
               56  JUMP_FORWARD         60  'to 60'
             58_0  COME_FROM            48  '48'
               58  POP_TOP          
             60_0  COME_FROM            56  '56'
               60  LOAD_STR                 'a'
               62  LOAD_FAST                'ch'
               64  DUP_TOP          
               66  ROT_THREE        
               68  COMPARE_OP               <=
               70  POP_JUMP_IF_FALSE    80  'to 80'
               72  LOAD_STR                 'z'
               74  COMPARE_OP               <=
               76  POP_JUMP_IF_TRUE     90  'to 90'
               78  JUMP_FORWARD         82  'to 82'
             80_0  COME_FROM            70  '70'
               80  POP_TOP          
             82_0  COME_FROM            78  '78'

 L. 811        82  LOAD_FAST                'ch'
               84  LOAD_STR                 '-_'
               86  COMPARE_OP               in
               88  POP_JUMP_IF_FALSE   110  'to 110'
             90_0  COME_FROM            76  '76'
             90_1  COME_FROM            54  '54'
             90_2  COME_FROM            32  '32'

 L. 812        90  LOAD_FAST                'length'
               92  LOAD_CONST               1
               94  INPLACE_ADD      
               96  STORE_FAST               'length'

 L. 813        98  LOAD_FAST                'self'
              100  LOAD_METHOD              peek
              102  LOAD_FAST                'length'
              104  CALL_METHOD_1         1  ''
              106  STORE_FAST               'ch'
              108  JUMP_BACK            16  'to 16'
            110_0  COME_FROM            88  '88'
              110  POP_BLOCK        
            112_0  COME_FROM_LOOP       14  '14'

 L. 814       112  LOAD_FAST                'length'
              114  POP_JUMP_IF_TRUE    138  'to 138'

 L. 815       116  LOAD_GLOBAL              ScannerError
              118  LOAD_STR                 'while scanning a directive'
              120  LOAD_FAST                'start_mark'

 L. 816       122  LOAD_STR                 'expected alphabetic or numeric character, but found %r'

 L. 817       124  LOAD_FAST                'ch'
              126  BINARY_MODULO    
              128  LOAD_FAST                'self'
              130  LOAD_METHOD              get_mark
              132  CALL_METHOD_0         0  ''
              134  CALL_FUNCTION_4       4  ''
              136  RAISE_VARARGS_1       1  ''
            138_0  COME_FROM           114  '114'

 L. 818       138  LOAD_FAST                'self'
              140  LOAD_METHOD              prefix
              142  LOAD_FAST                'length'
              144  CALL_METHOD_1         1  ''
              146  STORE_FAST               'value'

 L. 819       148  LOAD_FAST                'self'
              150  LOAD_METHOD              forward
              152  LOAD_FAST                'length'
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          

 L. 820       158  LOAD_FAST                'self'
              160  LOAD_METHOD              peek
              162  CALL_METHOD_0         0  ''
              164  STORE_FAST               'ch'

 L. 821       166  LOAD_FAST                'ch'
              168  LOAD_STR                 '\x00 \r\n\x85\u2028\u2029'
              170  COMPARE_OP               not-in
              172  POP_JUMP_IF_FALSE   196  'to 196'

 L. 822       174  LOAD_GLOBAL              ScannerError
              176  LOAD_STR                 'while scanning a directive'
              178  LOAD_FAST                'start_mark'

 L. 823       180  LOAD_STR                 'expected alphabetic or numeric character, but found %r'

 L. 824       182  LOAD_FAST                'ch'
              184  BINARY_MODULO    
              186  LOAD_FAST                'self'
              188  LOAD_METHOD              get_mark
              190  CALL_METHOD_0         0  ''
              192  CALL_FUNCTION_4       4  ''
              194  RAISE_VARARGS_1       1  ''
            196_0  COME_FROM           172  '172'

 L. 825       196  LOAD_FAST                'value'
              198  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 110

    def scan_yaml_directive_value(self, start_mark):
        while self.peek() == ' ':
            self.forward()

        major = self.scan_yaml_directive_number(start_mark)
        if self.peek() != '.':
            raise ScannerError('while scanning a directive', start_mark, "expected a digit or '.', but found %r" % self.peek(), self.get_mark())
        self.forward()
        minor = self.scan_yaml_directive_number(start_mark)
        if self.peek() not in '\x00 \r\n\x85\u2028\u2029':
            raise ScannerError('while scanning a directive', start_mark, "expected a digit or ' ', but found %r" % self.peek(), self.get_mark())
        return (major, minor)

    def scan_yaml_directive_number(self, start_mark):
        ch = self.peek()
        if not '0' <= ch <= '9':
            raise ScannerError('while scanning a directive', start_mark, 'expected a digit, but found %r' % ch, self.get_mark())
        length = 0
        while '0' <= self.peek(length) <= '9':
            length += 1

        value = int(self.prefix(length))
        self.forward(length)
        return value

    def scan_tag_directive_value(self, start_mark):
        while self.peek() == ' ':
            self.forward()

        handle = self.scan_tag_directive_handle(start_mark)
        while self.peek() == ' ':
            self.forward()

        prefix = self.scan_tag_directive_prefix(start_mark)
        return (
         handle, prefix)

    def scan_tag_directive_handle(self, start_mark):
        value = self.scan_tag_handle('directive', start_mark)
        ch = self.peek()
        if ch != ' ':
            raise ScannerError('while scanning a directive', start_mark, "expected ' ', but found %r" % ch, self.get_mark())
        return value

    def scan_tag_directive_prefix(self, start_mark):
        value = self.scan_tag_uri('directive', start_mark)
        ch = self.peek()
        if ch not in '\x00 \r\n\x85\u2028\u2029':
            raise ScannerError('while scanning a directive', start_mark, "expected ' ', but found %r" % ch, self.get_mark())
        return value

    def scan_directive_ignored_line(self, start_mark):
        while self.peek() == ' ':
            self.forward()

        if self.peek() == '#':
            while self.peek() not in '\x00\r\n\x85\u2028\u2029':
                self.forward()

        ch = self.peek()
        if ch not in '\x00\r\n\x85\u2028\u2029':
            raise ScannerError('while scanning a directive', start_mark, 'expected a comment or a line break, but found %r' % ch, self.get_mark())
        self.scan_line_break()

    def scan_anchor--- This code section failed: ---

 L. 908         0  LOAD_FAST                'self'
                2  LOAD_METHOD              get_mark
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'start_mark'

 L. 909         8  LOAD_FAST                'self'
               10  LOAD_METHOD              peek
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'indicator'

 L. 910        16  LOAD_FAST                'indicator'
               18  LOAD_STR                 '*'
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    30  'to 30'

 L. 911        24  LOAD_STR                 'alias'
               26  STORE_FAST               'name'
               28  JUMP_FORWARD         34  'to 34'
             30_0  COME_FROM            22  '22'

 L. 913        30  LOAD_STR                 'anchor'
               32  STORE_FAST               'name'
             34_0  COME_FROM            28  '28'

 L. 914        34  LOAD_FAST                'self'
               36  LOAD_METHOD              forward
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          

 L. 915        42  LOAD_CONST               0
               44  STORE_FAST               'length'

 L. 916        46  LOAD_FAST                'self'
               48  LOAD_METHOD              peek
               50  LOAD_FAST                'length'
               52  CALL_METHOD_1         1  ''
               54  STORE_FAST               'ch'

 L. 917        56  SETUP_LOOP          154  'to 154'
               58  LOAD_STR                 '0'
               60  LOAD_FAST                'ch'
               62  DUP_TOP          
               64  ROT_THREE        
               66  COMPARE_OP               <=
               68  POP_JUMP_IF_FALSE    78  'to 78'
               70  LOAD_STR                 '9'
               72  COMPARE_OP               <=
               74  POP_JUMP_IF_TRUE    132  'to 132'
               76  JUMP_FORWARD         80  'to 80'
             78_0  COME_FROM            68  '68'
               78  POP_TOP          
             80_0  COME_FROM            76  '76'
               80  LOAD_STR                 'A'
               82  LOAD_FAST                'ch'
               84  DUP_TOP          
               86  ROT_THREE        
               88  COMPARE_OP               <=
               90  POP_JUMP_IF_FALSE   100  'to 100'
               92  LOAD_STR                 'Z'
               94  COMPARE_OP               <=
               96  POP_JUMP_IF_TRUE    132  'to 132'
               98  JUMP_FORWARD        102  'to 102'
            100_0  COME_FROM            90  '90'
              100  POP_TOP          
            102_0  COME_FROM            98  '98'
              102  LOAD_STR                 'a'
              104  LOAD_FAST                'ch'
              106  DUP_TOP          
              108  ROT_THREE        
              110  COMPARE_OP               <=
              112  POP_JUMP_IF_FALSE   122  'to 122'
              114  LOAD_STR                 'z'
              116  COMPARE_OP               <=
              118  POP_JUMP_IF_TRUE    132  'to 132'
              120  JUMP_FORWARD        124  'to 124'
            122_0  COME_FROM           112  '112'
              122  POP_TOP          
            124_0  COME_FROM           120  '120'

 L. 918       124  LOAD_FAST                'ch'
              126  LOAD_STR                 '-_'
              128  COMPARE_OP               in
              130  POP_JUMP_IF_FALSE   152  'to 152'
            132_0  COME_FROM           118  '118'
            132_1  COME_FROM            96  '96'
            132_2  COME_FROM            74  '74'

 L. 919       132  LOAD_FAST                'length'
              134  LOAD_CONST               1
              136  INPLACE_ADD      
              138  STORE_FAST               'length'

 L. 920       140  LOAD_FAST                'self'
              142  LOAD_METHOD              peek
              144  LOAD_FAST                'length'
              146  CALL_METHOD_1         1  ''
              148  STORE_FAST               'ch'
              150  JUMP_BACK            58  'to 58'
            152_0  COME_FROM           130  '130'
              152  POP_BLOCK        
            154_0  COME_FROM_LOOP       56  '56'

 L. 921       154  LOAD_FAST                'length'
              156  POP_JUMP_IF_TRUE    184  'to 184'

 L. 922       158  LOAD_GLOBAL              ScannerError
              160  LOAD_STR                 'while scanning an %s'
              162  LOAD_FAST                'name'
              164  BINARY_MODULO    
              166  LOAD_FAST                'start_mark'

 L. 923       168  LOAD_STR                 'expected alphabetic or numeric character, but found %r'

 L. 924       170  LOAD_FAST                'ch'
              172  BINARY_MODULO    
              174  LOAD_FAST                'self'
              176  LOAD_METHOD              get_mark
              178  CALL_METHOD_0         0  ''
              180  CALL_FUNCTION_4       4  ''
              182  RAISE_VARARGS_1       1  ''
            184_0  COME_FROM           156  '156'

 L. 925       184  LOAD_FAST                'self'
              186  LOAD_METHOD              prefix
              188  LOAD_FAST                'length'
              190  CALL_METHOD_1         1  ''
              192  STORE_FAST               'value'

 L. 926       194  LOAD_FAST                'self'
              196  LOAD_METHOD              forward
              198  LOAD_FAST                'length'
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          

 L. 927       204  LOAD_FAST                'self'
              206  LOAD_METHOD              peek
              208  CALL_METHOD_0         0  ''
              210  STORE_FAST               'ch'

 L. 928       212  LOAD_FAST                'ch'
              214  LOAD_STR                 '\x00 \t\r\n\x85\u2028\u2029?:,]}%@`'
              216  COMPARE_OP               not-in
              218  POP_JUMP_IF_FALSE   246  'to 246'

 L. 929       220  LOAD_GLOBAL              ScannerError
              222  LOAD_STR                 'while scanning an %s'
              224  LOAD_FAST                'name'
              226  BINARY_MODULO    
              228  LOAD_FAST                'start_mark'

 L. 930       230  LOAD_STR                 'expected alphabetic or numeric character, but found %r'

 L. 931       232  LOAD_FAST                'ch'
              234  BINARY_MODULO    
              236  LOAD_FAST                'self'
              238  LOAD_METHOD              get_mark
              240  CALL_METHOD_0         0  ''
              242  CALL_FUNCTION_4       4  ''
              244  RAISE_VARARGS_1       1  ''
            246_0  COME_FROM           218  '218'

 L. 932       246  LOAD_FAST                'self'
              248  LOAD_METHOD              get_mark
              250  CALL_METHOD_0         0  ''
              252  STORE_FAST               'end_mark'

 L. 933       254  LOAD_FAST                'TokenClass'
              256  LOAD_FAST                'value'
              258  LOAD_FAST                'start_mark'
              260  LOAD_FAST                'end_mark'
              262  CALL_FUNCTION_3       3  ''
              264  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 152

    def scan_tag(self):
        start_mark = self.get_mark()
        ch = self.peek(1)
        if ch == '<':
            handle = None
            self.forward(2)
            suffix = self.scan_tag_uri('tag', start_mark)
            if self.peek() != '>':
                raise ScannerError('while parsing a tag', start_mark, "expected '>', but found %r" % self.peek(), self.get_mark())
            self.forward()
        elif ch in '\x00 \t\r\n\x85\u2028\u2029':
            handle = None
            suffix = '!'
            self.forward()
        else:
            length = 1
            use_handle = False
            while ch not in '\x00 \r\n\x85\u2028\u2029':
                if ch == '!':
                    use_handle = True
                    break
                length += 1
                ch = self.peek(length)

            handle = '!'
            if use_handle:
                handle = self.scan_tag_handle('tag', start_mark)
            else:
                handle = '!'
                self.forward()
            suffix = self.scan_tag_uri('tag', start_mark)
        ch = self.peek()
        if ch not in '\x00 \r\n\x85\u2028\u2029':
            raise ScannerError('while scanning a tag', start_mark, "expected ' ', but found %r" % ch, self.get_mark())
        value = (
         handle, suffix)
        end_mark = self.get_mark()
        return TagToken(value, start_mark, end_mark)

    def scan_block_scalar(self, style):
        if style == '>':
            folded = True
        else:
            folded = False
        chunks = []
        start_mark = self.get_mark()
        self.forward()
        chomping, increment = self.scan_block_scalar_indicators(start_mark)
        self.scan_block_scalar_ignored_line(start_mark)
        min_indent = self.indent + 1
        if min_indent < 1:
            min_indent = 1
        elif increment is None:
            breaks, max_indent, end_mark = self.scan_block_scalar_indentation()
            indent = max(min_indent, max_indent)
        else:
            indent = min_indent + increment - 1
            breaks, end_mark = self.scan_block_scalar_breaks(indent)
        line_break = ''
        while self.column == indent:
            if self.peek() != '\x00':
                chunks.extend(breaks)
                leading_non_space = self.peek() not in ' \t'
                length = 0
                while self.peek(length) not in '\x00\r\n\x85\u2028\u2029':
                    length += 1

                chunks.append(self.prefix(length))
                self.forward(length)
                line_break = self.scan_line_break()
                breaks, end_mark = self.scan_block_scalar_breaks(indent)
                if self.column == indent:
                    if self.peek() != '\x00':
                        if folded and line_break == '\n' and leading_non_space and self.peek() not in ' \t':
                            if not breaks:
                                chunks.append(' ')
                    else:
                        chunks.append(line_break)
            else:
                break

        if chomping is not False:
            chunks.append(line_break)
        if chomping is True:
            chunks.extend(breaks)
        return ScalarToken(''.join(chunks), False, start_mark, end_mark, style)

    def scan_block_scalar_indicators(self, start_mark):
        chomping = None
        increment = None
        ch = self.peek()
        if ch in '+-':
            if ch == '+':
                chomping = True
            else:
                chomping = False
            self.forward()
            ch = self.peek()
            if ch in '0123456789':
                increment = int(ch)
                if increment == 0:
                    raise ScannerError('while scanning a block scalar', start_mark, 'expected indentation indicator in the range 1-9, but found 0', self.get_mark())
                self.forward()
        elif ch in '0123456789':
            increment = int(ch)
            if increment == 0:
                raise ScannerError('while scanning a block scalar', start_mark, 'expected indentation indicator in the range 1-9, but found 0', self.get_mark())
            self.forward()
            ch = self.peek()
            if ch in '+-':
                if ch == '+':
                    chomping = True
                else:
                    chomping = False
                self.forward()
        ch = self.peek()
        if ch not in '\x00 \r\n\x85\u2028\u2029':
            raise ScannerError('while scanning a block scalar', start_mark, 'expected chomping or indentation indicators, but found %r' % ch, self.get_mark())
        return (chomping, increment)

    def scan_block_scalar_ignored_line(self, start_mark):
        while self.peek() == ' ':
            self.forward()

        if self.peek() == '#':
            while self.peek() not in '\x00\r\n\x85\u2028\u2029':
                self.forward()

        ch = self.peek()
        if ch not in '\x00\r\n\x85\u2028\u2029':
            raise ScannerError('while scanning a block scalar', start_mark, 'expected a comment or a line break, but found %r' % ch, self.get_mark())
        self.scan_line_break()

    def scan_block_scalar_indentation(self):
        chunks = []
        max_indent = 0
        end_mark = self.get_mark()
        while self.peek() in ' \r\n\x85\u2028\u2029':
            if self.peek() != ' ':
                chunks.append(self.scan_line_break())
                end_mark = self.get_mark()
            else:
                self.forward()
                if self.column > max_indent:
                    max_indent = self.column

        return (
         chunks, max_indent, end_mark)

    def scan_block_scalar_breaks(self, indent):
        chunks = []
        end_mark = self.get_mark()
        while self.column < indent and self.peek() == ' ':
            self.forward()

        while self.peek() in '\r\n\x85\u2028\u2029':
            chunks.append(self.scan_line_break())
            end_mark = self.get_mark()
            while self.column < indent and self.peek() == ' ':
                self.forward()

        return (
         chunks, end_mark)

    def scan_flow_scalar(self, style):
        if style == '"':
            double = True
        else:
            double = False
        chunks = []
        start_mark = self.get_mark()
        quote = self.peek()
        self.forward()
        chunks.extend(self.scan_flow_scalar_non_spaces(double, start_mark))
        while self.peek() != quote:
            chunks.extend(self.scan_flow_scalar_spaces(double, start_mark))
            chunks.extend(self.scan_flow_scalar_non_spaces(double, start_mark))

        self.forward()
        end_mark = self.get_mark()
        return ScalarToken(''.join(chunks), False, start_mark, end_mark, style)

    ESCAPE_REPLACEMENTS = {'0':'\x00', 
     'a':'\x07', 
     'b':'\x08', 
     't':'\t', 
     '\t':'\t', 
     'n':'\n', 
     'v':'\x0b', 
     'f':'\x0c', 
     'r':'\r', 
     'e':'\x1b', 
     ' ':' ', 
     '"':'"', 
     '\\':'\\', 
     '/':'/', 
     'N':'\x85', 
     '_':'\xa0', 
     'L':'\u2028', 
     'P':'\u2029'}
    ESCAPE_CODES = {'x':2, 
     'u':4, 
     'U':8}

    def scan_flow_scalar_non_spaces(self, double, start_mark):
        chunks = []
        while 1:
            length = 0
            while self.peek(length) not in '\'"\\\x00 \t\r\n\x85\u2028\u2029':
                length += 1

            if length:
                chunks.append(self.prefix(length))
                self.forward(length)
            ch = self.peek()
            if not double:
                if ch == "'":
                    if self.peek(1) == "'":
                        chunks.append("'")
                        self.forward(2)
                else:
                    if double and not ch == "'" or :
                        if ch in '"\\':
                            chunks.append(ch)
                            self.forward()
                    if double:
                        if ch == '\\':
                            self.forward()
                            ch = self.peek()
                            if ch in self.ESCAPE_REPLACEMENTS:
                                chunks.append(self.ESCAPE_REPLACEMENTS[ch])
                                self.forward()
                            elif ch in self.ESCAPE_CODES:
                                length = self.ESCAPE_CODES[ch]
                                self.forward()
                                for k in range(length):
                                    if self.peek(k) not in '0123456789ABCDEFabcdef':
                                        raise ScannerError('while scanning a double-quoted scalar', start_mark, 'expected escape sequence of %d hexdecimal numbers, but found %r' % (
                                         length, self.peek(k)), self.get_mark())

                                code = int(self.prefix(length), 16)
                                chunks.append(chr(code))
                                self.forward(length)
                            elif ch in '\r\n\x85\u2028\u2029':
                                self.scan_line_break()
                                chunks.extend(self.scan_flow_scalar_breaks(double, start_mark))
                            else:
                                raise ScannerError('while scanning a double-quoted scalar', start_mark, 'found unknown escape character %r' % ch, self.get_mark())
                return chunks

    def scan_flow_scalar_spaces(self, double, start_mark):
        chunks = []
        length = 0
        while self.peek(length) in ' \t':
            length += 1

        whitespaces = self.prefix(length)
        self.forward(length)
        ch = self.peek()
        if ch == '\x00':
            raise ScannerError('while scanning a quoted scalar', start_mark, 'found unexpected end of stream', self.get_mark())
        elif ch in '\r\n\x85\u2028\u2029':
            line_break = self.scan_line_break()
            breaks = self.scan_flow_scalar_breaks(double, start_mark)
            if line_break != '\n':
                chunks.append(line_break)
            elif not breaks:
                chunks.append(' ')
            chunks.extend(breaks)
        else:
            chunks.append(whitespaces)
        return chunks

    def scan_flow_scalar_breaks(self, double, start_mark):
        chunks = []
        while 1:
            prefix = self.prefix(3)
            if not prefix == '---':
                if prefix == '...':
                    if self.peek(3) in '\x00 \t\r\n\x85\u2028\u2029':
                        raise ScannerError('while scanning a quoted scalar', start_mark, 'found unexpected document separator', self.get_mark())
                while self.peek() in ' \t':
                    self.forward()

                if self.peek() in '\r\n\x85\u2028\u2029':
                    chunks.append(self.scan_line_break())
                else:
                    return chunks

    def scan_plain(self):
        chunks = []
        start_mark = self.get_mark()
        end_mark = start_mark
        indent = self.indent + 1
        spaces = []
        while 1:
            length = 0
            if self.peek() == '#':
                break
            while 1:
                ch = self.peek(length)
                if not ch in '\x00 \t\r\n\x85\u2028\u2029':
                    if not (ch == ':' and self.peek(length + 1) in '\x00 \t\r\n\x85\u2028\u2029' + (',[]{}' if self.flow_level else '')):
                        if not self.flow_level or ch in ',?[]{}':
                            break
                    length += 1

            if length == 0:
                break
            self.allow_simple_key = False
            chunks.extend(spaces)
            chunks.append(self.prefix(length))
            self.forward(length)
            end_mark = self.get_mark()
            spaces = self.scan_plain_spaces(indent, start_mark)
            if not spaces or self.peek() == '#' or self.flow_level or self.column < indent:
                break

        return ScalarToken(''.join(chunks), True, start_mark, end_mark)

    def scan_plain_spaces(self, indent, start_mark):
        chunks = []
        length = 0
        while self.peek(length) in ' ':
            length += 1

        whitespaces = self.prefix(length)
        self.forward(length)
        ch = self.peek()
        if ch in '\r\n\x85\u2028\u2029':
            line_break = self.scan_line_break()
            self.allow_simple_key = True
            prefix = self.prefix(3)
            if prefix == '---' or prefix == '...':
                if self.peek(3) in '\x00 \t\r\n\x85\u2028\u2029':
                    return
            breaks = []
            while self.peek() in ' \r\n\x85\u2028\u2029':
                if self.peek() == ' ':
                    self.forward()
                else:
                    breaks.append(self.scan_line_break())
                    prefix = self.prefix(3)
                    if prefix == '---' or prefix == '...':
                        if self.peek(3) in '\x00 \t\r\n\x85\u2028\u2029':
                            return

            if line_break != '\n':
                chunks.append(line_break)
            elif not breaks:
                chunks.append(' ')
            chunks.extend(breaks)
        elif whitespaces:
            chunks.append(whitespaces)
        return chunks

    def scan_tag_handle--- This code section failed: ---

 L.1352         0  LOAD_FAST                'self'
                2  LOAD_METHOD              peek
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'ch'

 L.1353         8  LOAD_FAST                'ch'
               10  LOAD_STR                 '!'
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    42  'to 42'

 L.1354        16  LOAD_GLOBAL              ScannerError
               18  LOAD_STR                 'while scanning a %s'
               20  LOAD_FAST                'name'
               22  BINARY_MODULO    
               24  LOAD_FAST                'start_mark'

 L.1355        26  LOAD_STR                 "expected '!', but found %r"
               28  LOAD_FAST                'ch'
               30  BINARY_MODULO    
               32  LOAD_FAST                'self'
               34  LOAD_METHOD              get_mark
               36  CALL_METHOD_0         0  ''
               38  CALL_FUNCTION_4       4  ''
               40  RAISE_VARARGS_1       1  ''
             42_0  COME_FROM            14  '14'

 L.1356        42  LOAD_CONST               1
               44  STORE_FAST               'length'

 L.1357        46  LOAD_FAST                'self'
               48  LOAD_METHOD              peek
               50  LOAD_FAST                'length'
               52  CALL_METHOD_1         1  ''
               54  STORE_FAST               'ch'

 L.1358        56  LOAD_FAST                'ch'
               58  LOAD_STR                 ' '
               60  COMPARE_OP               !=
               62  POP_JUMP_IF_FALSE   214  'to 214'

 L.1359        64  SETUP_LOOP          162  'to 162'
               66  LOAD_STR                 '0'
               68  LOAD_FAST                'ch'
               70  DUP_TOP          
               72  ROT_THREE        
               74  COMPARE_OP               <=
               76  POP_JUMP_IF_FALSE    86  'to 86'
               78  LOAD_STR                 '9'
               80  COMPARE_OP               <=
               82  POP_JUMP_IF_TRUE    140  'to 140'
               84  JUMP_FORWARD         88  'to 88'
             86_0  COME_FROM            76  '76'
               86  POP_TOP          
             88_0  COME_FROM            84  '84'
               88  LOAD_STR                 'A'
               90  LOAD_FAST                'ch'
               92  DUP_TOP          
               94  ROT_THREE        
               96  COMPARE_OP               <=
               98  POP_JUMP_IF_FALSE   108  'to 108'
              100  LOAD_STR                 'Z'
              102  COMPARE_OP               <=
              104  POP_JUMP_IF_TRUE    140  'to 140'
              106  JUMP_FORWARD        110  'to 110'
            108_0  COME_FROM            98  '98'
              108  POP_TOP          
            110_0  COME_FROM           106  '106'
              110  LOAD_STR                 'a'
              112  LOAD_FAST                'ch'
              114  DUP_TOP          
              116  ROT_THREE        
              118  COMPARE_OP               <=
              120  POP_JUMP_IF_FALSE   130  'to 130'
              122  LOAD_STR                 'z'
              124  COMPARE_OP               <=
              126  POP_JUMP_IF_TRUE    140  'to 140'
              128  JUMP_FORWARD        132  'to 132'
            130_0  COME_FROM           120  '120'
              130  POP_TOP          
            132_0  COME_FROM           128  '128'

 L.1360       132  LOAD_FAST                'ch'
              134  LOAD_STR                 '-_'
              136  COMPARE_OP               in
              138  POP_JUMP_IF_FALSE   160  'to 160'
            140_0  COME_FROM           126  '126'
            140_1  COME_FROM           104  '104'
            140_2  COME_FROM            82  '82'

 L.1361       140  LOAD_FAST                'length'
              142  LOAD_CONST               1
              144  INPLACE_ADD      
              146  STORE_FAST               'length'

 L.1362       148  LOAD_FAST                'self'
              150  LOAD_METHOD              peek
              152  LOAD_FAST                'length'
              154  CALL_METHOD_1         1  ''
              156  STORE_FAST               'ch'
              158  JUMP_BACK            66  'to 66'
            160_0  COME_FROM           138  '138'
              160  POP_BLOCK        
            162_0  COME_FROM_LOOP       64  '64'

 L.1363       162  LOAD_FAST                'ch'
              164  LOAD_STR                 '!'
              166  COMPARE_OP               !=
              168  POP_JUMP_IF_FALSE   206  'to 206'

 L.1364       170  LOAD_FAST                'self'
              172  LOAD_METHOD              forward
              174  LOAD_FAST                'length'
              176  CALL_METHOD_1         1  ''
              178  POP_TOP          

 L.1365       180  LOAD_GLOBAL              ScannerError
              182  LOAD_STR                 'while scanning a %s'
              184  LOAD_FAST                'name'
              186  BINARY_MODULO    
              188  LOAD_FAST                'start_mark'

 L.1366       190  LOAD_STR                 "expected '!', but found %r"
              192  LOAD_FAST                'ch'
              194  BINARY_MODULO    
              196  LOAD_FAST                'self'
              198  LOAD_METHOD              get_mark
              200  CALL_METHOD_0         0  ''
              202  CALL_FUNCTION_4       4  ''
              204  RAISE_VARARGS_1       1  ''
            206_0  COME_FROM           168  '168'

 L.1367       206  LOAD_FAST                'length'
              208  LOAD_CONST               1
              210  INPLACE_ADD      
              212  STORE_FAST               'length'
            214_0  COME_FROM            62  '62'

 L.1368       214  LOAD_FAST                'self'
              216  LOAD_METHOD              prefix
              218  LOAD_FAST                'length'
              220  CALL_METHOD_1         1  ''
              222  STORE_FAST               'value'

 L.1369       224  LOAD_FAST                'self'
              226  LOAD_METHOD              forward
              228  LOAD_FAST                'length'
              230  CALL_METHOD_1         1  ''
              232  POP_TOP          

 L.1370       234  LOAD_FAST                'value'
              236  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 160

    def scan_tag_uri--- This code section failed: ---

 L.1375         0  BUILD_LIST_0          0 
                2  STORE_FAST               'chunks'

 L.1376         4  LOAD_CONST               0
                6  STORE_FAST               'length'

 L.1377         8  LOAD_FAST                'self'
               10  LOAD_METHOD              peek
               12  LOAD_FAST                'length'
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'ch'

 L.1378        18  SETUP_LOOP          174  'to 174'
               20  LOAD_STR                 '0'
               22  LOAD_FAST                'ch'
               24  DUP_TOP          
               26  ROT_THREE        
               28  COMPARE_OP               <=
               30  POP_JUMP_IF_FALSE    40  'to 40'
               32  LOAD_STR                 '9'
               34  COMPARE_OP               <=
               36  POP_JUMP_IF_TRUE     94  'to 94'
               38  JUMP_FORWARD         42  'to 42'
             40_0  COME_FROM            30  '30'
               40  POP_TOP          
             42_0  COME_FROM            38  '38'
               42  LOAD_STR                 'A'
               44  LOAD_FAST                'ch'
               46  DUP_TOP          
               48  ROT_THREE        
               50  COMPARE_OP               <=
               52  POP_JUMP_IF_FALSE    62  'to 62'
               54  LOAD_STR                 'Z'
               56  COMPARE_OP               <=
               58  POP_JUMP_IF_TRUE     94  'to 94'
               60  JUMP_FORWARD         64  'to 64'
             62_0  COME_FROM            52  '52'
               62  POP_TOP          
             64_0  COME_FROM            60  '60'
               64  LOAD_STR                 'a'
               66  LOAD_FAST                'ch'
               68  DUP_TOP          
               70  ROT_THREE        
               72  COMPARE_OP               <=
               74  POP_JUMP_IF_FALSE    84  'to 84'
               76  LOAD_STR                 'z'
               78  COMPARE_OP               <=
               80  POP_JUMP_IF_TRUE     94  'to 94'
               82  JUMP_FORWARD         86  'to 86'
             84_0  COME_FROM            74  '74'
               84  POP_TOP          
             86_0  COME_FROM            82  '82'

 L.1379        86  LOAD_FAST                'ch'
               88  LOAD_STR                 "-;/?:@&=+$,_.!~*'()[]%"
               90  COMPARE_OP               in
               92  POP_JUMP_IF_FALSE   172  'to 172'
             94_0  COME_FROM            80  '80'
             94_1  COME_FROM            58  '58'
             94_2  COME_FROM            36  '36'

 L.1380        94  LOAD_FAST                'ch'
               96  LOAD_STR                 '%'
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   152  'to 152'

 L.1381       102  LOAD_FAST                'chunks'
              104  LOAD_METHOD              append
              106  LOAD_FAST                'self'
              108  LOAD_METHOD              prefix
              110  LOAD_FAST                'length'
              112  CALL_METHOD_1         1  ''
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L.1382       118  LOAD_FAST                'self'
              120  LOAD_METHOD              forward
              122  LOAD_FAST                'length'
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          

 L.1383       128  LOAD_CONST               0
              130  STORE_FAST               'length'

 L.1384       132  LOAD_FAST                'chunks'
              134  LOAD_METHOD              append
              136  LOAD_FAST                'self'
              138  LOAD_METHOD              scan_uri_escapes
              140  LOAD_FAST                'name'
              142  LOAD_FAST                'start_mark'
              144  CALL_METHOD_2         2  ''
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          
              150  JUMP_FORWARD        160  'to 160'
            152_0  COME_FROM           100  '100'

 L.1386       152  LOAD_FAST                'length'
              154  LOAD_CONST               1
              156  INPLACE_ADD      
              158  STORE_FAST               'length'
            160_0  COME_FROM           150  '150'

 L.1387       160  LOAD_FAST                'self'
              162  LOAD_METHOD              peek
              164  LOAD_FAST                'length'
              166  CALL_METHOD_1         1  ''
              168  STORE_FAST               'ch'
              170  JUMP_BACK            20  'to 20'
            172_0  COME_FROM            92  '92'
              172  POP_BLOCK        
            174_0  COME_FROM_LOOP       18  '18'

 L.1388       174  LOAD_FAST                'length'
              176  POP_JUMP_IF_FALSE   208  'to 208'

 L.1389       178  LOAD_FAST                'chunks'
              180  LOAD_METHOD              append
              182  LOAD_FAST                'self'
              184  LOAD_METHOD              prefix
              186  LOAD_FAST                'length'
              188  CALL_METHOD_1         1  ''
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          

 L.1390       194  LOAD_FAST                'self'
              196  LOAD_METHOD              forward
              198  LOAD_FAST                'length'
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          

 L.1391       204  LOAD_CONST               0
              206  STORE_FAST               'length'
            208_0  COME_FROM           176  '176'

 L.1392       208  LOAD_FAST                'chunks'
              210  POP_JUMP_IF_TRUE    238  'to 238'

 L.1393       212  LOAD_GLOBAL              ScannerError
              214  LOAD_STR                 'while parsing a %s'
              216  LOAD_FAST                'name'
              218  BINARY_MODULO    
              220  LOAD_FAST                'start_mark'

 L.1394       222  LOAD_STR                 'expected URI, but found %r'
              224  LOAD_FAST                'ch'
              226  BINARY_MODULO    
              228  LOAD_FAST                'self'
              230  LOAD_METHOD              get_mark
              232  CALL_METHOD_0         0  ''
              234  CALL_FUNCTION_4       4  ''
              236  RAISE_VARARGS_1       1  ''
            238_0  COME_FROM           210  '210'

 L.1395       238  LOAD_STR                 ''
              240  LOAD_METHOD              join
              242  LOAD_FAST                'chunks'
              244  CALL_METHOD_1         1  ''
              246  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 172

    def scan_uri_escapes(self, name, start_mark):
        codes = []
        mark = self.get_mark()
        while self.peek() == '%':
            self.forward()
            for k in range(2):
                if self.peek(k) not in '0123456789ABCDEFabcdef':
                    raise ScannerError('while scanning a %s' % name, start_mark, 'expected URI escape sequence of 2 hexdecimal numbers, but found %r' % self.peek(k), self.get_mark())

            codes.append(int(self.prefix(2), 16))
            self.forward(2)

        try:
            value = bytes(codes).decode('utf-8')
        except UnicodeDecodeError as exc:
            try:
                raise ScannerError('while scanning a %s' % name, start_mark, str(exc), mark)
            finally:
                exc = None
                del exc

        return value

    def scan_line_break(self):
        ch = self.peek()
        if ch in '\r\n\x85':
            if self.prefix(2) == '\r\n':
                self.forward(2)
            else:
                self.forward()
            return '\n'
        if ch in '\u2028\u2029':
            self.forward()
            return ch
        return ''