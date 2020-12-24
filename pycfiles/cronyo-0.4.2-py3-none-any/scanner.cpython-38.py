# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./vendor/yaml/scanner.py
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
        else:
            while True:
                if self.indent > column:
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
        return ch not in '\x00 \t\r\n\x85\u2028\u2029-?:,[]{}#&*!|>\'"%@`' or self.peek(1) not in '\x00 \t\r\n\x85\u2028\u2029' and (ch == '-' or not self.flow_level and ch in '?:')

    def scan_to_next_token--- This code section failed: ---

 L. 772         0  LOAD_FAST                'self'
                2  LOAD_ATTR                index
                4  LOAD_CONST               0
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    30  'to 30'
               10  LOAD_FAST                'self'
               12  LOAD_METHOD              peek
               14  CALL_METHOD_0         0  ''
               16  LOAD_STR                 '\ufeff'
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 773        22  LOAD_FAST                'self'
               24  LOAD_METHOD              forward
               26  CALL_METHOD_0         0  ''
               28  POP_TOP          
             30_0  COME_FROM            20  '20'
             30_1  COME_FROM             8  '8'

 L. 774        30  LOAD_CONST               False
               32  STORE_FAST               'found'

 L. 775        34  LOAD_FAST                'found'
               36  POP_JUMP_IF_TRUE    122  'to 122'

 L. 776        38  LOAD_FAST                'self'
               40  LOAD_METHOD              peek
               42  CALL_METHOD_0         0  ''
               44  LOAD_STR                 ' '
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    60  'to 60'

 L. 777        50  LOAD_FAST                'self'
               52  LOAD_METHOD              forward
               54  CALL_METHOD_0         0  ''
               56  POP_TOP          
               58  JUMP_BACK            38  'to 38'
             60_0  COME_FROM            48  '48'

 L. 778        60  LOAD_FAST                'self'
               62  LOAD_METHOD              peek
               64  CALL_METHOD_0         0  ''
               66  LOAD_STR                 '#'
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE    94  'to 94'

 L. 779        72  LOAD_FAST                'self'
               74  LOAD_METHOD              peek
               76  CALL_METHOD_0         0  ''
               78  LOAD_STR                 '\x00\r\n\x85\u2028\u2029'
               80  COMPARE_OP               not-in
               82  POP_JUMP_IF_FALSE    94  'to 94'

 L. 780        84  LOAD_FAST                'self'
               86  LOAD_METHOD              forward
               88  CALL_METHOD_0         0  ''
               90  POP_TOP          
               92  JUMP_BACK            72  'to 72'
             94_0  COME_FROM            82  '82'
             94_1  COME_FROM            70  '70'

 L. 781        94  LOAD_FAST                'self'
               96  LOAD_METHOD              scan_line_break
               98  CALL_METHOD_0         0  ''
              100  POP_JUMP_IF_FALSE   116  'to 116'

 L. 782       102  LOAD_FAST                'self'
              104  LOAD_ATTR                flow_level
              106  POP_JUMP_IF_TRUE    120  'to 120'

 L. 783       108  LOAD_CONST               True
              110  LOAD_FAST                'self'
              112  STORE_ATTR               allow_simple_key
              114  JUMP_BACK            34  'to 34'
            116_0  COME_FROM           100  '100'

 L. 785       116  LOAD_CONST               True
              118  STORE_FAST               'found'
            120_0  COME_FROM           106  '106'
              120  JUMP_BACK            34  'to 34'
            122_0  COME_FROM            36  '36'

