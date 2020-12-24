# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/featureflow/datawriter.py
# Compiled at: 2019-03-01 22:03:23
# Size of source mod 2**32: 4505 bytes
from io import StringIO, BytesIO
from .extractor import Node
import json

class BaseDataWriter(Node):

    def __init__(self, needs=None, key_builder=None, database=None):
        super(BaseDataWriter, self).__init__(needs=needs)
        self.key_builder = key_builder
        self.database = database


class DataWriter(BaseDataWriter):

    def __init__(self, needs=None, _id=None, feature_name=None, feature_version=None, key_builder=None, database=None, event_log=None):
        super(DataWriter, self).__init__(needs=needs,
          key_builder=key_builder,
          database=database)
        self.event_log = event_log
        self.feature_version = feature_version
        self._id = _id
        self.feature_name = feature_name
        self.content_type = needs.content_type

    @property
    def key(self):
        assert self.feature_version is not None
        return self.key_builder.build(self._id, self.feature_name, self.feature_version)

    def __enter__(self):
        self._stream = self.database.write_stream(self.key, self.content_type)
        return self

    def _close_stream(self):
        try:
            self._stream.close()
        except (IOError, ValueError):
            pass

    def _cleanup_after_error(self):
        try:
            del self.database[self.key]
        except:
            pass

    def _log_events(self):
        if self.event_log is None:
            return
        self.event_log.append(json.dumps({'_id':self._id, 
         'name':self.feature_name, 
         'version':self.feature_version}))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close_stream()
        if exc_type:
            self._cleanup_after_error()
            return
        self._log_events()

    def _process(self, data):
        try:
            data = data.encode()
        except AttributeError:
            pass

        yield self._stream.write(data)


class ClobberDataWriter(DataWriter):

    def __init__(self, needs=None, _id=None, feature_name=None, feature_version=None, key_builder=None, database=None, event_log=None):
        super(ClobberDataWriter, self).__init__(needs=needs,
          _id=_id,
          feature_name=feature_name,
          feature_version=feature_version,
          key_builder=key_builder,
          database=database,
          event_log=event_log)

    def _cleanup_after_error(self):
        pass

    def _process(self, data):
        self._stream = self.database.write_stream(self.key, self.content_type)
        try:
            x = self._stream.write(data)
        except TypeError:
            x = self._stream.write(data.encode())

        self._stream.close()
        yield x


class BytesIODataWriter(BaseDataWriter):

    def __init__(self, needs=None, _id=None, feature_name=None, feature_version=None, key_builder=None, database=None, event_log=None, buffer_size_limit=None):
        super(BytesIODataWriter, self).__init__(needs=needs,
          key_builder=key_builder,
          database=database)
        self.buffer_size_limit = buffer_size_limit or 2147483648
        self.event_log = event_log
        self.feature_version = feature_version
        self._id = _id
        self.feature_name = feature_name
        self.content_type = needs.content_type
        self._stream = BytesIO()

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self._stream

    def _process(self, data):
        if len(data) < self.buffer_size_limit:
            try:
                yield self._stream.write(data)
            except TypeError:
                yield self._stream.write(data.encode())

        else:
            chunksize = self.buffer_size_limit // 2
            for i in range(0, len(data), chunksize):
                yield self._stream.write(data[i:i + chunksize])