# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/http/multipartparser.py
# Compiled at: 2018-07-11 18:15:30
"""
Multi-part parsing for file uploads.

Exposes one class, ``MultiPartParser``, which feeds chunks of uploaded data to
file upload handlers for processing.
"""
from __future__ import unicode_literals
import base64, cgi
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.utils.datastructures import MultiValueDict
from django.utils.encoding import force_text
from django.utils import six
from django.utils.text import unescape_entities
from django.core.files.uploadhandler import StopUpload, SkipFile, StopFutureHandlers
__all__ = ('MultiPartParser', 'MultiPartParserError', 'InputStreamExhausted')

class MultiPartParserError(Exception):
    pass


class InputStreamExhausted(Exception):
    """
    No more reads are allowed from this device.
    """
    pass


RAW = b'raw'
FILE = b'file'
FIELD = b'field'

class MultiPartParser(object):
    """
    A rfc2388 multipart/form-data parser.

    ``MultiValueDict.parse()`` reads the input stream in ``chunk_size`` chunks
    and returns a tuple of ``(MultiValueDict(POST), MultiValueDict(FILES))``.
    """

    def __init__(self, META, input_data, upload_handlers, encoding=None):
        """
        Initialize the MultiPartParser object.

        :META:
            The standard ``META`` dictionary in Django request objects.
        :input_data:
            The raw post data, as a file-like object.
        :upload_handler:
            An UploadHandler instance that performs operations on the uploaded
            data.
        :encoding:
            The encoding with which to treat the incoming data.
        """
        content_type = META.get(b'HTTP_CONTENT_TYPE', META.get(b'CONTENT_TYPE', b''))
        if not content_type.startswith(b'multipart/'):
            raise MultiPartParserError(b'Invalid Content-Type: %s' % content_type)
        ctypes, opts = parse_header(content_type.encode(b'ascii'))
        boundary = opts.get(b'boundary')
        if not boundary or not cgi.valid_boundary(boundary):
            raise MultiPartParserError(b'Invalid boundary in multipart: %s' % boundary)
        try:
            content_length = int(META.get(b'HTTP_CONTENT_LENGTH', META.get(b'CONTENT_LENGTH', 0)))
        except (ValueError, TypeError):
            content_length = 0

        if content_length < 0:
            raise MultiPartParserError(b'Invalid content length: %r' % content_length)
        if isinstance(boundary, six.text_type):
            boundary = boundary.encode(b'ascii')
        self._boundary = boundary
        self._input_data = input_data
        possible_sizes = [ x.chunk_size for x in upload_handlers if x.chunk_size ]
        self._chunk_size = min([2147483644] + possible_sizes)
        self._meta = META
        self._encoding = encoding or settings.DEFAULT_CHARSET
        self._content_length = content_length
        self._upload_handlers = upload_handlers

    def parse(self):
        """
        Parse the POST data and break it into a FILES MultiValueDict and a POST
        MultiValueDict.

        Returns a tuple containing the POST and FILES dictionary, respectively.
        """
        from django.http import QueryDict
        encoding = self._encoding
        handlers = self._upload_handlers
        if self._content_length == 0:
            return (QueryDict(b'', encoding=self._encoding), MultiValueDict())
        else:
            for handler in handlers:
                result = handler.handle_raw_input(self._input_data, self._meta, self._content_length, self._boundary, encoding)
                if result is not None:
                    return (result[0], result[1])

            self._post = QueryDict(b'', mutable=True)
            self._files = MultiValueDict()
            stream = LazyStream(ChunkIter(self._input_data, self._chunk_size))
            old_field_name = None
            counters = [0] * len(handlers)
            try:
                for item_type, meta_data, field_stream in Parser(stream, self._boundary):
                    if old_field_name:
                        self.handle_file_complete(old_field_name, counters)
                        old_field_name = None
                    try:
                        disposition = meta_data[b'content-disposition'][1]
                        field_name = disposition[b'name'].strip()
                    except (KeyError, IndexError, AttributeError):
                        continue

                    transfer_encoding = meta_data.get(b'content-transfer-encoding')
                    if transfer_encoding is not None:
                        transfer_encoding = transfer_encoding[0].strip()
                    field_name = force_text(field_name, encoding, errors=b'replace')
                    if item_type == FIELD:
                        if transfer_encoding == b'base64':
                            raw_data = field_stream.read()
                            try:
                                data = str(raw_data).decode(b'base64')
                            except:
                                data = raw_data

                        else:
                            data = field_stream.read()
                        self._post.appendlist(field_name, force_text(data, encoding, errors=b'replace'))
                    elif item_type == FILE:
                        file_name = disposition.get(b'filename')
                        if not file_name:
                            continue
                        file_name = force_text(file_name, encoding, errors=b'replace')
                        file_name = self.IE_sanitize(unescape_entities(file_name))
                        content_type = meta_data.get(b'content-type', ('', ))[0].strip()
                        try:
                            charset = meta_data.get(b'content-type', (0, {}))[1].get(b'charset', None)
                        except:
                            charset = None

                        try:
                            content_length = int(meta_data.get(b'content-length')[0])
                        except (IndexError, TypeError, ValueError):
                            content_length = None

                        counters = [0] * len(handlers)
                        try:
                            for handler in handlers:
                                try:
                                    handler.new_file(field_name, file_name, content_type, content_length, charset)
                                except StopFutureHandlers:
                                    break

                            for chunk in field_stream:
                                if transfer_encoding == b'base64':
                                    over_bytes = len(chunk) % 4
                                    if over_bytes:
                                        over_chunk = field_stream.read(4 - over_bytes)
                                        chunk += over_chunk
                                    try:
                                        chunk = base64.b64decode(chunk)
                                    except Exception as e:
                                        raise MultiPartParserError(b'Could not decode base64 data: %r' % e)

                                for i, handler in enumerate(handlers):
                                    chunk_length = len(chunk)
                                    chunk = handler.receive_data_chunk(chunk, counters[i])
                                    counters[i] += chunk_length
                                    if chunk is None:
                                        break

                        except SkipFile:
                            exhaust(field_stream)
                        else:
                            old_field_name = field_name

                    else:
                        exhaust(stream)

            except StopUpload as e:
                if not e.connection_reset:
                    exhaust(self._input_data)
            else:
                exhaust(self._input_data)

            for handler in handlers:
                retval = handler.upload_complete()
                if retval:
                    break

            return (
             self._post, self._files)

    def handle_file_complete(self, old_field_name, counters):
        """
        Handle all the signalling that takes place when a file is complete.
        """
        for i, handler in enumerate(self._upload_handlers):
            file_obj = handler.file_complete(counters[i])
            if file_obj:
                self._files.appendlist(force_text(old_field_name, self._encoding, errors=b'replace'), file_obj)
                break

    def IE_sanitize(self, filename):
        """Cleanup filename from Internet Explorer full paths."""
        return filename and filename[filename.rfind(b'\\') + 1:].strip()


