# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/requests-toolbelt/requests_toolbelt/multipart/encoder.py
# Compiled at: 2020-01-10 16:25:32
# Size of source mod 2**32: 20772 bytes
"""

requests_toolbelt.multipart.encoder
===================================

This holds all of the implementation details of the MultipartEncoder

"""
import contextlib, io, os
from uuid import uuid4
import requests
from .._compat import fields

class FileNotSupportedError(Exception):
    __doc__ = 'File not supported error.'


class MultipartEncoder(object):
    __doc__ = '\n\n    The ``MultipartEncoder`` object is a generic interface to the engine that\n    will create a ``multipart/form-data`` body for you.\n\n    The basic usage is:\n\n    .. code-block:: python\n\n        import requests\n        from requests_toolbelt import MultipartEncoder\n\n        encoder = MultipartEncoder({\'field\': \'value\',\n                                    \'other_field\', \'other_value\'})\n        r = requests.post(\'https://httpbin.org/post\', data=encoder,\n                          headers={\'Content-Type\': encoder.content_type})\n\n    If you do not need to take advantage of streaming the post body, you can\n    also do:\n\n    .. code-block:: python\n\n        r = requests.post(\'https://httpbin.org/post\',\n                          data=encoder.to_string(),\n                          headers={\'Content-Type\': encoder.content_type})\n\n    If you want the encoder to use a specific order, you can use an\n    OrderedDict or more simply, a list of tuples:\n\n    .. code-block:: python\n\n        encoder = MultipartEncoder([(\'field\', \'value\'),\n                                    (\'other_field\', \'other_value\')])\n\n    .. versionchanged:: 0.4.0\n\n    You can also provide tuples as part values as you would provide them to\n    requests\' ``files`` parameter.\n\n    .. code-block:: python\n\n        encoder = MultipartEncoder({\n            \'field\': (\'file_name\', b\'{"a": "b"}\', \'application/json\',\n                      {\'X-My-Header\': \'my-value\'})\n        ])\n\n    .. warning::\n\n        This object will end up directly in :mod:`httplib`. Currently,\n        :mod:`httplib` has a hard-coded read size of **8192 bytes**. This\n        means that it will loop until the file has been read and your upload\n        could take a while. This is **not** a bug in requests. A feature is\n        being considered for this object to allow you, the user, to specify\n        what size should be returned on a read. If you have opinions on this,\n        please weigh in on `this issue`_.\n\n    .. _this issue:\n        https://github.com/requests/toolbelt/issues/75\n\n    '

    def __init__(self, fields, boundary=None, encoding='utf-8'):
        self.boundary_value = boundary or uuid4().hex
        self.boundary = '--{0}'.format(self.boundary_value)
        self.encoding = encoding
        self._encoded_boundary = (b'').join([
         encode_with(self.boundary, self.encoding),
         encode_with('\r\n', self.encoding)])
        self.fields = fields
        self.finished = False
        self.parts = []
        self._iter_parts = iter([])
        self._current_part = None
        self._len = None
        self._buffer = CustomBytesIO(encoding=encoding)
        self._prepare_parts()
        self._write_boundary()

    @property
    def len(self):
        """Length of the multipart/form-data body.

        requests will first attempt to get the length of the body by calling
        ``len(body)`` and then by checking for the ``len`` attribute.

        On 32-bit systems, the ``__len__`` method cannot return anything
        larger than an integer (in C) can hold. If the total size of the body
        is even slightly larger than 4GB users will see an OverflowError. This
        manifested itself in `bug #80`_.

        As such, we now calculate the length lazily as a property.

        .. _bug #80:
            https://github.com/requests/toolbelt/issues/80
        """
        return self._len or self._calculate_length()

    def __repr__(self):
        return '<MultipartEncoder: {0!r}>'.format(self.fields)

    def _calculate_length(self):
        """
        This uses the parts to calculate the length of the body.

        This returns the calculated length so __len__ can be lazy.
        """
        boundary_len = len(self.boundary)
        self._len = sum(boundary_len + total_len(p) + 4 for p in self.parts) + boundary_len + 4
        return self._len

    def _calculate_load_amount(self, read_size):
        """This calculates how many bytes need to be added to the buffer.

        When a consumer read's ``x`` from the buffer, there are two cases to
        satisfy:

            1. Enough data in the buffer to return the requested amount
            2. Not enough data

        This function uses the amount of unread bytes in the buffer and
        determines how much the Encoder has to load before it can return the
        requested amount of bytes.

        :param int read_size: the number of bytes the consumer requests
        :returns: int -- the number of bytes that must be loaded into the
            buffer before the read can be satisfied. This will be strictly
            non-negative
        """
        amount = read_size - total_len(self._buffer)
        if amount > 0:
            return amount
        else:
            return 0

    def _load(self, amount):
        """Load ``amount`` number of bytes into the buffer."""
        self._buffer.smart_truncate()
        part = self._current_part or self._next_part()
        while amount == -1 or amount > 0:
            written = 0
            if part:
                if not part.bytes_left_to_write():
                    written += self._write(b'\r\n')
                    written += self._write_boundary()
                    part = self._next_part()
            if not part:
                written += self._write_closing_boundary()
                self.finished = True
                break
            written += part.write_to(self._buffer, amount)
            if amount != -1:
                amount -= written

    def _next_part(self):
        try:
            p = self._current_part = next(self._iter_parts)
        except StopIteration:
            p = None

        return p

    def _iter_fields(self):
        _fields = self.fields
        if hasattr(self.fields, 'items'):
            _fields = list(self.fields.items())
        for k, v in _fields:
            file_name = None
            file_type = None
            file_headers = None
            if isinstance(v, (list, tuple)):
                if len(v) == 2:
                    file_name, file_pointer = v
                else:
                    if len(v) == 3:
                        file_name, file_pointer, file_type = v
                    else:
                        file_name, file_pointer, file_type, file_headers = v
            else:
                file_pointer = v
            field = fields.RequestField(name=k, data=file_pointer, filename=file_name,
              headers=file_headers)
            field.make_multipart(content_type=file_type)
            yield field

    def _prepare_parts(self):
        """This uses the fields provided by the user and creates Part objects.

        It populates the `parts` attribute and uses that to create a
        generator for iteration.
        """
        enc = self.encoding
        self.parts = [Part.from_field(f, enc) for f in self._iter_fields()]
        self._iter_parts = iter(self.parts)

    def _write(self, bytes_to_write):
        """Write the bytes to the end of the buffer.

        :param bytes bytes_to_write: byte-string (or bytearray) to append to
            the buffer
        :returns: int -- the number of bytes written
        """
        return self._buffer.append(bytes_to_write)

    def _write_boundary(self):
        """Write the boundary to the end of the buffer."""
        return self._write(self._encoded_boundary)

    def _write_closing_boundary(self):
        """Write the bytes necessary to finish a multipart/form-data body."""
        with reset(self._buffer):
            self._buffer.seek(-2, 2)
            self._buffer.write(b'--\r\n')
        return 2

    def _write_headers(self, headers):
        """Write the current part's headers to the buffer."""
        return self._write(encode_with(headers, self.encoding))

    @property
    def content_type(self):
        return str('multipart/form-data; boundary={0}'.format(self.boundary_value))

    def to_string(self):
        """Return the entirety of the data in the encoder.

        .. note::

            This simply reads all of the data it can. If you have started
            streaming or reading data from the encoder, this method will only
            return whatever data is left in the encoder.

        .. note::

            This method affects the internal state of the encoder. Calling
            this method will exhaust the encoder.

        :returns: the multipart message
        :rtype: bytes
        """
        return self.read()

    def read(self, size=-1):
        """Read data from the streaming encoder.

        :param int size: (optional), If provided, ``read`` will return exactly
            that many bytes. If it is not provided, it will return the
            remaining bytes.
        :returns: bytes
        """
        if self.finished:
            return self._buffer.read(size)
        else:
            bytes_to_load = size
            if bytes_to_load != -1:
                if bytes_to_load is not None:
                    bytes_to_load = self._calculate_load_amount(int(size))
            self._load(bytes_to_load)
            return self._buffer.read(size)


