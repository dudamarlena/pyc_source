# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/pyyaml/yaml/emitter.py
# Compiled at: 2019-07-30 18:47:04
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
        else:
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
        if isinstance(self.event, DocumentStartEvent):
            if self.event.version or self.event.tags:
                if self.open_ended:
                    self.write_indicator('...', True)
                    self.write_indent()
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

            else:
                implicit = first and not self.event.explicit and not self.canonical and not self.event.version and not self.event.tags and not self.check_empty_document()
                if not implicit:
                    self.write_indent()
                    self.write_indicator('---', True)
                    if self.canonical:
                        self.write_indent()
            self.state = self.expect_document_root
        else:
            if isinstance(self.event, StreamEndEvent):
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

    def expect_node(self, root=False, sequence=False, mapping=False, simple_key=False):
        self.root_context = root
        self.sequence_context = sequence
        self.mapping_context = mapping
        self.simple_key_context = simple_key
        if isinstance(self.event, AliasEvent):
            self.expect_alias()
        else:
            if isinstance(self.event, (ScalarEvent, CollectionStartEvent)):
                self.process_anchor('&')
                self.process_tag()
                if isinstance(self.event, ScalarEvent):
                    self.expect_scalar()
                else:
                    if isinstance(self.event, SequenceStartEvent):
                        if self.flow_level or self.canonical or self.event.flow_style or self.check_empty_sequence():
                            self.expect_flow_sequence()
                        else:
                            self.expect_block_sequence()
                    elif isinstance(self.event, MappingStartEvent):
                        if self.flow_level or self.canonical or self.event.flow_style or self.check_empty_mapping():
                            self.expect_flow_mapping()
                        else:
                            self.expect_block_mapping()
            else:
                raise EmitterError('expected NodeEvent, but got %s' % self.event)

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
        elif self.canonical or self.column > self.best_width:
            self.write_indent()
        elif not self.canonical and self.check_simple_key():
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
            if self.canonical or self.column > self.best_width:
                self.write_indent()
            elif not self.canonical and self.check_simple_key():
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
        if not first and isinstance(self.event, MappingEndEvent):
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
        if not isinstance(self.event, DocumentStartEvent) or not self.events:
            return False
        else:
            event = self.events[0]
            return isinstance(event, ScalarEvent) and event.anchor is None and event.tag is None and event.implicit and event.value == ''

    def check_simple_key(self):
        length = 0
        if isinstance(self.event, NodeEvent):
            if self.event.anchor is not None:
                if self.prepared_anchor is None:
                    self.prepared_anchor = self.prepare_anchor(self.event.anchor)
                length += len(self.prepared_anchor)
        else:
            if isinstance(self.event, (ScalarEvent, CollectionStartEvent)):
                if self.event.tag is not None:
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
        else:
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
            if not self.canonical or tag is None:
                if self.style == '' and self.event.implicit[0] or self.style != '' and self.event.implicit[1]:
                    self.prepared_tag = None
                    return
            if self.event.implicit[0]:
                if tag is None:
                    tag = '!'
                    self.prepared_tag = None
        else:
            if not self.canonical or tag is None:
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
        if self.event.style == '"' or self.canonical:
            return '"'
        else:
            if not self.event.style:
                if self.event.implicit[0]:
                    if not (self.simple_key_context and (self.analysis.empty or self.analysis.multiline)):
                        if self.flow_level and self.analysis.allow_flow_plain or not self.flow_level and self.analysis.allow_block_plain:
                            return ''
                if self.event.style:
                    if self.event.style in '|>':
                        if not self.flow_level:
                            if not self.simple_key_context:
                                if self.analysis.allow_block:
                                    return self.event.style
            else:
                if not self.event.style or self.event.style == "'":
                    if self.analysis.allow_single_quoted:
                        if not (self.simple_key_context and self.analysis.multiline):
                            return "'"
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
            if not ('0' <= ch <= '9' or 'A' <= ch <= 'Z' or 'a' <= ch <= 'z' or ch in '-_'):
                raise EmitterError('invalid character %r in the tag handle: %r' % (
                 ch, handle))

        return handle

    def prepare_tag_prefix(self, prefix):
        if not prefix:
            raise EmitterError('tag prefix must not be empty')
        else:
            chunks = []
            start = end = 0
            if prefix[0] == '!':
                end = 1
            while end < len(prefix):
                ch = prefix[end]
                if '0' <= ch <= '9' or 'A' <= ch <= 'Z' or 'a' <= ch <= 'z' or ch in "-;/?!:@&=+$,_.~*'()[]":
                    end += 1
                else:
                    if start < end:
                        chunks.append(prefix[start:end])
                    start = end = end + 1
                    data = ch.encode('utf-8')
                    for ch in data:
                        chunks.append('%%%02X' % ord(ch))

            if start < end:
                chunks.append(prefix[start:end])
        return ''.join(chunks)

    def prepare_tag(self, tag):
        if not tag:
            raise EmitterError('tag must not be empty')
        if tag == '!':
            return tag
        else:
            handle = None
            suffix = tag
            prefixes = sorted(self.tag_prefixes.keys())
            for prefix in prefixes:
                if tag.startswith(prefix) and (prefix == '!' or len(prefix) < len(tag)):
                    handle = self.tag_prefixes[prefix]
                    suffix = tag[len(prefix):]

            chunks = []
            start = end = 0
            while end < len(suffix):
                ch = suffix[end]
                if '0' <= ch <= '9' or 'A' <= ch <= 'Z' or 'a' <= ch <= 'z' or ch in "-;/?:@&=+$,_.~*'()[]" or ch == '!' and handle != '!':
                    end += 1
                else:
                    if start < end:
                        chunks.append(suffix[start:end])
                    start = end = end + 1
                    data = ch.encode('utf-8')
                    for ch in data:
                        chunks.append('%%%02X' % ch)

            if start < end:
                chunks.append(suffix[start:end])
            suffix_text = ''.join(chunks)
            if handle:
                return '%s%s' % (handle, suffix_text)
            return '!<%s>' % suffix_text

    def prepare_anchor(self, anchor):
        if not anchor:
            raise EmitterError('anchor must not be empty')
        for ch in anchor:
            if not ('0' <= ch <= '9' or 'A' <= ch <= 'Z' or 'a' <= ch <= 'z' or ch in '-_'):
                raise EmitterError('invalid character %r in the anchor: %r' % (
                 ch, anchor))

        return anchor

    def analyze_scalar(self, scalar):
        if not scalar:
            return ScalarAnalysis(scalar=scalar, empty=True, multiline=False, allow_flow_plain=False,
              allow_block_plain=True,
              allow_single_quoted=True,
              allow_double_quoted=True,
              allow_block=False)
        else:
            block_indicators = False
            flow_indicators = False
            line_breaks = False
            special_characters = False
            leading_space = False
            leading_break = False
            trailing_space = False
            trailing_break = False
            break_space = False
            space_break = False
            if scalar.startswith('---') or scalar.startswith('...'):
                block_indicators = True
                flow_indicators = True
            preceded_by_whitespace = True
            followed_by_whitespace = len(scalar) == 1 or scalar[1] in '\x00 \t\r\n\x85\u2028\u2029'
            previous_space = False
            previous_break = False
            index = 0
            while index < len(scalar):
                ch = scalar[index]
                if index == 0:
                    if ch in '#,[]{}&*!|>\'"%@`':
                        flow_indicators = True
                        block_indicators = True
                    else:
                        if ch in '?:':
                            flow_indicators = True
                            if followed_by_whitespace:
                                block_indicators = True
                        if ch == '-':
                            if followed_by_whitespace:
                                flow_indicators = True
                                block_indicators = True
                else:
                    if ch in ',?[]{}':
                        flow_indicators = True
                    elif ch == ':':
                        flow_indicators = True
                        if followed_by_whitespace:
                            block_indicators = True
                        if ch == '#':
                            if preceded_by_whitespace:
                                flow_indicators = True
                                block_indicators = True
                        if ch in '\n\x85\u2028\u2029':
                            line_breaks = True
                    else:
                        if ch == '\n' or ' ' <= ch <= '~' or ch == '\x85' or '\xa0' <= ch <= '\ud7ff' or '\ue000' <= ch <= '�' or '𐀀' <= ch < '\U0010ffff' and ch != '\ufeff':
                            unicode_characters = True
                            if not self.allow_unicode:
                                special_characters = True
                        else:
                            special_characters = True
                        if ch == ' ':
                            if index == 0:
                                leading_space = True
                            else:
                                if index == len(scalar) - 1:
                                    trailing_space = True
                                if previous_break:
                                    break_space = True
                            previous_space = True
                            previous_break = False
                        else:
                            if ch in '\n\x85\u2028\u2029':
                                if index == 0:
                                    leading_break = True
                                else:
                                    if index == len(scalar) - 1:
                                        trailing_break = True
                                    if previous_space:
                                        space_break = True
                                previous_space = False
                                previous_break = True
                            else:
                                previous_space = False
                        previous_break = False
                    index += 1
                    preceded_by_whitespace = ch in '\x00 \t\r\n\x85\u2028\u2029'
                    followed_by_whitespace = index + 1 >= len(scalar) or scalar[(index + 1)] in '\x00 \t\r\n\x85\u2028\u2029'

            allow_flow_plain = True
            allow_block_plain = True
            allow_single_quoted = True
            allow_double_quoted = True
            allow_block = True
            if leading_space or leading_break or trailing_space or trailing_break:
                allow_flow_plain = allow_block_plain = False
            if trailing_space:
                allow_block = False
            if break_space:
                allow_flow_plain = allow_block_plain = allow_single_quoted = False
            if space_break or special_characters:
                allow_flow_plain = allow_block_plain = allow_single_quoted = allow_block = False
            if line_breaks:
                allow_flow_plain = allow_block_plain = False
            if flow_indicators:
                allow_flow_plain = False
            if block_indicators:
                allow_block_plain = False
            return ScalarAnalysis(scalar=scalar, empty=False,
              multiline=line_breaks,
              allow_flow_plain=allow_flow_plain,
              allow_block_plain=allow_block_plain,
              allow_single_quoted=allow_single_quoted,
              allow_double_quoted=allow_double_quoted,
              allow_block=allow_block)

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
        if self.whitespace or not need_whitespace:
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

    def write_indent(self):
        indent = self.indent or 0
        if not self.indention or self.column > indent or self.column == indent and not self.whitespace:
            self.write_line_break()
        if self.column < indent:
            self.whitespace = True
            data = ' ' * (indent - self.column)
            self.column = indent
            if self.encoding:
                data = data.encode(self.encoding)
            self.stream.write(data)

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
            if spaces:
                if ch is None or ch != ' ':
                    if start + 1 == end:
                        if self.column > self.best_width:
                            if split:
                                if start != 0:
                                    if end != len(text):
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
                2  LOAD_ATTR                write_indicator
                4  LOAD_STR                 '"'
                6  LOAD_CONST               True
                8  CALL_FUNCTION_2       2  '2 positional arguments'
               10  POP_TOP          

 L. 928        12  LOAD_CONST               0
               14  DUP_TOP          
               16  STORE_FAST               'start'
               18  STORE_FAST               'end'

 L. 929        20  SETUP_LOOP          652  'to 652'
               24  LOAD_FAST                'end'
               26  LOAD_GLOBAL              len
               28  LOAD_FAST                'text'
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  COMPARE_OP               <=
               34  POP_JUMP_IF_FALSE   650  'to 650'

 L. 930        38  LOAD_CONST               None
               40  STORE_FAST               'ch'

 L. 931        42  LOAD_FAST                'end'
               44  LOAD_GLOBAL              len
               46  LOAD_FAST                'text'
               48  CALL_FUNCTION_1       1  '1 positional argument'
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
               68  POP_JUMP_IF_TRUE    160  'to 160'
               70  LOAD_FAST                'ch'
               72  LOAD_STR                 '"\\\x85\u2028\u2029\ufeff'
               74  COMPARE_OP               in
               76  POP_JUMP_IF_TRUE    160  'to 160'

 L. 934        78  LOAD_STR                 ' '
               80  LOAD_FAST                'ch'
               82  DUP_TOP          
               84  ROT_THREE        
               86  COMPARE_OP               <=
               88  JUMP_IF_FALSE_OR_POP    96  'to 96'
               90  LOAD_STR                 '~'
               92  COMPARE_OP               <=
               94  JUMP_FORWARD        100  'to 100'
             96_0  COME_FROM            88  '88'
               96  ROT_TWO          
               98  POP_TOP          
            100_0  COME_FROM            94  '94'
              100  JUMP_IF_TRUE_OR_POP   154  'to 154'

 L. 935       102  LOAD_FAST                'self'
              104  LOAD_ATTR                allow_unicode
              106  JUMP_IF_FALSE_OR_POP   154  'to 154'

 L. 936       108  LOAD_STR                 '\xa0'
              110  LOAD_FAST                'ch'
              112  DUP_TOP          
              114  ROT_THREE        
              116  COMPARE_OP               <=
              118  JUMP_IF_FALSE_OR_POP   126  'to 126'
              120  LOAD_STR                 '\ud7ff'
              122  COMPARE_OP               <=
              124  JUMP_FORWARD        130  'to 130'
            126_0  COME_FROM           118  '118'
              126  ROT_TWO          
              128  POP_TOP          
            130_0  COME_FROM           124  '124'
              130  JUMP_IF_TRUE_OR_POP   154  'to 154'

 L. 937       132  LOAD_STR                 '\ue000'
              134  LOAD_FAST                'ch'
              136  DUP_TOP          
              138  ROT_THREE        
              140  COMPARE_OP               <=
              142  JUMP_IF_FALSE_OR_POP   150  'to 150'
              144  LOAD_STR                 '�'
              146  COMPARE_OP               <=
            148_0  COME_FROM           130  '130'
            148_1  COME_FROM           106  '106'
            148_2  COME_FROM           100  '100'
              148  JUMP_FORWARD        154  'to 154'
            150_0  COME_FROM           142  '142'
              150  ROT_TWO          
              152  POP_TOP          
            154_0  COME_FROM           148  '148'
              154  UNARY_NOT        
            156_0  COME_FROM            76  '76'
            156_1  COME_FROM            68  '68'
              156  POP_JUMP_IF_FALSE   388  'to 388'

 L. 938       160  LOAD_FAST                'start'
              162  LOAD_FAST                'end'
              164  COMPARE_OP               <
              166  POP_JUMP_IF_FALSE   232  'to 232'

 L. 939       168  LOAD_FAST                'text'
              170  LOAD_FAST                'start'
              172  LOAD_FAST                'end'
              174  BUILD_SLICE_2         2 
              176  BINARY_SUBSCR    
              178  STORE_FAST               'data'

 L. 940       180  LOAD_FAST                'self'
              182  DUP_TOP          
              184  LOAD_ATTR                column
              186  LOAD_GLOBAL              len
              188  LOAD_FAST                'data'
              190  CALL_FUNCTION_1       1  '1 positional argument'
              192  INPLACE_ADD      
              194  ROT_TWO          
              196  STORE_ATTR               column

 L. 941       198  LOAD_FAST                'self'
              200  LOAD_ATTR                encoding
              202  POP_JUMP_IF_FALSE   216  'to 216'

 L. 942       204  LOAD_FAST                'data'
              206  LOAD_ATTR                encode
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                encoding
              212  CALL_FUNCTION_1       1  '1 positional argument'
              214  STORE_FAST               'data'
            216_0  COME_FROM           202  '202'

 L. 943       216  LOAD_FAST                'self'
              218  LOAD_ATTR                stream
              220  LOAD_ATTR                write
              222  LOAD_FAST                'data'
              224  CALL_FUNCTION_1       1  '1 positional argument'
              226  POP_TOP          

 L. 944       228  LOAD_FAST                'end'
              230  STORE_FAST               'start'
            232_0  COME_FROM           166  '166'

 L. 945       232  LOAD_FAST                'ch'
              234  LOAD_CONST               None
              236  COMPARE_OP               is-not
              238  POP_JUMP_IF_FALSE   388  'to 388'

 L. 946       242  LOAD_FAST                'ch'
              244  LOAD_FAST                'self'
              246  LOAD_ATTR                ESCAPE_REPLACEMENTS
              248  COMPARE_OP               in
              250  POP_JUMP_IF_FALSE   270  'to 270'

 L. 947       254  LOAD_STR                 '\\'
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                ESCAPE_REPLACEMENTS
              260  LOAD_FAST                'ch'
              262  BINARY_SUBSCR    
              264  BINARY_ADD       
              266  STORE_FAST               'data'
              268  JUMP_FORWARD        330  'to 330'
              270  ELSE                     '330'

 L. 948       270  LOAD_FAST                'ch'
              272  LOAD_STR                 'ÿ'
              274  COMPARE_OP               <=
              276  POP_JUMP_IF_FALSE   294  'to 294'

 L. 949       280  LOAD_STR                 '\\x%02X'
              282  LOAD_GLOBAL              ord
              284  LOAD_FAST                'ch'
              286  CALL_FUNCTION_1       1  '1 positional argument'
              288  BINARY_MODULO    
              290  STORE_FAST               'data'
              292  JUMP_FORWARD        330  'to 330'
              294  ELSE                     '330'

 L. 950       294  LOAD_FAST                'ch'
              296  LOAD_STR                 '\uffff'
              298  COMPARE_OP               <=
              300  POP_JUMP_IF_FALSE   318  'to 318'

 L. 951       304  LOAD_STR                 '\\u%04X'
              306  LOAD_GLOBAL              ord
              308  LOAD_FAST                'ch'
              310  CALL_FUNCTION_1       1  '1 positional argument'
              312  BINARY_MODULO    
              314  STORE_FAST               'data'
              316  JUMP_FORWARD        330  'to 330'
              318  ELSE                     '330'

 L. 953       318  LOAD_STR                 '\\U%08X'
              320  LOAD_GLOBAL              ord
              322  LOAD_FAST                'ch'
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  BINARY_MODULO    
              328  STORE_FAST               'data'
            330_0  COME_FROM           316  '316'
            330_1  COME_FROM           292  '292'
            330_2  COME_FROM           268  '268'

 L. 954       330  LOAD_FAST                'self'
              332  DUP_TOP          
              334  LOAD_ATTR                column
              336  LOAD_GLOBAL              len
              338  LOAD_FAST                'data'
              340  CALL_FUNCTION_1       1  '1 positional argument'
              342  INPLACE_ADD      
              344  ROT_TWO          
              346  STORE_ATTR               column

 L. 955       348  LOAD_FAST                'self'
              350  LOAD_ATTR                encoding
              352  POP_JUMP_IF_FALSE   368  'to 368'

 L. 956       356  LOAD_FAST                'data'
              358  LOAD_ATTR                encode
              360  LOAD_FAST                'self'
              362  LOAD_ATTR                encoding
              364  CALL_FUNCTION_1       1  '1 positional argument'
              366  STORE_FAST               'data'
            368_0  COME_FROM           352  '352'

 L. 957       368  LOAD_FAST                'self'
              370  LOAD_ATTR                stream
              372  LOAD_ATTR                write
              374  LOAD_FAST                'data'
              376  CALL_FUNCTION_1       1  '1 positional argument'
              378  POP_TOP          

 L. 958       380  LOAD_FAST                'end'
              382  LOAD_CONST               1
              384  BINARY_ADD       
              386  STORE_FAST               'start'
            388_0  COME_FROM           238  '238'
            388_1  COME_FROM           156  '156'

 L. 959       388  LOAD_CONST               0
              390  LOAD_FAST                'end'
              392  DUP_TOP          
              394  ROT_THREE        
              396  COMPARE_OP               <
              398  JUMP_IF_FALSE_OR_POP   416  'to 416'
              402  LOAD_GLOBAL              len
              404  LOAD_FAST                'text'
              406  CALL_FUNCTION_1       1  '1 positional argument'
              408  LOAD_CONST               1
              410  BINARY_SUBTRACT  
              412  COMPARE_OP               <
              414  JUMP_FORWARD        420  'to 420'
            416_0  COME_FROM           398  '398'
              416  ROT_TWO          
              418  POP_TOP          
            420_0  COME_FROM           414  '414'
              420  POP_JUMP_IF_FALSE   640  'to 640'
              424  LOAD_FAST                'ch'
              426  LOAD_STR                 ' '
              428  COMPARE_OP               ==
              430  POP_JUMP_IF_TRUE    444  'to 444'
              434  LOAD_FAST                'start'
              436  LOAD_FAST                'end'
              438  COMPARE_OP               >=
            440_0  COME_FROM           430  '430'
              440  POP_JUMP_IF_FALSE   640  'to 640'

 L. 960       444  LOAD_FAST                'self'
              446  LOAD_ATTR                column
              448  LOAD_FAST                'end'
              450  LOAD_FAST                'start'
              452  BINARY_SUBTRACT  
              454  BINARY_ADD       
              456  LOAD_FAST                'self'
              458  LOAD_ATTR                best_width
              460  COMPARE_OP               >
              462  POP_JUMP_IF_FALSE   640  'to 640'
              466  LOAD_FAST                'split'
              468  POP_JUMP_IF_FALSE   640  'to 640'

 L. 961       472  LOAD_FAST                'text'
              474  LOAD_FAST                'start'
              476  LOAD_FAST                'end'
              478  BUILD_SLICE_2         2 
              480  BINARY_SUBSCR    
              482  LOAD_STR                 '\\'
              484  BINARY_ADD       
              486  STORE_FAST               'data'

 L. 962       488  LOAD_FAST                'start'
              490  LOAD_FAST                'end'
              492  COMPARE_OP               <
              494  POP_JUMP_IF_FALSE   502  'to 502'

 L. 963       498  LOAD_FAST                'end'
              500  STORE_FAST               'start'
            502_0  COME_FROM           494  '494'

 L. 964       502  LOAD_FAST                'self'
              504  DUP_TOP          
              506  LOAD_ATTR                column
              508  LOAD_GLOBAL              len
              510  LOAD_FAST                'data'
              512  CALL_FUNCTION_1       1  '1 positional argument'
              514  INPLACE_ADD      
              516  ROT_TWO          
              518  STORE_ATTR               column

 L. 965       520  LOAD_FAST                'self'
              522  LOAD_ATTR                encoding
              524  POP_JUMP_IF_FALSE   540  'to 540'

 L. 966       528  LOAD_FAST                'data'
              530  LOAD_ATTR                encode
              532  LOAD_FAST                'self'
              534  LOAD_ATTR                encoding
              536  CALL_FUNCTION_1       1  '1 positional argument'
              538  STORE_FAST               'data'
            540_0  COME_FROM           524  '524'

 L. 967       540  LOAD_FAST                'self'
              542  LOAD_ATTR                stream
              544  LOAD_ATTR                write
              546  LOAD_FAST                'data'
              548  CALL_FUNCTION_1       1  '1 positional argument'
              550  POP_TOP          

 L. 968       552  LOAD_FAST                'self'
              554  LOAD_ATTR                write_indent
              556  CALL_FUNCTION_0       0  '0 positional arguments'
              558  POP_TOP          

 L. 969       560  LOAD_CONST               False
              562  LOAD_FAST                'self'
              564  STORE_ATTR               whitespace

 L. 970       566  LOAD_CONST               False
              568  LOAD_FAST                'self'
              570  STORE_ATTR               indention

 L. 971       572  LOAD_FAST                'text'
              574  LOAD_FAST                'start'
              576  BINARY_SUBSCR    
              578  LOAD_STR                 ' '
              580  COMPARE_OP               ==
              582  POP_JUMP_IF_FALSE   640  'to 640'

 L. 972       586  LOAD_STR                 '\\'
              588  STORE_FAST               'data'

 L. 973       590  LOAD_FAST                'self'
              592  DUP_TOP          
              594  LOAD_ATTR                column
              596  LOAD_GLOBAL              len
              598  LOAD_FAST                'data'
              600  CALL_FUNCTION_1       1  '1 positional argument'
              602  INPLACE_ADD      
              604  ROT_TWO          
              606  STORE_ATTR               column

 L. 974       608  LOAD_FAST                'self'
              610  LOAD_ATTR                encoding
              612  POP_JUMP_IF_FALSE   628  'to 628'

 L. 975       616  LOAD_FAST                'data'
              618  LOAD_ATTR                encode
              620  LOAD_FAST                'self'
              622  LOAD_ATTR                encoding
              624  CALL_FUNCTION_1       1  '1 positional argument'
              626  STORE_FAST               'data'
            628_0  COME_FROM           612  '612'

 L. 976       628  LOAD_FAST                'self'
              630  LOAD_ATTR                stream
              632  LOAD_ATTR                write
              634  LOAD_FAST                'data'
              636  CALL_FUNCTION_1       1  '1 positional argument'
              638  POP_TOP          
            640_0  COME_FROM           582  '582'
            640_1  COME_FROM           468  '468'
            640_2  COME_FROM           462  '462'
            640_3  COME_FROM           440  '440'
            640_4  COME_FROM           420  '420'

 L. 977       640  LOAD_FAST                'end'
              642  LOAD_CONST               1
              644  INPLACE_ADD      
              646  STORE_FAST               'end'
              648  JUMP_BACK            24  'to 24'
            650_0  COME_FROM            34  '34'
              650  POP_BLOCK        
            652_0  COME_FROM_LOOP       20  '20'

 L. 978       652  LOAD_FAST                'self'
              654  LOAD_ATTR                write_indicator
              656  LOAD_STR                 '"'
              658  LOAD_CONST               False
              660  CALL_FUNCTION_2       2  '2 positional arguments'
              662  POP_TOP          

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 156

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
            else:
                if spaces:
                    if ch != ' ':
                        if start + 1 == end:
                            if self.column > self.best_width:
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
            if breaks:
                if ch is None or ch not in '\n\x85\u2028\u2029':
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
        while end <= len(text):
            ch = None
            if end < len(text):
                ch = text[end]
            if spaces:
                if ch != ' ':
                    if start + 1 == end:
                        if self.column > self.best_width:
                            if split:
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
            else:
                if breaks:
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