class LazyStream(six.Iterator):
    """
    The LazyStream wrapper allows one to get and "unget" bytes from a stream.

    Given a producer object (an iterator that yields bytestrings), the
    LazyStream object will support iteration, reading, and keeping a "look-back"
    variable in case you need to "unget" some bytes.
    """

    def __init__(self, producer, length=None):
        """
        Every LazyStream must have a producer when instantiated.

        A producer is an iterable that returns a string each time it
        is called.
        """
        self._producer = producer
        self._empty = False
        self._leftover = b''
        self.length = length
        self.position = 0
        self._remaining = length
        self._unget_history = []

    def tell(self):
        return self.position

    def read(self, size=None):

        def parts():
            remaining = (size is not None and [size] or [self._remaining])[0]
            if remaining is None:
                yield (b'').join(self)
                return
            else:
                while remaining != 0:
                    assert remaining > 0, b'remaining bytes to read should never go negative'
                    chunk = next(self)
                    emitting = chunk[:remaining]
                    self.unget(chunk[remaining:])
                    remaining -= len(emitting)
                    yield emitting

                return

        out = (b'').join(parts())
        return out

    def __next__(self):
        """
        Used when the exact number of bytes to read is unimportant.

        This procedure just returns whatever is chunk is conveniently returned
        from the iterator instead. Useful to avoid unnecessary bookkeeping if
        performance is an issue.
        """
        if self._leftover:
            output = self._leftover
            self._leftover = b''
        else:
            output = next(self._producer)
            self._unget_history = []
        self.position += len(output)
        return output

    def close(self):
        """
        Used to invalidate/disable this lazy stream.

        Replaces the producer with an empty list. Any leftover bytes that have
        already been read will still be reported upon read() and/or next().
        """
        self._producer = []

    def __iter__(self):
        return self

    def unget(self, bytes):
        """
        Places bytes back onto the front of the lazy stream.

        Future calls to read() will return those bytes first. The
        stream position and thus tell() will be rewound.
        """
        if not bytes:
            return
        self._update_unget_history(len(bytes))
        self.position -= len(bytes)
        self._leftover = (b'').join([bytes, self._leftover])

    def _update_unget_history(self, num_bytes):
        """
        Updates the unget history as a sanity check to see if we've pushed
        back the same number of bytes in one chunk. If we keep ungetting the
        same number of bytes many times (here, 50), we're mostly likely in an
        infinite loop of some sort. This is usually caused by a
        maliciously-malformed MIME request.
        """
        self._unget_history = [
         num_bytes] + self._unget_history[:49]
        number_equal = len([ current_number for current_number in self._unget_history if current_number == num_bytes
                           ])
        if number_equal > 40:
            raise SuspiciousOperation(b"The multipart parser got stuck, which shouldn't happen with normal uploaded files. Check for malicious upload activity; if there is none, report this to the Django developers.")


