# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Support/whoosh/filedb/filewriting.py
# Compiled at: 2015-06-30 06:52:38
from array import array
from collections import defaultdict
from alfanous.Support.whoosh.fields import UnknownFieldError
from alfanous.Support.whoosh.store import LockError
from alfanous.Support.whoosh.writing import IndexWriter
from alfanous.Support.whoosh.filedb import postpool
from alfanous.Support.whoosh.support.filelock import try_for
from alfanous.Support.whoosh.filedb.fileindex import SegmentDeletionMixin, Segment, SegmentSet
from alfanous.Support.whoosh.filedb.filepostings import FilePostingWriter
from alfanous.Support.whoosh.filedb.filetables import FileTableWriter, FileListWriter, FileRecordWriter, encode_termkey, encode_vectorkey, encode_terminfo, enpickle, packint
from alfanous.Support.whoosh.util import fib
DOCLENGTH_TYPE = 'H'
DOCLENGTH_LIMIT = 65535

def NO_MERGE(ix, writer, segments):
    """This policy does not merge any existing segments.
    """
    return segments


def MERGE_SMALL(ix, writer, segments):
    """This policy merges small segments, where "small" is defined using a
    heuristic based on the fibonacci sequence.
    """
    from alfanous.Support.whoosh.filedb.filereading import SegmentReader
    newsegments = SegmentSet()
    sorted_segment_list = sorted((s.doc_count_all(), s) for s in segments)
    total_docs = 0
    for i, (count, seg) in enumerate(sorted_segment_list):
        if count > 0:
            total_docs += count
            if total_docs < fib(i + 5):
                writer.add_reader(SegmentReader(ix.storage, seg, ix.schema))
            else:
                newsegments.append(seg)

    return newsegments


def OPTIMIZE(ix, writer, segments):
    """This policy merges all existing segments.
    """
    from alfanous.Support.whoosh.filedb.filereading import SegmentReader
    for seg in segments:
        writer.add_reader(SegmentReader(ix.storage, seg, ix.schema))

    return SegmentSet()


def create_terms(storage, segment):
    termfile = storage.create_file(segment.term_filename)
    return FileTableWriter(termfile, keycoder=encode_termkey, valuecoder=encode_terminfo)


def create_storedfields(storage, segment):
    listfile = storage.create_file(segment.docs_filename)
    return FileListWriter(listfile, valuecoder=enpickle)


def create_vectors(storage, segment):
    vectorfile = storage.create_file(segment.vector_filename)
    return FileTableWriter(vectorfile, keycoder=encode_vectorkey, valuecoder=packint)


def create_doclengths(storage, segment, fieldcount):
    recordformat = '!' + DOCLENGTH_TYPE * fieldcount
    recordfile = storage.create_file(segment.doclen_filename)
    return FileRecordWriter(recordfile, recordformat)


class FileIndexWriter(SegmentDeletionMixin, IndexWriter):

    def __init__(self, ix, postlimit=33554432, blocklimit=128, timeout=0.0, delay=0.1):
        """
        :param ix: the Index object you want to write to.
        :param postlimit: Essentially controls the maximum amount of memory the
            indexer uses at a time, in bytes (the actual amount of memory used
            by the Python process will be much larger because of other
            overhead). The default (32MB) is a bit small. You may want to
            increase this value for very large collections, e.g.
            ``postlimit=256*1024*1024``.
        """
        self.lock = ix.storage.lock(ix.indexname + '_LOCK')
        if not try_for(self.lock.acquire, timeout=timeout, delay=delay):
            raise LockError('Index %s is already locked for writing')
        self.index = ix
        self.segments = ix.segments.copy()
        self.postlimit = postlimit
        self.blocklimit = blocklimit
        self._segment_writer = None
        self._searcher = ix.searcher()
        return

    def _finish(self):
        self._close_reader()
        self.lock.release()
        self._segment_writer = None
        return

    def segment_writer(self):
        """Returns the underlying SegmentWriter object.
        """
        if not self._segment_writer:
            self._segment_writer = SegmentWriter(self.index, self.postlimit, self.blocklimit)
        return self._segment_writer

    def add_document(self, **fields):
        self.segment_writer().add_document(fields)

    def commit(self, mergetype=MERGE_SMALL):
        """Finishes writing and unlocks the index.
        
        :param mergetype: How to merge existing segments. One of
            :class:`whoosh.filedb.filewriting.NO_MERGE`,
            :class:`whoosh.filedb.filewriting.MERGE_SMALL`,
            or :class:`whoosh.filedb.filewriting.OPTIMIZE`.
        """
        self._close_reader()
        if self._segment_writer or mergetype is OPTIMIZE:
            self._merge_segments(mergetype)
        self.index.commit(self.segments)
        self._finish()

    def cancel(self):
        if self._segment_writer:
            self._segment_writer._close_all()
        self._finish()

    def _merge_segments(self, mergetype):
        sw = self.segment_writer()
        new_segments = mergetype(self.index, sw, self.segments)
        sw.close()
        new_segments.append(sw.segment())
        self.segments = new_segments


