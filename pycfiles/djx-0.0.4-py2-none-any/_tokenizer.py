# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_vendor/html5lib/_tokenizer.py
# Compiled at: 2019-02-14 00:35:07
from __future__ import absolute_import, division, unicode_literals
from pip._vendor.six import unichr as chr
from collections import deque
from .constants import spaceCharacters
from .constants import entities
from .constants import asciiLetters, asciiUpper2Lower
from .constants import digits, hexDigits, EOF
from .constants import tokenTypes, tagTokenTypes
from .constants import replacementCharacters
from ._inputstream import HTMLInputStream
from ._trie import Trie
entitiesTrie = Trie(entities)

class HTMLTokenizer(object):
    """ This class takes care of tokenizing HTML.

    * self.currentToken
      Holds the token that is currently being processed.

    * self.state
      Holds a reference to the method to be invoked... XXX

    * self.stream
      Points to HTMLInputStream object.
    """

    def __init__(self, stream, parser=None, **kwargs):
        self.stream = HTMLInputStream(stream, **kwargs)
        self.parser = parser
        self.escapeFlag = False
        self.lastFourChars = []
        self.state = self.dataState
        self.escape = False
        self.currentToken = None
        super(HTMLTokenizer, self).__init__()
        return

    def __iter__(self):
        """ This is where the magic happens.

        We do our usually processing through the states and when we have a token
        to return we yield the token which pauses processing until the next token
        is requested.
        """
        self.tokenQueue = deque([])
        while self.state():
            while self.stream.errors:
                yield {b'type': tokenTypes[b'ParseError'], b'data': self.stream.errors.pop(0)}

            while self.tokenQueue:
                yield self.tokenQueue.popleft()

    def consumeNumberEntity(self, isHex):
        """This function returns either U+FFFD or the character based on the
        decimal or hexadecimal representation. It also discards ";" if present.
        If not present self.tokenQueue.append({"type": tokenTypes["ParseError"]}) is invoked.
        """
        allowed = digits
        radix = 10
        if isHex:
            allowed = hexDigits
            radix = 16
        charStack = []
        c = self.stream.char()
        while c in allowed and c is not EOF:
            charStack.append(c)
            c = self.stream.char()

        charAsInt = int((b'').join(charStack), radix)
        if charAsInt in replacementCharacters:
            char = replacementCharacters[charAsInt]
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'illegal-codepoint-for-numeric-entity', 
               b'datavars': {b'charAsInt': charAsInt}})
        elif 55296 <= charAsInt <= 57343 or charAsInt > 1114111:
            char = b'�'
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'illegal-codepoint-for-numeric-entity', 
               b'datavars': {b'charAsInt': charAsInt}})
        else:
            if 1 <= charAsInt <= 8 or 14 <= charAsInt <= 31 or 127 <= charAsInt <= 159 or 64976 <= charAsInt <= 65007 or charAsInt in frozenset([11, 65534, 65535, 131070,
             131071, 196606, 196607, 262142,
             262143, 327678, 327679, 393214,
             393215, 458750, 458751, 524286,
             524287, 589822, 589823, 655358,
             655359, 720894, 720895, 786430,
             786431, 851966, 851967, 917502,
             917503, 983038, 983039, 1048574,
             1048575, 1114110, 1114111]):
                self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'illegal-codepoint-for-numeric-entity', 
                   b'datavars': {b'charAsInt': charAsInt}})
            try:
                char = chr(charAsInt)
            except ValueError:
                v = charAsInt - 65536
                char = chr(55296 | v >> 10) + chr(56320 | v & 1023)

        if c != b';':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'numeric-entity-without-semicolon'})
            self.stream.unget(c)
        return char

    def consumeEntity(self, allowedChar=None, fromAttribute=False):
        output = b'&'
        charStack = [
         self.stream.char()]
        if charStack[0] in spaceCharacters or charStack[0] in (EOF, b'<', b'&') or allowedChar is not None and allowedChar == charStack[0]:
            self.stream.unget(charStack[0])
        elif charStack[0] == b'#':
            hex = False
            charStack.append(self.stream.char())
            if charStack[(-1)] in ('x', 'X'):
                hex = True
                charStack.append(self.stream.char())
            if hex and charStack[(-1)] in hexDigits or not hex and charStack[(-1)] in digits:
                self.stream.unget(charStack[(-1)])
                output = self.consumeNumberEntity(hex)
            else:
                self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'expected-numeric-entity'})
                self.stream.unget(charStack.pop())
                output = b'&' + (b'').join(charStack)
        else:
            while charStack[(-1)] is not EOF:
                if not entitiesTrie.has_keys_with_prefix((b'').join(charStack)):
                    break
                charStack.append(self.stream.char())

            try:
                entityName = entitiesTrie.longest_prefix((b'').join(charStack[:-1]))
                entityLength = len(entityName)
            except KeyError:
                entityName = None

            if entityName is not None:
                if entityName[(-1)] != b';':
                    self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'named-entity-without-semicolon'})
                if entityName[(-1)] != b';' and fromAttribute and (charStack[entityLength] in asciiLetters or charStack[entityLength] in digits or charStack[entityLength] == b'='):
                    self.stream.unget(charStack.pop())
                    output = b'&' + (b'').join(charStack)
                else:
                    output = entities[entityName]
                    self.stream.unget(charStack.pop())
                    output += (b'').join(charStack[entityLength:])
            else:
                self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'expected-named-entity'})
                self.stream.unget(charStack.pop())
                output = b'&' + (b'').join(charStack)
        if fromAttribute:
            self.currentToken[b'data'][(-1)][1] += output
        else:
            if output in spaceCharacters:
                tokenType = b'SpaceCharacters'
            else:
                tokenType = b'Characters'
            self.tokenQueue.append({b'type': tokenTypes[tokenType], b'data': output})
        return

    def processEntityInAttribute(self, allowedChar):
        """This method replaces the need for "entityInAttributeValueState".
        """
        self.consumeEntity(allowedChar=allowedChar, fromAttribute=True)

    def emitCurrentToken(self):
        """This method is a generic handler for emitting the tags. It also sets
        the state to "data" because that's what's needed after a token has been
        emitted.
        """
        token = self.currentToken
        if token[b'type'] in tagTokenTypes:
            token[b'name'] = token[b'name'].translate(asciiUpper2Lower)
            if token[b'type'] == tokenTypes[b'EndTag']:
                if token[b'data']:
                    self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'attributes-in-end-tag'})
                if token[b'selfClosing']:
                    self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'self-closing-flag-on-end-tag'})
        self.tokenQueue.append(token)
        self.state = self.dataState

    def dataState(self):
        data = self.stream.char()
        if data == b'&':
            self.state = self.entityDataState
        elif data == b'<':
            self.state = self.tagOpenState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'\x00'})
        else:
            if data is EOF:
                return False
            if data in spaceCharacters:
                self.tokenQueue.append({b'type': tokenTypes[b'SpaceCharacters'], b'data': data + self.stream.charsUntil(spaceCharacters, True)})
            else:
                chars = self.stream.charsUntil(('&', '<', '\x00'))
                self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': data + chars})
        return True

    def entityDataState(self):
        self.consumeEntity()
        self.state = self.dataState
        return True

    def rcdataState(self):
        data = self.stream.char()
        if data == b'&':
            self.state = self.characterReferenceInRcdata
        elif data == b'<':
            self.state = self.rcdataLessThanSignState
        else:
            if data == EOF:
                return False
            if data == b'\x00':
                self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
                self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'�'})
            elif data in spaceCharacters:
                self.tokenQueue.append({b'type': tokenTypes[b'SpaceCharacters'], b'data': data + self.stream.charsUntil(spaceCharacters, True)})
            else:
                chars = self.stream.charsUntil(('&', '<', '\x00'))
                self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': data + chars})
        return True

    def characterReferenceInRcdata(self):
        self.consumeEntity()
        self.state = self.rcdataState
        return True

    def rawtextState(self):
        data = self.stream.char()
        if data == b'<':
            self.state = self.rawtextLessThanSignState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'�'})
        else:
            if data == EOF:
                return False
            chars = self.stream.charsUntil(('<', '\x00'))
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': data + chars})
        return True

    def scriptDataState(self):
        data = self.stream.char()
        if data == b'<':
            self.state = self.scriptDataLessThanSignState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'�'})
        else:
            if data == EOF:
                return False
            chars = self.stream.charsUntil(('<', '\x00'))
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': data + chars})
        return True

    def plaintextState(self):
        data = self.stream.char()
        if data == EOF:
            return False
        if data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'�'})
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': data + self.stream.charsUntil(b'\x00')})
        return True

    def tagOpenState(self):
        data = self.stream.char()
        if data == b'!':
            self.state = self.markupDeclarationOpenState
        elif data == b'/':
            self.state = self.closeTagOpenState
        elif data in asciiLetters:
            self.currentToken = {b'type': tokenTypes[b'StartTag'], b'name': data, b'data': [], b'selfClosing': False, 
               b'selfClosingAcknowledged': False}
            self.state = self.tagNameState
        elif data == b'>':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'expected-tag-name-but-got-right-bracket'})
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'<>'})
            self.state = self.dataState
        elif data == b'?':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'expected-tag-name-but-got-question-mark'})
            self.stream.unget(data)
            self.state = self.bogusCommentState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'expected-tag-name'})
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'<'})
            self.stream.unget(data)
            self.state = self.dataState
        return True

    def closeTagOpenState(self):
        data = self.stream.char()
        if data in asciiLetters:
            self.currentToken = {b'type': tokenTypes[b'EndTag'], b'name': data, b'data': [], b'selfClosing': False}
            self.state = self.tagNameState
        elif data == b'>':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'expected-closing-tag-but-got-right-bracket'})
            self.state = self.dataState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'expected-closing-tag-but-got-eof'})
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'</'})
            self.state = self.dataState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'expected-closing-tag-but-got-char', 
               b'datavars': {b'data': data}})
            self.stream.unget(data)
            self.state = self.bogusCommentState
        return True

    def tagNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeAttributeNameState
        elif data == b'>':
            self.emitCurrentToken()
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-tag-name'})
            self.state = self.dataState
        elif data == b'/':
            self.state = self.selfClosingStartTagState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'name'] += b'�'
        else:
            self.currentToken[b'name'] += data
        return True

    def rcdataLessThanSignState(self):
        data = self.stream.char()
        if data == b'/':
            self.temporaryBuffer = b''
            self.state = self.rcdataEndTagOpenState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'<'})
            self.stream.unget(data)
            self.state = self.rcdataState
        return True

    def rcdataEndTagOpenState(self):
        data = self.stream.char()
        if data in asciiLetters:
            self.temporaryBuffer += data
            self.state = self.rcdataEndTagNameState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'</'})
            self.stream.unget(data)
            self.state = self.rcdataState
        return True

    def rcdataEndTagNameState(self):
        appropriate = self.currentToken and self.currentToken[b'name'].lower() == self.temporaryBuffer.lower()
        data = self.stream.char()
        if data in spaceCharacters and appropriate:
            self.currentToken = {b'type': tokenTypes[b'EndTag'], b'name': self.temporaryBuffer, b'data': [], b'selfClosing': False}
            self.state = self.beforeAttributeNameState
        elif data == b'/' and appropriate:
            self.currentToken = {b'type': tokenTypes[b'EndTag'], b'name': self.temporaryBuffer, b'data': [], b'selfClosing': False}
            self.state = self.selfClosingStartTagState
        elif data == b'>' and appropriate:
            self.currentToken = {b'type': tokenTypes[b'EndTag'], b'name': self.temporaryBuffer, b'data': [], b'selfClosing': False}
            self.emitCurrentToken()
            self.state = self.dataState
        elif data in asciiLetters:
            self.temporaryBuffer += data
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'</' + self.temporaryBuffer})
            self.stream.unget(data)
            self.state = self.rcdataState
        return True

    def rawtextLessThanSignState(self):
        data = self.stream.char()
        if data == b'/':
            self.temporaryBuffer = b''
            self.state = self.rawtextEndTagOpenState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'<'})
            self.stream.unget(data)
            self.state = self.rawtextState
        return True

    def rawtextEndTagOpenState(self):
        data = self.stream.char()
        if data in asciiLetters:
            self.temporaryBuffer += data
            self.state = self.rawtextEndTagNameState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'</'})
            self.stream.unget(data)
            self.state = self.rawtextState
        return True

    def rawtextEndTagNameState(self):
        appropriate = self.currentToken and self.currentToken[b'name'].lower() == self.temporaryBuffer.lower()
        data = self.stream.char()
        if data in spaceCharacters and appropriate:
            self.currentToken = {b'type': tokenTypes[b'EndTag'], b'name': self.temporaryBuffer, b'data': [], b'selfClosing': False}
            self.state = self.beforeAttributeNameState
        elif data == b'/' and appropriate:
            self.currentToken = {b'type': tokenTypes[b'EndTag'], b'name': self.temporaryBuffer, b'data': [], b'selfClosing': False}
            self.state = self.selfClosingStartTagState
        elif data == b'>' and appropriate:
            self.currentToken = {b'type': tokenTypes[b'EndTag'], b'name': self.temporaryBuffer, b'data': [], b'selfClosing': False}
            self.emitCurrentToken()
            self.state = self.dataState
        elif data in asciiLetters:
            self.temporaryBuffer += data
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'</' + self.temporaryBuffer})
            self.stream.unget(data)
            self.state = self.rawtextState
        return True

    def scriptDataLessThanSignState(self):
        data = self.stream.char()
        if data == b'/':
            self.temporaryBuffer = b''
            self.state = self.scriptDataEndTagOpenState
        elif data == b'!':
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'<!'})
            self.state = self.scriptDataEscapeStartState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'<'})
            self.stream.unget(data)
            self.state = self.scriptDataState
        return True

    def scriptDataEndTagOpenState(self):
        data = self.stream.char()
        if data in asciiLetters:
            self.temporaryBuffer += data
            self.state = self.scriptDataEndTagNameState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'</'})
            self.stream.unget(data)
            self.state = self.scriptDataState
        return True

    def scriptDataEndTagNameState(self):
        appropriate = self.currentToken and self.currentToken[b'name'].lower() == self.temporaryBuffer.lower()
        data = self.stream.char()
        if data in spaceCharacters and appropriate:
            self.currentToken = {b'type': tokenTypes[b'EndTag'], b'name': self.temporaryBuffer, b'data': [], b'selfClosing': False}
            self.state = self.beforeAttributeNameState
        elif data == b'/' and appropriate:
            self.currentToken = {b'type': tokenTypes[b'EndTag'], b'name': self.temporaryBuffer, b'data': [], b'selfClosing': False}
            self.state = self.selfClosingStartTagState
        elif data == b'>' and appropriate:
            self.currentToken = {b'type': tokenTypes[b'EndTag'], b'name': self.temporaryBuffer, b'data': [], b'selfClosing': False}
            self.emitCurrentToken()
            self.state = self.dataState
        elif data in asciiLetters:
            self.temporaryBuffer += data
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'</' + self.temporaryBuffer})
            self.stream.unget(data)
            self.state = self.scriptDataState
        return True

    def scriptDataEscapeStartState(self):
        data = self.stream.char()
        if data == b'-':
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'-'})
            self.state = self.scriptDataEscapeStartDashState
        else:
            self.stream.unget(data)
            self.state = self.scriptDataState
        return True

    def scriptDataEscapeStartDashState(self):
        data = self.stream.char()
        if data == b'-':
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'-'})
            self.state = self.scriptDataEscapedDashDashState
        else:
            self.stream.unget(data)
            self.state = self.scriptDataState
        return True

    def scriptDataEscapedState(self):
        data = self.stream.char()
        if data == b'-':
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'-'})
            self.state = self.scriptDataEscapedDashState
        elif data == b'<':
            self.state = self.scriptDataEscapedLessThanSignState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'�'})
        elif data == EOF:
            self.state = self.dataState
        else:
            chars = self.stream.charsUntil(('<', '-', '\x00'))
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': data + chars})
        return True

    def scriptDataEscapedDashState(self):
        data = self.stream.char()
        if data == b'-':
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'-'})
            self.state = self.scriptDataEscapedDashDashState
        elif data == b'<':
            self.state = self.scriptDataEscapedLessThanSignState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'�'})
            self.state = self.scriptDataEscapedState
        elif data == EOF:
            self.state = self.dataState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': data})
            self.state = self.scriptDataEscapedState
        return True

    def scriptDataEscapedDashDashState(self):
        data = self.stream.char()
        if data == b'-':
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'-'})
        elif data == b'<':
            self.state = self.scriptDataEscapedLessThanSignState
        elif data == b'>':
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'>'})
            self.state = self.scriptDataState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'�'})
            self.state = self.scriptDataEscapedState
        elif data == EOF:
            self.state = self.dataState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': data})
            self.state = self.scriptDataEscapedState
        return True

    def scriptDataEscapedLessThanSignState(self):
        data = self.stream.char()
        if data == b'/':
            self.temporaryBuffer = b''
            self.state = self.scriptDataEscapedEndTagOpenState
        elif data in asciiLetters:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'<' + data})
            self.temporaryBuffer = data
            self.state = self.scriptDataDoubleEscapeStartState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'<'})
            self.stream.unget(data)
            self.state = self.scriptDataEscapedState
        return True

    def scriptDataEscapedEndTagOpenState(self):
        data = self.stream.char()
        if data in asciiLetters:
            self.temporaryBuffer = data
            self.state = self.scriptDataEscapedEndTagNameState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'</'})
            self.stream.unget(data)
            self.state = self.scriptDataEscapedState
        return True

    def scriptDataEscapedEndTagNameState(self):
        appropriate = self.currentToken and self.currentToken[b'name'].lower() == self.temporaryBuffer.lower()
        data = self.stream.char()
        if data in spaceCharacters and appropriate:
            self.currentToken = {b'type': tokenTypes[b'EndTag'], b'name': self.temporaryBuffer, b'data': [], b'selfClosing': False}
            self.state = self.beforeAttributeNameState
        elif data == b'/' and appropriate:
            self.currentToken = {b'type': tokenTypes[b'EndTag'], b'name': self.temporaryBuffer, b'data': [], b'selfClosing': False}
            self.state = self.selfClosingStartTagState
        elif data == b'>' and appropriate:
            self.currentToken = {b'type': tokenTypes[b'EndTag'], b'name': self.temporaryBuffer, b'data': [], b'selfClosing': False}
            self.emitCurrentToken()
            self.state = self.dataState
        elif data in asciiLetters:
            self.temporaryBuffer += data
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'</' + self.temporaryBuffer})
            self.stream.unget(data)
            self.state = self.scriptDataEscapedState
        return True

    def scriptDataDoubleEscapeStartState(self):
        data = self.stream.char()
        if data in spaceCharacters | frozenset(('/', '>')):
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': data})
            if self.temporaryBuffer.lower() == b'script':
                self.state = self.scriptDataDoubleEscapedState
            else:
                self.state = self.scriptDataEscapedState
        elif data in asciiLetters:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': data})
            self.temporaryBuffer += data
        else:
            self.stream.unget(data)
            self.state = self.scriptDataEscapedState
        return True

    def scriptDataDoubleEscapedState(self):
        data = self.stream.char()
        if data == b'-':
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'-'})
            self.state = self.scriptDataDoubleEscapedDashState
        elif data == b'<':
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'<'})
            self.state = self.scriptDataDoubleEscapedLessThanSignState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'�'})
        elif data == EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-script-in-script'})
            self.state = self.dataState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': data})
        return True

    def scriptDataDoubleEscapedDashState(self):
        data = self.stream.char()
        if data == b'-':
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'-'})
            self.state = self.scriptDataDoubleEscapedDashDashState
        elif data == b'<':
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'<'})
            self.state = self.scriptDataDoubleEscapedLessThanSignState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'�'})
            self.state = self.scriptDataDoubleEscapedState
        elif data == EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-script-in-script'})
            self.state = self.dataState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': data})
            self.state = self.scriptDataDoubleEscapedState
        return True

    def scriptDataDoubleEscapedDashDashState(self):
        data = self.stream.char()
        if data == b'-':
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'-'})
        elif data == b'<':
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'<'})
            self.state = self.scriptDataDoubleEscapedLessThanSignState
        elif data == b'>':
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'>'})
            self.state = self.scriptDataState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'�'})
            self.state = self.scriptDataDoubleEscapedState
        elif data == EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-script-in-script'})
            self.state = self.dataState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': data})
            self.state = self.scriptDataDoubleEscapedState
        return True

    def scriptDataDoubleEscapedLessThanSignState(self):
        data = self.stream.char()
        if data == b'/':
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': b'/'})
            self.temporaryBuffer = b''
            self.state = self.scriptDataDoubleEscapeEndState
        else:
            self.stream.unget(data)
            self.state = self.scriptDataDoubleEscapedState
        return True

    def scriptDataDoubleEscapeEndState(self):
        data = self.stream.char()
        if data in spaceCharacters | frozenset(('/', '>')):
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': data})
            if self.temporaryBuffer.lower() == b'script':
                self.state = self.scriptDataEscapedState
            else:
                self.state = self.scriptDataDoubleEscapedState
        elif data in asciiLetters:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': data})
            self.temporaryBuffer += data
        else:
            self.stream.unget(data)
            self.state = self.scriptDataDoubleEscapedState
        return True

    def beforeAttributeNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.stream.charsUntil(spaceCharacters, True)
        elif data in asciiLetters:
            self.currentToken[b'data'].append([data, b''])
            self.state = self.attributeNameState
        elif data == b'>':
            self.emitCurrentToken()
        elif data == b'/':
            self.state = self.selfClosingStartTagState
        elif data in ("'", '"', '=', '<'):
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-character-in-attribute-name'})
            self.currentToken[b'data'].append([data, b''])
            self.state = self.attributeNameState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'data'].append([b'�', b''])
            self.state = self.attributeNameState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'expected-attribute-name-but-got-eof'})
            self.state = self.dataState
        else:
            self.currentToken[b'data'].append([data, b''])
            self.state = self.attributeNameState
        return True

    def attributeNameState(self):
        data = self.stream.char()
        leavingThisState = True
        emitToken = False
        if data == b'=':
            self.state = self.beforeAttributeValueState
        elif data in asciiLetters:
            self.currentToken[b'data'][(-1)][0] += data + self.stream.charsUntil(asciiLetters, True)
            leavingThisState = False
        elif data == b'>':
            emitToken = True
        elif data in spaceCharacters:
            self.state = self.afterAttributeNameState
        elif data == b'/':
            self.state = self.selfClosingStartTagState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'data'][(-1)][0] += b'�'
            leavingThisState = False
        elif data in ("'", '"', '<'):
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-character-in-attribute-name'})
            self.currentToken[b'data'][(-1)][0] += data
            leavingThisState = False
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-attribute-name'})
            self.state = self.dataState
        else:
            self.currentToken[b'data'][(-1)][0] += data
            leavingThisState = False
        if leavingThisState:
            self.currentToken[b'data'][(-1)][0] = self.currentToken[b'data'][(-1)][0].translate(asciiUpper2Lower)
            for name, _ in self.currentToken[b'data'][:-1]:
                if self.currentToken[b'data'][(-1)][0] == name:
                    self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'duplicate-attribute'})
                    break

            if emitToken:
                self.emitCurrentToken()
        return True

    def afterAttributeNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.stream.charsUntil(spaceCharacters, True)
        elif data == b'=':
            self.state = self.beforeAttributeValueState
        elif data == b'>':
            self.emitCurrentToken()
        elif data in asciiLetters:
            self.currentToken[b'data'].append([data, b''])
            self.state = self.attributeNameState
        elif data == b'/':
            self.state = self.selfClosingStartTagState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'data'].append([b'�', b''])
            self.state = self.attributeNameState
        elif data in ("'", '"', '<'):
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-character-after-attribute-name'})
            self.currentToken[b'data'].append([data, b''])
            self.state = self.attributeNameState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'expected-end-of-tag-but-got-eof'})
            self.state = self.dataState
        else:
            self.currentToken[b'data'].append([data, b''])
            self.state = self.attributeNameState
        return True

    def beforeAttributeValueState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.stream.charsUntil(spaceCharacters, True)
        elif data == b'"':
            self.state = self.attributeValueDoubleQuotedState
        elif data == b'&':
            self.state = self.attributeValueUnQuotedState
            self.stream.unget(data)
        elif data == b"'":
            self.state = self.attributeValueSingleQuotedState
        elif data == b'>':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'expected-attribute-value-but-got-right-bracket'})
            self.emitCurrentToken()
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'data'][(-1)][1] += b'�'
            self.state = self.attributeValueUnQuotedState
        elif data in ('=', '<', '`'):
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'equals-in-unquoted-attribute-value'})
            self.currentToken[b'data'][(-1)][1] += data
            self.state = self.attributeValueUnQuotedState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'expected-attribute-value-but-got-eof'})
            self.state = self.dataState
        else:
            self.currentToken[b'data'][(-1)][1] += data
            self.state = self.attributeValueUnQuotedState
        return True

    def attributeValueDoubleQuotedState(self):
        data = self.stream.char()
        if data == b'"':
            self.state = self.afterAttributeValueState
        elif data == b'&':
            self.processEntityInAttribute(b'"')
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'data'][(-1)][1] += b'�'
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-attribute-value-double-quote'})
            self.state = self.dataState
        else:
            self.currentToken[b'data'][(-1)][1] += data + self.stream.charsUntil(('"',
                                                                                  '&',
                                                                                  '\x00'))
        return True

    def attributeValueSingleQuotedState(self):
        data = self.stream.char()
        if data == b"'":
            self.state = self.afterAttributeValueState
        elif data == b'&':
            self.processEntityInAttribute(b"'")
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'data'][(-1)][1] += b'�'
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-attribute-value-single-quote'})
            self.state = self.dataState
        else:
            self.currentToken[b'data'][(-1)][1] += data + self.stream.charsUntil(("'",
                                                                                  '&',
                                                                                  '\x00'))
        return True

    def attributeValueUnQuotedState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeAttributeNameState
        elif data == b'&':
            self.processEntityInAttribute(b'>')
        elif data == b'>':
            self.emitCurrentToken()
        elif data in ('"', "'", '=', '<', '`'):
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-character-in-unquoted-attribute-value'})
            self.currentToken[b'data'][(-1)][1] += data
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'data'][(-1)][1] += b'�'
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-attribute-value-no-quotes'})
            self.state = self.dataState
        else:
            self.currentToken[b'data'][(-1)][1] += data + self.stream.charsUntil(frozenset(('&',
                                                                                            '>',
                                                                                            '"',
                                                                                            "'",
                                                                                            '=',
                                                                                            '<',
                                                                                            '`',
                                                                                            '\x00')) | spaceCharacters)
        return True

    def afterAttributeValueState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeAttributeNameState
        elif data == b'>':
            self.emitCurrentToken()
        elif data == b'/':
            self.state = self.selfClosingStartTagState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-EOF-after-attribute-value'})
            self.stream.unget(data)
            self.state = self.dataState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-character-after-attribute-value'})
            self.stream.unget(data)
            self.state = self.beforeAttributeNameState
        return True

    def selfClosingStartTagState(self):
        data = self.stream.char()
        if data == b'>':
            self.currentToken[b'selfClosing'] = True
            self.emitCurrentToken()
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-EOF-after-solidus-in-tag'})
            self.stream.unget(data)
            self.state = self.dataState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-character-after-solidus-in-tag'})
            self.stream.unget(data)
            self.state = self.beforeAttributeNameState
        return True

    def bogusCommentState(self):
        data = self.stream.charsUntil(b'>')
        data = data.replace(b'\x00', b'�')
        self.tokenQueue.append({b'type': tokenTypes[b'Comment'], b'data': data})
        self.stream.char()
        self.state = self.dataState
        return True

    def markupDeclarationOpenState(self):
        charStack = [
         self.stream.char()]
        if charStack[(-1)] == b'-':
            charStack.append(self.stream.char())
            if charStack[(-1)] == b'-':
                self.currentToken = {b'type': tokenTypes[b'Comment'], b'data': b''}
                self.state = self.commentStartState
                return True
        else:
            if charStack[(-1)] in ('d', 'D'):
                matched = True
                for expected in (('o', 'O'), ('c', 'C'), ('t', 'T'),
                 ('y', 'Y'), ('p', 'P'), ('e', 'E')):
                    charStack.append(self.stream.char())
                    if charStack[(-1)] not in expected:
                        matched = False
                        break

                if matched:
                    self.currentToken = {b'type': tokenTypes[b'Doctype'], b'name': b'', b'publicId': None, 
                       b'systemId': None, b'correct': True}
                    self.state = self.doctypeState
                    return True
            elif charStack[(-1)] == b'[' and self.parser is not None and self.parser.tree.openElements and self.parser.tree.openElements[(-1)].namespace != self.parser.tree.defaultNamespace:
                matched = True
                for expected in [b'C', b'D', b'A', b'T', b'A', b'[']:
                    charStack.append(self.stream.char())
                    if charStack[(-1)] != expected:
                        matched = False
                        break

                if matched:
                    self.state = self.cdataSectionState
                    return True
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'expected-dashes-or-doctype'})
            while charStack:
                self.stream.unget(charStack.pop())

        self.state = self.bogusCommentState
        return True

    def commentStartState(self):
        data = self.stream.char()
        if data == b'-':
            self.state = self.commentStartDashState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'data'] += b'�'
        elif data == b'>':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'incorrect-comment'})
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-comment'})
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.currentToken[b'data'] += data
            self.state = self.commentState
        return True

    def commentStartDashState(self):
        data = self.stream.char()
        if data == b'-':
            self.state = self.commentEndState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'data'] += b'-�'
        elif data == b'>':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'incorrect-comment'})
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-comment'})
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.currentToken[b'data'] += b'-' + data
            self.state = self.commentState
        return True

    def commentState(self):
        data = self.stream.char()
        if data == b'-':
            self.state = self.commentEndDashState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'data'] += b'�'
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-comment'})
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.currentToken[b'data'] += data + self.stream.charsUntil(('-', '\x00'))
        return True

    def commentEndDashState(self):
        data = self.stream.char()
        if data == b'-':
            self.state = self.commentEndState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'data'] += b'-�'
            self.state = self.commentState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-comment-end-dash'})
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.currentToken[b'data'] += b'-' + data
            self.state = self.commentState
        return True

    def commentEndState(self):
        data = self.stream.char()
        if data == b'>':
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'data'] += b'--�'
            self.state = self.commentState
        elif data == b'!':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-bang-after-double-dash-in-comment'})
            self.state = self.commentEndBangState
        elif data == b'-':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-dash-after-double-dash-in-comment'})
            self.currentToken[b'data'] += data
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-comment-double-dash'})
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-char-in-comment'})
            self.currentToken[b'data'] += b'--' + data
            self.state = self.commentState
        return True

    def commentEndBangState(self):
        data = self.stream.char()
        if data == b'>':
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data == b'-':
            self.currentToken[b'data'] += b'--!'
            self.state = self.commentEndDashState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'data'] += b'--!�'
            self.state = self.commentState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-comment-end-bang-state'})
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.currentToken[b'data'] += b'--!' + data
            self.state = self.commentState
        return True

    def doctypeState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeDoctypeNameState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'expected-doctype-name-but-got-eof'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'need-space-after-doctype'})
            self.stream.unget(data)
            self.state = self.beforeDoctypeNameState
        return True

    def beforeDoctypeNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        elif data == b'>':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'expected-doctype-name-but-got-right-bracket'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'name'] = b'�'
            self.state = self.doctypeNameState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'expected-doctype-name-but-got-eof'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.currentToken[b'name'] = data
            self.state = self.doctypeNameState
        return True

    def doctypeNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.currentToken[b'name'] = self.currentToken[b'name'].translate(asciiUpper2Lower)
            self.state = self.afterDoctypeNameState
        elif data == b'>':
            self.currentToken[b'name'] = self.currentToken[b'name'].translate(asciiUpper2Lower)
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'name'] += b'�'
            self.state = self.doctypeNameState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-doctype-name'})
            self.currentToken[b'correct'] = False
            self.currentToken[b'name'] = self.currentToken[b'name'].translate(asciiUpper2Lower)
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.currentToken[b'name'] += data
        return True

    def afterDoctypeNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        elif data == b'>':
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data is EOF:
            self.currentToken[b'correct'] = False
            self.stream.unget(data)
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-doctype'})
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            if data in ('p', 'P'):
                matched = True
                for expected in (('u', 'U'), ('b', 'B'), ('l', 'L'),
                 ('i', 'I'), ('c', 'C')):
                    data = self.stream.char()
                    if data not in expected:
                        matched = False
                        break

                if matched:
                    self.state = self.afterDoctypePublicKeywordState
                    return True
            elif data in ('s', 'S'):
                matched = True
                for expected in (('y', 'Y'), ('s', 'S'), ('t', 'T'),
                 ('e', 'E'), ('m', 'M')):
                    data = self.stream.char()
                    if data not in expected:
                        matched = False
                        break

                if matched:
                    self.state = self.afterDoctypeSystemKeywordState
                    return True
            self.stream.unget(data)
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'expected-space-or-right-bracket-in-doctype', 
               b'datavars': {b'data': data}})
            self.currentToken[b'correct'] = False
            self.state = self.bogusDoctypeState
        return True

    def afterDoctypePublicKeywordState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeDoctypePublicIdentifierState
        elif data in ("'", '"'):
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-char-in-doctype'})
            self.stream.unget(data)
            self.state = self.beforeDoctypePublicIdentifierState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-doctype'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.stream.unget(data)
            self.state = self.beforeDoctypePublicIdentifierState
        return True

    def beforeDoctypePublicIdentifierState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        elif data == b'"':
            self.currentToken[b'publicId'] = b''
            self.state = self.doctypePublicIdentifierDoubleQuotedState
        elif data == b"'":
            self.currentToken[b'publicId'] = b''
            self.state = self.doctypePublicIdentifierSingleQuotedState
        elif data == b'>':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-end-of-doctype'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-doctype'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-char-in-doctype'})
            self.currentToken[b'correct'] = False
            self.state = self.bogusDoctypeState
        return True

    def doctypePublicIdentifierDoubleQuotedState(self):
        data = self.stream.char()
        if data == b'"':
            self.state = self.afterDoctypePublicIdentifierState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'publicId'] += b'�'
        elif data == b'>':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-end-of-doctype'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-doctype'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.currentToken[b'publicId'] += data
        return True

    def doctypePublicIdentifierSingleQuotedState(self):
        data = self.stream.char()
        if data == b"'":
            self.state = self.afterDoctypePublicIdentifierState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'publicId'] += b'�'
        elif data == b'>':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-end-of-doctype'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-doctype'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.currentToken[b'publicId'] += data
        return True

    def afterDoctypePublicIdentifierState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.betweenDoctypePublicAndSystemIdentifiersState
        elif data == b'>':
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data == b'"':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-char-in-doctype'})
            self.currentToken[b'systemId'] = b''
            self.state = self.doctypeSystemIdentifierDoubleQuotedState
        elif data == b"'":
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-char-in-doctype'})
            self.currentToken[b'systemId'] = b''
            self.state = self.doctypeSystemIdentifierSingleQuotedState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-doctype'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-char-in-doctype'})
            self.currentToken[b'correct'] = False
            self.state = self.bogusDoctypeState
        return True

    def betweenDoctypePublicAndSystemIdentifiersState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        elif data == b'>':
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data == b'"':
            self.currentToken[b'systemId'] = b''
            self.state = self.doctypeSystemIdentifierDoubleQuotedState
        elif data == b"'":
            self.currentToken[b'systemId'] = b''
            self.state = self.doctypeSystemIdentifierSingleQuotedState
        elif data == EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-doctype'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-char-in-doctype'})
            self.currentToken[b'correct'] = False
            self.state = self.bogusDoctypeState
        return True

    def afterDoctypeSystemKeywordState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeDoctypeSystemIdentifierState
        elif data in ("'", '"'):
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-char-in-doctype'})
            self.stream.unget(data)
            self.state = self.beforeDoctypeSystemIdentifierState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-doctype'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.stream.unget(data)
            self.state = self.beforeDoctypeSystemIdentifierState
        return True

    def beforeDoctypeSystemIdentifierState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        elif data == b'"':
            self.currentToken[b'systemId'] = b''
            self.state = self.doctypeSystemIdentifierDoubleQuotedState
        elif data == b"'":
            self.currentToken[b'systemId'] = b''
            self.state = self.doctypeSystemIdentifierSingleQuotedState
        elif data == b'>':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-char-in-doctype'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-doctype'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-char-in-doctype'})
            self.currentToken[b'correct'] = False
            self.state = self.bogusDoctypeState
        return True

    def doctypeSystemIdentifierDoubleQuotedState(self):
        data = self.stream.char()
        if data == b'"':
            self.state = self.afterDoctypeSystemIdentifierState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'systemId'] += b'�'
        elif data == b'>':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-end-of-doctype'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-doctype'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.currentToken[b'systemId'] += data
        return True

    def doctypeSystemIdentifierSingleQuotedState(self):
        data = self.stream.char()
        if data == b"'":
            self.state = self.afterDoctypeSystemIdentifierState
        elif data == b'\x00':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})
            self.currentToken[b'systemId'] += b'�'
        elif data == b'>':
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-end-of-doctype'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-doctype'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.currentToken[b'systemId'] += data
        return True

    def afterDoctypeSystemIdentifierState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        elif data == b'>':
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data is EOF:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'eof-in-doctype'})
            self.currentToken[b'correct'] = False
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'unexpected-char-in-doctype'})
            self.state = self.bogusDoctypeState
        return True

    def bogusDoctypeState(self):
        data = self.stream.char()
        if data == b'>':
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data is EOF:
            self.stream.unget(data)
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        return True

    def cdataSectionState(self):
        data = []
        while True:
            data.append(self.stream.charsUntil(b']'))
            data.append(self.stream.charsUntil(b'>'))
            char = self.stream.char()
            if char == EOF:
                break
            else:
                assert char == b'>'
                if data[(-1)][-2:] == b']]':
                    data[-1] = data[(-1)][:-2]
                    break
                else:
                    data.append(char)

        data = (b'').join(data)
        nullCount = data.count(b'\x00')
        if nullCount > 0:
            for _ in range(nullCount):
                self.tokenQueue.append({b'type': tokenTypes[b'ParseError'], b'data': b'invalid-codepoint'})

            data = data.replace(b'\x00', b'�')
        if data:
            self.tokenQueue.append({b'type': tokenTypes[b'Characters'], b'data': data})
        self.state = self.dataState
        return True