class ChunkIter(six.Iterator):
    """
    An iterable that will yield chunks of data. Given a file-like object as the
    constructor, this object will yield chunks of read operations from that
    object.
    """

    def __init__(self, flo, chunk_size=65536):
        self.flo = flo
        self.chunk_size = chunk_size

    def __next__(self):
        try:
            data = self.flo.read(self.chunk_size)
        except InputStreamExhausted:
            raise StopIteration()

        if data:
            return data
        raise StopIteration()

    def __iter__(self):
        return self


class InterBoundaryIter(six.Iterator):
    """
    A Producer that will iterate over boundaries.
    """

    def __init__(self, stream, boundary):
        self._stream = stream
        self._boundary = boundary

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return LazyStream(BoundaryIter(self._stream, self._boundary))
        except InputStreamExhausted:
            raise StopIteration()


class BoundaryIter(six.Iterator):
    """
    A Producer that is sensitive to boundaries.

    Will happily yield bytes until a boundary is found. Will yield the bytes
    before the boundary, throw away the boundary bytes themselves, and push the
    post-boundary bytes back on the stream.

    The future calls to next() after locating the boundary will raise a
    StopIteration exception.
    """

    def __init__(self, stream, boundary):
        self._stream = stream
        self._boundary = boundary
        self._done = False
        self._rollback = len(boundary) + 6
        unused_char = self._stream.read(1)
        if not unused_char:
            raise InputStreamExhausted()
        self._stream.unget(unused_char)
        try:
            from mx.TextTools import FS
            self._fs = FS(boundary).find
        except ImportError:
            self._fs = lambda data: data.find(boundary)

    def __iter__(self):
        return self

    def __next__(self):
        if self._done:
            raise StopIteration()
        stream = self._stream
        rollback = self._rollback
        bytes_read = 0
        chunks = []
        for bytes in stream:
            bytes_read += len(bytes)
            chunks.append(bytes)
            if bytes_read > rollback:
                break
            if not bytes:
                break
        else:
            self._done = True

        if not chunks:
            raise StopIteration()
        chunk = (b'').join(chunks)
        boundary = self._find_boundary(chunk, len(chunk) < self._rollback)
        if boundary:
            end, next = boundary
            stream.unget(chunk[next:])
            self._done = True
            return chunk[:end]
        else:
            if not chunk[:-rollback]:
                self._done = True
                return chunk
            stream.unget(chunk[-rollback:])
            return chunk[:-rollback]

    def _find_boundary(self, data, eof=False):
        """
        Finds a multipart boundary in data.

        Should no boundry exist in the data None is returned instead. Otherwise
        a tuple containing the indices of the following are returned:

         * the end of current encapsulation
         * the start of the next encapsulation
        """
        index = self._fs(data)
        if index < 0:
            return
        else:
            end = index
            next = index + len(self._boundary)
            last = max(0, end - 1)
            if data[last:last + 1] == b'\n':
                end -= 1
            last = max(0, end - 1)
            if data[last:last + 1] == b'\r':
                end -= 1
            return (
             end, next)
            return


