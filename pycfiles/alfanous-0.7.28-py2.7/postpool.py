# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Support/whoosh/filedb/postpool.py
# Compiled at: 2015-06-30 06:52:38
"""Support functions and classes implementing the KinoSearch-like external sort
merging model. This module does not contain any user-level objects.
"""
import os, tempfile
from heapq import heapify, heapreplace, heappop
from struct import Struct
from alfanous.Support.whoosh.filedb.structfile import StructFile, pack_ushort, unpack_ushort
from alfanous.Support.whoosh.system import _INT_SIZE, _USHORT_SIZE
from alfanous.Support.whoosh.util import utf8encode, utf8decode
_2int_struct = Struct('!II')
pack2ints = _2int_struct.pack
unpack2ints = _2int_struct.unpack

def encode_posting(fieldnum, text, doc, freq, datastring):
    """Encodes a posting as a string, for sorting.
    """
    return ('').join([pack_ushort(fieldnum),
     utf8encode(text)[0],
     chr(0),
     pack2ints(doc, freq),
     datastring])


def decode_posting(posting):
    """Decodes an encoded posting string into a
    (field_number, text, document_number, datastring) tuple.
    """
    fieldnum = unpack_ushort(posting[:_USHORT_SIZE])[0]
    zero = posting.find(chr(0), _USHORT_SIZE)
    text = utf8decode(posting[_USHORT_SIZE:zero])[0]
    metastart = zero + 1
    metaend = metastart + _INT_SIZE * 2
    doc, freq = unpack2ints(posting[metastart:metaend])
    datastring = posting[metaend:]
    return (
     fieldnum, text, doc, freq, datastring)


def merge(run_readers, max_chunk_size):
    current = [ (r.next(), i) for i, r in enumerate(run_readers)
              ]
    heapify(current)
    active = len(run_readers)
    output = []
    outputBufferSize = 0
    while active > 0:
        p, i = current[0]
        output.append(p)
        outputBufferSize += len(p)
        if outputBufferSize > max_chunk_size:
            for p in output:
                yield decode_posting(p)

            output = []
            outputBufferSize = 0
        if run_readers[i] is not None:
            p = run_readers[i].next()
            if p:
                heapreplace(current, (p, i))
            else:
                heappop(current)
                active -= 1

    if len(current) > 0:
        output.extend([ p for p, i in current ])
    if len(output) > 0:
        for p in output:
            yield decode_posting(p)

    return


class RunReader(object):
    """An iterator that yields posting strings from a "run" on disk.
    This class buffers the reads to improve efficiency.
    """

    def __init__(self, stream, count, buffer_size):
        """
        :param stream: the file from which to read.
        :param count: the number of postings in the stream.
        :param buffer_size: the size (in bytes) of the read buffer to use.
        """
        self.stream = stream
        self.count = count
        self.buffer_size = buffer_size
        self.buffer = []
        self.pointer = 0
        self.finished = False

    def close(self):
        self.stream.close()

    def _fill(self):
        if self.finished:
            return
        buffer = self.buffer = []
        self.pointer = 0
        so_far = 0
        count = self.count
        while so_far < self.buffer_size:
            if count <= 0:
                break
            p = self.stream.read_string2()
            buffer.append(p)
            so_far += len(p)
            count -= 1

        self.count = count

    def __iter__(self):
        return self

    def next(self):
        assert self.pointer <= len(self.buffer)
        if self.pointer == len(self.buffer):
            self._fill()
        if len(self.buffer) == 0:
            self.finished = True
            return None
        else:
            r = self.buffer[self.pointer]
            self.pointer += 1
            return r


class PostingPool(object):
    """Represents the "pool" of all postings to be sorted. As documents are
    added, this object writes out "runs" of sorted encoded postings. When all
    documents have been added, this object merge sorts the runs from disk,
    yielding decoded postings to the SegmentWriter.
    """

    def __init__(self, limit):
        """
        :param limit: the maximum amount of memory to use at once for adding
            postings and the merge sort.
        """
        self.limit = limit
        self.size = 0
        self.postings = []
        self.finished = False
        self.runs = []
        self.tempfilenames = []
        self.count = 0

    def add_posting(self, field_num, text, doc, freq, datastring):
        """Adds a posting to the pool.
        """
        if self.finished:
            raise Exception("Can't add postings after you iterate over the pool")
        if self.size >= self.limit:
            self._flush_run()
        posting = encode_posting(field_num, text, doc, freq, datastring)
        self.size += len(posting)
        self.postings.append(posting)
        self.count += 1

    def _flush_run(self):
        if self.size > 0:
            tempfd, tempname = tempfile.mkstemp('.whooshrun')
            runfile = StructFile(os.fdopen(tempfd, 'w+b'))
            self.postings.sort()
            for p in self.postings:
                runfile.write_string2(p)

            runfile.flush()
            runfile.seek(0)
            self.runs.append((runfile, self.count))
            self.tempfilenames.append(tempname)
            self.postings = []
            self.size = 0
            self.count = 0

    def __iter__(self):
        if self.finished:
            raise Exception('Tried to iterate on PostingPool twice')
        run_count = len(self.runs)
        if self.postings and run_count == 0:
            self.postings.sort()
            for p in self.postings:
                yield decode_posting(p)

            return
        if not self.postings and run_count == 0:
            return
        if self.postings:
            self._flush_run()
            run_count = len(self.runs)
        max_chunk_size = int(self.limit / (run_count + 1))
        run_readers = [ RunReader(run_file, count, max_chunk_size) for run_file, count in self.runs
                      ]
        for decoded_posting in merge(run_readers, max_chunk_size):
            yield decoded_posting

        for rr in run_readers:
            assert rr.count == 0
            rr.close()

        for tempfilename in self.tempfilenames:
            os.remove(tempfilename)

        self.finished = True