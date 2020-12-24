# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/amcnabb/python/mrs/bucket.py
# Compiled at: 2012-11-07 19:04:07
from __future__ import division, print_function
import os
from . import fileformats
from . import util
try:
    from urllib.parse import urlparse, urlunparse
except ImportError:
    from urlparse import urlparse, urlunparse

from logging import getLogger
logger = getLogger('mrs')
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

class ReadBucket(object):
    """Hold data from a source.

    Attributes:
        source: An integer showing which source the data come from.
        split: An integer showing which split the data is directed to.
        serializers: A Serializers instance: functions for serializing and
            deserializing between Python objects and bytes.
        url: A string showing a URL that can be used to read the data.
    """

    def __init__(self, source, split, serializers=None):
        self._data = []
        self.source = source
        self.split = split
        self.serializers = serializers
        self.url = None
        return

    def addpair(self, kvpair):
        """Collect a single key-value pair."""
        self._data.append(kvpair)

    def collect(self, pairiter):
        """Collect all key-value pairs from the given iterable

        The collection can be a generator or a Mrs format.  This will block if
        the iterator blocks.
        """
        data = self._data
        for kvpair in pairiter:
            data.append(kvpair)

    def sort(self):
        self._data.sort()

    def clean(self):
        """Removes any temporary files created and empties cached data."""
        self._data = None
        return

    def __getstate__(self):
        """Pickle (serialize) the bucket."""
        state = self.__dict__.copy()
        if self._data:
            buf = BytesIO()
            with fileformats.BinWriter(buf, self.serializers) as (writer):
                for pair in self._data:
                    writer.writepair(pair)

            state['_data'] = buf.getvalue()
            buf.close()
        else:
            state['_data'] = ''
        return state

    def __setstate__(self, state):
        """Unpickle (deserialize) the bucket."""
        self.__dict__ = state
        if self._data == '':
            self._data = []
        else:
            buf = BytesIO(self._data)
            self._data = []
            reader = fileformats.BinReader(buf, self.serializers)
            self.collect(reader)
            buf.close()

    def __len__(self):
        return len(self._data)

    def __getitem__(self, item):
        """Get a particular item, mainly for debugging purposes"""
        return self._data[item]

    def stream(self, serializers=None):
        """Stream over kvpairs from the remote URL (or local data, if loaded).

        Use the given serializers, defaulting to self.serializers.
        """
        if self._data:
            return iter(self)
        else:
            if serializers is None:
                serializers = self.serializers
            return self._stream(serializers)
            return

    def _stream(self, serializers):
        with fileformats.open_url(self.url, serializers=serializers) as (reader):
            for kvpair in reader:
                yield kvpair

    def __iter__(self):
        """Iterate over all already-loaded data."""
        return iter(self._data)


class WriteBucket(ReadBucket):
    """Hold data for a split.

    Data can be manually dumped to disk, in which case the data will be saved
    to the given filename with the specified format.

    Attributes:
        url: Always None: use `readonly_copy` to make it readable
        source: An integer showing which source the data come from.
        split: An integer showing which split the data is directed to.
        serializers: A Serializers instance: functions for serializing and
            deserializing between Python objects and bytes.
        dir: A string specifying the directory for writes.
        format: The class to be used for formatting writes.
        path: The local path of the written file.

    >>> b = WriteBucket(0, 0)
    >>> b.addpair((4, 'test'))
    >>> b.collect([(3, 'a'), (1, 'This'), (2, 'is')])
    >>> ' '.join(value for key, value in b)
    'test a This is'
    >>> b.sort()
    >>> ' '.join(value for key, value in b)
    'This is a test'
    >>>
    """

    def __init__(self, source, split, dir=None, format=None, **kwds):
        super(WriteBucket, self).__init__(source, split, **kwds)
        self.dir = dir
        if format is None:
            format = fileformats.default_write_format
        self.format = format
        self._filename = None
        self._output_file = None
        self._writer = None
        return

    def __setstate__(self, state):
        raise NotImplementedError

    def readonly_copy(self):
        b = ReadBucket(self.source, self.split, self.serializers)
        b._data = self._data
        b.url = self._filename
        return b

    def open_writer(self):
        if self.dir and not self._filename and not self._writer:
            suffix = '.' + self.format.ext
            self._output_file, self._filename = util.mktempfile(self.dir, self.prefix(), suffix)
            self._writer = self.format(self._output_file, self.serializers)

    def close_writer(self, do_sync):
        """Close the bucket for future writes."""
        if self._writer:
            self._writer.finish()
        if self._output_file:
            if do_sync:
                self._output_file.flush()
                os.fsync(self._output_file.fileno())
            self._output_file.close()
            self._output_file = None
        self._writer = None
        return

    def addpair(self, kvpair, write_only=False):
        """Collect a single key-value pair."""
        if not write_only:
            self._data.append(kvpair)
        if self.dir:
            if not self._writer:
                self.open_writer()
            self._writer.writepair(kvpair)

    def collect(self, pairiter, write_only=False):
        """Collect all key-value pairs from the given iterable

        The collection can be a generator or a Mrs format.  This will block if
        the iterator blocks.
        """
        data = self._data
        if self.dir:
            if not self._writer:
                self.open_writer()
            if write_only:
                for kvpair in pairiter:
                    self._writer.writepair(kvpair)

            else:
                for kvpair in pairiter:
                    data.append(kvpair)
                    self._writer.writepair(kvpair)

        else:
            for kvpair in pairiter:
                data.append(kvpair)

    def prefix(self):
        """Return the filename for the output split for the given index.

        >>> b = WriteBucket(2, 4)
        >>> b.prefix()
        'source_2_split_4_'
        >>>
        """
        return 'source_%s_split_%s_' % (self.source, self.split)

    def clean(self):
        """Removes any temporary files created and empties cached data."""
        super(WriteBucket, self).clean()
        self._data = None
        if self._filename:
            os.remove(self._filename)
        return


class URLConverter(object):

    def __init__(self, addr, port, basedir):
        assert port is not None
        self.addr = addr
        self.port = port
        self.netloc = '%s:%s' % (addr, port)
        self.basedir = basedir
        return

    def local_to_global(self, path):
        """Creates a URL corresponding to the given path."""
        url_path = os.path.relpath(path, self.basedir)
        if url_path.startswith('..'):
            return path
        else:
            url_components = (
             'http', self.netloc, url_path, None, None, None)
            url = urlunparse(url_components)
            return url
            return

    def global_to_local(self, url, master):
        """Creates a locally accessible URL from the given URL.

        The urls, as sent by the master, may have any empty host fields in the
        urls if any data was created on the master.  Also, it may be possible
        to create a locally-accessible path in place of an http url.
        """
        result = urlparse(url)
        if result.scheme and not result.hostname:
            components = list(result)
            components[1] = master
            if result.port:
                components[1] += ':%s' % result.port
            url = urlunparse(components)
        elif result.hostname == self.addr and result.port == self.port:
            path = result.path.lstrip('/')
            url = os.path.join(self.basedir, path)
        return url