# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/ruamel/yaml/reader.py
# Compiled at: 2017-07-27 07:36:53
from __future__ import absolute_import
import codecs, re
try:
    from .error import YAMLError, Mark
    from .compat import text_type, binary_type, PY3
except (ImportError, ValueError):
    from ruamel.yaml.error import YAMLError, Mark
    from ruamel.yaml.compat import text_type, binary_type, PY3

__all__ = [
 'Reader', 'ReaderError']

class ReaderError(YAMLError):

    def __init__(self, name, position, character, encoding, reason):
        self.name = name
        self.character = character
        self.position = position
        self.encoding = encoding
        self.reason = reason

    def __str__(self):
        if isinstance(self.character, binary_type):
            return '\'%s\' codec can\'t decode byte #x%02x: %s\n  in "%s", position %d' % (
             self.encoding, ord(self.character), self.reason,
             self.name, self.position)
        else:
            return 'unacceptable character #x%04x: %s\n  in "%s", position %d' % (
             self.character, self.reason,
             self.name, self.position)


class Reader(object):

    def __init__(self, stream):
        self.name = None
        self.stream = None
        self.stream_pointer = 0
        self.eof = True
        self.buffer = ''
        self.pointer = 0
        self.raw_buffer = None
        self.raw_decode = None
        self.encoding = None
        self.index = 0
        self.line = 0
        self.column = 0
        if isinstance(stream, text_type):
            self.name = '<unicode string>'
            self.check_printable(stream)
            self.buffer = stream + '\x00'
        elif isinstance(stream, binary_type):
            self.name = '<byte string>'
            self.raw_buffer = stream
            self.determine_encoding()
        else:
            self.stream = stream
            self.name = getattr(stream, 'name', '<file>')
            self.eof = False
            self.raw_buffer = None
            self.determine_encoding()
        return

    def peek(self, index=0):
        try:
            return self.buffer[(self.pointer + index)]
        except IndexError:
            self.update(index + 1)
            return self.buffer[(self.pointer + index)]

    def prefix(self, length=1):
        if self.pointer + length >= len(self.buffer):
            self.update(length)
        return self.buffer[self.pointer:self.pointer + length]

    def forward(self, length=1):
        if self.pointer + length + 1 >= len(self.buffer):
            self.update(length + 1)
        while length:
            ch = self.buffer[self.pointer]
            self.pointer += 1
            self.index += 1
            if ch in '\n\x85\u2028\u2029' or ch == '\r' and self.buffer[self.pointer] != '\n':
                self.line += 1
                self.column = 0
            elif ch != '\ufeff':
                self.column += 1
            length -= 1

    def get_mark(self):
        if self.stream is None:
            return Mark(self.name, self.index, self.line, self.column, self.buffer, self.pointer)
        else:
            return Mark(self.name, self.index, self.line, self.column, None, None)
            return

    def determine_encoding(self):
        while not self.eof and (self.raw_buffer is None or len(self.raw_buffer) < 2):
            self.update_raw()

        if isinstance(self.raw_buffer, binary_type):
            if self.raw_buffer.startswith(codecs.BOM_UTF16_LE):
                self.raw_decode = codecs.utf_16_le_decode
                self.encoding = 'utf-16-le'
            elif self.raw_buffer.startswith(codecs.BOM_UTF16_BE):
                self.raw_decode = codecs.utf_16_be_decode
                self.encoding = 'utf-16-be'
            else:
                self.raw_decode = codecs.utf_8_decode
                self.encoding = 'utf-8'
        self.update(1)
        return

    NON_PRINTABLE = re.compile('[^\t\n\r -~\x85\xa0-\ud7ff\ue000-�]')

    def check_printable(self, data):
        match = self.NON_PRINTABLE.search(data)
        if match:
            character = match.group()
            position = self.index + (len(self.buffer) - self.pointer) + match.start()
            raise ReaderError(self.name, position, ord(character), 'unicode', 'special characters are not allowed')

    def update(self, length):
        if self.raw_buffer is None:
            return
        else:
            self.buffer = self.buffer[self.pointer:]
            self.pointer = 0
            while len(self.buffer) < length:
                if not self.eof:
                    self.update_raw()
                if self.raw_decode is not None:
                    try:
                        data, converted = self.raw_decode(self.raw_buffer, 'strict', self.eof)
                    except UnicodeDecodeError as exc:
                        if PY3:
                            character = self.raw_buffer[exc.start]
                        else:
                            character = exc.object[exc.start]
                        if self.stream is not None:
                            position = self.stream_pointer - len(self.raw_buffer) + exc.start
                        else:
                            position = exc.start
                        raise ReaderError(self.name, position, character, exc.encoding, exc.reason)

                else:
                    data = self.raw_buffer
                    converted = len(data)
                self.check_printable(data)
                self.buffer += data
                self.raw_buffer = self.raw_buffer[converted:]
                if self.eof:
                    self.buffer += '\x00'
                    self.raw_buffer = None
                    break

            return

    def update_raw(self, size=None):
        if size is None:
            size = 4096 if PY3 else 1024
        data = self.stream.read(size)
        if self.raw_buffer is None:
            self.raw_buffer = data
        else:
            self.raw_buffer += data
        self.stream_pointer += len(data)
        if not data:
            self.eof = True
        return