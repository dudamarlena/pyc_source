# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./vendor/yaml/emitter.py
# Compiled at: 2019-03-12 19:45:05
# Size of source mod 2**32: 43006 bytes
__all__ = [
 'Emitter', 'EmitterError']
from .error import YAMLError
from .events import *

class EmitterError(YAMLError):
    pass


class ScalarAnalysis:

    def __init__(self, scalar, empty, multiline, allow_flow_plain, allow_block_plain, allow_single_quoted, allow_double_quoted, allow_block):
        self.scalar = scalar
        self.empty = empty
        self.multiline = multiline
        self.allow_flow_plain = allow_flow_plain
        self.allow_block_plain = allow_block_plain
        self.allow_single_quoted = allow_single_quoted
        self.allow_double_quoted = allow_double_quoted
        self.allow_block = allow_block


class Emitter:
    DEFAULT_TAG_PREFIXES = {'!':'!', 
     'tag:yaml.org,2002:':'!!'}

    def __init__(self, stream, canonical=None, indent=None, width=None, allow_unicode=None, line_break=None):
        self.stream = stream
        self.encoding = None
        self.states = []
        self.state = self.expect_stream_start
        self.events = []
        self.event = None
        self.indents = []
        self.indent = None
        self.flow_level = 0
        self.root_context = False
        self.sequence_context = False
        self.mapping_context = False
        self.simple_key_context = False
        self.line = 0
        self.column = 0
        self.whitespace = True
        self.indention = True
        self.open_ended = False
        self.canonical = canonical
        self.allow_unicode = allow_unicode
        self.best_indent = 2
        if indent:
            if 1 < indent < 10:
                self.best_indent = indent
        self.best_width = 80
        if width:
            if width > self.best_indent * 2:
                self.best_width = width
        self.best_line_break = '\n'
        if line_break in ('\r', '\n', '\r\n'):
            self.best_line_break = line_break
        self.tag_prefixes = None
        self.prepared_anchor = None
        self.prepared_tag = None
        self.analysis = None
        self.style = None

    def dispose(self):
        self.states = []
        self.state = None

    def emit(self, event):
        self.events.append(event)
        while not self.need_more_events():
            self.event = self.events.pop(0)
            self.state()
            self.event = None

    def need_more_events(self):
        if not self.events:
            return True
        event = self.events[0]
        if isinstance(event, DocumentStartEvent):
            return self.need_events(1)
        if isinstance(event, SequenceStartEvent):
            return self.need_events(2)
        if isinstance(event, MappingStartEvent):
            return self.need_events(3)
        return False

    def need_events(self, count):
        level = 0
        for event in self.events[1:]:
            if isinstance(event, (DocumentStartEvent, CollectionStartEvent)):
                level += 1
            else:
                if isinstance(event, (DocumentEndEvent, CollectionEndEvent)):
                    level -= 1
                else:
                    if isinstance(event, StreamEndEvent):
                        level = -1
            if level < 0:
                return False
            return len(self.events) < count + 1

    def increase_indent(self, flow=False, indentless=False):
        self.indents.append(self.indent)
        if self.indent is None:
            if flow:
                self.indent = self.best_indent
            else:
                self.indent = 0
        elif not indentless:
            self.indent += self.best_indent

    def expect_stream_start(self):
        if isinstance(self.event, StreamStartEvent):
            if self.event.encoding:
                if not hasattr(self.stream, 'encoding'):
                    self.encoding = self.event.encoding
            self.write_stream_start()
            self.state = self.expect_first_document_start
        else:
            raise EmitterError('expected StreamStartEvent, but got %s' % self.event)

    def expect_nothing(self):
        raise EmitterError('expected nothing, but got %s' % self.event)

    def expect_first_document_start(self):
        return self.expect_document_start(first=True)

    def expect_document_start(self, first=False):
        if isinstance(self.event, DocumentStartEvent) and not self.event.version:
            if self.event.tags:
                if self.open_ended:
                    self.write_indicator('...', True)
                    self.write_indent()
        else:
            if self.event.version:
                version_text = self.prepare_version(self.event.version)
                self.write_version_directive(version_text)
            self.tag_prefixes = self.DEFAULT_TAG_PREFIXES.copy()
            if self.event.tags:
                handles = sorted(self.event.tags.keys())
                for handle in handles:
                    prefix = self.event.tags[handle]
                    self.tag_prefixes[prefix] = handle
                    handle_text = self.prepare_tag_handle(handle)
                    prefix_text = self.prepare_tag_prefix(prefix)
                    self.write_tag_directive(handle_text, prefix_text)

        implicit = first and not self.event.explicit and not self.canonical and not self.event.version and not self.event.tags and not self.check_empty_document()
        if not implicit:
            self.write_indent()
            self.write_indicator('---', True)
            if self.canonical:
                self.write_indent()
            self.state = self.expect_document_root
        elif isinstance(self.event, StreamEndEvent):
            if self.open_ended:
                self.write_indicator('...', True)
                self.write_indent()
            self.write_stream_end()
            self.state = self.expect_nothing
        else:
            raise EmitterError('expected DocumentStartEvent, but got %s' % self.event)

    def expect_document_end(self):
        if isinstance(self.event, DocumentEndEvent):
            self.write_indent()
            if self.event.explicit:
                self.write_indicator('...', True)
                self.write_indent()
            self.flush_stream()
            self.state = self.expect_document_start
        else:
            raise EmitterError('expected DocumentEndEvent, but got %s' % self.event)

    def expect_document_root(self):
        self.states.append(self.expect_document_end)
        self.expect_node(root=True)

    def expect_node--- This code section failed: ---

 L. 234         0  LOAD_FAST                'root'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               root_context

 L. 235         6  LOAD_FAST                'sequence'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               sequence_context

 L. 236        12  LOAD_FAST                'mapping'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               mapping_context

 L. 237        18  LOAD_FAST                'simple_key'
               20  LOAD_FAST                'self'
               22  STORE_ATTR               simple_key_context

 L. 238        24  LOAD_GLOBAL              isinstance
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                event
               30  LOAD_GLOBAL              AliasEvent
               32  CALL_FUNCTION_2       2  ''
               34  POP_JUMP_IF_FALSE    46  'to 46'

 L. 239        36  LOAD_FAST                'self'
               38  LOAD_METHOD              expect_alias
               40  CALL_METHOD_0         0  ''
               42  POP_TOP          
               44  JUMP_FORWARD        236  'to 236'
             46_0  COME_FROM            34  '34'

 L. 240        46  LOAD_GLOBAL              isinstance
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                event
               52  LOAD_GLOBAL              ScalarEvent
               54  LOAD_GLOBAL              CollectionStartEvent
               56  BUILD_TUPLE_2         2 
               58  CALL_FUNCTION_2       2  ''
               60  POP_JUMP_IF_FALSE   222  'to 222'

 L. 241        62  LOAD_FAST                'self'
               64  LOAD_METHOD              process_anchor
               66  LOAD_STR                 '&'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L. 242        72  LOAD_FAST                'self'
               74  LOAD_METHOD              process_tag
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          

 L. 243        80  LOAD_GLOBAL              isinstance
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                event
               86  LOAD_GLOBAL              ScalarEvent
               88  CALL_FUNCTION_2       2  ''
               90  POP_JUMP_IF_FALSE   102  'to 102'

 L. 244        92  LOAD_FAST                'self'
               94  LOAD_METHOD              expect_scalar
               96  CALL_METHOD_0         0  ''
               98  POP_TOP          
              100  JUMP_ABSOLUTE       236  'to 236'
            102_0  COME_FROM            90  '90'

 L. 245       102  LOAD_GLOBAL              isinstance
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                event
              108  LOAD_GLOBAL              SequenceStartEvent
              110  CALL_FUNCTION_2       2  ''
              112  POP_JUMP_IF_FALSE   162  'to 162'

 L. 246       114  LOAD_FAST                'self'
              116  LOAD_ATTR                flow_level
              118  POP_JUMP_IF_TRUE    142  'to 142'
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                canonical
              124  POP_JUMP_IF_TRUE    142  'to 142'
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                event
              130  LOAD_ATTR                flow_style
              132  POP_JUMP_IF_TRUE    142  'to 142'

 L. 247       134  LOAD_FAST                'self'
              136  LOAD_METHOD              check_empty_sequence
              138  CALL_METHOD_0         0  ''

 L. 246       140  POP_JUMP_IF_FALSE   152  'to 152'
            142_0  COME_FROM           132  '132'
            142_1  COME_FROM           124  '124'
            142_2  COME_FROM           118  '118'

 L. 248       142  LOAD_FAST                'self'
              144  LOAD_METHOD              expect_flow_sequence
              146  CALL_METHOD_0         0  ''
              148  POP_TOP          
              150  JUMP_ABSOLUTE       220  'to 220'
            152_0  COME_FROM           140  '140'

 L. 250       152  LOAD_FAST                'self'
              154  LOAD_METHOD              expect_block_sequence
              156  CALL_METHOD_0         0  ''
              158  POP_TOP          
              160  JUMP_ABSOLUTE       236  'to 236'
            162_0  COME_FROM           112  '112'

 L. 251       162  LOAD_GLOBAL              isinstance
              164  LOAD_FAST                'self'
              166  LOAD_ATTR                event
              168  LOAD_GLOBAL              MappingStartEvent
              170  CALL_FUNCTION_2       2  ''
              172  POP_JUMP_IF_FALSE   236  'to 236'

 L. 252       174  LOAD_FAST                'self'
              176  LOAD_ATTR                flow_level
              178  POP_JUMP_IF_TRUE    202  'to 202'
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                canonical
              184  POP_JUMP_IF_TRUE    202  'to 202'
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                event
              190  LOAD_ATTR                flow_style
              192  POP_JUMP_IF_TRUE    202  'to 202'

 L. 253       194  LOAD_FAST                'self'
              196  LOAD_METHOD              check_empty_mapping
              198  CALL_METHOD_0         0  ''

 L. 252       200  POP_JUMP_IF_FALSE   212  'to 212'
            202_0  COME_FROM           192  '192'
            202_1  COME_FROM           184  '184'
            202_2  COME_FROM           178  '178'

 L. 254       202  LOAD_FAST                'self'
              204  LOAD_METHOD              expect_flow_mapping
              206  CALL_METHOD_0         0  ''
              208  POP_TOP          
              210  JUMP_ABSOLUTE       236  'to 236'
            212_0  COME_FROM           200  '200'

 L. 256       212  LOAD_FAST                'self'
              214  LOAD_METHOD              expect_block_mapping
              216  CALL_METHOD_0         0  ''
              218  POP_TOP          
              220  JUMP_FORWARD        236  'to 236'
            222_0  COME_FROM            60  '60'

 L. 258       222  LOAD_GLOBAL              EmitterError
              224  LOAD_STR                 'expected NodeEvent, but got %s'
              226  LOAD_FAST                'self'
              228  LOAD_ATTR                event
              230  BINARY_MODULO    
              232  CALL_FUNCTION_1       1  ''
              234  RAISE_VARARGS_1       1  'exception instance'
            236_0  COME_FROM           220  '220'
            236_1  COME_FROM           172  '172'
            236_2  COME_FROM            44  '44'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 150

    def expect_alias(self):
        if self.event.anchor is None:
            raise EmitterError('anchor is not specified for alias')
        self.process_anchor('*')
        self.state = self.states.pop()

    def expect_scalar(self):
        self.increase_indent(flow=True)
        self.process_scalar()
        self.indent = self.indents.pop()
        self.state = self.states.pop()

    def expect_flow_sequence(self):
        self.write_indicator('[', True, whitespace=True)
        self.flow_level += 1
        self.increase_indent(flow=True)
        self.state = self.expect_first_flow_sequence_item

    def expect_first_flow_sequence_item(self):
        if isinstance(self.event, SequenceEndEvent):
            self.indent = self.indents.pop()
            self.flow_level -= 1
            self.write_indicator(']', False)
            self.state = self.states.pop()
        else:
            if self.canonical or self.column > self.best_width:
                self.write_indent()
            self.states.append(self.expect_flow_sequence_item)
            self.expect_node(sequence=True)

    def expect_flow_sequence_item(self):
        if isinstance(self.event, SequenceEndEvent):
            self.indent = self.indents.pop()
            self.flow_level -= 1
            if self.canonical:
                self.write_indicator(',', False)
                self.write_indent()
            self.write_indicator(']', False)
            self.state = self.states.pop()
        else:
            self.write_indicator(',', False)
            if self.canonical or self.column > self.best_width:
                self.write_indent()
            self.states.append(self.expect_flow_sequence_item)
            self.expect_node(sequence=True)

    def expect_flow_mapping(self):
        self.write_indicator('{', True, whitespace=True)
        self.flow_level += 1
        self.increase_indent(flow=True)
        self.state = self.expect_first_flow_mapping_key

    def expect_first_flow_mapping_key(self):
        if isinstance(self.event, MappingEndEvent):
            self.indent = self.indents.pop()
            self.flow_level -= 1
            self.write_indicator('}', False)
            self.state = self.states.pop()
        else:
            if not self.canonical:
                if self.column > self.best_width:
                    self.write_indent()
                if not self.canonical:
                    if self.check_simple_key():
                        self.states.append(self.expect_flow_mapping_simple_value)
                        self.expect_node(mapping=True, simple_key=True)
            else:
                self.write_indicator('?', True)
                self.states.append(self.expect_flow_mapping_value)
                self.expect_node(mapping=True)

    def expect_flow_mapping_key(self):
        if isinstance(self.event, MappingEndEvent):
            self.indent = self.indents.pop()
            self.flow_level -= 1
            if self.canonical:
                self.write_indicator(',', False)
                self.write_indent()
            self.write_indicator('}', False)
            self.state = self.states.pop()
        else:
            self.write_indicator(',', False)
            if not self.canonical:
                if self.column > self.best_width:
                    self.write_indent()
                if not self.canonical:
                    if self.check_simple_key():
                        self.states.append(self.expect_flow_mapping_simple_value)
                        self.expect_node(mapping=True, simple_key=True)
            else:
                self.write_indicator('?', True)
                self.states.append(self.expect_flow_mapping_value)
                self.expect_node(mapping=True)

    def expect_flow_mapping_simple_value(self):
        self.write_indicator(':', False)
        self.states.append(self.expect_flow_mapping_key)
        self.expect_node(mapping=True)

    def expect_flow_mapping_value(self):
        if self.canonical or self.column > self.best_width:
            self.write_indent()
        self.write_indicator(':', True)
        self.states.append(self.expect_flow_mapping_key)
        self.expect_node(mapping=True)

    def expect_block_sequence(self):
        indentless = self.mapping_context and not self.indention
        self.increase_indent(flow=False, indentless=indentless)
        self.state = self.expect_first_block_sequence_item

    def expect_first_block_sequence_item(self):
        return self.expect_block_sequence_item(first=True)

    def expect_block_sequence_item(self, first=False):
        if (first or isinstance)(self.event, SequenceEndEvent):
            self.indent = self.indents.pop()
            self.state = self.states.pop()
        else:
            self.write_indent()
            self.write_indicator('-', True, indention=True)
            self.states.append(self.expect_block_sequence_item)
            self.expect_node(sequence=True)

    def expect_block_mapping(self):
        self.increase_indent(flow=False)
        self.state = self.expect_first_block_mapping_key

    def expect_first_block_mapping_key(self):
        return self.expect_block_mapping_key(first=True)

    def expect_block_mapping_key(self, first=False):
        if (first or isinstance)(self.event, MappingEndEvent):
            self.indent = self.indents.pop()
            self.state = self.states.pop()
        else:
            self.write_indent()
            if self.check_simple_key():
                self.states.append(self.expect_block_mapping_simple_value)
                self.expect_node(mapping=True, simple_key=True)
            else:
                self.write_indicator('?', True, indention=True)
                self.states.append(self.expect_block_mapping_value)
                self.expect_node(mapping=True)

    def expect_block_mapping_simple_value(self):
        self.write_indicator(':', False)
        self.states.append(self.expect_block_mapping_key)
        self.expect_node(mapping=True)

    def expect_block_mapping_value(self):
        self.write_indent()
        self.write_indicator(':', True, indention=True)
        self.states.append(self.expect_block_mapping_key)
        self.expect_node(mapping=True)

    def check_empty_sequence(self):
        return isinstance(self.event, SequenceStartEvent) and self.events and isinstance(self.events[0], SequenceEndEvent)

    def check_empty_mapping(self):
        return isinstance(self.event, MappingStartEvent) and self.events and isinstance(self.events[0], MappingEndEvent)

    def check_empty_document(self):
        return isinstance(self.event, DocumentStartEvent) and self.events or False
        event = self.events[0]
        return isinstance(event, ScalarEvent) and event.anchor is None and event.tag is None and event.implicit and event.value == ''

    def check_simple_key(self):
        length = 0
        if isinstance(self.event, NodeEvent):
            if self.event.anchor is not None:
                if self.prepared_anchor is None:
                    self.prepared_anchor = self.prepare_anchor(self.event.anchor)
                length += len(self.prepared_anchor)
        elif isinstance(self.event, (ScalarEvent, CollectionStartEvent)) and self.event.tag is not None:
            if self.prepared_tag is None:
                self.prepared_tag = self.prepare_tag(self.event.tag)
            length += len(self.prepared_tag)
        if isinstance(self.event, ScalarEvent):
            if self.analysis is None:
                self.analysis = self.analyze_scalar(self.event.value)
            length += len(self.analysis.scalar)
        return length < 128 and (isinstance(self.event, AliasEvent) or isinstance(self.event, ScalarEvent) and not self.analysis.empty and not self.analysis.multiline or self.check_empty_sequence() or self.check_empty_mapping())

    def process_anchor(self, indicator):
        if self.event.anchor is None:
            self.prepared_anchor = None
            return
        if self.prepared_anchor is None:
            self.prepared_anchor = self.prepare_anchor(self.event.anchor)
        if self.prepared_anchor:
            self.write_indicator(indicator + self.prepared_anchor, True)
        self.prepared_anchor = None

    def process_tag(self):
        tag = self.event.tag
        if isinstance(self.event, ScalarEvent):
            if self.style is None:
                self.style = self.choose_scalar_style()
            elif not self.canonical or tag is None:
                if not (self.style == '' and self.event.implicit[0]):
                    if not self.style != '' or self.event.implicit[1]:
                        self.prepared_tag = None
                        return
            if self.event.implicit[0] and tag is None:
                tag = '!'
                self.prepared_tag = None
        elif not self.canonical or tag is None:
            if self.event.implicit:
                self.prepared_tag = None
                return
        if tag is None:
            raise EmitterError('tag is not specified')
        if self.prepared_tag is None:
            self.prepared_tag = self.prepare_tag(tag)
        if self.prepared_tag:
            self.write_indicator(self.prepared_tag, True)
        self.prepared_tag = None

    def choose_scalar_style(self):
        if self.analysis is None:
            self.analysis = self.analyze_scalar(self.event.value)
        elif not self.event.style == '"':
            if self.canonical:
                return '"'
            if not self.event.style:
                if self.event.implicit[0]:
                    if self.simple_key_context:
                        if not self.analysis.empty:
                            if not self.analysis.multiline:
                                if not (self.flow_level and self.analysis.allow_flow_plain):
                                    if not self.flow_level:
                                        if self.analysis.allow_block_plain:
                                            return ''
        else:
            if self.event.style:
                if self.event.style in '|>':
                    if not self.flow_level:
                        if not self.simple_key_context:
                            if self.analysis.allow_block:
                                return self.event.style
            if not self.event.style or self.event.style == "'":
                if self.analysis.allow_single_quoted:
                    return self.simple_key_context and self.analysis.multiline or "'"
        return '"'

    def process_scalar(self):
        if self.analysis is None:
            self.analysis = self.analyze_scalar(self.event.value)
        elif self.style is None:
            self.style = self.choose_scalar_style()
        else:
            split = not self.simple_key_context
            if self.style == '"':
                self.write_double_quoted(self.analysis.scalar, split)
            else:
                if self.style == "'":
                    self.write_single_quoted(self.analysis.scalar, split)
                else:
                    if self.style == '>':
                        self.write_folded(self.analysis.scalar)
                    else:
                        if self.style == '|':
                            self.write_literal(self.analysis.scalar)
                        else:
                            self.write_plain(self.analysis.scalar, split)
        self.analysis = None
        self.style = None

    def prepare_version(self, version):
        major, minor = version
        if major != 1:
            raise EmitterError('unsupported YAML version: %d.%d' % (major, minor))
        return '%d.%d' % (major, minor)

    def prepare_tag_handle(self, handle):
        if not handle:
            raise EmitterError('tag handle must not be empty')
        if handle[0] != '!' or handle[(-1)] != '!':
            raise EmitterError("tag handle must start and end with '!': %r" % handle)
        for ch in handle[1:-1]:
            if not '0' <= ch <= '9':
                if not 'A' <= ch <= 'Z':
                    if not 'a' <= ch <= 'z':
                        if not ch in '-_':
                            raise EmitterError('invalid character %r in the tag handle: %r' % (
                             ch, handle))
                        return handle

    def prepare_tag_prefix--- This code section failed: ---

 L. 558         0  LOAD_FAST                'prefix'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L. 559         4  LOAD_GLOBAL              EmitterError
                6  LOAD_STR                 'tag prefix must not be empty'
                8  CALL_FUNCTION_1       1  ''
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             2  '2'

 L. 560        12  BUILD_LIST_0          0 
               14  STORE_FAST               'chunks'

 L. 561        16  LOAD_CONST               0
               18  DUP_TOP          
               20  STORE_FAST               'start'
               22  STORE_FAST               'end'

 L. 562        24  LOAD_FAST                'prefix'
               26  LOAD_CONST               0
               28  BINARY_SUBSCR    
               30  LOAD_STR                 '!'
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    40  'to 40'

 L. 563        36  LOAD_CONST               1
               38  STORE_FAST               'end'
             40_0  COME_FROM            34  '34'

 L. 564        40  LOAD_FAST                'end'
               42  LOAD_GLOBAL              len
               44  LOAD_FAST                'prefix'
               46  CALL_FUNCTION_1       1  ''
               48  COMPARE_OP               <
               50  POP_JUMP_IF_FALSE   222  'to 222'

 L. 565        52  LOAD_FAST                'prefix'
               54  LOAD_FAST                'end'
               56  BINARY_SUBSCR    
               58  STORE_FAST               'ch'

 L. 566        60  LOAD_STR                 '0'
               62  LOAD_FAST                'ch'
               64  DUP_TOP          
               66  ROT_THREE        
               68  COMPARE_OP               <=
               70  POP_JUMP_IF_FALSE    80  'to 80'
               72  LOAD_STR                 '9'
               74  COMPARE_OP               <=
               76  POP_JUMP_IF_TRUE    134  'to 134'
               78  JUMP_FORWARD         82  'to 82'
             80_0  COME_FROM            70  '70'
               80  POP_TOP          
             82_0  COME_FROM            78  '78'
               82  LOAD_STR                 'A'
               84  LOAD_FAST                'ch'
               86  DUP_TOP          
               88  ROT_THREE        
               90  COMPARE_OP               <=
               92  POP_JUMP_IF_FALSE   102  'to 102'
               94  LOAD_STR                 'Z'
               96  COMPARE_OP               <=
               98  POP_JUMP_IF_TRUE    134  'to 134'
              100  JUMP_FORWARD        104  'to 104'
            102_0  COME_FROM            92  '92'
              102  POP_TOP          
            104_0  COME_FROM           100  '100'
              104  LOAD_STR                 'a'
              106  LOAD_FAST                'ch'
              108  DUP_TOP          
              110  ROT_THREE        
              112  COMPARE_OP               <=
              114  POP_JUMP_IF_FALSE   124  'to 124'
              116  LOAD_STR                 'z'
              118  COMPARE_OP               <=
              120  POP_JUMP_IF_TRUE    134  'to 134'
              122  JUMP_FORWARD        126  'to 126'
            124_0  COME_FROM           114  '114'
              124  POP_TOP          
            126_0  COME_FROM           122  '122'

 L. 567       126  LOAD_FAST                'ch'
              128  LOAD_STR                 "-;/?!:@&=+$,_.~*'()[]"
              130  COMPARE_OP               in

 L. 566       132  POP_JUMP_IF_FALSE   144  'to 144'
            134_0  COME_FROM           120  '120'
            134_1  COME_FROM            98  '98'
            134_2  COME_FROM            76  '76'

 L. 568       134  LOAD_FAST                'end'
              136  LOAD_CONST               1
              138  INPLACE_ADD      
              140  STORE_FAST               'end'
              142  JUMP_BACK            40  'to 40'
            144_0  COME_FROM           132  '132'

 L. 570       144  LOAD_FAST                'start'
              146  LOAD_FAST                'end'
              148  COMPARE_OP               <
              150  POP_JUMP_IF_FALSE   170  'to 170'

 L. 571       152  LOAD_FAST                'chunks'
              154  LOAD_METHOD              append
              156  LOAD_FAST                'prefix'
              158  LOAD_FAST                'start'
              160  LOAD_FAST                'end'
              162  BUILD_SLICE_2         2 
              164  BINARY_SUBSCR    
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          
            170_0  COME_FROM           150  '150'

 L. 572       170  LOAD_FAST                'end'
              172  LOAD_CONST               1
              174  BINARY_ADD       
              176  DUP_TOP          
              178  STORE_FAST               'start'
              180  STORE_FAST               'end'

 L. 573       182  LOAD_FAST                'ch'
              184  LOAD_METHOD              encode
              186  LOAD_STR                 'utf-8'
              188  CALL_METHOD_1         1  ''
              190  STORE_FAST               'data'

 L. 574       192  LOAD_FAST                'data'
              194  GET_ITER         
              196  FOR_ITER            220  'to 220'
              198  STORE_FAST               'ch'

 L. 575       200  LOAD_FAST                'chunks'
              202  LOAD_METHOD              append
              204  LOAD_STR                 '%%%02X'
              206  LOAD_GLOBAL              ord
              208  LOAD_FAST                'ch'
              210  CALL_FUNCTION_1       1  ''
              212  BINARY_MODULO    
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          
              218  JUMP_BACK           196  'to 196'
              220  JUMP_BACK            40  'to 40'
            222_0  COME_FROM            50  '50'

 L. 576       222  LOAD_FAST                'start'
              224  LOAD_FAST                'end'
              226  COMPARE_OP               <
              228  POP_JUMP_IF_FALSE   248  'to 248'

 L. 577       230  LOAD_FAST                'chunks'
              232  LOAD_METHOD              append
              234  LOAD_FAST                'prefix'
              236  LOAD_FAST                'start'
              238  LOAD_FAST                'end'
              240  BUILD_SLICE_2         2 
              242  BINARY_SUBSCR    
              244  CALL_METHOD_1         1  ''
              246  POP_TOP          
            248_0  COME_FROM           228  '228'

 L. 578       248  LOAD_STR                 ''
              250  LOAD_METHOD              join
              252  LOAD_FAST                'chunks'
              254  CALL_METHOD_1         1  ''
              256  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 256

    def prepare_tag--- This code section failed: ---

 L. 581         0  LOAD_FAST                'tag'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L. 582         4  LOAD_GLOBAL              EmitterError
                6  LOAD_STR                 'tag must not be empty'
                8  CALL_FUNCTION_1       1  ''
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             2  '2'

 L. 583        12  LOAD_FAST                'tag'
               14  LOAD_STR                 '!'
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 584        20  LOAD_FAST                'tag'
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 585        24  LOAD_CONST               None
               26  STORE_FAST               'handle'

 L. 586        28  LOAD_FAST                'tag'
               30  STORE_FAST               'suffix'

 L. 587        32  LOAD_GLOBAL              sorted
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                tag_prefixes
               38  LOAD_METHOD              keys
               40  CALL_METHOD_0         0  ''
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'prefixes'

 L. 588        46  LOAD_FAST                'prefixes'
               48  GET_ITER         
             50_0  COME_FROM            86  '86'
             50_1  COME_FROM            62  '62'
               50  FOR_ITER            116  'to 116'
               52  STORE_FAST               'prefix'

 L. 589        54  LOAD_FAST                'tag'
               56  LOAD_METHOD              startswith
               58  LOAD_FAST                'prefix'
               60  CALL_METHOD_1         1  ''
               62  POP_JUMP_IF_FALSE    50  'to 50'

 L. 590        64  LOAD_FAST                'prefix'
               66  LOAD_STR                 '!'
               68  COMPARE_OP               ==

 L. 589        70  POP_JUMP_IF_TRUE     88  'to 88'

 L. 590        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'prefix'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_GLOBAL              len
               80  LOAD_FAST                'tag'
               82  CALL_FUNCTION_1       1  ''
               84  COMPARE_OP               <

 L. 589        86  POP_JUMP_IF_FALSE    50  'to 50'
             88_0  COME_FROM            70  '70'

 L. 591        88  LOAD_FAST                'self'
               90  LOAD_ATTR                tag_prefixes
               92  LOAD_FAST                'prefix'
               94  BINARY_SUBSCR    
               96  STORE_FAST               'handle'

 L. 592        98  LOAD_FAST                'tag'
              100  LOAD_GLOBAL              len
              102  LOAD_FAST                'prefix'
              104  CALL_FUNCTION_1       1  ''
              106  LOAD_CONST               None
              108  BUILD_SLICE_2         2 
              110  BINARY_SUBSCR    
              112  STORE_FAST               'suffix'
              114  JUMP_BACK            50  'to 50'

 L. 593       116  BUILD_LIST_0          0 
              118  STORE_FAST               'chunks'

 L. 594       120  LOAD_CONST               0
              122  DUP_TOP          
              124  STORE_FAST               'start'
              126  STORE_FAST               'end'

 L. 595       128  LOAD_FAST                'end'
              130  LOAD_GLOBAL              len
              132  LOAD_FAST                'suffix'
              134  CALL_FUNCTION_1       1  ''
              136  COMPARE_OP               <
          138_140  POP_JUMP_IF_FALSE   328  'to 328'

 L. 596       142  LOAD_FAST                'suffix'
              144  LOAD_FAST                'end'
              146  BINARY_SUBSCR    
              148  STORE_FAST               'ch'

 L. 597       150  LOAD_STR                 '0'
              152  LOAD_FAST                'ch'
              154  DUP_TOP          
              156  ROT_THREE        
              158  COMPARE_OP               <=
              160  POP_JUMP_IF_FALSE   170  'to 170'
              162  LOAD_STR                 '9'
              164  COMPARE_OP               <=
              166  POP_JUMP_IF_TRUE    240  'to 240'
              168  JUMP_FORWARD        172  'to 172'
            170_0  COME_FROM           160  '160'
              170  POP_TOP          
            172_0  COME_FROM           168  '168'
              172  LOAD_STR                 'A'
              174  LOAD_FAST                'ch'
              176  DUP_TOP          
              178  ROT_THREE        
              180  COMPARE_OP               <=
              182  POP_JUMP_IF_FALSE   192  'to 192'
              184  LOAD_STR                 'Z'
              186  COMPARE_OP               <=
              188  POP_JUMP_IF_TRUE    240  'to 240'
              190  JUMP_FORWARD        194  'to 194'
            192_0  COME_FROM           182  '182'
              192  POP_TOP          
            194_0  COME_FROM           190  '190'
              194  LOAD_STR                 'a'
              196  LOAD_FAST                'ch'
              198  DUP_TOP          
              200  ROT_THREE        
              202  COMPARE_OP               <=
              204  POP_JUMP_IF_FALSE   214  'to 214'
              206  LOAD_STR                 'z'
              208  COMPARE_OP               <=
              210  POP_JUMP_IF_TRUE    240  'to 240'
              212  JUMP_FORWARD        216  'to 216'
            214_0  COME_FROM           204  '204'
              214  POP_TOP          
            216_0  COME_FROM           212  '212'

 L. 598       216  LOAD_FAST                'ch'
              218  LOAD_STR                 "-;/?:@&=+$,_.~*'()[]"
              220  COMPARE_OP               in

 L. 597       222  POP_JUMP_IF_TRUE    240  'to 240'

 L. 599       224  LOAD_FAST                'ch'
              226  LOAD_STR                 '!'
              228  COMPARE_OP               ==

 L. 597       230  POP_JUMP_IF_FALSE   250  'to 250'

 L. 599       232  LOAD_FAST                'handle'
              234  LOAD_STR                 '!'
              236  COMPARE_OP               !=

 L. 597       238  POP_JUMP_IF_FALSE   250  'to 250'
            240_0  COME_FROM           222  '222'
            240_1  COME_FROM           210  '210'
            240_2  COME_FROM           188  '188'
            240_3  COME_FROM           166  '166'

 L. 600       240  LOAD_FAST                'end'
              242  LOAD_CONST               1
              244  INPLACE_ADD      
              246  STORE_FAST               'end'
              248  JUMP_BACK           128  'to 128'
            250_0  COME_FROM           238  '238'
            250_1  COME_FROM           230  '230'

 L. 602       250  LOAD_FAST                'start'
              252  LOAD_FAST                'end'
              254  COMPARE_OP               <
          256_258  POP_JUMP_IF_FALSE   278  'to 278'

 L. 603       260  LOAD_FAST                'chunks'
              262  LOAD_METHOD              append
              264  LOAD_FAST                'suffix'
              266  LOAD_FAST                'start'
              268  LOAD_FAST                'end'
              270  BUILD_SLICE_2         2 
              272  BINARY_SUBSCR    
              274  CALL_METHOD_1         1  ''
              276  POP_TOP          
            278_0  COME_FROM           256  '256'

 L. 604       278  LOAD_FAST                'end'
              280  LOAD_CONST               1
              282  BINARY_ADD       
              284  DUP_TOP          
              286  STORE_FAST               'start'
              288  STORE_FAST               'end'

 L. 605       290  LOAD_FAST                'ch'
              292  LOAD_METHOD              encode
              294  LOAD_STR                 'utf-8'
              296  CALL_METHOD_1         1  ''
              298  STORE_FAST               'data'

 L. 606       300  LOAD_FAST                'data'
              302  GET_ITER         
              304  FOR_ITER            326  'to 326'
              306  STORE_FAST               'ch'

 L. 607       308  LOAD_FAST                'chunks'
              310  LOAD_METHOD              append
              312  LOAD_STR                 '%%%02X'
              314  LOAD_FAST                'ch'
              316  BINARY_MODULO    
              318  CALL_METHOD_1         1  ''
              320  POP_TOP          
          322_324  JUMP_BACK           304  'to 304'
              326  JUMP_BACK           128  'to 128'
            328_0  COME_FROM           138  '138'

 L. 608       328  LOAD_FAST                'start'
              330  LOAD_FAST                'end'
              332  COMPARE_OP               <
          334_336  POP_JUMP_IF_FALSE   356  'to 356'

 L. 609       338  LOAD_FAST                'chunks'
              340  LOAD_METHOD              append
              342  LOAD_FAST                'suffix'
              344  LOAD_FAST                'start'
              346  LOAD_FAST                'end'
              348  BUILD_SLICE_2         2 
              350  BINARY_SUBSCR    
              352  CALL_METHOD_1         1  ''
              354  POP_TOP          
            356_0  COME_FROM           334  '334'

 L. 610       356  LOAD_STR                 ''
              358  LOAD_METHOD              join
              360  LOAD_FAST                'chunks'
              362  CALL_METHOD_1         1  ''
              364  STORE_FAST               'suffix_text'

 L. 611       366  LOAD_FAST                'handle'
          368_370  POP_JUMP_IF_FALSE   384  'to 384'

 L. 612       372  LOAD_STR                 '%s%s'
              374  LOAD_FAST                'handle'
              376  LOAD_FAST                'suffix_text'
              378  BUILD_TUPLE_2         2 
              380  BINARY_MODULO    
              382  RETURN_VALUE     
            384_0  COME_FROM           368  '368'

 L. 614       384  LOAD_STR                 '!<%s>'
              386  LOAD_FAST                'suffix_text'
              388  BINARY_MODULO    
              390  RETURN_VALUE     

