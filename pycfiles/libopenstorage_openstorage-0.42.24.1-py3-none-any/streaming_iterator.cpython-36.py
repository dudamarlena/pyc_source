# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/requests-toolbelt/requests_toolbelt/streaming_iterator.py
# Compiled at: 2020-01-10 16:25:32
# Size of source mod 2**32: 4044 bytes
"""

requests_toolbelt.streaming_iterator
====================================

This holds the implementation details for the :class:`StreamingIterator`. It
is designed for the case where you, the user, know the size of the upload but
need to provide the data as an iterator. This class will allow you to specify
the size and stream the data without using a chunked transfer-encoding.

"""
from requests.utils import super_len
from .multipart.encoder import CustomBytesIO, encode_with

class StreamingIterator(object):
    __doc__ = "\n    This class provides a way of allowing iterators with a known size to be\n    streamed instead of chunked.\n\n    In requests, if you pass in an iterator it assumes you want to use\n    chunked transfer-encoding to upload the data, which not all servers\n    support well. Additionally, you may want to set the content-length\n    yourself to avoid this but that will not work. The only way to preempt\n    requests using a chunked transfer-encoding and forcing it to stream the\n    uploads is to mimic a very specific interace. Instead of having to know\n    these details you can instead just use this class. You simply provide the\n    size and iterator and pass the instance of StreamingIterator to requests\n    via the data parameter like so:\n\n    .. code-block:: python\n\n        from requests_toolbelt import StreamingIterator\n\n        import requests\n\n        # Let iterator be some generator that you already have and size be\n        # the size of the data produced by the iterator\n\n        r = requests.post(url, data=StreamingIterator(size, iterator))\n\n    You can also pass file-like objects to :py:class:`StreamingIterator` in\n    case requests can't determize the filesize itself. This is the case with\n    streaming file objects like ``stdin`` or any sockets. Wrapping e.g. files\n    that are on disk with ``StreamingIterator`` is unnecessary, because\n    requests can determine the filesize itself.\n\n    Naturally, you should also set the `Content-Type` of your upload\n    appropriately because the toolbelt will not attempt to guess that for you.\n    "

    def __init__(self, size, iterator, encoding='utf-8'):
        self.size = int(size)
        if self.size < 0:
            raise ValueError('The size of the upload must be a positive integer')
        else:
            self.len = self.size
            self.encoding = encoding
            self.iterator = iterator
            if hasattr(iterator, 'read'):
                self._file = iterator
            else:
                self._file = _IteratorAsBinaryFile(iterator, encoding)

    def read(self, size=-1):
        return encode_with(self._file.read(size), self.encoding)


class _IteratorAsBinaryFile(object):

    def __init__(self, iterator, encoding='utf-8'):
        self.iterator = iterator
        self.encoding = encoding
        self._buffer = CustomBytesIO()

    def _get_bytes(self):
        try:
            return encode_with(next(self.iterator), self.encoding)
        except StopIteration:
            return b''

    def _load_bytes(self, size):
        self._buffer.smart_truncate()
        amount_to_load = size - super_len(self._buffer)
        bytes_to_append = True
        while amount_to_load > 0 and bytes_to_append:
            bytes_to_append = self._get_bytes()
            amount_to_load -= self._buffer.append(bytes_to_append)

    def read(self, size=-1):
        size = int(size)
        if size == -1:
            return (b'').join(self.iterator)
        else:
            self._load_bytes(size)
            return self._buffer.read(size)