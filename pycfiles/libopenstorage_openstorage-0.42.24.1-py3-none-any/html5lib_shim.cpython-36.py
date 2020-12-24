# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/bleach/bleach/html5lib_shim.py
# Compiled at: 2020-01-10 16:25:34
# Size of source mod 2**32: 17929 bytes
"""
Shim module between Bleach and html5lib. This makes it easier to upgrade the
html5lib library without having to change a lot of code.
"""
from __future__ import unicode_literals
import re, string, six
from bleach._vendor.html5lib import HTMLParser, getTreeWalker
from bleach._vendor.html5lib import constants
from bleach._vendor.html5lib.constants import namespaces, prefixes
from bleach._vendor.html5lib.constants import _ReparseException as ReparseException
from bleach._vendor.html5lib.filters.base import Filter
from bleach._vendor.html5lib.filters.sanitizer import allowed_protocols
from bleach._vendor.html5lib.filters.sanitizer import Filter as SanitizerFilter
from bleach._vendor.html5lib._inputstream import HTMLInputStream
from bleach._vendor.html5lib.serializer import HTMLSerializer
from bleach._vendor.html5lib._tokenizer import HTMLTokenizer
from bleach._vendor.html5lib._trie import Trie
ENTITIES = constants.entities
ENTITIES_TRIE = Trie(ENTITIES)
TAG_TOKEN_TYPES = set([
 constants.tokenTypes['StartTag'],
 constants.tokenTypes['EndTag'],
 constants.tokenTypes['EmptyTag']])
CHARACTERS_TYPE = constants.tokenTypes['Characters']
PARSEERROR_TYPE = constants.tokenTypes['ParseError']
HTML_TAGS = [
 'a',
 'abbr',
 'address',
 'area',
 'article',
 'aside',
 'audio',
 'b',
 'base',
 'bdi',
 'bdo',
 'blockquote',
 'body',
 'br',
 'button',
 'canvas',
 'caption',
 'cite',
 'code',
 'col',
 'colgroup',
 'data',
 'datalist',
 'dd',
 'del',
 'details',
 'dfn',
 'dialog',
 'div',
 'dl',
 'dt',
 'em',
 'embed',
 'fieldset',
 'figcaption',
 'figure',
 'footer',
 'form',
 'h1',
 'h2',
 'h3',
 'h4',
 'h5',
 'h6',
 'head',
 'header',
 'hgroup',
 'hr',
 'html',
 'i',
 'iframe',
 'img',
 'input',
 'ins',
 'kbd',
 'keygen',
 'label',
 'legend',
 'li',
 'link',
 'map',
 'mark',
 'menu',
 'meta',
 'meter',
 'nav',
 'noscript',
 'object',
 'ol',
 'optgroup',
 'option',
 'output',
 'p',
 'param',
 'picture',
 'pre',
 'progress',
 'q',
 'rp',
 'rt',
 'ruby',
 's',
 'samp',
 'script',
 'section',
 'select',
 'slot',
 'small',
 'source',
 'span',
 'strong',
 'style',
 'sub',
 'summary',
 'sup',
 'table',
 'tbody',
 'td',
 'template',
 'textarea',
 'tfoot',
 'th',
 'thead',
 'time',
 'title',
 'tr',
 'track',
 'u',
 'ul',
 'var',
 'video',
 'wbr']

class InputStreamWithMemory(object):
    __doc__ = 'Wraps an HTMLInputStream to remember characters since last <\n\n    This wraps existing HTMLInputStream classes to keep track of the stream\n    since the last < which marked an open tag state.\n\n    '

    def __init__(self, inner_stream):
        self._inner_stream = inner_stream
        self.reset = self._inner_stream.reset
        self.position = self._inner_stream.position
        self._buffer = []

    @property
    def errors(self):
        return self._inner_stream.errors

    @property
    def charEncoding(self):
        return self._inner_stream.charEncoding

    @property
    def changeEncoding(self):
        return self._inner_stream.changeEncoding

    def char(self):
        c = self._inner_stream.char()
        if c:
            self._buffer.append(c)
        return c

    def charsUntil(self, characters, opposite=False):
        chars = self._inner_stream.charsUntil(characters, opposite=opposite)
        self._buffer.extend(list(chars))
        return chars

    def unget(self, char):
        if self._buffer:
            self._buffer.pop(-1)
        return self._inner_stream.unget(char)

    def get_tag(self):
        """Returns the stream history since last '<'

        Since the buffer starts at the last '<' as as seen by tagOpenState(),
        we know that everything from that point to when this method is called
        is the "tag" that is being tokenized.

        """
        return six.text_type('').join(self._buffer)

    def start_tag(self):
        """Resets stream history to just '<'

        This gets called by tagOpenState() which marks a '<' that denotes an
        open tag. Any time we see that, we reset the buffer.

        """
        self._buffer = [
         '<']