def exhaust(stream_or_iterable):
    """
    Completely exhausts an iterator or stream.

    Raise a MultiPartParserError if the argument is not a stream or an iterable.
    """
    iterator = None
    try:
        iterator = iter(stream_or_iterable)
    except TypeError:
        iterator = ChunkIter(stream_or_iterable, 16384)

    if iterator is None:
        raise MultiPartParserError(b'multipartparser.exhaust() was passed a non-iterable or stream parameter')
    for __ in iterator:
        pass

    return


def parse_boundary_stream(stream, max_header_size):
    """
    Parses one and exactly one stream that encapsulates a boundary.
    """
    chunk = stream.read(max_header_size)
    header_end = chunk.find(b'\r\n\r\n')

    def _parse_header(line):
        main_value_pair, params = parse_header(line)
        try:
            name, value = main_value_pair.split(b':', 1)
        except:
            raise ValueError(b'Invalid header: %r' % line)

        return (
         name, (value, params))

    if header_end == -1:
        stream.unget(chunk)
        return (
         RAW, {}, stream)
    header = chunk[:header_end]
    stream.unget(chunk[header_end + 4:])
    TYPE = RAW
    outdict = {}
    for line in header.split(b'\r\n'):
        try:
            name, (value, params) = _parse_header(line)
        except:
            continue

        if name == b'content-disposition':
            TYPE = FIELD
            if params.get(b'filename'):
                TYPE = FILE
        outdict[name] = (
         value, params)

    if TYPE == RAW:
        stream.unget(chunk)
    return (TYPE, outdict, stream)


class Parser(object):

    def __init__(self, stream, boundary):
        self._stream = stream
        self._separator = b'--' + boundary

    def __iter__(self):
        boundarystream = InterBoundaryIter(self._stream, self._separator)
        for sub_stream in boundarystream:
            yield parse_boundary_stream(sub_stream, 1024)


def parse_header(line):
    """ Parse the header into a key-value.
        Input (line): bytes, output: unicode for key/name, bytes for value which
        will be decoded later
    """
    plist = _parse_header_params(b';' + line)
    key = plist.pop(0).lower().decode(b'ascii')
    pdict = {}
    for p in plist:
        i = p.find(b'=')
        if i >= 0:
            name = p[:i].strip().lower().decode(b'ascii')
            value = p[i + 1:].strip()
            if len(value) >= 2 and value[:1] == value[-1:] == b'"':
                value = value[1:-1]
                value = value.replace(b'\\\\', b'\\').replace(b'\\"', b'"')
            pdict[name] = value

    return (
     key, pdict)


def _parse_header_params(s):
    plist = []
    while s[:1] == b';':
        s = s[1:]
        end = s.find(b';')
        while end > 0 and s.count(b'"', 0, end) % 2:
            end = s.find(b';', end + 1)

        if end < 0:
            end = len(s)
        f = s[:end]
        plist.append(f.strip())
        s = s[end:]

    return plist