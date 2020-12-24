# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-target-g7omgaxk/lib/python/yaml/emitter.py
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
            elif isinstance(event, (DocumentEndEvent, CollectionEndEvent)):
                level -= 1
            elif isinstance(event, StreamEndEvent):
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
        if not isinstance(self.event, DocumentStartEvent) or self.event.version or self.event.tags:
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
              140  POP_JUMP_IF_FALSE   152  'to 152'
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
              200  POP_JUMP_IF_FALSE   212  'to 212'
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
              234  RAISE_VARARGS_1       1  ''
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
        elif not self.canonical:
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
        if not first:
            if isinstance(self.event, SequenceEndEvent):
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
        if not first:
            if isinstance(self.event, MappingEndEvent):
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
        return isinstance(self.event, DocumentStartEvent) and self.events or 
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
        return length < 128 and (isinstance(self.event, AliasEvent) or )

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
        if self.event.implicit[0]:
            if tag is None:
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
                    return self.simple_key_context and self.analysis.multiline or 
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
            elif self.style == "'":
                self.write_single_quoted(self.analysis.scalar, split)
            elif self.style == '>':
                self.write_folded(self.analysis.scalar)
            elif self.style == '|':
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
                        assert ch in '-_', 'invalid character %r in the tag handle: %r' % (
                         ch, handle)

        return handle

    def prepare_tag_prefix--- This code section failed: ---

 L. 558         0  LOAD_FAST                'prefix'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L. 559         4  LOAD_GLOBAL              EmitterError
                6  LOAD_STR                 'tag prefix must not be empty'
                8  CALL_FUNCTION_1       1  ''
               10  RAISE_VARARGS_1       1  ''
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

 L. 564        40  SETUP_LOOP          230  'to 230'
               42  LOAD_FAST                'end'
               44  LOAD_GLOBAL              len
               46  LOAD_FAST                'prefix'
               48  CALL_FUNCTION_1       1  ''
               50  COMPARE_OP               <
               52  POP_JUMP_IF_FALSE   228  'to 228'

 L. 565        54  LOAD_FAST                'prefix'
               56  LOAD_FAST                'end'
               58  BINARY_SUBSCR    
               60  STORE_FAST               'ch'

 L. 566        62  LOAD_STR                 '0'
               64  LOAD_FAST                'ch'
               66  DUP_TOP          
               68  ROT_THREE        
               70  COMPARE_OP               <=
               72  POP_JUMP_IF_FALSE    82  'to 82'
               74  LOAD_STR                 '9'
               76  COMPARE_OP               <=
               78  POP_JUMP_IF_TRUE    136  'to 136'
               80  JUMP_FORWARD         84  'to 84'
             82_0  COME_FROM            72  '72'
               82  POP_TOP          
             84_0  COME_FROM            80  '80'
               84  LOAD_STR                 'A'
               86  LOAD_FAST                'ch'
               88  DUP_TOP          
               90  ROT_THREE        
               92  COMPARE_OP               <=
               94  POP_JUMP_IF_FALSE   104  'to 104'
               96  LOAD_STR                 'Z'
               98  COMPARE_OP               <=
              100  POP_JUMP_IF_TRUE    136  'to 136'
              102  JUMP_FORWARD        106  'to 106'
            104_0  COME_FROM            94  '94'
              104  POP_TOP          
            106_0  COME_FROM           102  '102'
              106  LOAD_STR                 'a'
              108  LOAD_FAST                'ch'
              110  DUP_TOP          
              112  ROT_THREE        
              114  COMPARE_OP               <=
              116  POP_JUMP_IF_FALSE   126  'to 126'
              118  LOAD_STR                 'z'
              120  COMPARE_OP               <=
              122  POP_JUMP_IF_TRUE    136  'to 136'
              124  JUMP_FORWARD        128  'to 128'
            126_0  COME_FROM           116  '116'
              126  POP_TOP          
            128_0  COME_FROM           124  '124'

 L. 567       128  LOAD_FAST                'ch'
              130  LOAD_STR                 "-;/?!:@&=+$,_.~*'()[]"
              132  COMPARE_OP               in
              134  POP_JUMP_IF_FALSE   146  'to 146'
            136_0  COME_FROM           122  '122'
            136_1  COME_FROM           100  '100'
            136_2  COME_FROM            78  '78'

 L. 568       136  LOAD_FAST                'end'
              138  LOAD_CONST               1
              140  INPLACE_ADD      
              142  STORE_FAST               'end'
              144  JUMP_BACK            42  'to 42'
            146_0  COME_FROM           134  '134'

 L. 570       146  LOAD_FAST                'start'
              148  LOAD_FAST                'end'
              150  COMPARE_OP               <
              152  POP_JUMP_IF_FALSE   172  'to 172'

 L. 571       154  LOAD_FAST                'chunks'
              156  LOAD_METHOD              append
              158  LOAD_FAST                'prefix'
              160  LOAD_FAST                'start'
              162  LOAD_FAST                'end'
              164  BUILD_SLICE_2         2 
              166  BINARY_SUBSCR    
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          
            172_0  COME_FROM           152  '152'

 L. 572       172  LOAD_FAST                'end'
              174  LOAD_CONST               1
              176  BINARY_ADD       
              178  DUP_TOP          
              180  STORE_FAST               'start'
              182  STORE_FAST               'end'

 L. 573       184  LOAD_FAST                'ch'
              186  LOAD_METHOD              encode
              188  LOAD_STR                 'utf-8'
              190  CALL_METHOD_1         1  ''
              192  STORE_FAST               'data'

 L. 574       194  SETUP_LOOP          226  'to 226'
              196  LOAD_FAST                'data'
              198  GET_ITER         
              200  FOR_ITER            224  'to 224'
              202  STORE_FAST               'ch'

 L. 575       204  LOAD_FAST                'chunks'
              206  LOAD_METHOD              append
              208  LOAD_STR                 '%%%02X'
              210  LOAD_GLOBAL              ord
              212  LOAD_FAST                'ch'
              214  CALL_FUNCTION_1       1  ''
              216  BINARY_MODULO    
              218  CALL_METHOD_1         1  ''
              220  POP_TOP          
              222  JUMP_BACK           200  'to 200'
              224  POP_BLOCK        
            226_0  COME_FROM_LOOP      194  '194'
              226  JUMP_BACK            42  'to 42'
            228_0  COME_FROM            52  '52'
              228  POP_BLOCK        
            230_0  COME_FROM_LOOP       40  '40'

 L. 576       230  LOAD_FAST                'start'
              232  LOAD_FAST                'end'
              234  COMPARE_OP               <
          236_238  POP_JUMP_IF_FALSE   258  'to 258'

 L. 577       240  LOAD_FAST                'chunks'
              242  LOAD_METHOD              append
              244  LOAD_FAST                'prefix'
              246  LOAD_FAST                'start'
              248  LOAD_FAST                'end'
              250  BUILD_SLICE_2         2 
              252  BINARY_SUBSCR    
              254  CALL_METHOD_1         1  ''
              256  POP_TOP          
            258_0  COME_FROM           236  '236'

 L. 578       258  LOAD_STR                 ''
              260  LOAD_METHOD              join
              262  LOAD_FAST                'chunks'
              264  CALL_METHOD_1         1  ''
              266  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 226

    def prepare_tag--- This code section failed: ---

 L. 581         0  LOAD_FAST                'tag'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L. 582         4  LOAD_GLOBAL              EmitterError
                6  LOAD_STR                 'tag must not be empty'
                8  CALL_FUNCTION_1       1  ''
               10  RAISE_VARARGS_1       1  ''
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

 L. 588        46  SETUP_LOOP          120  'to 120'
               48  LOAD_FAST                'prefixes'
               50  GET_ITER         
             52_0  COME_FROM            88  '88'
             52_1  COME_FROM            64  '64'
               52  FOR_ITER            118  'to 118'
               54  STORE_FAST               'prefix'

 L. 589        56  LOAD_FAST                'tag'
               58  LOAD_METHOD              startswith
               60  LOAD_FAST                'prefix'
               62  CALL_METHOD_1         1  ''
               64  POP_JUMP_IF_FALSE    52  'to 52'

 L. 590        66  LOAD_FAST                'prefix'
               68  LOAD_STR                 '!'
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_TRUE     90  'to 90'
               74  LOAD_GLOBAL              len
               76  LOAD_FAST                'prefix'
               78  CALL_FUNCTION_1       1  ''
               80  LOAD_GLOBAL              len
               82  LOAD_FAST                'tag'
               84  CALL_FUNCTION_1       1  ''
               86  COMPARE_OP               <
               88  POP_JUMP_IF_FALSE    52  'to 52'
             90_0  COME_FROM            72  '72'

 L. 591        90  LOAD_FAST                'self'
               92  LOAD_ATTR                tag_prefixes
               94  LOAD_FAST                'prefix'
               96  BINARY_SUBSCR    
               98  STORE_FAST               'handle'

 L. 592       100  LOAD_FAST                'tag'
              102  LOAD_GLOBAL              len
              104  LOAD_FAST                'prefix'
              106  CALL_FUNCTION_1       1  ''
              108  LOAD_CONST               None
              110  BUILD_SLICE_2         2 
              112  BINARY_SUBSCR    
              114  STORE_FAST               'suffix'
              116  JUMP_BACK            52  'to 52'
              118  POP_BLOCK        
            120_0  COME_FROM_LOOP       46  '46'

 L. 593       120  BUILD_LIST_0          0 
              122  STORE_FAST               'chunks'

 L. 594       124  LOAD_CONST               0
              126  DUP_TOP          
              128  STORE_FAST               'start'
              130  STORE_FAST               'end'

 L. 595       132  SETUP_LOOP          344  'to 344'
              134  LOAD_FAST                'end'
              136  LOAD_GLOBAL              len
              138  LOAD_FAST                'suffix'
              140  CALL_FUNCTION_1       1  ''
              142  COMPARE_OP               <
          144_146  POP_JUMP_IF_FALSE   342  'to 342'

 L. 596       148  LOAD_FAST                'suffix'
              150  LOAD_FAST                'end'
              152  BINARY_SUBSCR    
              154  STORE_FAST               'ch'

 L. 597       156  LOAD_STR                 '0'
              158  LOAD_FAST                'ch'
              160  DUP_TOP          
              162  ROT_THREE        
              164  COMPARE_OP               <=
              166  POP_JUMP_IF_FALSE   176  'to 176'
              168  LOAD_STR                 '9'
              170  COMPARE_OP               <=
              172  POP_JUMP_IF_TRUE    250  'to 250'
              174  JUMP_FORWARD        178  'to 178'
            176_0  COME_FROM           166  '166'
              176  POP_TOP          
            178_0  COME_FROM           174  '174'
              178  LOAD_STR                 'A'
              180  LOAD_FAST                'ch'
              182  DUP_TOP          
              184  ROT_THREE        
              186  COMPARE_OP               <=
              188  POP_JUMP_IF_FALSE   198  'to 198'
              190  LOAD_STR                 'Z'
              192  COMPARE_OP               <=
              194  POP_JUMP_IF_TRUE    250  'to 250'
              196  JUMP_FORWARD        200  'to 200'
            198_0  COME_FROM           188  '188'
              198  POP_TOP          
            200_0  COME_FROM           196  '196'
              200  LOAD_STR                 'a'
              202  LOAD_FAST                'ch'
              204  DUP_TOP          
              206  ROT_THREE        
              208  COMPARE_OP               <=
              210  POP_JUMP_IF_FALSE   220  'to 220'
              212  LOAD_STR                 'z'
              214  COMPARE_OP               <=
              216  POP_JUMP_IF_TRUE    250  'to 250'
              218  JUMP_FORWARD        222  'to 222'
            220_0  COME_FROM           210  '210'
              220  POP_TOP          
            222_0  COME_FROM           218  '218'

 L. 598       222  LOAD_FAST                'ch'
              224  LOAD_STR                 "-;/?:@&=+$,_.~*'()[]"
              226  COMPARE_OP               in
              228  POP_JUMP_IF_TRUE    250  'to 250'

 L. 599       230  LOAD_FAST                'ch'
              232  LOAD_STR                 '!'
              234  COMPARE_OP               ==
          236_238  POP_JUMP_IF_FALSE   260  'to 260'
              240  LOAD_FAST                'handle'
              242  LOAD_STR                 '!'
              244  COMPARE_OP               !=
          246_248  POP_JUMP_IF_FALSE   260  'to 260'
            250_0  COME_FROM           228  '228'
            250_1  COME_FROM           216  '216'
            250_2  COME_FROM           194  '194'
            250_3  COME_FROM           172  '172'

 L. 600       250  LOAD_FAST                'end'
              252  LOAD_CONST               1
              254  INPLACE_ADD      
              256  STORE_FAST               'end'
              258  JUMP_BACK           134  'to 134'
            260_0  COME_FROM           246  '246'
            260_1  COME_FROM           236  '236'

 L. 602       260  LOAD_FAST                'start'
              262  LOAD_FAST                'end'
              264  COMPARE_OP               <
          266_268  POP_JUMP_IF_FALSE   288  'to 288'

 L. 603       270  LOAD_FAST                'chunks'
              272  LOAD_METHOD              append
              274  LOAD_FAST                'suffix'
              276  LOAD_FAST                'start'
              278  LOAD_FAST                'end'
              280  BUILD_SLICE_2         2 
              282  BINARY_SUBSCR    
              284  CALL_METHOD_1         1  ''
              286  POP_TOP          
            288_0  COME_FROM           266  '266'

 L. 604       288  LOAD_FAST                'end'
              290  LOAD_CONST               1
              292  BINARY_ADD       
              294  DUP_TOP          
              296  STORE_FAST               'start'
              298  STORE_FAST               'end'

 L. 605       300  LOAD_FAST                'ch'
              302  LOAD_METHOD              encode
              304  LOAD_STR                 'utf-8'
              306  CALL_METHOD_1         1  ''
              308  STORE_FAST               'data'

 L. 606       310  SETUP_LOOP          340  'to 340'
              312  LOAD_FAST                'data'
              314  GET_ITER         
              316  FOR_ITER            338  'to 338'
              318  STORE_FAST               'ch'

 L. 607       320  LOAD_FAST                'chunks'
              322  LOAD_METHOD              append
              324  LOAD_STR                 '%%%02X'
              326  LOAD_FAST                'ch'
              328  BINARY_MODULO    
              330  CALL_METHOD_1         1  ''
              332  POP_TOP          
          334_336  JUMP_BACK           316  'to 316'
              338  POP_BLOCK        
            340_0  COME_FROM_LOOP      310  '310'
              340  JUMP_BACK           134  'to 134'
            342_0  COME_FROM           144  '144'
              342  POP_BLOCK        
            344_0  COME_FROM_LOOP      132  '132'

 L. 608       344  LOAD_FAST                'start'
              346  LOAD_FAST                'end'
              348  COMPARE_OP               <
          350_352  POP_JUMP_IF_FALSE   372  'to 372'

 L. 609       354  LOAD_FAST                'chunks'
              356  LOAD_METHOD              append
              358  LOAD_FAST                'suffix'
              360  LOAD_FAST                'start'
              362  LOAD_FAST                'end'
              364  BUILD_SLICE_2         2 
              366  BINARY_SUBSCR    
              368  CALL_METHOD_1         1  ''
              370  POP_TOP          
            372_0  COME_FROM           350  '350'

 L. 610       372  LOAD_STR                 ''
              374  LOAD_METHOD              join
              376  LOAD_FAST                'chunks'
              378  CALL_METHOD_1         1  ''
              380  STORE_FAST               'suffix_text'

 L. 611       382  LOAD_FAST                'handle'
          384_386  POP_JUMP_IF_FALSE   400  'to 400'

 L. 612       388  LOAD_STR                 '%s%s'
              390  LOAD_FAST                'handle'
              392  LOAD_FAST                'suffix_text'
              394  BUILD_TUPLE_2         2 
              396  BINARY_MODULO    
              398  RETURN_VALUE     
            400_0  COME_FROM           384  '384'

 L. 614       400  LOAD_STR                 '!<%s>'
              402  LOAD_FAST                'suffix_text'
              404  BINARY_MODULO    
              406  RETURN_VALUE     