class BleachHTMLTokenizer(HTMLTokenizer):
    __doc__ = "Tokenizer that doesn't consume character entities"

    def __init__(self, consume_entities=False, **kwargs):
        (super(BleachHTMLTokenizer, self).__init__)(**kwargs)
        self.consume_entities = consume_entities
        self.stream = InputStreamWithMemory(self.stream)

    def __iter__(self):
        last_error_token = None
        for token in super(BleachHTMLTokenizer, self).__iter__():
            if last_error_token is not None:
                if last_error_token['data'] == 'invalid-character-in-attribute-name':
                    if token['type'] in TAG_TOKEN_TYPES:
                        if token.get('data'):
                            token['data'] = [item for item in token['data'] if '"' not in item[0] if "'" not in item[0] if '<' not in item[0]]
                            last_error_token = None
                            yield token
                if last_error_token['data'] == 'expected-closing-tag-but-got-char':
                    if token['data'].lower().strip() not in self.parser.tags:
                        token['data'] = self.stream.get_tag()
                        token['type'] = CHARACTERS_TYPE
                        last_error_token = None
                        yield token
                if token['type'] == PARSEERROR_TYPE:
                    yield last_error_token
                    last_error_token = token
                else:
                    yield last_error_token
                    yield token
                    last_error_token = None
            elif token['type'] == PARSEERROR_TYPE:
                last_error_token = token
            else:
                yield token

        if last_error_token:
            yield last_error_token

    def consumeEntity(self, allowedChar=None, fromAttribute=False):
        if self.consume_entities:
            return super(BleachHTMLTokenizer, self).consumeEntity(allowedChar, fromAttribute)
        else:
            if fromAttribute:
                self.currentToken['data'][(-1)][1] += '&'
            else:
                self.tokenQueue.append({'type':CHARACTERS_TYPE,  'data':'&'})

    def tagOpenState(self):
        self.stream.start_tag()
        return super(BleachHTMLTokenizer, self).tagOpenState()

    def emitCurrentToken(self):
        token = self.currentToken
        if self.parser.tags is not None:
            if token['type'] in TAG_TOKEN_TYPES:
                if token['name'].lower() not in self.parser.tags:
                    if self.parser.strip:
                        new_data = ''
                    else:
                        new_data = self.stream.get_tag()
                    new_token = {'type':CHARACTERS_TYPE, 
                     'data':new_data}
                    self.currentToken = new_token
                    self.tokenQueue.append(new_token)
                    self.state = self.dataState
                    return
        super(BleachHTMLTokenizer, self).emitCurrentToken()


class BleachHTMLParser(HTMLParser):
    __doc__ = 'Parser that uses BleachHTMLTokenizer'

    def __init__(self, tags, strip, consume_entities, **kwargs):
        self.tags = [tag.lower() for tag in tags] if tags is not None else None
        self.strip = strip
        self.consume_entities = consume_entities
        (super(BleachHTMLParser, self).__init__)(**kwargs)

    def _parse(self, stream, innerHTML=False, container='div', scripting=False, **kwargs):
        self.innerHTMLMode = innerHTML
        self.container = container
        self.scripting = scripting
        self.tokenizer = BleachHTMLTokenizer(stream=stream, 
         consume_entities=self.consume_entities, 
         parser=self, **kwargs)
        self.reset()
        try:
            self.mainLoop()
        except ReparseException:
            self.reset()
            self.mainLoop()