Parse error at or near `JUMP_BACK' instruction at offset 120

    def scan_directive(self):
        start_mark = self.get_mark()
        self.forward()
        name = self.scan_directive_name(start_mark)
        value = None
        if name == 'YAML':
            value = self.scan_yaml_directive_value(start_mark)
            end_mark = self.get_mark()
        else:
            if name == 'TAG':
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

 L. 810        14  LOAD_STR                 '0'
               16  LOAD_FAST                'ch'
               18  DUP_TOP          
               20  ROT_THREE        
               22  COMPARE_OP               <=
               24  POP_JUMP_IF_FALSE    34  'to 34'
               26  LOAD_STR                 '9'
               28  COMPARE_OP               <=
               30  POP_JUMP_IF_TRUE     88  'to 88'
               32  JUMP_FORWARD         36  'to 36'
             34_0  COME_FROM            24  '24'
               34  POP_TOP          
             36_0  COME_FROM            32  '32'
               36  LOAD_STR                 'A'
               38  LOAD_FAST                'ch'
               40  DUP_TOP          
               42  ROT_THREE        
               44  COMPARE_OP               <=
               46  POP_JUMP_IF_FALSE    56  'to 56'
               48  LOAD_STR                 'Z'
               50  COMPARE_OP               <=
               52  POP_JUMP_IF_TRUE     88  'to 88'
               54  JUMP_FORWARD         58  'to 58'
             56_0  COME_FROM            46  '46'
               56  POP_TOP          
             58_0  COME_FROM            54  '54'
               58  LOAD_STR                 'a'
               60  LOAD_FAST                'ch'
               62  DUP_TOP          
               64  ROT_THREE        
               66  COMPARE_OP               <=
               68  POP_JUMP_IF_FALSE    78  'to 78'
               70  LOAD_STR                 'z'
               72  COMPARE_OP               <=
               74  POP_JUMP_IF_TRUE     88  'to 88'
               76  JUMP_FORWARD         80  'to 80'
             78_0  COME_FROM            68  '68'
               78  POP_TOP          
             80_0  COME_FROM            76  '76'

 L. 811        80  LOAD_FAST                'ch'
               82  LOAD_STR                 '-_'
               84  COMPARE_OP               in

 L. 810        86  POP_JUMP_IF_FALSE   108  'to 108'
             88_0  COME_FROM            74  '74'
             88_1  COME_FROM            52  '52'
             88_2  COME_FROM            30  '30'

 L. 812        88  LOAD_FAST                'length'
               90  LOAD_CONST               1
               92  INPLACE_ADD      
               94  STORE_FAST               'length'

 L. 813        96  LOAD_FAST                'self'
               98  LOAD_METHOD              peek
              100  LOAD_FAST                'length'
              102  CALL_METHOD_1         1  ''
              104  STORE_FAST               'ch'
              106  JUMP_BACK            14  'to 14'
            108_0  COME_FROM            86  '86'

 L. 814       108  LOAD_FAST                'length'
              110  POP_JUMP_IF_TRUE    134  'to 134'

 L. 815       112  LOAD_GLOBAL              ScannerError
              114  LOAD_STR                 'while scanning a directive'
              116  LOAD_FAST                'start_mark'

 L. 816       118  LOAD_STR                 'expected alphabetic or numeric character, but found %r'

 L. 817       120  LOAD_FAST                'ch'

 L. 816       122  BINARY_MODULO    

 L. 817       124  LOAD_FAST                'self'
              126  LOAD_METHOD              get_mark
              128  CALL_METHOD_0         0  ''

 L. 815       130  CALL_FUNCTION_4       4  ''
              132  RAISE_VARARGS_1       1  'exception instance'
            134_0  COME_FROM           110  '110'

 L. 818       134  LOAD_FAST                'self'
              136  LOAD_METHOD              prefix
              138  LOAD_FAST                'length'
              140  CALL_METHOD_1         1  ''
              142  STORE_FAST               'value'

 L. 819       144  LOAD_FAST                'self'
              146  LOAD_METHOD              forward
              148  LOAD_FAST                'length'
              150  CALL_METHOD_1         1  ''
              152  POP_TOP          

 L. 820       154  LOAD_FAST                'self'
              156  LOAD_METHOD              peek
              158  CALL_METHOD_0         0  ''
              160  STORE_FAST               'ch'

 L. 821       162  LOAD_FAST                'ch'
              164  LOAD_STR                 '\x00 \r\n\x85\u2028\u2029'
              166  COMPARE_OP               not-in
              168  POP_JUMP_IF_FALSE   192  'to 192'

 L. 822       170  LOAD_GLOBAL              ScannerError
              172  LOAD_STR                 'while scanning a directive'
              174  LOAD_FAST                'start_mark'

 L. 823       176  LOAD_STR                 'expected alphabetic or numeric character, but found %r'

 L. 824       178  LOAD_FAST                'ch'

 L. 823       180  BINARY_MODULO    

 L. 824       182  LOAD_FAST                'self'
              184  LOAD_METHOD              get_mark
              186  CALL_METHOD_0         0  ''

 L. 822       188  CALL_FUNCTION_4       4  ''
              190  RAISE_VARARGS_1       1  'exception instance'
            192_0  COME_FROM           168  '168'

 L. 825       192  LOAD_FAST                'value'
              194  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 194

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
        return (
         major, minor)

    def scan_yaml_directive_number(self, start_mark):
        ch = self.peek()
        if not '0' <= ch <= '9':
            raise ScannerError('while scanning a directive', start_mark, 'expected a digit, but found %r' % ch, self.get_mark())
        else:
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
        return (handle, prefix)

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

 L. 917        56  LOAD_STR                 '0'
               58  LOAD_FAST                'ch'
               60  DUP_TOP          
               62  ROT_THREE        
               64  COMPARE_OP               <=
               66  POP_JUMP_IF_FALSE    76  'to 76'
               68  LOAD_STR                 '9'
               70  COMPARE_OP               <=
               72  POP_JUMP_IF_TRUE    130  'to 130'
               74  JUMP_FORWARD         78  'to 78'
             76_0  COME_FROM            66  '66'
               76  POP_TOP          
             78_0  COME_FROM            74  '74'
               78  LOAD_STR                 'A'
               80  LOAD_FAST                'ch'
               82  DUP_TOP          
               84  ROT_THREE        
               86  COMPARE_OP               <=
               88  POP_JUMP_IF_FALSE    98  'to 98'
               90  LOAD_STR                 'Z'
               92  COMPARE_OP               <=
               94  POP_JUMP_IF_TRUE    130  'to 130'
               96  JUMP_FORWARD        100  'to 100'
             98_0  COME_FROM            88  '88'
               98  POP_TOP          
            100_0  COME_FROM            96  '96'
              100  LOAD_STR                 'a'
              102  LOAD_FAST                'ch'
              104  DUP_TOP          
              106  ROT_THREE        
              108  COMPARE_OP               <=
              110  POP_JUMP_IF_FALSE   120  'to 120'
              112  LOAD_STR                 'z'
              114  COMPARE_OP               <=
              116  POP_JUMP_IF_TRUE    130  'to 130'
              118  JUMP_FORWARD        122  'to 122'
            120_0  COME_FROM           110  '110'
              120  POP_TOP          
            122_0  COME_FROM           118  '118'

 L. 918       122  LOAD_FAST                'ch'
              124  LOAD_STR                 '-_'
              126  COMPARE_OP               in

 L. 917       128  POP_JUMP_IF_FALSE   150  'to 150'
            130_0  COME_FROM           116  '116'
            130_1  COME_FROM            94  '94'
            130_2  COME_FROM            72  '72'

 L. 919       130  LOAD_FAST                'length'
              132  LOAD_CONST               1
              134  INPLACE_ADD      
              136  STORE_FAST               'length'

 L. 920       138  LOAD_FAST                'self'
              140  LOAD_METHOD              peek
              142  LOAD_FAST                'length'
              144  CALL_METHOD_1         1  ''
              146  STORE_FAST               'ch'
              148  JUMP_BACK            56  'to 56'
            150_0  COME_FROM           128  '128'

 L. 921       150  LOAD_FAST                'length'
              152  POP_JUMP_IF_TRUE    180  'to 180'

 L. 922       154  LOAD_GLOBAL              ScannerError
              156  LOAD_STR                 'while scanning an %s'
              158  LOAD_FAST                'name'
              160  BINARY_MODULO    
              162  LOAD_FAST                'start_mark'

 L. 923       164  LOAD_STR                 'expected alphabetic or numeric character, but found %r'

 L. 924       166  LOAD_FAST                'ch'

 L. 923       168  BINARY_MODULO    

 L. 924       170  LOAD_FAST                'self'
              172  LOAD_METHOD              get_mark
              174  CALL_METHOD_0         0  ''

 L. 922       176  CALL_FUNCTION_4       4  ''
              178  RAISE_VARARGS_1       1  'exception instance'
            180_0  COME_FROM           152  '152'

 L. 925       180  LOAD_FAST                'self'
              182  LOAD_METHOD              prefix
              184  LOAD_FAST                'length'
              186  CALL_METHOD_1         1  ''
              188  STORE_FAST               'value'

 L. 926       190  LOAD_FAST                'self'
              192  LOAD_METHOD              forward
              194  LOAD_FAST                'length'
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          

 L. 927       200  LOAD_FAST                'self'
              202  LOAD_METHOD              peek
              204  CALL_METHOD_0         0  ''
              206  STORE_FAST               'ch'

 L. 928       208  LOAD_FAST                'ch'
              210  LOAD_STR                 '\x00 \t\r\n\x85\u2028\u2029?:,]}%@`'
              212  COMPARE_OP               not-in
              214  POP_JUMP_IF_FALSE   242  'to 242'

 L. 929       216  LOAD_GLOBAL              ScannerError
              218  LOAD_STR                 'while scanning an %s'
              220  LOAD_FAST                'name'
              222  BINARY_MODULO    
              224  LOAD_FAST                'start_mark'

 L. 930       226  LOAD_STR                 'expected alphabetic or numeric character, but found %r'

 L. 931       228  LOAD_FAST                'ch'

 L. 930       230  BINARY_MODULO    

 L. 931       232  LOAD_FAST                'self'
              234  LOAD_METHOD              get_mark
              236  CALL_METHOD_0         0  ''

 L. 929       238  CALL_FUNCTION_4       4  ''
              240  RAISE_VARARGS_1       1  'exception instance'
            242_0  COME_FROM           214  '214'

 L. 932       242  LOAD_FAST                'self'
              244  LOAD_METHOD              get_mark
              246  CALL_METHOD_0         0  ''
              248  STORE_FAST               'end_mark'

 L. 933       250  LOAD_FAST                'TokenClass'
              252  LOAD_FAST                'value'
              254  LOAD_FAST                'start_mark'
              256  LOAD_FAST                'end_mark'
              258  CALL_FUNCTION_3       3  ''
              260  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 260

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
        else:
            if ch in '\x00 \t\r\n\x85\u2028\u2029':
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
        else:
            if increment is None:
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
                    if self.peek(length) not in '\x00\r\n\x85\u2028\u2029':
                        length += 1
                else:
                    chunks.append(self.prefix(length))
                    self.forward(length)
                    line_break = self.scan_line_break()
                    breaks, end_mark = self.scan_block_scalar_breaks(indent)
                    if self.column == indent and self.peek() != '\x00':
                        if folded and line_break == '\n' and leading_non_space and self.peek() not in ' \t':
                            breaks or chunks.append(' ')
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
        return (
         chomping, increment)

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
        if self.column < indent:
            if self.peek() == ' ':
                self.forward()
        else:
            while True:
                if self.peek() in '\r\n\x85\u2028\u2029':
                    chunks.append(self.scan_line_break())
                    end_mark = self.get_mark()
                    while True:
                        if self.column < indent and self.peek() == ' ':
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
        while True:
            length = 0
            if self.peek(length) not in '\'"\\\x00 \t\r\n\x85\u2028\u2029':
                length += 1
            else:
                if length:
                    chunks.append(self.prefix(length))
                    self.forward(length)
                ch = self.peek()
                if not double:
                    if ch == "'":
                        if self.peek(1) == "'":
                            chunks.append("'")
                            self.forward(2)
                if double:
                    if ch == "'" or (double or ch) in '"\\':
                        chunks.append(ch)
                        self.forward()
                elif double:
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

                    else:
                        if ch in '\r\n\x85\u2028\u2029':
                            self.scan_line_break()
                            chunks.extend(self.scan_flow_scalar_breaks(double, start_mark))
                        else:
                            raise ScannerError('while scanning a double-quoted scalar', start_mark, 'found unknown escape character %r' % ch, self.get_mark())
                else:
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
        else:
            if ch in '\r\n\x85\u2028\u2029':
                line_break = self.scan_line_break()
                breaks = self.scan_flow_scalar_breaks(double, start_mark)
                if line_break != '\n':
                    chunks.append(line_break)
                else:
                    if not breaks:
                        chunks.append(' ')
                chunks.extend(breaks)
            else:
                chunks.append(whitespaces)
        return chunks

    def scan_flow_scalar_breaks(self, double, start_mark):
        chunks = []
        while True:
            prefix = self.prefix(3)
            if prefix == '---' or prefix == '...':
                if self.peek(3) in '\x00 \t\r\n\x85\u2028\u2029':
                    raise ScannerError('while scanning a quoted scalar', start_mark, 'found unexpected document separator', self.get_mark())
            if self.peek() in ' \t':
                self.forward()
            elif self.peek() in '\r\n\x85\u2028\u2029':
                chunks.append(self.scan_line_break())
            else:
                return chunks

    def scan_plain--- This code section failed: ---

 L.1276         0  BUILD_LIST_0          0 
                2  STORE_FAST               'chunks'

 L.1277         4  LOAD_FAST                'self'
                6  LOAD_METHOD              get_mark
                8  CALL_METHOD_0         0  ''
               10  STORE_FAST               'start_mark'

 L.1278        12  LOAD_FAST                'start_mark'
               14  STORE_FAST               'end_mark'

 L.1279        16  LOAD_FAST                'self'
               18  LOAD_ATTR                indent
               20  LOAD_CONST               1
               22  BINARY_ADD       
               24  STORE_FAST               'indent'

 L.1284        26  BUILD_LIST_0          0 
               28  STORE_FAST               'spaces'
             30_0  COME_FROM           234  '234'
             30_1  COME_FROM           224  '224'

 L.1286        30  LOAD_CONST               0
               32  STORE_FAST               'length'

 L.1287        34  LOAD_FAST                'self'
               36  LOAD_METHOD              peek
               38  CALL_METHOD_0         0  ''
               40  LOAD_STR                 '#'
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    48  'to 48'

 L.1288        46  BREAK_LOOP          240  'to 240'
             48_0  COME_FROM            44  '44'

 L.1290        48  LOAD_FAST                'self'
               50  LOAD_METHOD              peek
               52  LOAD_FAST                'length'
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'ch'

 L.1291        58  LOAD_FAST                'ch'
               60  LOAD_STR                 '\x00 \t\r\n\x85\u2028\u2029'
               62  COMPARE_OP               in
               64  POP_JUMP_IF_TRUE    132  'to 132'

 L.1292        66  LOAD_FAST                'ch'
               68  LOAD_STR                 ':'
               70  COMPARE_OP               ==

 L.1291        72  POP_JUMP_IF_FALSE   106  'to 106'

 L.1293        74  LOAD_FAST                'self'
               76  LOAD_METHOD              peek
               78  LOAD_FAST                'length'
               80  LOAD_CONST               1
               82  BINARY_ADD       
               84  CALL_METHOD_1         1  ''
               86  LOAD_STR                 '\x00 \t\r\n\x85\u2028\u2029'

 L.1294        88  LOAD_FAST                'self'
               90  LOAD_ATTR                flow_level
               92  POP_JUMP_IF_FALSE    98  'to 98'
               94  LOAD_STR                 ',[]{}'
               96  JUMP_FORWARD        100  'to 100'
             98_0  COME_FROM            92  '92'
               98  LOAD_STR                 ''
            100_0  COME_FROM            96  '96'

 L.1293       100  BINARY_ADD       
              102  COMPARE_OP               in

 L.1291       104  POP_JUMP_IF_TRUE    132  'to 132'
            106_0  COME_FROM            72  '72'

 L.1295       106  LOAD_FAST                'self'
              108  LOAD_ATTR                flow_level

 L.1291       110  POP_JUMP_IF_FALSE   122  'to 122'

 L.1295       112  LOAD_FAST                'ch'
              114  LOAD_STR                 ',?[]{}'
              116  COMPARE_OP               in

 L.1291       118  POP_JUMP_IF_FALSE   122  'to 122'

 L.1296       120  BREAK_LOOP          132  'to 132'
            122_0  COME_FROM           118  '118'
            122_1  COME_FROM           110  '110'

 L.1297       122  LOAD_FAST                'length'
              124  LOAD_CONST               1
              126  INPLACE_ADD      
              128  STORE_FAST               'length'
              130  JUMP_BACK            48  'to 48'
            132_0  COME_FROM           104  '104'
            132_1  COME_FROM            64  '64'

 L.1298       132  LOAD_FAST                'length'
              134  LOAD_CONST               0
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   142  'to 142'

 L.1299       140  BREAK_LOOP          240  'to 240'
            142_0  COME_FROM           138  '138'

 L.1300       142  LOAD_CONST               False
              144  LOAD_FAST                'self'
              146  STORE_ATTR               allow_simple_key

 L.1301       148  LOAD_FAST                'chunks'
              150  LOAD_METHOD              extend
              152  LOAD_FAST                'spaces'
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          

 L.1302       158  LOAD_FAST                'chunks'
              160  LOAD_METHOD              append
              162  LOAD_FAST                'self'
              164  LOAD_METHOD              prefix
              166  LOAD_FAST                'length'
              168  CALL_METHOD_1         1  ''
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          

 L.1303       174  LOAD_FAST                'self'
              176  LOAD_METHOD              forward
              178  LOAD_FAST                'length'
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          

 L.1304       184  LOAD_FAST                'self'
              186  LOAD_METHOD              get_mark
              188  CALL_METHOD_0         0  ''
              190  STORE_FAST               'end_mark'

 L.1305       192  LOAD_FAST                'self'
              194  LOAD_METHOD              scan_plain_spaces
              196  LOAD_FAST                'indent'
              198  LOAD_FAST                'start_mark'
              200  CALL_METHOD_2         2  ''
              202  STORE_FAST               'spaces'

 L.1306       204  LOAD_FAST                'spaces'
              206  POP_JUMP_IF_FALSE   240  'to 240'
              208  LOAD_FAST                'self'
              210  LOAD_METHOD              peek
              212  CALL_METHOD_0         0  ''
              214  LOAD_STR                 '#'
              216  COMPARE_OP               ==
              218  POP_JUMP_IF_TRUE    240  'to 240'

 L.1307       220  LOAD_FAST                'self'
              222  LOAD_ATTR                flow_level

 L.1306       224  POP_JUMP_IF_TRUE     30  'to 30'

 L.1307       226  LOAD_FAST                'self'
              228  LOAD_ATTR                column
              230  LOAD_FAST                'indent'
              232  COMPARE_OP               <

 L.1306       234  POP_JUMP_IF_FALSE    30  'to 30'

 L.1308       236  BREAK_LOOP          240  'to 240'
              238  JUMP_BACK            30  'to 30'
            240_0  COME_FROM           218  '218'
            240_1  COME_FROM           206  '206'

 L.1309       240  LOAD_GLOBAL              ScalarToken
              242  LOAD_STR                 ''
              244  LOAD_METHOD              join
              246  LOAD_FAST                'chunks'
              248  CALL_METHOD_1         1  ''
              250  LOAD_CONST               True
              252  LOAD_FAST                'start_mark'
              254  LOAD_FAST                'end_mark'
              256  CALL_FUNCTION_4       4  ''
              258  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 258

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
        else:
            breaks = []
        while self.peek() in ' \r\n\x85\u2028\u2029':
            if self.peek() == ' ':
                self.forward()

        breaks.append(self.scan_line_break())
        prefix = self.prefix(3)
        if not prefix == '---':
            if prefix == '...':
                if self.peek(3) in '\x00 \t\r\n\x85\u2028\u2029':
                    return
                elif line_break != '\n':
                    chunks.append(line_break)
                else:
                    if not breaks:
                        chunks.append(' ')
            chunks.extend(breaks)
        else:
            if whitespaces:
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

 L.1355        32  LOAD_FAST                'self'
               34  LOAD_METHOD              get_mark
               36  CALL_METHOD_0         0  ''

 L.1354        38  CALL_FUNCTION_4       4  ''
               40  RAISE_VARARGS_1       1  'exception instance'
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
               62  POP_JUMP_IF_FALSE   210  'to 210'

 L.1359        64  LOAD_STR                 '0'
               66  LOAD_FAST                'ch'
               68  DUP_TOP          
               70  ROT_THREE        
               72  COMPARE_OP               <=
               74  POP_JUMP_IF_FALSE    84  'to 84'
               76  LOAD_STR                 '9'
               78  COMPARE_OP               <=
               80  POP_JUMP_IF_TRUE    138  'to 138'
               82  JUMP_FORWARD         86  'to 86'
             84_0  COME_FROM            74  '74'
               84  POP_TOP          
             86_0  COME_FROM            82  '82'
               86  LOAD_STR                 'A'
               88  LOAD_FAST                'ch'
               90  DUP_TOP          
               92  ROT_THREE        
               94  COMPARE_OP               <=
               96  POP_JUMP_IF_FALSE   106  'to 106'
               98  LOAD_STR                 'Z'
              100  COMPARE_OP               <=
              102  POP_JUMP_IF_TRUE    138  'to 138'
              104  JUMP_FORWARD        108  'to 108'
            106_0  COME_FROM            96  '96'
              106  POP_TOP          
            108_0  COME_FROM           104  '104'
              108  LOAD_STR                 'a'
              110  LOAD_FAST                'ch'
              112  DUP_TOP          
              114  ROT_THREE        
              116  COMPARE_OP               <=
              118  POP_JUMP_IF_FALSE   128  'to 128'
              120  LOAD_STR                 'z'
              122  COMPARE_OP               <=
              124  POP_JUMP_IF_TRUE    138  'to 138'
              126  JUMP_FORWARD        130  'to 130'
            128_0  COME_FROM           118  '118'
              128  POP_TOP          
            130_0  COME_FROM           126  '126'

 L.1360       130  LOAD_FAST                'ch'
              132  LOAD_STR                 '-_'
              134  COMPARE_OP               in

 L.1359       136  POP_JUMP_IF_FALSE   158  'to 158'
            138_0  COME_FROM           124  '124'
            138_1  COME_FROM           102  '102'
            138_2  COME_FROM            80  '80'

 L.1361       138  LOAD_FAST                'length'
              140  LOAD_CONST               1
              142  INPLACE_ADD      
              144  STORE_FAST               'length'

 L.1362       146  LOAD_FAST                'self'
              148  LOAD_METHOD              peek
              150  LOAD_FAST                'length'
              152  CALL_METHOD_1         1  ''
              154  STORE_FAST               'ch'
              156  JUMP_BACK            64  'to 64'
            158_0  COME_FROM           136  '136'

 L.1363       158  LOAD_FAST                'ch'
              160  LOAD_STR                 '!'
              162  COMPARE_OP               !=
              164  POP_JUMP_IF_FALSE   202  'to 202'

 L.1364       166  LOAD_FAST                'self'
              168  LOAD_METHOD              forward
              170  LOAD_FAST                'length'
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          

 L.1365       176  LOAD_GLOBAL              ScannerError
              178  LOAD_STR                 'while scanning a %s'
              180  LOAD_FAST                'name'
              182  BINARY_MODULO    
              184  LOAD_FAST                'start_mark'

 L.1366       186  LOAD_STR                 "expected '!', but found %r"
              188  LOAD_FAST                'ch'
              190  BINARY_MODULO    

 L.1366       192  LOAD_FAST                'self'
              194  LOAD_METHOD              get_mark
              196  CALL_METHOD_0         0  ''

 L.1365       198  CALL_FUNCTION_4       4  ''
              200  RAISE_VARARGS_1       1  'exception instance'
            202_0  COME_FROM           164  '164'

 L.1367       202  LOAD_FAST                'length'
              204  LOAD_CONST               1
              206  INPLACE_ADD      
              208  STORE_FAST               'length'
            210_0  COME_FROM            62  '62'

 L.1368       210  LOAD_FAST                'self'
              212  LOAD_METHOD              prefix
              214  LOAD_FAST                'length'
              216  CALL_METHOD_1         1  ''
              218  STORE_FAST               'value'

 L.1369       220  LOAD_FAST                'self'
              222  LOAD_METHOD              forward
              224  LOAD_FAST                'length'
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          

 L.1370       230  LOAD_FAST                'value'
              232  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 232

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

 L.1378        18  LOAD_STR                 '0'
               20  LOAD_FAST                'ch'
               22  DUP_TOP          
               24  ROT_THREE        
               26  COMPARE_OP               <=
               28  POP_JUMP_IF_FALSE    38  'to 38'
               30  LOAD_STR                 '9'
               32  COMPARE_OP               <=
               34  POP_JUMP_IF_TRUE     92  'to 92'
               36  JUMP_FORWARD         40  'to 40'
             38_0  COME_FROM            28  '28'
               38  POP_TOP          
             40_0  COME_FROM            36  '36'
               40  LOAD_STR                 'A'
               42  LOAD_FAST                'ch'
               44  DUP_TOP          
               46  ROT_THREE        
               48  COMPARE_OP               <=
               50  POP_JUMP_IF_FALSE    60  'to 60'
               52  LOAD_STR                 'Z'
               54  COMPARE_OP               <=
               56  POP_JUMP_IF_TRUE     92  'to 92'
               58  JUMP_FORWARD         62  'to 62'
             60_0  COME_FROM            50  '50'
               60  POP_TOP          
             62_0  COME_FROM            58  '58'
               62  LOAD_STR                 'a'
               64  LOAD_FAST                'ch'
               66  DUP_TOP          
               68  ROT_THREE        
               70  COMPARE_OP               <=
               72  POP_JUMP_IF_FALSE    82  'to 82'
               74  LOAD_STR                 'z'
               76  COMPARE_OP               <=
               78  POP_JUMP_IF_TRUE     92  'to 92'
               80  JUMP_FORWARD         84  'to 84'
             82_0  COME_FROM            72  '72'
               82  POP_TOP          
             84_0  COME_FROM            80  '80'

 L.1379        84  LOAD_FAST                'ch'
               86  LOAD_STR                 "-;/?:@&=+$,_.!~*'()[]%"
               88  COMPARE_OP               in

 L.1378        90  POP_JUMP_IF_FALSE   170  'to 170'
             92_0  COME_FROM            78  '78'
             92_1  COME_FROM            56  '56'
             92_2  COME_FROM            34  '34'

 L.1380        92  LOAD_FAST                'ch'
               94  LOAD_STR                 '%'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   150  'to 150'

 L.1381       100  LOAD_FAST                'chunks'
              102  LOAD_METHOD              append
              104  LOAD_FAST                'self'
              106  LOAD_METHOD              prefix
              108  LOAD_FAST                'length'
              110  CALL_METHOD_1         1  ''
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          

 L.1382       116  LOAD_FAST                'self'
              118  LOAD_METHOD              forward
              120  LOAD_FAST                'length'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L.1383       126  LOAD_CONST               0
              128  STORE_FAST               'length'

 L.1384       130  LOAD_FAST                'chunks'
              132  LOAD_METHOD              append
              134  LOAD_FAST                'self'
              136  LOAD_METHOD              scan_uri_escapes
              138  LOAD_FAST                'name'
              140  LOAD_FAST                'start_mark'
              142  CALL_METHOD_2         2  ''
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          
              148  JUMP_FORWARD        158  'to 158'
            150_0  COME_FROM            98  '98'

 L.1386       150  LOAD_FAST                'length'
              152  LOAD_CONST               1
              154  INPLACE_ADD      
              156  STORE_FAST               'length'
            158_0  COME_FROM           148  '148'

 L.1387       158  LOAD_FAST                'self'
              160  LOAD_METHOD              peek
              162  LOAD_FAST                'length'
              164  CALL_METHOD_1         1  ''
              166  STORE_FAST               'ch'
              168  JUMP_BACK            18  'to 18'
            170_0  COME_FROM            90  '90'

 L.1388       170  LOAD_FAST                'length'
              172  POP_JUMP_IF_FALSE   204  'to 204'

 L.1389       174  LOAD_FAST                'chunks'
              176  LOAD_METHOD              append
              178  LOAD_FAST                'self'
              180  LOAD_METHOD              prefix
              182  LOAD_FAST                'length'
              184  CALL_METHOD_1         1  ''
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          

 L.1390       190  LOAD_FAST                'self'
              192  LOAD_METHOD              forward
              194  LOAD_FAST                'length'
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          

 L.1391       200  LOAD_CONST               0
              202  STORE_FAST               'length'
            204_0  COME_FROM           172  '172'

 L.1392       204  LOAD_FAST                'chunks'
              206  POP_JUMP_IF_TRUE    234  'to 234'

 L.1393       208  LOAD_GLOBAL              ScannerError
              210  LOAD_STR                 'while parsing a %s'
              212  LOAD_FAST                'name'
              214  BINARY_MODULO    
              216  LOAD_FAST                'start_mark'

 L.1394       218  LOAD_STR                 'expected URI, but found %r'
              220  LOAD_FAST                'ch'
              222  BINARY_MODULO    

 L.1394       224  LOAD_FAST                'self'
              226  LOAD_METHOD              get_mark
              228  CALL_METHOD_0         0  ''

 L.1393       230  CALL_FUNCTION_4       4  ''
              232  RAISE_VARARGS_1       1  'exception instance'
            234_0  COME_FROM           206  '206'

 L.1395       234  LOAD_STR                 ''
              236  LOAD_METHOD              join
              238  LOAD_FAST                'chunks'
              240  CALL_METHOD_1         1  ''
              242  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 242

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

        else:
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