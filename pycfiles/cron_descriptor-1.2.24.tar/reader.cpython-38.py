# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./vendor/yaml/reader.py
# Compiled at: 2019-02-27 21:17:00
# Size of source mod 2**32: 6794 bytes
__all__ = [
 'Reader', 'ReaderError']
from .error import YAMLError, Mark
import codecs, re

class ReaderError(YAMLError):

    def __init__(self, name, position, character, encoding, reason):
        self.name = name
        self.character = character
        self.position = position
        self.encoding = encoding
        self.reason = reason

    def __str__(self):
        if isinstance(self.character, bytes):
            return '\'%s\' codec can\'t decode byte #x%02x: %s\n  in "%s", position %d' % (
             self.encoding, ord(self.character), self.reason,
             self.name, self.position)
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
        if isinstance(stream, str):
            self.name = '<unicode string>'
            self.check_printable(stream)
            self.buffer = stream + '\x00'
        elif isinstance(stream, bytes):
            self.name = '<byte string>'
            self.raw_buffer = stream
            self.determine_encoding()
        else:
            self.stream = stream
            self.name = getattr(stream, 'name', '<file>')
            self.eof = False
            self.raw_buffer = None
            self.determine_encoding()

    def peek--- This code section failed: ---

 L.  88         0  SETUP_FINALLY        20  'to 20'

 L.  89         2  LOAD_FAST                'self'
                4  LOAD_ATTR                buffer
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                pointer
               10  LOAD_FAST                'index'
               12  BINARY_ADD       
               14  BINARY_SUBSCR    
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L.  90        20  DUP_TOP          
               22  LOAD_GLOBAL              IndexError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    68  'to 68'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.  91        34  LOAD_FAST                'self'
               36  LOAD_METHOD              update
               38  LOAD_FAST                'index'
               40  LOAD_CONST               1
               42  BINARY_ADD       
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L.  92        48  LOAD_FAST                'self'
               50  LOAD_ATTR                buffer
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                pointer
               56  LOAD_FAST                'index'
               58  BINARY_ADD       
               60  BINARY_SUBSCR    
               62  ROT_FOUR         
               64  POP_EXCEPT       
               66  RETURN_VALUE     
             68_0  COME_FROM            26  '26'
               68  END_FINALLY      

Parse error at or near `DUP_TOP' instruction at offset 20

    def prefix(self, length=1):
        if self.pointer + length >= len(self.buffer):
            self.update(length)
        return self.buffer[self.pointer:self.pointer + length]

    def forward(self, length=1):
        if self.pointer + length + 1 >= len(self.buffer):
            self.update(length + 1)
        else:
            while True:
                if length:
                    ch = self.buffer[self.pointer]
                    self.pointer += 1
                    self.index += 1
                    if not ch in '\n\x85\u2028\u2029':
                        if not ch == '\r' or self.buffer[self.pointer] != '\n':
                            self.line += 1
                            self.column = 0
                    elif ch != '\ufeff':
                        self.column += 1
                    length -= 1

    def get_mark(self):
        if self.stream is None:
            return Mark(self.name, self.index, self.line, self.column, self.buffer, self.pointer)
        return Mark(self.name, self.index, self.line, self.column, None, None)

    def determine_encoding(self):
        if not self.eof:
            if self.raw_buffer is None or len(self.raw_buffer) < 2:
                self.update_raw()
        elif isinstance(self.raw_buffer, bytes):
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

    NON_PRINTABLE = re.compile('[^\t\n\r -~\x85\xa0-\ud7ff\ue000-�𐀀-\U0010ffff]')

    def check_printable(self, data):
        match = self.NON_PRINTABLE.search(data)
        if match:
            character = match.group()
            position = self.index + (len(self.buffer) - self.pointer) + match.start()
            raise ReaderError(self.name, position, ord(character), 'unicode', 'special characters are not allowed')

    def update(self, length):
        if self.raw_buffer is None:
            return
            self.buffer = self.buffer[self.pointer:]
            self.pointer = 0
        else:
            while True:
                if len(self.buffer) < length:
                    if not self.eof:
                        self.update_raw()
                    elif self.raw_decode is not None:
                        try:
                            data, converted = self.raw_decode(self.raw_buffer, 'strict', self.eof)
                        except UnicodeDecodeError as exc:
                            try:
                                character = self.raw_buffer[exc.start]
                                if self.stream is not None:
                                    position = self.stream_pointer - len(self.raw_buffer) + exc.start
                                else:
                                    position = exc.start
                                raise ReaderError(self.name, position, character, exc.encoding, exc.reason)
                            finally:
                                exc = None
                                del exc

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

    def update_raw(self, size=4096):
        data = self.stream.read(size)
        if self.raw_buffer is None:
            self.raw_buffer = data
        else:
            self.raw_buffer += data
        self.stream_pointer += len(data)
        if not data:
            self.eof = True


# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
# not in loop:
#	break
#      L. 175   296_298  BREAK_LOOP          302  'to 302'