def IDENTITY(monitor):
    return monitor


class MultipartEncoderMonitor(object):
    __doc__ = "\n    An object used to monitor the progress of a :class:`MultipartEncoder`.\n\n    The :class:`MultipartEncoder` should only be responsible for preparing and\n    streaming the data. For anyone who wishes to monitor it, they shouldn't be\n    using that instance to manage that as well. Using this class, they can\n    monitor an encoder and register a callback. The callback receives the\n    instance of the monitor.\n\n    To use this monitor, you construct your :class:`MultipartEncoder` as you\n    normally would.\n\n    .. code-block:: python\n\n        from requests_toolbelt import (MultipartEncoder,\n                                       MultipartEncoderMonitor)\n        import requests\n\n        def callback(monitor):\n            # Do something with this information\n            pass\n\n        m = MultipartEncoder(fields={'field0': 'value0'})\n        monitor = MultipartEncoderMonitor(m, callback)\n        headers = {'Content-Type': monitor.content_type}\n        r = requests.post('https://httpbin.org/post', data=monitor,\n                          headers=headers)\n\n    Alternatively, if your use case is very simple, you can use the following\n    pattern.\n\n    .. code-block:: python\n\n        from requests_toolbelt import MultipartEncoderMonitor\n        import requests\n\n        def callback(monitor):\n            # Do something with this information\n            pass\n\n        monitor = MultipartEncoderMonitor.from_fields(\n            fields={'field0': 'value0'}, callback\n            )\n        headers = {'Content-Type': montior.content_type}\n        r = requests.post('https://httpbin.org/post', data=monitor,\n                          headers=headers)\n\n    "

    def __init__(self, encoder, callback=None):
        self.encoder = encoder
        self.callback = callback or IDENTITY
        self.bytes_read = 0
        self.len = self.encoder.len

    @classmethod
    def from_fields(cls, fields, boundary=None, encoding='utf-8', callback=None):
        encoder = MultipartEncoder(fields, boundary, encoding)
        return cls(encoder, callback)

    @property
    def content_type(self):
        return self.encoder.content_type

    def to_string(self):
        return self.read()

    def read(self, size=-1):
        string = self.encoder.read(size)
        self.bytes_read += len(string)
        self.callback(self)
        return string