Parse error at or near `COME_FROM' instruction at offset 260_1

    def prepare_anchor(self, anchor):
        if not anchor:
            raise EmitterError('anchor must not be empty')
        for ch in anchor:
            if not '0' <= ch <= '9':
                if not 'A' <= ch <= 'Z':
                    if not 'a' <= ch <= 'z':
                        assert ch in '-_', 'invalid character %r in the anchor: %r' % (
                         ch, anchor)

        return anchor

    def analyze_scalar--- This code section failed: ---

 L. 629         0  LOAD_FAST                'scalar'
                2  POP_JUMP_IF_TRUE     28  'to 28'

 L. 630         4  LOAD_GLOBAL              ScalarAnalysis
                6  LOAD_FAST                'scalar'
                8  LOAD_CONST               True
               10  LOAD_CONST               False

 L. 631        12  LOAD_CONST               False
               14  LOAD_CONST               True

 L. 632        16  LOAD_CONST               True
               18  LOAD_CONST               True

 L. 633        20  LOAD_CONST               False
               22  LOAD_CONST               ('scalar', 'empty', 'multiline', 'allow_flow_plain', 'allow_block_plain', 'allow_single_quoted', 'allow_double_quoted', 'allow_block')
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
              122  STORE_FAST               'followed_by_whitespace'

 L. 662       124  LOAD_CONST               False
              126  STORE_FAST               'previous_space'

 L. 665       128  LOAD_CONST               False
              130  STORE_FAST               'previous_break'

 L. 667       132  LOAD_CONST               0
              134  STORE_FAST               'index'

 L. 668   136_138  SETUP_LOOP          654  'to 654'
              140  LOAD_FAST                'index'
              142  LOAD_GLOBAL              len
              144  LOAD_FAST                'scalar'
              146  CALL_FUNCTION_1       1  ''
              148  COMPARE_OP               <
          150_152  POP_JUMP_IF_FALSE   652  'to 652'

 L. 669       154  LOAD_FAST                'scalar'
              156  LOAD_FAST                'index'
              158  BINARY_SUBSCR    
              160  STORE_FAST               'ch'

 L. 672       162  LOAD_FAST                'index'
              164  LOAD_CONST               0
              166  COMPARE_OP               ==
              168  POP_JUMP_IF_FALSE   228  'to 228'

 L. 674       170  LOAD_FAST                'ch'
              172  LOAD_STR                 '#,[]{}&*!|>\'"%@`'
              174  COMPARE_OP               in
              176  POP_JUMP_IF_FALSE   186  'to 186'

 L. 675       178  LOAD_CONST               True
              180  STORE_FAST               'flow_indicators'

 L. 676       182  LOAD_CONST               True
              184  STORE_FAST               'block_indicators'
            186_0  COME_FROM           176  '176'

 L. 677       186  LOAD_FAST                'ch'
              188  LOAD_STR                 '?:'
              190  COMPARE_OP               in
              192  POP_JUMP_IF_FALSE   206  'to 206'

 L. 678       194  LOAD_CONST               True
              196  STORE_FAST               'flow_indicators'

 L. 679       198  LOAD_FAST                'followed_by_whitespace'
              200  POP_JUMP_IF_FALSE   206  'to 206'

 L. 680       202  LOAD_CONST               True
              204  STORE_FAST               'block_indicators'
            206_0  COME_FROM           200  '200'
            206_1  COME_FROM           192  '192'

 L. 681       206  LOAD_FAST                'ch'
              208  LOAD_STR                 '-'
              210  COMPARE_OP               ==
              212  POP_JUMP_IF_FALSE   226  'to 226'
              214  LOAD_FAST                'followed_by_whitespace'
              216  POP_JUMP_IF_FALSE   226  'to 226'

 L. 682       218  LOAD_CONST               True
              220  STORE_FAST               'flow_indicators'

 L. 683       222  LOAD_CONST               True
              224  STORE_FAST               'block_indicators'
            226_0  COME_FROM           216  '216'
            226_1  COME_FROM           212  '212'
              226  JUMP_FORWARD        288  'to 288'
            228_0  COME_FROM           168  '168'

 L. 686       228  LOAD_FAST                'ch'
              230  LOAD_STR                 ',?[]{}'
              232  COMPARE_OP               in
              234  POP_JUMP_IF_FALSE   240  'to 240'

 L. 687       236  LOAD_CONST               True
              238  STORE_FAST               'flow_indicators'
            240_0  COME_FROM           234  '234'

 L. 688       240  LOAD_FAST                'ch'
              242  LOAD_STR                 ':'
              244  COMPARE_OP               ==
          246_248  POP_JUMP_IF_FALSE   264  'to 264'

 L. 689       250  LOAD_CONST               True
              252  STORE_FAST               'flow_indicators'

 L. 690       254  LOAD_FAST                'followed_by_whitespace'
          256_258  POP_JUMP_IF_FALSE   264  'to 264'

 L. 691       260  LOAD_CONST               True
              262  STORE_FAST               'block_indicators'
            264_0  COME_FROM           256  '256'
            264_1  COME_FROM           246  '246'

 L. 692       264  LOAD_FAST                'ch'
              266  LOAD_STR                 '#'
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_FALSE   288  'to 288'
              274  LOAD_FAST                'preceded_by_whitespace'
          276_278  POP_JUMP_IF_FALSE   288  'to 288'

 L. 693       280  LOAD_CONST               True
              282  STORE_FAST               'flow_indicators'

 L. 694       284  LOAD_CONST               True
              286  STORE_FAST               'block_indicators'
            288_0  COME_FROM           276  '276'
            288_1  COME_FROM           270  '270'
            288_2  COME_FROM           226  '226'

 L. 697       288  LOAD_FAST                'ch'
              290  LOAD_STR                 '\n\x85\u2028\u2029'
              292  COMPARE_OP               in
          294_296  POP_JUMP_IF_FALSE   302  'to 302'

 L. 698       298  LOAD_CONST               True
              300  STORE_FAST               'line_breaks'
            302_0  COME_FROM           294  '294'

 L. 699       302  LOAD_FAST                'ch'
              304  LOAD_STR                 '\n'
              306  COMPARE_OP               ==
          308_310  POP_JUMP_IF_TRUE    460  'to 460'
              312  LOAD_STR                 ' '
              314  LOAD_FAST                'ch'
              316  DUP_TOP          
              318  ROT_THREE        
              320  COMPARE_OP               <=
          322_324  POP_JUMP_IF_FALSE   336  'to 336'
              326  LOAD_STR                 '~'
              328  COMPARE_OP               <=
          330_332  POP_JUMP_IF_TRUE    460  'to 460'
              334  JUMP_FORWARD        338  'to 338'
            336_0  COME_FROM           322  '322'
              336  POP_TOP          
            338_0  COME_FROM           334  '334'

 L. 700       338  LOAD_FAST                'ch'
              340  LOAD_STR                 '\x85'
              342  COMPARE_OP               ==
          344_346  POP_JUMP_IF_TRUE    428  'to 428'
              348  LOAD_STR                 '\xa0'
              350  LOAD_FAST                'ch'
              352  DUP_TOP          
              354  ROT_THREE        
              356  COMPARE_OP               <=
          358_360  POP_JUMP_IF_FALSE   372  'to 372'
              362  LOAD_STR                 '\ud7ff'
              364  COMPARE_OP               <=
          366_368  POP_JUMP_IF_TRUE    428  'to 428'
              370  JUMP_FORWARD        374  'to 374'
            372_0  COME_FROM           358  '358'
              372  POP_TOP          
            374_0  COME_FROM           370  '370'

 L. 701       374  LOAD_STR                 '\ue000'
              376  LOAD_FAST                'ch'
              378  DUP_TOP          
              380  ROT_THREE        
              382  COMPARE_OP               <=
          384_386  POP_JUMP_IF_FALSE   398  'to 398'
              388  LOAD_STR                 '�'
              390  COMPARE_OP               <=
          392_394  POP_JUMP_IF_TRUE    428  'to 428'
              396  JUMP_FORWARD        400  'to 400'
            398_0  COME_FROM           384  '384'
              398  POP_TOP          
            400_0  COME_FROM           396  '396'

 L. 702       400  LOAD_STR                 '𐀀'
              402  LOAD_FAST                'ch'
              404  DUP_TOP          
              406  ROT_THREE        
              408  COMPARE_OP               <=
          410_412  POP_JUMP_IF_FALSE   424  'to 424'
              414  LOAD_STR                 '\U0010ffff'
              416  COMPARE_OP               <
          418_420  POP_JUMP_IF_FALSE   456  'to 456'
              422  JUMP_FORWARD        428  'to 428'
            424_0  COME_FROM           410  '410'
              424  POP_TOP          
              426  JUMP_FORWARD        456  'to 456'
            428_0  COME_FROM           422  '422'
            428_1  COME_FROM           392  '392'
            428_2  COME_FROM           366  '366'
            428_3  COME_FROM           344  '344'
              428  LOAD_FAST                'ch'
              430  LOAD_STR                 '\ufeff'
              432  COMPARE_OP               !=
          434_436  POP_JUMP_IF_FALSE   456  'to 456'

 L. 703       438  LOAD_CONST               True
              440  STORE_FAST               'unicode_characters'

 L. 704       442  LOAD_FAST                'self'
              444  LOAD_ATTR                allow_unicode
          446_448  POP_JUMP_IF_TRUE    460  'to 460'

 L. 705       450  LOAD_CONST               True
              452  STORE_FAST               'special_characters'
              454  JUMP_FORWARD        460  'to 460'
            456_0  COME_FROM           434  '434'
            456_1  COME_FROM           426  '426'
            456_2  COME_FROM           418  '418'

 L. 707       456  LOAD_CONST               True
              458  STORE_FAST               'special_characters'
            460_0  COME_FROM           454  '454'
            460_1  COME_FROM           446  '446'
            460_2  COME_FROM           330  '330'
            460_3  COME_FROM           308  '308'

 L. 710       460  LOAD_FAST                'ch'
              462  LOAD_STR                 ' '
              464  COMPARE_OP               ==
          466_468  POP_JUMP_IF_FALSE   526  'to 526'

 L. 711       470  LOAD_FAST                'index'
              472  LOAD_CONST               0
              474  COMPARE_OP               ==
          476_478  POP_JUMP_IF_FALSE   484  'to 484'

 L. 712       480  LOAD_CONST               True
              482  STORE_FAST               'leading_space'
            484_0  COME_FROM           476  '476'

 L. 713       484  LOAD_FAST                'index'
              486  LOAD_GLOBAL              len
              488  LOAD_FAST                'scalar'
              490  CALL_FUNCTION_1       1  ''
              492  LOAD_CONST               1
              494  BINARY_SUBTRACT  
              496  COMPARE_OP               ==
          498_500  POP_JUMP_IF_FALSE   506  'to 506'

 L. 714       502  LOAD_CONST               True
              504  STORE_FAST               'trailing_space'
            506_0  COME_FROM           498  '498'

 L. 715       506  LOAD_FAST                'previous_break'
          508_510  POP_JUMP_IF_FALSE   516  'to 516'

 L. 716       512  LOAD_CONST               True
              514  STORE_FAST               'break_space'
            516_0  COME_FROM           508  '508'

 L. 717       516  LOAD_CONST               True
              518  STORE_FAST               'previous_space'

 L. 718       520  LOAD_CONST               False
              522  STORE_FAST               'previous_break'
              524  JUMP_FORWARD        600  'to 600'
            526_0  COME_FROM           466  '466'

 L. 719       526  LOAD_FAST                'ch'
              528  LOAD_STR                 '\n\x85\u2028\u2029'
              530  COMPARE_OP               in
          532_534  POP_JUMP_IF_FALSE   592  'to 592'

 L. 720       536  LOAD_FAST                'index'
              538  LOAD_CONST               0
              540  COMPARE_OP               ==
          542_544  POP_JUMP_IF_FALSE   550  'to 550'

 L. 721       546  LOAD_CONST               True
              548  STORE_FAST               'leading_break'
            550_0  COME_FROM           542  '542'

 L. 722       550  LOAD_FAST                'index'
              552  LOAD_GLOBAL              len
              554  LOAD_FAST                'scalar'
              556  CALL_FUNCTION_1       1  ''
              558  LOAD_CONST               1
              560  BINARY_SUBTRACT  
              562  COMPARE_OP               ==
          564_566  POP_JUMP_IF_FALSE   572  'to 572'

 L. 723       568  LOAD_CONST               True
              570  STORE_FAST               'trailing_break'
            572_0  COME_FROM           564  '564'

 L. 724       572  LOAD_FAST                'previous_space'
          574_576  POP_JUMP_IF_FALSE   582  'to 582'

 L. 725       578  LOAD_CONST               True
              580  STORE_FAST               'space_break'
            582_0  COME_FROM           574  '574'

 L. 726       582  LOAD_CONST               False
              584  STORE_FAST               'previous_space'

 L. 727       586  LOAD_CONST               True
              588  STORE_FAST               'previous_break'
              590  JUMP_FORWARD        600  'to 600'
            592_0  COME_FROM           532  '532'

 L. 729       592  LOAD_CONST               False
              594  STORE_FAST               'previous_space'

 L. 730       596  LOAD_CONST               False
              598  STORE_FAST               'previous_break'
            600_0  COME_FROM           590  '590'
            600_1  COME_FROM           524  '524'

 L. 733       600  LOAD_FAST                'index'
              602  LOAD_CONST               1
              604  INPLACE_ADD      
              606  STORE_FAST               'index'

 L. 734       608  LOAD_FAST                'ch'
              610  LOAD_STR                 '\x00 \t\r\n\x85\u2028\u2029'
              612  COMPARE_OP               in
              614  STORE_FAST               'preceded_by_whitespace'

 L. 735       616  LOAD_FAST                'index'
              618  LOAD_CONST               1
              620  BINARY_ADD       
              622  LOAD_GLOBAL              len
              624  LOAD_FAST                'scalar'
              626  CALL_FUNCTION_1       1  ''
              628  COMPARE_OP               >=
          630_632  JUMP_IF_TRUE_OR_POP   648  'to 648'

 L. 736       634  LOAD_FAST                'scalar'
              636  LOAD_FAST                'index'
              638  LOAD_CONST               1
              640  BINARY_ADD       
              642  BINARY_SUBSCR    
              644  LOAD_STR                 '\x00 \t\r\n\x85\u2028\u2029'
              646  COMPARE_OP               in
            648_0  COME_FROM           630  '630'
              648  STORE_FAST               'followed_by_whitespace'
              650  JUMP_BACK           140  'to 140'
            652_0  COME_FROM           150  '150'
              652  POP_BLOCK        
            654_0  COME_FROM_LOOP      136  '136'

 L. 739       654  LOAD_CONST               True
              656  STORE_FAST               'allow_flow_plain'

 L. 740       658  LOAD_CONST               True
              660  STORE_FAST               'allow_block_plain'

 L. 741       662  LOAD_CONST               True
              664  STORE_FAST               'allow_single_quoted'

 L. 742       666  LOAD_CONST               True
              668  STORE_FAST               'allow_double_quoted'

 L. 743       670  LOAD_CONST               True
              672  STORE_FAST               'allow_block'

 L. 746       674  LOAD_FAST                'leading_space'
          676_678  POP_JUMP_IF_TRUE    698  'to 698'
              680  LOAD_FAST                'leading_break'
          682_684  POP_JUMP_IF_TRUE    698  'to 698'

 L. 747       686  LOAD_FAST                'trailing_space'
          688_690  POP_JUMP_IF_TRUE    698  'to 698'
              692  LOAD_FAST                'trailing_break'
          694_696  POP_JUMP_IF_FALSE   706  'to 706'
            698_0  COME_FROM           688  '688'
            698_1  COME_FROM           682  '682'
            698_2  COME_FROM           676  '676'

 L. 748       698  LOAD_CONST               False
              700  DUP_TOP          
              702  STORE_FAST               'allow_flow_plain'
              704  STORE_FAST               'allow_block_plain'
            706_0  COME_FROM           694  '694'

 L. 751       706  LOAD_FAST                'trailing_space'
          708_710  POP_JUMP_IF_FALSE   716  'to 716'

 L. 752       712  LOAD_CONST               False
              714  STORE_FAST               'allow_block'
            716_0  COME_FROM           708  '708'

 L. 756       716  LOAD_FAST                'break_space'
          718_720  POP_JUMP_IF_FALSE   734  'to 734'

 L. 757       722  LOAD_CONST               False
              724  DUP_TOP          
              726  STORE_FAST               'allow_flow_plain'
              728  DUP_TOP          
              730  STORE_FAST               'allow_block_plain'
              732  STORE_FAST               'allow_single_quoted'
            734_0  COME_FROM           718  '718'

 L. 761       734  LOAD_FAST                'space_break'
          736_738  POP_JUMP_IF_TRUE    746  'to 746'
              740  LOAD_FAST                'special_characters'
          742_744  POP_JUMP_IF_FALSE   762  'to 762'
            746_0  COME_FROM           736  '736'

 L. 763       746  LOAD_CONST               False
              748  DUP_TOP          
              750  STORE_FAST               'allow_flow_plain'
              752  DUP_TOP          
              754  STORE_FAST               'allow_block_plain'
              756  DUP_TOP          
              758  STORE_FAST               'allow_single_quoted'
              760  STORE_FAST               'allow_block'
            762_0  COME_FROM           742  '742'

 L. 767       762  LOAD_FAST                'line_breaks'
          764_766  POP_JUMP_IF_FALSE   776  'to 776'

 L. 768       768  LOAD_CONST               False
              770  DUP_TOP          
              772  STORE_FAST               'allow_flow_plain'
              774  STORE_FAST               'allow_block_plain'
            776_0  COME_FROM           764  '764'

 L. 771       776  LOAD_FAST                'flow_indicators'
          778_780  POP_JUMP_IF_FALSE   786  'to 786'

 L. 772       782  LOAD_CONST               False
              784  STORE_FAST               'allow_flow_plain'
            786_0  COME_FROM           778  '778'

 L. 775       786  LOAD_FAST                'block_indicators'
          788_790  POP_JUMP_IF_FALSE   796  'to 796'

 L. 776       792  LOAD_CONST               False
              794  STORE_FAST               'allow_block_plain'
            796_0  COME_FROM           788  '788'

 L. 778       796  LOAD_GLOBAL              ScalarAnalysis
              798  LOAD_FAST                'scalar'

 L. 779       800  LOAD_CONST               False
              802  LOAD_FAST                'line_breaks'

 L. 780       804  LOAD_FAST                'allow_flow_plain'

 L. 781       806  LOAD_FAST                'allow_block_plain'

 L. 782       808  LOAD_FAST                'allow_single_quoted'

 L. 783       810  LOAD_FAST                'allow_double_quoted'

 L. 784       812  LOAD_FAST                'allow_block'
              814  LOAD_CONST               ('scalar', 'empty', 'multiline', 'allow_flow_plain', 'allow_block_plain', 'allow_single_quoted', 'allow_double_quoted', 'allow_block')
              816  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              818  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 652

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
               34  POP_JUMP_IF_FALSE    50  'to 50'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                whitespace
               40  POP_JUMP_IF_TRUE     50  'to 50'
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
                if breaks:
                    if ch is None or ch not in '\n\x85\u2028\u2029':
                        if text[start] == '\n':
                            self.write_line_break()
                        for br in text[start:end]:
                            if br == '\n':
                                self.write_line_break()
                            else:
                                self.write_line_break(br)

                        self.write_indent()
                        start = end
                else:
                    if ch is None or ch in ' \n\x85\u2028\u2029' or ch == "'":
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

 L. 929     20_22  SETUP_LOOP          648  'to 648'
               24  LOAD_FAST                'end'
               26  LOAD_GLOBAL              len
               28  LOAD_FAST                'text'
               30  CALL_FUNCTION_1       1  ''
               32  COMPARE_OP               <=
            34_36  POP_JUMP_IF_FALSE   646  'to 646'

 L. 930        38  LOAD_CONST               None
               40  STORE_FAST               'ch'

 L. 931        42  LOAD_FAST                'end'
               44  LOAD_GLOBAL              len
               46  LOAD_FAST                'text'
               48  CALL_FUNCTION_1       1  ''
               50  COMPARE_OP               <
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 932        54  LOAD_FAST                'text'
               56  LOAD_FAST                'end'
               58  BINARY_SUBSCR    
               60  STORE_FAST               'ch'
             62_0  COME_FROM            52  '52'

 L. 933        62  LOAD_FAST                'ch'
               64  LOAD_CONST               None
               66  COMPARE_OP               is
               68  POP_JUMP_IF_TRUE    156  'to 156'
               70  LOAD_FAST                'ch'
               72  LOAD_STR                 '"\\\x85\u2028\u2029\ufeff'
               74  COMPARE_OP               in
               76  POP_JUMP_IF_TRUE    156  'to 156'

 L. 934        78  LOAD_STR                 ' '
               80  LOAD_FAST                'ch'
               82  DUP_TOP          
               84  ROT_THREE        
               86  COMPARE_OP               <=
               88  POP_JUMP_IF_FALSE   100  'to 100'
               90  LOAD_STR                 '~'
               92  COMPARE_OP               <=
            94_96  POP_JUMP_IF_TRUE    384  'to 384'
               98  JUMP_FORWARD        102  'to 102'
            100_0  COME_FROM            88  '88'
              100  POP_TOP          
            102_0  COME_FROM            98  '98'

 L. 935       102  LOAD_FAST                'self'
              104  LOAD_ATTR                allow_unicode
              106  POP_JUMP_IF_FALSE   156  'to 156'

 L. 936       108  LOAD_STR                 '\xa0'
              110  LOAD_FAST                'ch'
              112  DUP_TOP          
              114  ROT_THREE        
              116  COMPARE_OP               <=
              118  POP_JUMP_IF_FALSE   130  'to 130'
              120  LOAD_STR                 '\ud7ff'
              122  COMPARE_OP               <=
          124_126  POP_JUMP_IF_TRUE    384  'to 384'
              128  JUMP_FORWARD        132  'to 132'
            130_0  COME_FROM           118  '118'
              130  POP_TOP          
            132_0  COME_FROM           128  '128'

 L. 937       132  LOAD_STR                 '\ue000'
              134  LOAD_FAST                'ch'
              136  DUP_TOP          
              138  ROT_THREE        
              140  COMPARE_OP               <=
              142  POP_JUMP_IF_FALSE   154  'to 154'
              144  LOAD_STR                 '�'
              146  COMPARE_OP               <=
          148_150  POP_JUMP_IF_TRUE    384  'to 384'
              152  JUMP_FORWARD        156  'to 156'
            154_0  COME_FROM           142  '142'
              154  POP_TOP          
            156_0  COME_FROM           152  '152'
            156_1  COME_FROM           106  '106'
            156_2  COME_FROM            76  '76'
            156_3  COME_FROM            68  '68'

 L. 938       156  LOAD_FAST                'start'
              158  LOAD_FAST                'end'
              160  COMPARE_OP               <
              162  POP_JUMP_IF_FALSE   228  'to 228'

 L. 939       164  LOAD_FAST                'text'
              166  LOAD_FAST                'start'
              168  LOAD_FAST                'end'
              170  BUILD_SLICE_2         2 
              172  BINARY_SUBSCR    
              174  STORE_FAST               'data'

 L. 940       176  LOAD_FAST                'self'
              178  DUP_TOP          
              180  LOAD_ATTR                column
              182  LOAD_GLOBAL              len
              184  LOAD_FAST                'data'
              186  CALL_FUNCTION_1       1  ''
              188  INPLACE_ADD      
              190  ROT_TWO          
              192  STORE_ATTR               column

 L. 941       194  LOAD_FAST                'self'
              196  LOAD_ATTR                encoding
              198  POP_JUMP_IF_FALSE   212  'to 212'

 L. 942       200  LOAD_FAST                'data'
              202  LOAD_METHOD              encode
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                encoding
              208  CALL_METHOD_1         1  ''
              210  STORE_FAST               'data'
            212_0  COME_FROM           198  '198'

 L. 943       212  LOAD_FAST                'self'
              214  LOAD_ATTR                stream
              216  LOAD_METHOD              write
              218  LOAD_FAST                'data'
              220  CALL_METHOD_1         1  ''
              222  POP_TOP          

 L. 944       224  LOAD_FAST                'end'
              226  STORE_FAST               'start'
            228_0  COME_FROM           162  '162'

 L. 945       228  LOAD_FAST                'ch'
              230  LOAD_CONST               None
              232  COMPARE_OP               is-not
          234_236  POP_JUMP_IF_FALSE   384  'to 384'

 L. 946       238  LOAD_FAST                'ch'
              240  LOAD_FAST                'self'
              242  LOAD_ATTR                ESCAPE_REPLACEMENTS
              244  COMPARE_OP               in
          246_248  POP_JUMP_IF_FALSE   266  'to 266'

 L. 947       250  LOAD_STR                 '\\'
              252  LOAD_FAST                'self'
              254  LOAD_ATTR                ESCAPE_REPLACEMENTS
              256  LOAD_FAST                'ch'
              258  BINARY_SUBSCR    
              260  BINARY_ADD       
              262  STORE_FAST               'data'
              264  JUMP_FORWARD        326  'to 326'
            266_0  COME_FROM           246  '246'

 L. 948       266  LOAD_FAST                'ch'
              268  LOAD_STR                 'ÿ'
              270  COMPARE_OP               <=
          272_274  POP_JUMP_IF_FALSE   290  'to 290'

 L. 949       276  LOAD_STR                 '\\x%02X'
              278  LOAD_GLOBAL              ord
              280  LOAD_FAST                'ch'
              282  CALL_FUNCTION_1       1  ''
              284  BINARY_MODULO    
              286  STORE_FAST               'data'
              288  JUMP_FORWARD        326  'to 326'
            290_0  COME_FROM           272  '272'

 L. 950       290  LOAD_FAST                'ch'
              292  LOAD_STR                 '\uffff'
              294  COMPARE_OP               <=
          296_298  POP_JUMP_IF_FALSE   314  'to 314'

 L. 951       300  LOAD_STR                 '\\u%04X'
              302  LOAD_GLOBAL              ord
              304  LOAD_FAST                'ch'
              306  CALL_FUNCTION_1       1  ''
              308  BINARY_MODULO    
              310  STORE_FAST               'data'
              312  JUMP_FORWARD        326  'to 326'
            314_0  COME_FROM           296  '296'

 L. 953       314  LOAD_STR                 '\\U%08X'
              316  LOAD_GLOBAL              ord
              318  LOAD_FAST                'ch'
              320  CALL_FUNCTION_1       1  ''
              322  BINARY_MODULO    
              324  STORE_FAST               'data'
            326_0  COME_FROM           312  '312'
            326_1  COME_FROM           288  '288'
            326_2  COME_FROM           264  '264'

 L. 954       326  LOAD_FAST                'self'
              328  DUP_TOP          
              330  LOAD_ATTR                column
              332  LOAD_GLOBAL              len
              334  LOAD_FAST                'data'
              336  CALL_FUNCTION_1       1  ''
              338  INPLACE_ADD      
              340  ROT_TWO          
              342  STORE_ATTR               column

 L. 955       344  LOAD_FAST                'self'
              346  LOAD_ATTR                encoding
          348_350  POP_JUMP_IF_FALSE   364  'to 364'

 L. 956       352  LOAD_FAST                'data'
              354  LOAD_METHOD              encode
              356  LOAD_FAST                'self'
              358  LOAD_ATTR                encoding
              360  CALL_METHOD_1         1  ''
              362  STORE_FAST               'data'
            364_0  COME_FROM           348  '348'

 L. 957       364  LOAD_FAST                'self'
              366  LOAD_ATTR                stream
              368  LOAD_METHOD              write
              370  LOAD_FAST                'data'
              372  CALL_METHOD_1         1  ''
              374  POP_TOP          

 L. 958       376  LOAD_FAST                'end'
              378  LOAD_CONST               1
              380  BINARY_ADD       
              382  STORE_FAST               'start'
            384_0  COME_FROM           234  '234'
            384_1  COME_FROM           148  '148'
            384_2  COME_FROM           124  '124'
            384_3  COME_FROM            94  '94'

 L. 959       384  LOAD_CONST               0
              386  LOAD_FAST                'end'
              388  DUP_TOP          
              390  ROT_THREE        
              392  COMPARE_OP               <
          394_396  POP_JUMP_IF_FALSE   416  'to 416'
              398  LOAD_GLOBAL              len
              400  LOAD_FAST                'text'
              402  CALL_FUNCTION_1       1  ''
              404  LOAD_CONST               1
              406  BINARY_SUBTRACT  
              408  COMPARE_OP               <
          410_412  POP_JUMP_IF_FALSE   636  'to 636'
              414  JUMP_FORWARD        420  'to 420'
            416_0  COME_FROM           394  '394'
              416  POP_TOP          
              418  JUMP_FORWARD        636  'to 636'
            420_0  COME_FROM           414  '414'
              420  LOAD_FAST                'ch'
              422  LOAD_STR                 ' '
              424  COMPARE_OP               ==
          426_428  POP_JUMP_IF_TRUE    440  'to 440'
              430  LOAD_FAST                'start'
              432  LOAD_FAST                'end'
              434  COMPARE_OP               >=
          436_438  POP_JUMP_IF_FALSE   636  'to 636'
            440_0  COME_FROM           426  '426'

 L. 960       440  LOAD_FAST                'self'
              442  LOAD_ATTR                column
              444  LOAD_FAST                'end'
              446  LOAD_FAST                'start'
              448  BINARY_SUBTRACT  
              450  BINARY_ADD       
              452  LOAD_FAST                'self'
              454  LOAD_ATTR                best_width
              456  COMPARE_OP               >
          458_460  POP_JUMP_IF_FALSE   636  'to 636'
              462  LOAD_FAST                'split'
          464_466  POP_JUMP_IF_FALSE   636  'to 636'

 L. 961       468  LOAD_FAST                'text'
              470  LOAD_FAST                'start'
              472  LOAD_FAST                'end'
              474  BUILD_SLICE_2         2 
              476  BINARY_SUBSCR    
              478  LOAD_STR                 '\\'
              480  BINARY_ADD       
              482  STORE_FAST               'data'

 L. 962       484  LOAD_FAST                'start'
              486  LOAD_FAST                'end'
              488  COMPARE_OP               <
          490_492  POP_JUMP_IF_FALSE   498  'to 498'

 L. 963       494  LOAD_FAST                'end'
              496  STORE_FAST               'start'
            498_0  COME_FROM           490  '490'

 L. 964       498  LOAD_FAST                'self'
              500  DUP_TOP          
              502  LOAD_ATTR                column
              504  LOAD_GLOBAL              len
              506  LOAD_FAST                'data'
              508  CALL_FUNCTION_1       1  ''
              510  INPLACE_ADD      
              512  ROT_TWO          
              514  STORE_ATTR               column

 L. 965       516  LOAD_FAST                'self'
              518  LOAD_ATTR                encoding
          520_522  POP_JUMP_IF_FALSE   536  'to 536'

 L. 966       524  LOAD_FAST                'data'
              526  LOAD_METHOD              encode
              528  LOAD_FAST                'self'
              530  LOAD_ATTR                encoding
              532  CALL_METHOD_1         1  ''
              534  STORE_FAST               'data'
            536_0  COME_FROM           520  '520'

 L. 967       536  LOAD_FAST                'self'
              538  LOAD_ATTR                stream
              540  LOAD_METHOD              write
              542  LOAD_FAST                'data'
              544  CALL_METHOD_1         1  ''
              546  POP_TOP          

 L. 968       548  LOAD_FAST                'self'
              550  LOAD_METHOD              write_indent
              552  CALL_METHOD_0         0  ''
              554  POP_TOP          

 L. 969       556  LOAD_CONST               False
              558  LOAD_FAST                'self'
              560  STORE_ATTR               whitespace

 L. 970       562  LOAD_CONST               False
              564  LOAD_FAST                'self'
              566  STORE_ATTR               indention

 L. 971       568  LOAD_FAST                'text'
              570  LOAD_FAST                'start'
              572  BINARY_SUBSCR    
              574  LOAD_STR                 ' '
              576  COMPARE_OP               ==
          578_580  POP_JUMP_IF_FALSE   636  'to 636'

 L. 972       582  LOAD_STR                 '\\'
              584  STORE_FAST               'data'

 L. 973       586  LOAD_FAST                'self'
              588  DUP_TOP          
              590  LOAD_ATTR                column
              592  LOAD_GLOBAL              len
              594  LOAD_FAST                'data'
              596  CALL_FUNCTION_1       1  ''
              598  INPLACE_ADD      
              600  ROT_TWO          
              602  STORE_ATTR               column

 L. 974       604  LOAD_FAST                'self'
              606  LOAD_ATTR                encoding
          608_610  POP_JUMP_IF_FALSE   624  'to 624'

 L. 975       612  LOAD_FAST                'data'
              614  LOAD_METHOD              encode
              616  LOAD_FAST                'self'
              618  LOAD_ATTR                encoding
              620  CALL_METHOD_1         1  ''
              622  STORE_FAST               'data'
            624_0  COME_FROM           608  '608'

 L. 976       624  LOAD_FAST                'self'
              626  LOAD_ATTR                stream
              628  LOAD_METHOD              write
              630  LOAD_FAST                'data'
              632  CALL_METHOD_1         1  ''
              634  POP_TOP          
            636_0  COME_FROM           578  '578'
            636_1  COME_FROM           464  '464'
            636_2  COME_FROM           458  '458'
            636_3  COME_FROM           436  '436'
            636_4  COME_FROM           418  '418'
            636_5  COME_FROM           410  '410'

 L. 977       636  LOAD_FAST                'end'
              638  LOAD_CONST               1
              640  INPLACE_ADD      
              642  STORE_FAST               'end'
              644  JUMP_BACK            24  'to 24'
            646_0  COME_FROM            34  '34'
              646  POP_BLOCK        
            648_0  COME_FROM_LOOP       20  '20'

 L. 978       648  LOAD_FAST                'self'
              650  LOAD_METHOD              write_indicator
              652  LOAD_STR                 '"'
              654  LOAD_CONST               False
              656  CALL_METHOD_2         2  ''
              658  POP_TOP          