def convert_entity(value):
    """Convert an entity (minus the & and ; part) into what it represents

    This handles numeric, hex, and text entities.

    :arg value: the string (minus the ``&`` and ``;`` part) to convert

    :returns: unicode character or None if it's an ambiguous ampersand that
        doesn't match a character entity

    """
    if value[0] == '#':
        if value[1] in ('x', 'X'):
            return six.unichr(int(value[2:], 16))
        return six.unichr(int(value[1:], 10))
    else:
        return ENTITIES.get(value, None)


def convert_entities(text):
    """Converts all found entities in the text

    :arg text: the text to convert entities in

    :returns: unicode text with converted entities

    """
    if '&' not in text:
        return text
    else:
        new_text = []
        for part in next_possible_entity(text):
            if not part:
                pass
            else:
                if part.startswith('&'):
                    entity = match_entity(part)
                    if entity is not None:
                        converted = convert_entity(entity)
                        if converted is not None:
                            new_text.append(converted)
                            remainder = part[len(entity) + 2:]
                            if part:
                                new_text.append(remainder)
                                continue
                    new_text.append(part)

        return ''.join(new_text)


def match_entity(stream):
    """Returns first entity in stream or None if no entity exists

    Note: For Bleach purposes, entities must start with a "&" and end with
    a ";". This ignoresambiguous character entities that have no ";" at the
    end.

    :arg stream: the character stream

    :returns: ``None`` or the entity string without "&" or ";"

    """
    if stream[0] != '&':
        raise ValueError('Stream should begin with "&"')
    else:
        stream = stream[1:]
        stream = list(stream)
        possible_entity = ''
        end_characters = '<&=;' + string.whitespace
        if stream:
            if stream[0] == '#':
                possible_entity = '#'
                stream.pop(0)
                if stream:
                    if stream[0] in ('x', 'X'):
                        allowed = '0123456789abcdefABCDEF'
                        possible_entity += stream.pop(0)
                else:
                    allowed = '0123456789'
                while stream and stream[0] not in end_characters:
                    c = stream.pop(0)
                    if c not in allowed:
                        break
                    possible_entity += c

                if possible_entity:
                    if stream:
                        if stream[0] == ';':
                            return possible_entity
                return
        while stream and stream[0] not in end_characters:
            c = stream.pop(0)
            if not ENTITIES_TRIE.has_keys_with_prefix(possible_entity):
                break
            possible_entity += c

        if possible_entity:
            if stream:
                if stream[0] == ';':
                    return possible_entity


AMP_SPLIT_RE = re.compile('(&)')

def next_possible_entity(text):
    """Takes a text and generates a list of possible entities

    :arg text: the text to look at

    :returns: generator where each part (except the first) starts with an
        "&"

    """
    for i, part in enumerate(AMP_SPLIT_RE.split(text)):
        if i == 0:
            yield part
        else:
            if i % 2 == 0:
                yield '&' + part


class BleachHTMLSerializer(HTMLSerializer):
    __doc__ = 'HTMLSerializer that undoes & -> &amp; in attributes'

    def escape_base_amp(self, stoken):
        """Escapes just bare & in HTML attribute values"""
        stoken = stoken.replace('&amp;', '&')
        for part in next_possible_entity(stoken):
            if not part:
                pass
            else:
                if part.startswith('&'):
                    entity = match_entity(part)
                    if entity is not None:
                        if convert_entity(entity) is not None:
                            yield '&' + entity + ';'
                            part = part[len(entity) + 2:]
                            if part:
                                yield part
                                continue
                    yield part.replace('&', '&amp;')

    def serialize(self, treewalker, encoding=None):
        """Wrap HTMLSerializer.serialize and conver & to &amp; in attribute values

        Note that this converts & to &amp; in attribute values where the & isn't
        already part of an unambiguous character entity.

        """
        in_tag = False
        after_equals = False
        for stoken in super(BleachHTMLSerializer, self).serialize(treewalker, encoding):
            if in_tag:
                if stoken == '>':
                    in_tag = False
                else:
                    if after_equals:
                        if stoken != '"':
                            for part in self.escape_base_amp(stoken):
                                yield part

                            after_equals = False
                            continue
                    else:
                        if stoken == '=':
                            after_equals = True
                yield stoken
            else:
                if stoken.startswith('<'):
                    in_tag = True
                yield stoken