def encode_with(string, encoding):
    """Encoding ``string`` with ``encoding`` if necessary.

    :param str string: If string is a bytes object, it will not encode it.
        Otherwise, this function will encode it with the provided encoding.
    :param str encoding: The encoding with which to encode string.
    :returns: encoded bytes object
    """
    if not (string is None or isinstance(string, bytes)):
        return string.encode(encoding)
    else:
        return string


def readable_data(data, encoding):
    """Coerce the data to an object with a ``read`` method."""
    if hasattr(data, 'read'):
        return data
    else:
        return CustomBytesIO(data, encoding)


def total_len(o):
    if hasattr(o, '__len__'):
        return len(o)
    else:
        if hasattr(o, 'len'):
            return o.len
        if hasattr(o, 'fileno'):
            try:
                fileno = o.fileno()
            except io.UnsupportedOperation:
                pass
            else:
                return os.fstat(fileno).st_size
        if hasattr(o, 'getvalue'):
            return len(o.getvalue())


@contextlib.contextmanager
def reset(buffer):
    """Keep track of the buffer's current position and write to the end.

    This is a context manager meant to be used when adding data to the buffer.
    It eliminates the need for every function to be concerned with the
    position of the cursor in the buffer.
    """
    original_position = buffer.tell()
    buffer.seek(0, 2)
    yield
    buffer.seek(original_position, 0)


def coerce_data(data, encoding):
    """Ensure that every object's __len__ behaves uniformly."""
    if isinstance(data, CustomBytesIO) or hasattr(data, 'getvalue'):
        return CustomBytesIO(data.getvalue(), encoding)
    else:
        if hasattr(data, 'fileno'):
            return FileWrapper(data)
        if not hasattr(data, 'read'):
            return CustomBytesIO(data, encoding)
        return data


def to_list(fields):
    if hasattr(fields, 'items'):
        return list(fields.items())
    else:
        return list(fields)