Parse error at or near `POP_BLOCK' instruction at offset 646

    def determine_block_hints(self, text):
        hints = ''
        if text:
            if text[0] in ' \n\x85\u2028\u2029':
                hints += str(self.best_indent)
            if text[(-1)] not in '\n\x85\u2028\u2029':
                hints += '-'
            elif len(text) == 1 or text[(-2)] in '\n\x85\u2028\u2029':
                hints += '+'
        return hints

    def write_folded(self, text):
        hints = self.determine_block_hints(text)
        self.write_indicator('>' + hints, True)
        if hints[-1:] == '+':
            self.open_ended = True
        self.write_line_break()
        leading_space = True
        spaces = False
        breaks = True
        start = end = 0
        while end <= len(text):
            ch = None
            if end < len(text):
                ch = text[end]
            if breaks:
                if ch is None or ch not in '\n\x85\u2028\u2029':
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

                    if ch is not None:
                        self.write_indent()
                    start = end
            elif spaces:
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
        self.write_line_break()
        breaks = True
        start = end = 0
        while end <= len(text):
            ch = None
            if end < len(text):
                ch = text[end]
            if breaks and not ch is None:
                if ch not in '\n\x85\u2028\u2029':
                    for br in text[start:end]:
                        if br == '\n':
                            self.write_line_break()
                        else:
                            self.write_line_break(br)

                    if ch is not None:
                        self.write_indent()
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
            data = self.whitespace or ' '
            self.column += len(data)
            if self.encoding:
                data = data.encode(self.encoding)
            self.stream.write(data)
        self.whitespace = False
        self.indention = False
        spaces = False
        breaks = False
        start = end = 0
        while end <= len(text):
            ch = None
            if end < len(text):
                ch = text[end]
            if spaces:
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

                    self.write_indent()
                    self.whitespace = False
                    self.indention = False
                    start = end
            else:
                if ch is None or ch in ' \n\x85\u2028\u2029':
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