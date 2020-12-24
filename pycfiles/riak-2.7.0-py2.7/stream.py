# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/transports/tcp/stream.py
# Compiled at: 2016-11-28 18:50:45
import json, riak.pb.messages
from riak.util import decode_index_value, bytes_to_str
from riak.client.index_page import CONTINUATION
from riak.codecs.ttb import TtbCodec
from six import PY2

class PbufStream(object):
    """
    Used internally by TcpTransport to implement streaming
    operations. Implements the iterator interface.
    """
    _expect = None

    def __init__(self, transport, codec):
        self.finished = False
        self.transport = transport
        self.codec = codec
        self.resource = None
        self._mid_stream = False
        return

    def __iter__(self):
        return self

    def next(self):
        if self.finished:
            raise StopIteration
        try:
            try:
                resp_code, data = self.transport._recv_msg(mid_stream=self._mid_stream)
                self.codec.maybe_riak_error(resp_code, data)
                expect = self._expect
                self.codec.maybe_incorrect_code(resp_code, expect)
                resp = self.codec.parse_msg(expect, data)
            except:
                self.finished = True
                raise

        finally:
            self._mid_stream = True

        if self._is_done(resp):
            self.finished = True
        return resp

    def __next__(self):
        return self.next()

    def _is_done(self, response):
        return response.done

    def attach(self, resource):
        self.resource = resource

    def close(self):
        try:
            while self.next():
                pass

        except StopIteration:
            pass

        self.resource.release()


class PbufKeyStream(PbufStream):
    """
    Used internally by TcpTransport to implement key-list streams.
    """
    _expect = riak.pb.messages.MSG_CODE_LIST_KEYS_RESP

    def next(self):
        response = super(PbufKeyStream, self).next()
        if response.done and len(response.keys) is 0:
            raise StopIteration
        return response.keys

    def __next__(self):
        return self.next()


class PbufMapredStream(PbufStream):
    """
    Used internally by TcpTransport to implement MapReduce
    streams.
    """
    _expect = riak.pb.messages.MSG_CODE_MAP_RED_RESP

    def next(self):
        response = super(PbufMapredStream, self).next()
        if response.done and not response.HasField('response'):
            raise StopIteration
        return (response.phase, json.loads(bytes_to_str(response.response)))

    def __next__(self):
        return self.next()


class PbufBucketStream(PbufStream):
    """
    Used internally by TcpTransport to implement key-list streams.
    """
    _expect = riak.pb.messages.MSG_CODE_LIST_BUCKETS_RESP

    def next(self):
        response = super(PbufBucketStream, self).next()
        if response.done and len(response.buckets) is 0:
            raise StopIteration
        return response.buckets

    def __next__(self):
        return self.next()


class PbufIndexStream(PbufStream):
    """
    Used internally by TcpTransport to implement Secondary Index
    streams.
    """
    _expect = riak.pb.messages.MSG_CODE_INDEX_RESP

    def __init__(self, transport, codec, index, return_terms=False):
        super(PbufIndexStream, self).__init__(transport, codec)
        self.index = index
        self.return_terms = return_terms

    def next(self):
        response = super(PbufIndexStream, self).next()
        if response.done and not (response.keys or response.results or response.continuation):
            raise StopIteration
        if self.return_terms and response.results:
            return [ (decode_index_value(self.index, r.key), bytes_to_str(r.value)) for r in response.results
                   ]
        if response.keys:
            if PY2:
                return response.keys[:]
            else:
                return [ bytes_to_str(key) for key in response.keys ]

        elif response.continuation:
            return CONTINUATION(bytes_to_str(response.continuation))

    def __next__(self):
        return self.next()


class PbufTsKeyStream(PbufStream, TtbCodec):
    """
    Used internally by TcpTransport to implement TS key-list streams.
    """
    _expect = riak.pb.messages.MSG_CODE_TS_LIST_KEYS_RESP

    def __init__(self, transport, codec, convert_timestamp=False):
        super(PbufTsKeyStream, self).__init__(transport, codec)
        self._convert_timestamp = convert_timestamp

    def next(self):
        response = super(PbufTsKeyStream, self).next()
        if response.done and len(response.keys) is 0:
            raise StopIteration
        keys = []
        for tsrow in response.keys:
            keys.append(self.codec.decode_timeseries_row(tsrow, convert_timestamp=self._convert_timestamp))

        return keys

    def __next__(self):
        return self.next()