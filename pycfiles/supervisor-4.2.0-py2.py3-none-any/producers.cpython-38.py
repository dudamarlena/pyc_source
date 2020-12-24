# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/medusa/producers.py
# Compiled at: 2019-04-05 17:19:18
# Size of source mod 2**32: 8972 bytes
RCS_ID = '$Id: producers.py,v 1.9 2004/04/21 13:56:28 akuchling Exp $'
from asynchat import find_prefix_at_end
from supervisor.compat import as_bytes

class simple_producer:
    __doc__ = 'producer for a string'

    def __init__(self, data, buffer_size=1024):
        self.data = data
        self.buffer_size = buffer_size

    def more(self):
        if len(self.data) > self.buffer_size:
            result = self.data[:self.buffer_size]
            self.data = self.data[self.buffer_size:]
            return result
        result = self.data
        self.data = b''
        return result


class scanning_producer:
    __doc__ = 'like simple_producer, but more efficient for large strings'

    def __init__(self, data, buffer_size=1024):
        self.data = data
        self.buffer_size = buffer_size
        self.pos = 0

    def more(self):
        if self.pos < len(self.data):
            lp = self.pos
            rp = min(len(self.data), self.pos + self.buffer_size)
            result = self.data[lp:rp]
            self.pos += len(result)
            return result
        return b''


class lines_producer:
    __doc__ = 'producer for a list of lines'

    def __init__(self, lines):
        self.lines = lines

    def more(self):
        if self.lines:
            chunk = self.lines[:50]
            self.lines = self.lines[50:]
            return '\r\n'.join(chunk) + '\r\n'
        return ''


class buffer_list_producer:
    __doc__ = 'producer for a list of strings'

    def __init__(self, buffers):
        self.index = 0
        self.buffers = buffers

    def more(self):
        if self.index >= len(self.buffers):
            return b''
        data = self.buffers[self.index]
        self.index += 1
        return data


class file_producer:
    __doc__ = 'producer wrapper for file[-like] objects'
    out_buffer_size = 65536

    def __init__(self, file):
        self.done = 0
        self.file = file

    def more(self):
        if self.done:
            return b''
        else:
            data = self.file.read(self.out_buffer_size)
            data or self.file.close()
            del self.file
            self.done = 1
            return b''
        return data


class output_producer:
    __doc__ = 'Acts like an output file; suitable for capturing sys.stdout'

    def __init__(self):
        self.data = b''

    def write(self, data):
        lines = data.split('\n')
        data = '\r\n'.join(lines)
        self.data += data

    def writeline(self, line):
        self.data = self.data + line + '\r\n'

    def writelines(self, lines):
        self.data = self.data + '\r\n'.join(lines) + '\r\n'

    def flush(self):
        pass

    def softspace(self, *args):
        pass

    def more(self):
        if self.data:
            result = self.data[:512]
            self.data = self.data[512:]
            return result
        return ''


class composite_producer:
    __doc__ = 'combine a fifo of producers into one'

    def __init__(self, producers):
        self.producers = producers

    def more(self):
        while len(self.producers):
            p = self.producers[0]
            d = p.more()
            if d:
                return d
            self.producers.pop(0)

        return b''


class globbing_producer:
    __doc__ = "\n    'glob' the output from a producer into a particular buffer size.\n    helps reduce the number of calls to send().  [this appears to\n    gain about 30% performance on requests to a single channel]\n    "

    def __init__(self, producer, buffer_size=65536):
        self.producer = producer
        self.buffer = b''
        self.buffer_size = buffer_size

    def more--- This code section failed: ---

 L. 174         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                buffer
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                buffer_size
               12  COMPARE_OP               <
               14  POP_JUMP_IF_FALSE    48  'to 48'

 L. 175        16  LOAD_FAST                'self'
               18  LOAD_ATTR                producer
               20  LOAD_METHOD              more
               22  CALL_METHOD_0         0  ''
               24  STORE_FAST               'data'

 L. 176        26  LOAD_FAST                'data'
               28  POP_JUMP_IF_FALSE    48  'to 48'

 L. 177        30  LOAD_FAST                'self'
               32  LOAD_ATTR                buffer
               34  LOAD_FAST                'data'
               36  BINARY_ADD       
               38  LOAD_FAST                'self'
               40  STORE_ATTR               buffer
               42  JUMP_BACK             0  'to 0'

 L. 179        44  BREAK_LOOP           48  'to 48'
               46  JUMP_BACK             0  'to 0'
             48_0  COME_FROM            28  '28'
             48_1  COME_FROM            14  '14'

 L. 180        48  LOAD_FAST                'self'
               50  LOAD_ATTR                buffer
               52  STORE_FAST               'r'

 L. 181        54  LOAD_CONST               b''
               56  LOAD_FAST                'self'
               58  STORE_ATTR               buffer

 L. 182        60  LOAD_FAST                'r'
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 62


class hooked_producer:
    __doc__ = '\n    A producer that will call <function> when it empties,.\n    with an argument of the number of bytes produced.  Useful\n    for logging/instrumentation purposes.\n    '

    def __init__(self, producer, function):
        self.producer = producer
        self.function = function
        self.bytes = 0

    def more(self):
        if self.producer:
            result = self.producer.more()
            if not result:
                self.producer = None
                self.function(self.bytes)
            else:
                self.bytes += len(result)
            return result
        return ''


class chunked_producer:
    __doc__ = "A producer that implements the 'chunked' transfer coding for HTTP/1.1.\n    Here is a sample usage:\n            request['Transfer-Encoding'] = 'chunked'\n            request.push (\n                    producers.chunked_producer (your_producer)\n                    )\n            request.done()\n    "

    def __init__(self, producer, footers=None):
        self.producer = producer
        self.footers = footers

    def more(self):
        if self.producer:
            data = self.producer.more()
            if data:
                s = '%x' % len(data)
                return as_bytes(s) + b'\r\n' + data + b'\r\n'
            self.producer = None
            if self.footers:
                return (b'\r\n').join([b'0'] + self.footers) + b'\r\n\r\n'
            return b'0\r\n\r\n'
        else:
            return b''


try:
    import zlib
except ImportError:
    zlib = None
else:

    class compressed_producer:
        __doc__ = '\n    Compress another producer on-the-fly, using ZLIB\n    '

        def __init__(self, producer, level=5):
            self.producer = producer
            self.compressor = zlib.compressobj(level)

        def more(self):
            if self.producer:
                cdata = b''
                if not cdata:
                    data = self.producer.more()
                    if not data:
                        self.producer = None
                        return self.compressor.flush()
                    cdata = self.compressor.compress(data)
                else:
                    return cdata
            return b''


    class escaping_producer:
        __doc__ = 'A producer that escapes a sequence of characters'

        def __init__(self, producer, esc_from='\r\n.', esc_to='\r\n..'):
            self.producer = producer
            self.esc_from = esc_from
            self.esc_to = esc_to
            self.buffer = b''
            self.find_prefix_at_end = find_prefix_at_end

        def more(self):
            esc_from = self.esc_from
            esc_to = self.esc_to
            buffer = self.buffer + self.producer.more()
            if buffer:
                buffer = buffer.replace(esc_from, esc_to)
                i = self.find_prefix_at_end(buffer, esc_from)
                if i:
                    self.buffer = buffer[-i:]
                    return buffer[:-i]
                self.buffer = b''
                return buffer
            else:
                return buffer