class Part(object):

    def __init__(self, headers, body):
        self.headers = headers
        self.body = body
        self.headers_unread = True
        self.len = len(self.headers) + total_len(self.body)

    @classmethod
    def from_field(cls, field, encoding):
        """Create a part from a Request Field generated by urllib3."""
        headers = encode_with(field.render_headers(), encoding)
        body = coerce_data(field.data, encoding)
        return cls(headers, body)

    def bytes_left_to_write(self):
        """Determine if there are bytes left to write.

        :returns: bool -- ``True`` if there are bytes left to write, otherwise
            ``False``
        """
        to_read = 0
        if self.headers_unread:
            to_read += len(self.headers)
        return to_read + total_len(self.body) > 0

    def write_to(self, buffer, size):
        """Write the requested amount of bytes to the buffer provided.

        The number of bytes written may exceed size on the first read since we
        load the headers ambitiously.

        :param CustomBytesIO buffer: buffer we want to write bytes to
        :param int size: number of bytes requested to be written to the buffer
        :returns: int -- number of bytes actually written
        """
        written = 0
        if self.headers_unread:
            written += buffer.append(self.headers)
            self.headers_unread = False
        while total_len(self.body) > 0 and (size == -1 or written < size):
            amount_to_read = size
            if size != -1:
                amount_to_read = size - written
            written += buffer.append(self.body.read(amount_to_read))

        return written


class CustomBytesIO(io.BytesIO):

    def __init__(self, buffer=None, encoding='utf-8'):
        buffer = encode_with(buffer, encoding)
        super(CustomBytesIO, self).__init__(buffer)

    def _get_end(self):
        current_pos = self.tell()
        self.seek(0, 2)
        length = self.tell()
        self.seek(current_pos, 0)
        return length

    @property
    def len(self):
        length = self._get_end()
        return length - self.tell()

    def append(self, bytes):
        with reset(self):
            written = self.write(bytes)
        return written

    def smart_truncate(self):
        to_be_read = total_len(self)
        already_read = self._get_end() - to_be_read
        if already_read >= to_be_read:
            old_bytes = self.read()
            self.seek(0, 0)
            self.truncate()
            self.write(old_bytes)
            self.seek(0, 0)


class FileWrapper(object):

    def __init__(self, file_object):
        self.fd = file_object

    @property
    def len(self):
        return total_len(self.fd) - self.fd.tell()

    def read(self, length=-1):
        return self.fd.read(length)


class FileFromURLWrapper(object):
    __doc__ = "File from URL wrapper.\n\n    The :class:`FileFromURLWrapper` object gives you the ability to stream file\n    from provided URL in chunks by :class:`MultipartEncoder`.\n    Provide a stateless solution for streaming file from one server to another.\n    You can use the :class:`FileFromURLWrapper` without a session or with\n    a session as demonstated by the examples below:\n\n    .. code-block:: python\n        # no session\n\n        import requests\n        from requests_toolbelt import MultipartEncoder, FileFromURLWrapper\n\n        url = 'https://httpbin.org/image/png'\n        streaming_encoder = MultipartEncoder(\n            fields={\n                'file': FileFromURLWrapper(url)\n            }\n        )\n        r = requests.post(\n            'https://httpbin.org/post', data=streaming_encoder,\n            headers={'Content-Type': streaming_encoder.content_type}\n        )\n\n    .. code-block:: python\n        # using a session\n\n        import requests\n        from requests_toolbelt import MultipartEncoder, FileFromURLWrapper\n\n        session = requests.Session()\n        url = 'https://httpbin.org/image/png'\n        streaming_encoder = MultipartEncoder(\n            fields={\n                'file': FileFromURLWrapper(url, session=session)\n            }\n        )\n        r = session.post(\n            'https://httpbin.org/post', data=streaming_encoder,\n            headers={'Content-Type': streaming_encoder.content_type}\n        )\n\n    "

    def __init__(self, file_url, session=None):
        self.session = session or requests.Session()
        requested_file = self._request_for_file(file_url)
        self.len = int(requested_file.headers['content-length'])
        self.raw_data = requested_file.raw

    def _request_for_file(self, file_url):
        """Make call for file under provided URL."""
        response = self.session.get(file_url, stream=True)
        content_length = response.headers.get('content-length', None)
        if content_length is None:
            error_msg = 'Data from provided URL {url} is not supported. Lack of content-length Header in requested file response.'.format(url=file_url)
            raise FileNotSupportedError(error_msg)
        else:
            if not content_length.isdigit():
                error_msg = 'Data from provided URL {url} is not supported. content-length header value is not a digit.'.format(url=file_url)
                raise FileNotSupportedError(error_msg)
        return response

    def read(self, chunk_size):
        """Read file in chunks."""
        chunk_size = chunk_size if chunk_size >= 0 else self.len
        chunk = self.raw_data.read(chunk_size) or b''
        self.len -= len(chunk) if chunk else 0
        return chunk