Parse error at or near `BINARY_MODULO' instruction at offset 388

    def prepare_anchor(self, anchor):
        if not anchor:
            raise EmitterError('anchor must not be empty')
        for ch in anchor:
            if not '0' <= ch <= '9':
                if not 'A' <= ch <= 'Z':
                    if not 'a' <= ch <= 'z':
                        if not ch in '-_':
                            raise EmitterError('invalid character %r in the anchor: %r' % (
                             ch, anchor))
                        return anchor

    def analyze_scalar--- This code section failed: ---

 L. 629         0  LOAD_FAST                'scalar'
                2  POP_JUMP_IF_TRUE     28  'to 28'

 L. 630         4  LOAD_GLOBAL              ScalarAnalysis
                6  LOAD_FAST                'scalar'
                8  LOAD_CONST               True
               10  LOAD_CONST               False

 L. 631        12  LOAD_CONST               False

 L. 631        14  LOAD_CONST               True

 L. 632        16  LOAD_CONST               True

 L. 632        18  LOAD_CONST               True

 L. 633        20  LOAD_CONST               False

 L. 630        22  LOAD_CONST               ('scalar', 'empty', 'multiline', 'allow_flow_plain', 'allow_block_plain', 'allow_single_quoted', 'allow_double_quoted', 'allow_block')
               24  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
               26  RETURN_VALUE     
             28_0  COME_FROM             2  '2'

 L. 636        28  LOAD_CONST               False
               30  STORE_FAST               'block_indicators'

 L. 637        32  LOAD_CONST               False
               34  STORE_FAST               'flow_indicators'

 L. 638        36  LOAD_CONST               False
               38  STORE_FAST               'line_breaks'

 L. 639        40  LOAD_CONST               False
               42  STORE_FAST               'special_characters'

 L. 642        44  LOAD_CONST               False
               46  STORE_FAST               'leading_space'

 L. 643        48  LOAD_CONST               False
               50  STORE_FAST               'leading_break'

 L. 644        52  LOAD_CONST               False
               54  STORE_FAST               'trailing_space'

 L. 645        56  LOAD_CONST               False
               58  STORE_FAST               'trailing_break'

 L. 646        60  LOAD_CONST               False
               62  STORE_FAST               'break_space'

 L. 647        64  LOAD_CONST               False
               66  STORE_FAST               'space_break'

 L. 650        68  LOAD_FAST                'scalar'
               70  LOAD_METHOD              startswith
               72  LOAD_STR                 '---'
               74  CALL_METHOD_1         1  ''
               76  POP_JUMP_IF_TRUE     88  'to 88'
               78  LOAD_FAST                'scalar'
               80  LOAD_METHOD              startswith
               82  LOAD_STR                 '...'
               84  CALL_METHOD_1         1  ''
               86  POP_JUMP_IF_FALSE    96  'to 96'
             88_0  COME_FROM            76  '76'

 L. 651        88  LOAD_CONST               True
               90  STORE_FAST               'block_indicators'

 L. 652        92  LOAD_CONST               True
               94  STORE_FAST               'flow_indicators'
             96_0  COME_FROM            86  '86'

 L. 655        96  LOAD_CONST               True
               98  STORE_FAST               'preceded_by_whitespace'

 L. 658       100  LOAD_GLOBAL              len
              102  LOAD_FAST                'scalar'
              104  CALL_FUNCTION_1       1  ''
              106  LOAD_CONST               1
              108  COMPARE_OP               ==
              110  JUMP_IF_TRUE_OR_POP   122  'to 122'

 L. 659       112  LOAD_FAST                'scalar'
              114  LOAD_CONST               1
              116  BINARY_SUBSCR    
              118  LOAD_STR                 '\x00 \t\r\n\x85\u2028\u2029'
              120  COMPARE_OP               in
            122_0  COME_FROM           110  '110'

 L. 658       122  STORE_FAST               'followed_by_whitespace'

 L. 662       124  LOAD_CONST               False
              126  STORE_FAST               'previous_space'

 L. 665       128  LOAD_CONST               False
              130  STORE_FAST               'previous_break'

 L. 667       132  LOAD_CONST               0
              134  STORE_FAST               'index'

 L. 668       136  LOAD_FAST                'index'
              138  LOAD_GLOBAL              len
              140  LOAD_FAST                'scalar'
              142  CALL_FUNCTION_1       1  ''
              144  COMPARE_OP               <
          146_148  POP_JUMP_IF_FALSE   648  'to 648'

 L. 669       150  LOAD_FAST                'scalar'
              152  LOAD_FAST                'index'
              154  BINARY_SUBSCR    
              156  STORE_FAST               'ch'

 L. 672       158  LOAD_FAST                'index'
              160  LOAD_CONST               0
              162  COMPARE_OP               ==
              164  POP_JUMP_IF_FALSE   224  'to 224'

 L. 674       166  LOAD_FAST                'ch'
              168  LOAD_STR                 '#,[]{}&*!|>\'"%@`'
              170  COMPARE_OP               in
              172  POP_JUMP_IF_FALSE   182  'to 182'

 L. 675       174  LOAD_CONST               True
              176  STORE_FAST               'flow_indicators'

 L. 676       178  LOAD_CONST               True
              180  STORE_FAST               'block_indicators'
            182_0  COME_FROM           172  '172'

 L. 677       182  LOAD_FAST                'ch'
              184  LOAD_STR                 '?:'
              186  COMPARE_OP               in
              188  POP_JUMP_IF_FALSE   202  'to 202'

 L. 678       190  LOAD_CONST               True
              192  STORE_FAST               'flow_indicators'

 L. 679       194  LOAD_FAST                'followed_by_whitespace'
              196  POP_JUMP_IF_FALSE   202  'to 202'

 L. 680       198  LOAD_CONST               True
              200  STORE_FAST               'block_indicators'
            202_0  COME_FROM           196  '196'
            202_1  COME_FROM           188  '188'

 L. 681       202  LOAD_FAST                'ch'
              204  LOAD_STR                 '-'
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_FALSE   222  'to 222'
              210  LOAD_FAST                'followed_by_whitespace'
              212  POP_JUMP_IF_FALSE   222  'to 222'

 L. 682       214  LOAD_CONST               True
              216  STORE_FAST               'flow_indicators'

 L. 683       218  LOAD_CONST               True
              220  STORE_FAST               'block_indicators'
            222_0  COME_FROM           212  '212'
            222_1  COME_FROM           208  '208'
              222  JUMP_FORWARD        284  'to 284'
            224_0  COME_FROM           164  '164'

 L. 686       224  LOAD_FAST                'ch'
              226  LOAD_STR                 ',?[]{}'
              228  COMPARE_OP               in
              230  POP_JUMP_IF_FALSE   236  'to 236'

 L. 687       232  LOAD_CONST               True
              234  STORE_FAST               'flow_indicators'
            236_0  COME_FROM           230  '230'

 L. 688       236  LOAD_FAST                'ch'
              238  LOAD_STR                 ':'
              240  COMPARE_OP               ==
          242_244  POP_JUMP_IF_FALSE   260  'to 260'

 L. 689       246  LOAD_CONST               True
              248  STORE_FAST               'flow_indicators'

 L. 690       250  LOAD_FAST                'followed_by_whitespace'
          252_254  POP_JUMP_IF_FALSE   260  'to 260'

 L. 691       256  LOAD_CONST               True
              258  STORE_FAST               'block_indicators'
            260_0  COME_FROM           252  '252'
            260_1  COME_FROM           242  '242'

 L. 692       260  LOAD_FAST                'ch'
              262  LOAD_STR                 '#'
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   284  'to 284'
              270  LOAD_FAST                'preceded_by_whitespace'
          272_274  POP_JUMP_IF_FALSE   284  'to 284'

 L. 693       276  LOAD_CONST               True
              278  STORE_FAST               'flow_indicators'

 L. 694       280  LOAD_CONST               True
              282  STORE_FAST               'block_indicators'
            284_0  COME_FROM           272  '272'
            284_1  COME_FROM           266  '266'
            284_2  COME_FROM           222  '222'

 L. 697       284  LOAD_FAST                'ch'
              286  LOAD_STR                 '\n\x85\u2028\u2029'
              288  COMPARE_OP               in
          290_292  POP_JUMP_IF_FALSE   298  'to 298'

 L. 698       294  LOAD_CONST               True
              296  STORE_FAST               'line_breaks'
            298_0  COME_FROM           290  '290'

 L. 699       298  LOAD_FAST                'ch'
              300  LOAD_STR                 '\n'
              302  COMPARE_OP               ==
          304_306  POP_JUMP_IF_TRUE    456  'to 456'
              308  LOAD_STR                 ' '
              310  LOAD_FAST                'ch'
              312  DUP_TOP          
              314  ROT_THREE        
              316  COMPARE_OP               <=
          318_320  POP_JUMP_IF_FALSE   332  'to 332'
              322  LOAD_STR                 '~'
              324  COMPARE_OP               <=
          326_328  POP_JUMP_IF_TRUE    456  'to 456'
              330  JUMP_FORWARD        334  'to 334'
            332_0  COME_FROM           318  '318'
              332  POP_TOP          
            334_0  COME_FROM           330  '330'

 L. 700       334  LOAD_FAST                'ch'
              336  LOAD_STR                 '\x85'
              338  COMPARE_OP               ==
          340_342  POP_JUMP_IF_TRUE    424  'to 424'
              344  LOAD_STR                 '\xa0'
              346  LOAD_FAST                'ch'
              348  DUP_TOP          
              350  ROT_THREE        
              352  COMPARE_OP               <=
          354_356  POP_JUMP_IF_FALSE   368  'to 368'
              358  LOAD_STR                 '\ud7ff'
              360  COMPARE_OP               <=
          362_364  POP_JUMP_IF_TRUE    424  'to 424'
              366  JUMP_FORWARD        370  'to 370'
            368_0  COME_FROM           354  '354'
              368  POP_TOP          
            370_0  COME_FROM           366  '366'

 L. 701       370  LOAD_STR                 '\ue000'

 L. 701       372  LOAD_FAST                'ch'

 L. 700       374  DUP_TOP          
              376  ROT_THREE        
              378  COMPARE_OP               <=
          380_382  POP_JUMP_IF_FALSE   394  'to 394'

 L. 701       384  LOAD_STR                 '�'

 L. 700       386  COMPARE_OP               <=
          388_390  POP_JUMP_IF_TRUE    424  'to 424'
              392  JUMP_FORWARD        396  'to 396'
            394_0  COME_FROM           380  '380'
              394  POP_TOP          
            396_0  COME_FROM           392  '392'

 L. 702       396  LOAD_STR                 '𐀀'

 L. 702       398  LOAD_FAST                'ch'

 L. 700       400  DUP_TOP          
              402  ROT_THREE        
              404  COMPARE_OP               <=
          406_408  POP_JUMP_IF_FALSE   420  'to 420'

 L. 702       410  LOAD_STR                 '\U0010ffff'

 L. 700       412  COMPARE_OP               <
          414_416  POP_JUMP_IF_FALSE   452  'to 452'
              418  JUMP_FORWARD        424  'to 424'
            420_0  COME_FROM           406  '406'
              420  POP_TOP          
              422  JUMP_FORWARD        452  'to 452'
            424_0  COME_FROM           418  '418'
            424_1  COME_FROM           388  '388'
            424_2  COME_FROM           362  '362'
            424_3  COME_FROM           340  '340'

 L. 702       424  LOAD_FAST                'ch'
              426  LOAD_STR                 '\ufeff'
              428  COMPARE_OP               !=

 L. 700   430_432  POP_JUMP_IF_FALSE   452  'to 452'

 L. 703       434  LOAD_CONST               True
              436  STORE_FAST               'unicode_characters'

 L. 704       438  LOAD_FAST                'self'
              440  LOAD_ATTR                allow_unicode
          442_444  POP_JUMP_IF_TRUE    456  'to 456'

 L. 705       446  LOAD_CONST               True
              448  STORE_FAST               'special_characters'
              450  JUMP_FORWARD        456  'to 456'
            452_0  COME_FROM           430  '430'
            452_1  COME_FROM           422  '422'
            452_2  COME_FROM           414  '414'

 L. 707       452  LOAD_CONST               True
              454  STORE_FAST               'special_characters'
            456_0  COME_FROM           450  '450'
            456_1  COME_FROM           442  '442'
            456_2  COME_FROM           326  '326'
            456_3  COME_FROM           304  '304'

 L. 710       456  LOAD_FAST                'ch'
              458  LOAD_STR                 ' '
              460  COMPARE_OP               ==
          462_464  POP_JUMP_IF_FALSE   522  'to 522'

 L. 711       466  LOAD_FAST                'index'
              468  LOAD_CONST               0
              470  COMPARE_OP               ==
          472_474  POP_JUMP_IF_FALSE   480  'to 480'

 L. 712       476  LOAD_CONST               True
              478  STORE_FAST               'leading_space'
            480_0  COME_FROM           472  '472'

 L. 713       480  LOAD_FAST                'index'
              482  LOAD_GLOBAL              len
              484  LOAD_FAST                'scalar'
              486  CALL_FUNCTION_1       1  ''
              488  LOAD_CONST               1
              490  BINARY_SUBTRACT  
              492  COMPARE_OP               ==
          494_496  POP_JUMP_IF_FALSE   502  'to 502'

 L. 714       498  LOAD_CONST               True
              500  STORE_FAST               'trailing_space'
            502_0  COME_FROM           494  '494'

 L. 715       502  LOAD_FAST                'previous_break'
          504_506  POP_JUMP_IF_FALSE   512  'to 512'

 L. 716       508  LOAD_CONST               True
              510  STORE_FAST               'break_space'
            512_0  COME_FROM           504  '504'

 L. 717       512  LOAD_CONST               True
              514  STORE_FAST               'previous_space'

 L. 718       516  LOAD_CONST               False
              518  STORE_FAST               'previous_break'
              520  JUMP_FORWARD        596  'to 596'
            522_0  COME_FROM           462  '462'

 L. 719       522  LOAD_FAST                'ch'
              524  LOAD_STR                 '\n\x85\u2028\u2029'
              526  COMPARE_OP               in
          528_530  POP_JUMP_IF_FALSE   588  'to 588'

 L. 720       532  LOAD_FAST                'index'
              534  LOAD_CONST               0
              536  COMPARE_OP               ==
          538_540  POP_JUMP_IF_FALSE   546  'to 546'

 L. 721       542  LOAD_CONST               True
              544  STORE_FAST               'leading_break'
            546_0  COME_FROM           538  '538'

 L. 722       546  LOAD_FAST                'index'
              548  LOAD_GLOBAL              len
              550  LOAD_FAST                'scalar'
              552  CALL_FUNCTION_1       1  ''
              554  LOAD_CONST               1
              556  BINARY_SUBTRACT  
              558  COMPARE_OP               ==
          560_562  POP_JUMP_IF_FALSE   568  'to 568'

 L. 723       564  LOAD_CONST               True
              566  STORE_FAST               'trailing_break'
            568_0  COME_FROM           560  '560'

 L. 724       568  LOAD_FAST                'previous_space'
          570_572  POP_JUMP_IF_FALSE   578  'to 578'

 L. 725       574  LOAD_CONST               True
              576  STORE_FAST               'space_break'
            578_0  COME_FROM           570  '570'

 L. 726       578  LOAD_CONST               False
              580  STORE_FAST               'previous_space'

 L. 727       582  LOAD_CONST               True
              584  STORE_FAST               'previous_break'
              586  JUMP_FORWARD        596  'to 596'
            588_0  COME_FROM           528  '528'

 L. 729       588  LOAD_CONST               False
              590  STORE_FAST               'previous_space'

 L. 730       592  LOAD_CONST               False
              594  STORE_FAST               'previous_break'
            596_0  COME_FROM           586  '586'
            596_1  COME_FROM           520  '520'

 L. 733       596  LOAD_FAST                'index'
              598  LOAD_CONST               1
              600  INPLACE_ADD      
              602  STORE_FAST               'index'

 L. 734       604  LOAD_FAST                'ch'
              606  LOAD_STR                 '\x00 \t\r\n\x85\u2028\u2029'
              608  COMPARE_OP               in
              610  STORE_FAST               'preceded_by_whitespace'

 L. 735       612  LOAD_FAST                'index'
              614  LOAD_CONST               1
              616  BINARY_ADD       
              618  LOAD_GLOBAL              len
              620  LOAD_FAST                'scalar'
              622  CALL_FUNCTION_1       1  ''
              624  COMPARE_OP               >=
          626_628  JUMP_IF_TRUE_OR_POP   644  'to 644'

 L. 736       630  LOAD_FAST                'scalar'
              632  LOAD_FAST                'index'
              634  LOAD_CONST               1
              636  BINARY_ADD       
              638  BINARY_SUBSCR    
              640  LOAD_STR                 '\x00 \t\r\n\x85\u2028\u2029'
              642  COMPARE_OP               in
            644_0  COME_FROM           626  '626'

 L. 735       644  STORE_FAST               'followed_by_whitespace'
              646  JUMP_BACK           136  'to 136'
            648_0  COME_FROM           146  '146'

 L. 739       648  LOAD_CONST               True
              650  STORE_FAST               'allow_flow_plain'

 L. 740       652  LOAD_CONST               True
              654  STORE_FAST               'allow_block_plain'

 L. 741       656  LOAD_CONST               True
              658  STORE_FAST               'allow_single_quoted'

 L. 742       660  LOAD_CONST               True
              662  STORE_FAST               'allow_double_quoted'

 L. 743       664  LOAD_CONST               True
              666  STORE_FAST               'allow_block'

 L. 746       668  LOAD_FAST                'leading_space'
          670_672  POP_JUMP_IF_TRUE    692  'to 692'
              674  LOAD_FAST                'leading_break'
          676_678  POP_JUMP_IF_TRUE    692  'to 692'

 L. 747       680  LOAD_FAST                'trailing_space'

 L. 746   682_684  POP_JUMP_IF_TRUE    692  'to 692'

 L. 747       686  LOAD_FAST                'trailing_break'

 L. 746   688_690  POP_JUMP_IF_FALSE   700  'to 700'
            692_0  COME_FROM           682  '682'
            692_1  COME_FROM           676  '676'
            692_2  COME_FROM           670  '670'

 L. 748       692  LOAD_CONST               False
              694  DUP_TOP          
              696  STORE_FAST               'allow_flow_plain'
              698  STORE_FAST               'allow_block_plain'
            700_0  COME_FROM           688  '688'

 L. 751       700  LOAD_FAST                'trailing_space'
          702_704  POP_JUMP_IF_FALSE   710  'to 710'

 L. 752       706  LOAD_CONST               False
              708  STORE_FAST               'allow_block'
            710_0  COME_FROM           702  '702'

 L. 756       710  LOAD_FAST                'break_space'
          712_714  POP_JUMP_IF_FALSE   728  'to 728'

 L. 757       716  LOAD_CONST               False
              718  DUP_TOP          
              720  STORE_FAST               'allow_flow_plain'
              722  DUP_TOP          
              724  STORE_FAST               'allow_block_plain'
              726  STORE_FAST               'allow_single_quoted'
            728_0  COME_FROM           712  '712'

 L. 761       728  LOAD_FAST                'space_break'
          730_732  POP_JUMP_IF_TRUE    740  'to 740'
              734  LOAD_FAST                'special_characters'
          736_738  POP_JUMP_IF_FALSE   756  'to 756'
            740_0  COME_FROM           730  '730'

 L. 763       740  LOAD_CONST               False

 L. 762       742  DUP_TOP          
              744  STORE_FAST               'allow_flow_plain'
              746  DUP_TOP          
              748  STORE_FAST               'allow_block_plain'
              750  DUP_TOP          

 L. 763       752  STORE_FAST               'allow_single_quoted'

 L. 763       754  STORE_FAST               'allow_block'
            756_0  COME_FROM           736  '736'

 L. 767       756  LOAD_FAST                'line_breaks'
          758_760  POP_JUMP_IF_FALSE   770  'to 770'

 L. 768       762  LOAD_CONST               False
              764  DUP_TOP          
              766  STORE_FAST               'allow_flow_plain'
              768  STORE_FAST               'allow_block_plain'
            770_0  COME_FROM           758  '758'

 L. 771       770  LOAD_FAST                'flow_indicators'
          772_774  POP_JUMP_IF_FALSE   780  'to 780'

 L. 772       776  LOAD_CONST               False
              778  STORE_FAST               'allow_flow_plain'
            780_0  COME_FROM           772  '772'

 L. 775       780  LOAD_FAST                'block_indicators'
          782_784  POP_JUMP_IF_FALSE   790  'to 790'

 L. 776       786  LOAD_CONST               False
              788  STORE_FAST               'allow_block_plain'
            790_0  COME_FROM           782  '782'

 L. 778       790  LOAD_GLOBAL              ScalarAnalysis
              792  LOAD_FAST                'scalar'

 L. 779       794  LOAD_CONST               False

 L. 779       796  LOAD_FAST                'line_breaks'

 L. 780       798  LOAD_FAST                'allow_flow_plain'

 L. 781       800  LOAD_FAST                'allow_block_plain'

 L. 782       802  LOAD_FAST                'allow_single_quoted'

 L. 783       804  LOAD_FAST                'allow_double_quoted'

 L. 784       806  LOAD_FAST                'allow_block'

 L. 778       808  LOAD_CONST               ('scalar', 'empty', 'multiline', 'allow_flow_plain', 'allow_block_plain', 'allow_single_quoted', 'allow_double_quoted', 'allow_block')
              810  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              812  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 812

    def flush_stream(self):
        if hasattr(self.stream, 'flush'):
            self.stream.flush()

    def write_stream_start(self):
        if self.encoding:
            if self.encoding.startswith('utf-16'):
                self.stream.write('\ufeff'.encode(self.encoding))

    def write_stream_end(self):
        self.flush_stream()

    def write_indicator(self, indicator, need_whitespace, whitespace=False, indention=False):
        if not self.whitespace:
            if not need_whitespace:
                data = indicator
        else:
            data = ' ' + indicator
        self.whitespace = whitespace
        self.indention = self.indention and indention
        self.column += len(data)
        self.open_ended = False
        if self.encoding:
            data = data.encode(self.encoding)
        self.stream.write(data)

    def write_indent--- This code section failed: ---

 L. 815         0  LOAD_FAST                'self'
                2  LOAD_ATTR                indent
                4  JUMP_IF_TRUE_OR_POP     8  'to 8'
                6  LOAD_CONST               0
              8_0  COME_FROM             4  '4'
                8  STORE_FAST               'indent'

 L. 816        10  LOAD_FAST                'self'
               12  LOAD_ATTR                indention
               14  POP_JUMP_IF_FALSE    42  'to 42'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                column
               20  LOAD_FAST                'indent'
               22  COMPARE_OP               >
               24  POP_JUMP_IF_TRUE     42  'to 42'

 L. 817        26  LOAD_FAST                'self'
               28  LOAD_ATTR                column
               30  LOAD_FAST                'indent'
               32  COMPARE_OP               ==

 L. 816        34  POP_JUMP_IF_FALSE    50  'to 50'

 L. 817        36  LOAD_FAST                'self'
               38  LOAD_ATTR                whitespace

 L. 816        40  POP_JUMP_IF_TRUE     50  'to 50'
             42_0  COME_FROM            24  '24'
             42_1  COME_FROM            14  '14'

 L. 818        42  LOAD_FAST                'self'
               44  LOAD_METHOD              write_line_break
               46  CALL_METHOD_0         0  ''
               48  POP_TOP          
             50_0  COME_FROM            40  '40'
             50_1  COME_FROM            34  '34'

 L. 819        50  LOAD_FAST                'self'
               52  LOAD_ATTR                column
               54  LOAD_FAST                'indent'
               56  COMPARE_OP               <
               58  POP_JUMP_IF_FALSE   116  'to 116'

 L. 820        60  LOAD_CONST               True
               62  LOAD_FAST                'self'
               64  STORE_ATTR               whitespace

 L. 821        66  LOAD_STR                 ' '
               68  LOAD_FAST                'indent'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                column
               74  BINARY_SUBTRACT  
               76  BINARY_MULTIPLY  
               78  STORE_FAST               'data'

 L. 822        80  LOAD_FAST                'indent'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               column

 L. 823        86  LOAD_FAST                'self'
               88  LOAD_ATTR                encoding
               90  POP_JUMP_IF_FALSE   104  'to 104'

 L. 824        92  LOAD_FAST                'data'
               94  LOAD_METHOD              encode
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                encoding
              100  CALL_METHOD_1         1  ''
              102  STORE_FAST               'data'
            104_0  COME_FROM            90  '90'

 L. 825       104  LOAD_FAST                'self'
              106  LOAD_ATTR                stream
              108  LOAD_METHOD              write
              110  LOAD_FAST                'data'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
            116_0  COME_FROM            58  '58'