class SegmentWriter(object):
    """Do not instantiate this object directly; it is created by the
    IndexWriter object.
    
    Handles the actual writing of new documents to the index: writes stored
    fields, handles the posting pool, and writes out the term index.
    """

    def __init__(self, ix, postlimit, blocklimit, name=None):
        """
        :param ix: the Index object in which to write the new segment.
        :param postlimit: the maximum size for a run in the posting pool.
        :param blocklimit: the maximum number of postings in a posting block.
        :param name: the name of the segment.
        """
        self.index = ix
        self.schema = ix.schema
        self.storage = storage = ix.storage
        self.name = name or ix._next_segment_name()
        self.max_doc = 0
        self.pool = postpool.PostingPool(postlimit)
        self._scorable_to_pos = dict((fnum, i) for i, fnum in enumerate(self.schema.scorable_fields()))
        self._stored_to_pos = dict((fnum, i) for i, fnum in enumerate(self.schema.stored_fields()))
        tempseg = Segment(self.name, 0, 0, None)
        self.termtable = create_terms(storage, tempseg)
        self.docslist = create_storedfields(storage, tempseg)
        self.doclengths = None
        if self.schema.scorable_fields():
            self.doclengths = create_doclengths(storage, tempseg, len(self._scorable_to_pos))
        postfile = storage.create_file(tempseg.posts_filename)
        self.postwriter = FilePostingWriter(postfile, blocklimit=blocklimit)
        self.vectortable = None
        if self.schema.has_vectored_fields():
            self.vectortable = create_vectors(storage, tempseg)
            vpostfile = storage.create_file(tempseg.vectorposts_filename)
            self.vpostwriter = FilePostingWriter(vpostfile, stringids=True)
        self.field_length_totals = defaultdict(int)
        return

    def segment(self):
        """Returns an index.Segment object for the segment being written."""
        return Segment(self.name, self.max_doc, dict(self.field_length_totals))

    def _close_all(self):
        self.termtable.close()
        self.postwriter.close()
        self.docslist.close()
        if self.doclengths:
            self.doclengths.close()
        if self.vectortable:
            self.vectortable.close()
            self.vpostwriter.close()

    def close(self):
        """Finishes writing the segment (flushes the posting pool out to disk)
        and closes all open files.
        """
        self._flush_pool()
        self._close_all()

    def add_reader(self, reader):
        """Adds the contents of another segment to this one. This is used to
        merge existing segments into the new one before deleting them.
        
        :param ix: The index.Index object containing the segment to merge.
        :param segment: The index.Segment object to merge into this one.
        """
        start_doc = self.max_doc
        has_deletions = reader.has_deletions()
        if has_deletions:
            doc_map = {}
        schema = self.schema
        name2num = schema.name_to_number
        stored_to_pos = self._stored_to_pos

        def storedkeyhelper(item):
            return stored_to_pos[name2num(item[0])]

        docnum = 0
        vectored_fieldnums = schema.vectored_fields()
        for docnum in xrange(reader.doc_count_all()):
            if not reader.is_deleted(docnum):
                storeditems = reader.stored_fields(docnum).items()
                storedvalues = [ v for k, v in sorted(storeditems, key=storedkeyhelper)
                               ]
                self._add_doc_data(storedvalues, reader.doc_field_lengths(docnum))
                if has_deletions:
                    doc_map[docnum] = self.max_doc
                for fieldnum in vectored_fieldnums:
                    if reader.has_vector(docnum, fieldnum):
                        self._add_vector(fieldnum, reader.vector(docnum, fieldnum).items())

                self.max_doc += 1

        for fieldnum in schema.scorable_fields():
            self.field_length_totals[fieldnum] += reader.field_length(fieldnum)

        current_fieldnum = None
        decoder = None
        for fieldnum, text, _, _ in reader:
            if fieldnum != current_fieldnum:
                current_fieldnum = fieldnum
                decoder = schema[fieldnum].format.decode_frequency
            postreader = reader.postings(fieldnum, text)
            for docnum, valuestring in postreader.all_items():
                if has_deletions:
                    newdoc = doc_map[docnum]
                else:
                    newdoc = start_doc + docnum
                freq = decoder(valuestring)
                self.pool.add_posting(fieldnum, text, newdoc, freq, valuestring)

        return

    def add_document(self, fields):
        scorable_to_pos = self._scorable_to_pos
        stored_to_pos = self._stored_to_pos
        schema = self.schema
        fieldnames = [ name for name in fields.keys() if not name.startswith('_')
                     ]
        fieldnames.sort(key=schema.name_to_number)
        for name in fieldnames:
            if name not in schema:
                raise UnknownFieldError('There is no field named %r' % name)

        fieldlengths = array(DOCLENGTH_TYPE, [0] * len(scorable_to_pos))
        storedvalues = [
         None] * len(stored_to_pos)
        for name in fieldnames:
            value = fields.get(name)
            if value:
                fieldnum = schema.name_to_number(name)
                field = schema.field_by_number(fieldnum)
                if field.indexed:
                    count = 0
                    unique = 0
                    for w, freq, valuestring in field.index(value):
                        self.pool.add_posting(fieldnum, w, self.max_doc, freq, valuestring)
                        count += freq
                        unique += 1

                    if field.scorable:
                        self.field_length_totals[fieldnum] += count
                        pos = scorable_to_pos[fieldnum]
                        fieldlengths[pos] = min(count, DOCLENGTH_LIMIT)
                vector = field.vector
                if vector:
                    vlist = sorted((w, valuestring) for w, freq, valuestring in vector.word_values(value, mode='index'))
                    self._add_vector(fieldnum, vlist)
                if field.stored:
                    storedname = '_stored_' + name
                    if storedname in fields:
                        stored_value = fields[storedname]
                    else:
                        stored_value = value
                    storedvalues[stored_to_pos[fieldnum]] = stored_value

        self._add_doc_data(storedvalues, fieldlengths)
        self.max_doc += 1
        return

    def _add_terms(self):
        pass

    def _add_doc_data(self, storedvalues, fieldlengths):
        self.docslist.append(storedvalues)
        if self.doclengths:
            self.doclengths.append(fieldlengths)

    def _add_vector(self, fieldnum, vlist):
        vpostwriter = self.vpostwriter
        vformat = self.schema[fieldnum].vector
        offset = vpostwriter.start(vformat)
        for text, valuestring in vlist:
            assert isinstance(text, unicode), '%r is not unicode' % text
            vpostwriter.write(text, valuestring)

        vpostwriter.finish()
        self.vectortable.add((self.max_doc, fieldnum), offset)

    def _flush_pool(self):
        termtable = self.termtable
        postwriter = self.postwriter
        schema = self.schema
        current_fieldnum = None
        current_text = None
        first = True
        current_freq = 0
        offset = None
        for fieldnum, text, docnum, freq, valuestring in self.pool:
            if first or fieldnum > current_fieldnum or text > current_text:
                if first:
                    first = False
                else:
                    postcount = postwriter.finish()
                    termtable.add((current_fieldnum, current_text), (
                     current_freq, offset, postcount))
                current_fieldnum = fieldnum
                current_text = text
                current_freq = 0
                offset = postwriter.start(schema[fieldnum].format)
            elif fieldnum < current_fieldnum or fieldnum == current_fieldnum and text < current_text:
                raise Exception('Postings are out of order: %s:%s .. %s:%s' % (
                 current_fieldnum, current_text, fieldnum, text))
            current_freq += freq
            postwriter.write(docnum, valuestring)

        if not first:
            postcount = postwriter.finish()
            termtable.add((current_fieldnum, current_text), (
             current_freq, offset, postcount))
        return