Parse error at or near `POP_TOP' instruction at offset 114

    def write_line_break(self, data=None):
        if data is None:
            data = self.best_line_break
        self.whitespace = True
        self.indention = True
        self.line += 1
        self.column = 0
        if self.encoding:
            data = data.encode(self.encoding)
        self.stream.write(data)

    def write_version_directive(self, version_text):
        data = '%%YAML %s' % version_text
        if self.encoding:
            data = data.encode(self.encoding)
        self.stream.write(data)
        self.write_line_break()

    def write_tag_directive(self, handle_text, prefix_text):
        data = '%%TAG %s %s' % (handle_text, prefix_text)
        if self.encoding:
            data = data.encode(self.encoding)
        self.stream.write(data)
        self.write_line_break()

    def write_single_quoted(self, text, split=True):
        self.write_indicator("'", True)
        spaces = False
        breaks = False
        start = end = 0
        while end <= len(text):
            ch = None
            if end < len(text):
                ch = text[end]
            if spaces and not ch is None:
                if ch != ' ':
                    if start + 1 == end and self.column > self.best_width and split and start != 0 and end != len(text):
                        self.write_indent()
                    else:
                        data = text[start:end]
                        self.column += len(data)
                        if self.encoding:
                            data = data.encode(self.encoding)
                        self.stream.write(data)
                    start = end
            else:
                pass
            if not breaks or ch is None or ch not in '\n\x85\u2028\u2029':
                if text[start] == '\n':
                    self.write_line_break()
                for br in text[start:end]:
                    if br == '\n':
                        self.write_line_break()
                    else:
                        self.write_line_break(br)
                else:
                    self.write_indent()
                    start = end

            else:
                pass
            if not ch is None:
                if ch in ' \n\x85\u2028\u2029' or ch == "'":
                    if start < end:
                        data = text[start:end]
                        self.column += len(data)
                        if self.encoding:
                            data = data.encode(self.encoding)
                        self.stream.write(data)
                        start = end
                if ch == "'":
                    data = "''"
                    self.column += 2
                    if self.encoding:
                        data = data.encode(self.encoding)
                    self.stream.write(data)
                    start = end + 1
                if ch is not None:
                    spaces = ch == ' '
                    breaks = ch in '\n\x85\u2028\u2029'
                end += 1

        self.write_indicator("'", False)

    ESCAPE_REPLACEMENTS = {'\x00':'0', 
     '\x07':'a', 
     '\x08':'b', 
     '\t':'t', 
     '\n':'n', 
     '\x0b':'v', 
     '\x0c':'f', 
     '\r':'r', 
     '\x1b':'e', 
     '"':'"', 
     '\\':'\\', 
     '\x85':'N', 
     '\xa0':'_', 
     '\u2028':'L', 
     '\u2029':'P'}

    def write_double_quoted--- This code section failed: ---

 L. 927         0  LOAD_FAST                'self'
                2  LOAD_METHOD              write_indicator
                4  LOAD_STR                 '"'
                6  LOAD_CONST               True
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 928        12  LOAD_CONST               0
               14  DUP_TOP          
               16  STORE_FAST               'start'
               18  STORE_FAST               'end'

 L. 929        20  LOAD_FAST                'end'
               22  LOAD_GLOBAL              len
               24  LOAD_FAST                'text'
               26  CALL_FUNCTION_1       1  ''
               28  COMPARE_OP               <=
            30_32  POP_JUMP_IF_FALSE   642  'to 642'

 L. 930        34  LOAD_CONST               None
               36  STORE_FAST               'ch'

 L. 931        38  LOAD_FAST                'end'
               40  LOAD_GLOBAL              len
               42  LOAD_FAST                'text'
               44  CALL_FUNCTION_1       1  ''
               46  COMPARE_OP               <
               48  POP_JUMP_IF_FALSE    58  'to 58'

 L. 932        50  LOAD_FAST                'text'
               52  LOAD_FAST                'end'
               54  BINARY_SUBSCR    
               56  STORE_FAST               'ch'
             58_0  COME_FROM            48  '48'

 L. 933        58  LOAD_FAST                'ch'
               60  LOAD_CONST               None
               62  COMPARE_OP               is
               64  POP_JUMP_IF_TRUE    152  'to 152'
               66  LOAD_FAST                'ch'
               68  LOAD_STR                 '"\\\x85\u2028\u2029\ufeff'
               70  COMPARE_OP               in
               72  POP_JUMP_IF_TRUE    152  'to 152'

 L. 934        74  LOAD_STR                 ' '

 L. 934        76  LOAD_FAST                'ch'

 L. 933        78  DUP_TOP          
               80  ROT_THREE        
               82  COMPARE_OP               <=
               84  POP_JUMP_IF_FALSE    96  'to 96'

 L. 934        86  LOAD_STR                 '~'

 L. 933        88  COMPARE_OP               <=
            90_92  POP_JUMP_IF_TRUE    380  'to 380'
               94  JUMP_FORWARD         98  'to 98'
             96_0  COME_FROM            84  '84'
               96  POP_TOP          
             98_0  COME_FROM            94  '94'

 L. 935        98  LOAD_FAST                'self'
              100  LOAD_ATTR                allow_unicode

 L. 933       102  POP_JUMP_IF_FALSE   152  'to 152'

 L. 936       104  LOAD_STR                 '\xa0'

 L. 936       106  LOAD_FAST                'ch'

 L. 933       108  DUP_TOP          
              110  ROT_THREE        
              112  COMPARE_OP               <=
              114  POP_JUMP_IF_FALSE   126  'to 126'

 L. 936       116  LOAD_STR                 '\ud7ff'

 L. 933       118  COMPARE_OP               <=
          120_122  POP_JUMP_IF_TRUE    380  'to 380'
              124  JUMP_FORWARD        128  'to 128'
            126_0  COME_FROM           114  '114'
              126  POP_TOP          
            128_0  COME_FROM           124  '124'

 L. 937       128  LOAD_STR                 '\ue000'

 L. 937       130  LOAD_FAST                'ch'

 L. 933       132  DUP_TOP          
              134  ROT_THREE        
              136  COMPARE_OP               <=
              138  POP_JUMP_IF_FALSE   150  'to 150'

 L. 937       140  LOAD_STR                 '�'

 L. 933       142  COMPARE_OP               <=
          144_146  POP_JUMP_IF_TRUE    380  'to 380'
              148  JUMP_FORWARD        152  'to 152'
            150_0  COME_FROM           138  '138'
              150  POP_TOP          
            152_0  COME_FROM           148  '148'
            152_1  COME_FROM           102  '102'
            152_2  COME_FROM            72  '72'
            152_3  COME_FROM            64  '64'

 L. 938       152  LOAD_FAST                'start'
              154  LOAD_FAST                'end'
              156  COMPARE_OP               <
              158  POP_JUMP_IF_FALSE   224  'to 224'

 L. 939       160  LOAD_FAST                'text'
              162  LOAD_FAST                'start'
              164  LOAD_FAST                'end'
              166  BUILD_SLICE_2         2 
              168  BINARY_SUBSCR    
              170  STORE_FAST               'data'

 L. 940       172  LOAD_FAST                'self'
              174  DUP_TOP          
              176  LOAD_ATTR                column
              178  LOAD_GLOBAL              len
              180  LOAD_FAST                'data'
              182  CALL_FUNCTION_1       1  ''
              184  INPLACE_ADD      
              186  ROT_TWO          
              188  STORE_ATTR               column

 L. 941       190  LOAD_FAST                'self'
              192  LOAD_ATTR                encoding
              194  POP_JUMP_IF_FALSE   208  'to 208'

 L. 942       196  LOAD_FAST                'data'
              198  LOAD_METHOD              encode
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                encoding
              204  CALL_METHOD_1         1  ''
              206  STORE_FAST               'data'
            208_0  COME_FROM           194  '194'

 L. 943       208  LOAD_FAST                'self'
              210  LOAD_ATTR                stream
              212  LOAD_METHOD              write
              214  LOAD_FAST                'data'
              216  CALL_METHOD_1         1  ''
              218  POP_TOP          

 L. 944       220  LOAD_FAST                'end'
              222  STORE_FAST               'start'
            224_0  COME_FROM           158  '158'

 L. 945       224  LOAD_FAST                'ch'
              226  LOAD_CONST               None
              228  COMPARE_OP               is-not
          230_232  POP_JUMP_IF_FALSE   380  'to 380'

 L. 946       234  LOAD_FAST                'ch'
              236  LOAD_FAST                'self'
              238  LOAD_ATTR                ESCAPE_REPLACEMENTS
              240  COMPARE_OP               in
          242_244  POP_JUMP_IF_FALSE   262  'to 262'

 L. 947       246  LOAD_STR                 '\\'
              248  LOAD_FAST                'self'
              250  LOAD_ATTR                ESCAPE_REPLACEMENTS
              252  LOAD_FAST                'ch'
              254  BINARY_SUBSCR    
              256  BINARY_ADD       
              258  STORE_FAST               'data'
              260  JUMP_FORWARD        322  'to 322'
            262_0  COME_FROM           242  '242'

 L. 948       262  LOAD_FAST                'ch'
              264  LOAD_STR                 'ÿ'
              266  COMPARE_OP               <=
          268_270  POP_JUMP_IF_FALSE   286  'to 286'

 L. 949       272  LOAD_STR                 '\\x%02X'
              274  LOAD_GLOBAL              ord
              276  LOAD_FAST                'ch'
              278  CALL_FUNCTION_1       1  ''
              280  BINARY_MODULO    
              282  STORE_FAST               'data'
              284  JUMP_FORWARD        322  'to 322'
            286_0  COME_FROM           268  '268'

 L. 950       286  LOAD_FAST                'ch'
              288  LOAD_STR                 '\uffff'
              290  COMPARE_OP               <=
          292_294  POP_JUMP_IF_FALSE   310  'to 310'

 L. 951       296  LOAD_STR                 '\\u%04X'
              298  LOAD_GLOBAL              ord
              300  LOAD_FAST                'ch'
              302  CALL_FUNCTION_1       1  ''
              304  BINARY_MODULO    
              306  STORE_FAST               'data'
              308  JUMP_FORWARD        322  'to 322'
            310_0  COME_FROM           292  '292'

 L. 953       310  LOAD_STR                 '\\U%08X'
              312  LOAD_GLOBAL              ord
              314  LOAD_FAST                'ch'
              316  CALL_FUNCTION_1       1  ''
              318  BINARY_MODULO    
              320  STORE_FAST               'data'
            322_0  COME_FROM           308  '308'
            322_1  COME_FROM           284  '284'
            322_2  COME_FROM           260  '260'

 L. 954       322  LOAD_FAST                'self'
              324  DUP_TOP          
              326  LOAD_ATTR                column
              328  LOAD_GLOBAL              len
              330  LOAD_FAST                'data'
              332  CALL_FUNCTION_1       1  ''
              334  INPLACE_ADD      
              336  ROT_TWO          
              338  STORE_ATTR               column

 L. 955       340  LOAD_FAST                'self'
              342  LOAD_ATTR                encoding
          344_346  POP_JUMP_IF_FALSE   360  'to 360'

 L. 956       348  LOAD_FAST                'data'
              350  LOAD_METHOD              encode
              352  LOAD_FAST                'self'
              354  LOAD_ATTR                encoding
              356  CALL_METHOD_1         1  ''
              358  STORE_FAST               'data'
            360_0  COME_FROM           344  '344'

 L. 957       360  LOAD_FAST                'self'
              362  LOAD_ATTR                stream
              364  LOAD_METHOD              write
              366  LOAD_FAST                'data'
              368  CALL_METHOD_1         1  ''
              370  POP_TOP          

 L. 958       372  LOAD_FAST                'end'
              374  LOAD_CONST               1
              376  BINARY_ADD       
              378  STORE_FAST               'start'
            380_0  COME_FROM           230  '230'
            380_1  COME_FROM           144  '144'
            380_2  COME_FROM           120  '120'
            380_3  COME_FROM            90  '90'

 L. 959       380  LOAD_CONST               0
              382  LOAD_FAST                'end'
              384  DUP_TOP          
              386  ROT_THREE        
              388  COMPARE_OP               <
          390_392  POP_JUMP_IF_FALSE   412  'to 412'
              394  LOAD_GLOBAL              len
              396  LOAD_FAST                'text'
              398  CALL_FUNCTION_1       1  ''
              400  LOAD_CONST               1
              402  BINARY_SUBTRACT  
              404  COMPARE_OP               <
          406_408  POP_JUMP_IF_FALSE   632  'to 632'
              410  JUMP_FORWARD        416  'to 416'
            412_0  COME_FROM           390  '390'
              412  POP_TOP          
              414  JUMP_FORWARD        632  'to 632'
            416_0  COME_FROM           410  '410'
              416  LOAD_FAST                'ch'
              418  LOAD_STR                 ' '
              420  COMPARE_OP               ==
          422_424  POP_JUMP_IF_TRUE    436  'to 436'
              426  LOAD_FAST                'start'
              428  LOAD_FAST                'end'
              430  COMPARE_OP               >=
          432_434  POP_JUMP_IF_FALSE   632  'to 632'
            436_0  COME_FROM           422  '422'

 L. 960       436  LOAD_FAST                'self'
              438  LOAD_ATTR                column
              440  LOAD_FAST                'end'
              442  LOAD_FAST                'start'
              444  BINARY_SUBTRACT  
              446  BINARY_ADD       
              448  LOAD_FAST                'self'
              450  LOAD_ATTR                best_width
              452  COMPARE_OP               >

 L. 959   454_456  POP_JUMP_IF_FALSE   632  'to 632'

 L. 960       458  LOAD_FAST                'split'

 L. 959   460_462  POP_JUMP_IF_FALSE   632  'to 632'

 L. 961       464  LOAD_FAST                'text'
              466  LOAD_FAST                'start'
              468  LOAD_FAST                'end'
              470  BUILD_SLICE_2         2 
              472  BINARY_SUBSCR    
              474  LOAD_STR                 '\\'
              476  BINARY_ADD       
              478  STORE_FAST               'data'

 L. 962       480  LOAD_FAST                'start'
              482  LOAD_FAST                'end'
              484  COMPARE_OP               <
          486_488  POP_JUMP_IF_FALSE   494  'to 494'

 L. 963       490  LOAD_FAST                'end'
              492  STORE_FAST               'start'
            494_0  COME_FROM           486  '486'

 L. 964       494  LOAD_FAST                'self'
              496  DUP_TOP          
              498  LOAD_ATTR                column
              500  LOAD_GLOBAL              len
              502  LOAD_FAST                'data'
              504  CALL_FUNCTION_1       1  ''
              506  INPLACE_ADD      
              508  ROT_TWO          
              510  STORE_ATTR               column

 L. 965       512  LOAD_FAST                'self'
              514  LOAD_ATTR                encoding
          516_518  POP_JUMP_IF_FALSE   532  'to 532'

 L. 966       520  LOAD_FAST                'data'
              522  LOAD_METHOD              encode
              524  LOAD_FAST                'self'
              526  LOAD_ATTR                encoding
              528  CALL_METHOD_1         1  ''
              530  STORE_FAST               'data'
            532_0  COME_FROM           516  '516'

 L. 967       532  LOAD_FAST                'self'
              534  LOAD_ATTR                stream
              536  LOAD_METHOD              write
              538  LOAD_FAST                'data'
              540  CALL_METHOD_1         1  ''
              542  POP_TOP          

 L. 968       544  LOAD_FAST                'self'
              546  LOAD_METHOD              write_indent
              548  CALL_METHOD_0         0  ''
              550  POP_TOP          

 L. 969       552  LOAD_CONST               False
              554  LOAD_FAST                'self'
              556  STORE_ATTR               whitespace

 L. 970       558  LOAD_CONST               False
              560  LOAD_FAST                'self'
              562  STORE_ATTR               indention

 L. 971       564  LOAD_FAST                'text'
              566  LOAD_FAST                'start'
              568  BINARY_SUBSCR    
              570  LOAD_STR                 ' '
              572  COMPARE_OP               ==
          574_576  POP_JUMP_IF_FALSE   632  'to 632'

 L. 972       578  LOAD_STR                 '\\'
              580  STORE_FAST               'data'

 L. 973       582  LOAD_FAST                'self'
              584  DUP_TOP          
              586  LOAD_ATTR                column
              588  LOAD_GLOBAL              len
              590  LOAD_FAST                'data'
              592  CALL_FUNCTION_1       1  ''
              594  INPLACE_ADD      
              596  ROT_TWO          
              598  STORE_ATTR               column

 L. 974       600  LOAD_FAST                'self'
              602  LOAD_ATTR                encoding
          604_606  POP_JUMP_IF_FALSE   620  'to 620'

 L. 975       608  LOAD_FAST                'data'
              610  LOAD_METHOD              encode
              612  LOAD_FAST                'self'
              614  LOAD_ATTR                encoding
              616  CALL_METHOD_1         1  ''
              618  STORE_FAST               'data'
            620_0  COME_FROM           604  '604'

 L. 976       620  LOAD_FAST                'self'
              622  LOAD_ATTR                stream
              624  LOAD_METHOD              write
              626  LOAD_FAST                'data'
              628  CALL_METHOD_1         1  ''
              630  POP_TOP          
            632_0  COME_FROM           574  '574'
            632_1  COME_FROM           460  '460'
            632_2  COME_FROM           454  '454'
            632_3  COME_FROM           432  '432'
            632_4  COME_FROM           414  '414'
            632_5  COME_FROM           406  '406'

 L. 977       632  LOAD_FAST                'end'
              634  LOAD_CONST               1
              636  INPLACE_ADD      
              638  STORE_FAST               'end'
              640  JUMP_BACK            20  'to 20'
            642_0  COME_FROM            30  '30'

 L. 978       642  LOAD_FAST                'self'
              644  LOAD_METHOD              write_indicator
              646  LOAD_STR                 '"'
              648  LOAD_CONST               False
              650  CALL_METHOD_2         2  ''
              652  POP_TOP          

Parse error at or near `CALL_METHOD_2' instruction at offset 650

    def determine_block_hints(self, text):
        hints = ''
        if text:
            if text[0] in ' \n\x85\u2028\u2029':
                hints += str(self.best_indent)
            elif text[(-1)] not in '\n\x85\u2028\u2029':
                hints += '-'
            else:
                if len(text) == 1 or text[(-2)] in '\n\x85\u2028\u2029':
                    hints += '+'
        return hints

    def write_folded(self, text):
        hints = self.determine_block_hints(text)
        self.write_indicator('>' + hints, True)
        if hints[-1:] == '+':
            self.open_ended = True
        else:
            self.write_line_break()
            leading_space = True
            spaces = False
            breaks = True
            start = end = 0
            while end <= len(text):
                ch = None
                if end < len(text):
                    ch = text[end]
                if breaks and not ch is None:
                    if ch not in '\n\x85\u2028\u2029':
                        if not leading_space:
                            if ch is not None:
                                if ch != ' ':
                                    if text[start] == '\n':
                                        self.write_line_break()
                        leading_space = ch == ' '
                        for br in text[start:end]:
                            if br == '\n':
                                self.write_line_break()
                            else:
                                self.write_line_break(br)
                        else:
                            if ch is not None:
                                self.write_indent()
                            start = end

                else:
                    if spaces:
                        if ch != ' ':
                            if start + 1 == end and self.column > self.best_width:
                                self.write_indent()
                            else:
                                data = text[start:end]
                                self.column += len(data)
                                if self.encoding:
                                    data = data.encode(self.encoding)
                                self.stream.write(data)
                            start = end
                    else:
                        if ch is None or ch in ' \n\x85\u2028\u2029':
                            data = text[start:end]
                            self.column += len(data)
                            if self.encoding:
                                data = data.encode(self.encoding)
                            self.stream.write(data)
                            if ch is None:
                                self.write_line_break()
                            start = end
                    if ch is not None:
                        breaks = ch in '\n\x85\u2028\u2029'
                        spaces = ch == ' '
                    end += 1

    def write_literal(self, text):
        hints = self.determine_block_hints(text)
        self.write_indicator('|' + hints, True)
        if hints[-1:] == '+':
            self.open_ended = True
        else:
            self.write_line_break()
            breaks = True
            start = end = 0
            while True:
                if end <= len(text):
                    ch = None
                    if end < len(text):
                        ch = text[end]
                    if breaks:
                        if ch is None or ch not in '\n\x85\u2028\u2029':
                            for br in text[start:end]:
                                if br == '\n':
                                    self.write_line_break()
                                else:
                                    self.write_line_break(br)

                            if ch is not None:
                                self.write_indent()
                    else:
                        start = end
                else:
                    if ch is None or ch in '\n\x85\u2028\u2029':
                        data = text[start:end]
                        if self.encoding:
                            data = data.encode(self.encoding)
                        self.stream.write(data)
                        if ch is None:
                            self.write_line_break()
                        start = end
                    if ch is not None:
                        breaks = ch in '\n\x85\u2028\u2029'
                    end += 1

    def write_plain(self, text, split=True):
        if self.root_context:
            self.open_ended = True
        else:
            if not text:
                return
            if not self.whitespace:
                data = ' '
                self.column += len(data)
                if self.encoding:
                    data = data.encode(self.encoding)
                self.stream.write(data)
            self.whitespace = False
            self.indention = False
            spaces = False
            breaks = False
            start = end = 0
            while True:
                if end <= len(text):
                    ch = None
                    if end < len(text):
                        ch = text[end]
                    elif spaces:
                        if ch != ' ':
                            if start + 1 == end and self.column > self.best_width and split:
                                self.write_indent()
                                self.whitespace = False
                                self.indention = False
                            else:
                                data = text[start:end]
                                self.column += len(data)
                                if self.encoding:
                                    data = data.encode(self.encoding)
                                self.stream.write(data)
                            start = end
                    elif breaks:
                        if ch not in '\n\x85\u2028\u2029':
                            if text[start] == '\n':
                                self.write_line_break()
                            for br in text[start:end]:
                                if br == '\n':
                                    self.write_line_break()
                                else:
                                    self.write_line_break(br)
                            else:
                                self.write_indent()
                                self.whitespace = False
                                self.indention = False
                                start = end

                    elif ch is None or ch in ' \n\x85\u2028\u2029':
                        data = text[start:end]
                        self.column += len(data)
                        if self.encoding:
                            data = data.encode(self.encoding)
                        self.stream.write(data)
                        start = end
                    if ch is not None:
                        spaces = ch == ' '
                        breaks = ch in '\n\x85\u2028\u2029'
                    end += 1