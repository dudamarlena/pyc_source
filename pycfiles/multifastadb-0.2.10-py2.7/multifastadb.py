# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/multifastadb.py
# Compiled at: 2015-09-10 18:04:53
from __future__ import absolute_import, division, print_function, unicode_literals
import collections, itertools, logging, os, re
from ordered_set import OrderedSet
import pysam

class MultiFastaDB(object):
    """
    """

    class SequenceProxy(object):
        """represents a future sequence fetch

        SequenceProxy defers the actual fetch until a slice is
        applied, allowing convenient and sexy slice syntax like this:

        >> mfdb = MultiFastaDB('/my/seqs')
        >> seq = mfdb['NM_01234.5'][4:20]

        """

        def __init__(self, mfdb, ac):
            self.mfdb = mfdb
            self.ac = ac

        def __getitem__(self, key):
            if isinstance(key, slice):
                return self.mfdb.fetch(self.ac, key.start, key.stop)[::key.step]
            raise TypeError(b'SequenceProxy accepts only slice intervals (in interbase coordinates)')

        def __str__(self):
            return self.mfdb.fetch(self.ac)

    file_suffixes = [
     b'fa', b'fasta', b'faa', b'fna']
    compression_suffixes = [b'bgz']
    default_suffixes = file_suffixes + [ fs + b'.' + cs for fs in file_suffixes for cs in compression_suffixes ]

    def __init__(self, sources=[], suffixes=default_suffixes, use_meta_index=False):
        self._fastas = None
        self._index = None
        self._logger = logging.getLogger(__name__)
        self.sources = sources
        self.suffixes = [ b'.' + sfx for sfx in suffixes ]
        self.use_meta_index = use_meta_index
        self.open_sources()
        return

    def open_sources(self):
        """Opens or reopens fasta sources (directories or files) provided when
        the instance was created.

        """

        def _has_valid_suffix(f):
            return any(f.endswith(sfx) for sfx in self.suffixes)

        def _find_files(sources):
            for s in sources:
                if os.path.isfile(s):
                    yield s
                    continue
                if os.path.isdir(s):
                    for r, _, fs in os.walk(s, followlinks=True):
                        for f in sorted(fs):
                            if _has_valid_suffix(f):
                                yield os.path.join(r, f)

                    continue
                raise IOError(s + b': invalid or non-existent source for fasta files')

        def _open1(fa_path):
            fai_path = fa_path + b'.fai'
            if os.path.exists(fai_path) and os.stat(fa_path).st_mtime > os.stat(fai_path).st_mtime:
                self._logger.warn(fai_path + b' is out-of-date (older than fasta file)')
            faf = pysam.Fastafile(fa_path)
            self._logger.info(b'opened ' + fa_path)
            return faf

        fa_paths = OrderedSet(os.path.realpath(f) for f in _find_files(self.sources))
        self._fastas = collections.OrderedDict((fa_path, _open1(fa_path)) for fa_path in fa_paths)
        self.create_index()

    def create_index(self):
        """Create a convenience meta index in which secondary accessions refer
        to primary accessions that occur in the fasta file. 

        For example, the primary accession
        'gi|548923668|ref|NM_001284401.1|' would generate two
        secondary accessions '548923668' and 'NM_001284401.1', and two
        tuples ('548923668', 'gi|548923668|ref|NM_001284401.1|') and
        ('NM_001284401.1', 'gi|548923668|ref|NM_001284401.1|') in the
        meta index. Attempts to lookup a secondary accession return
        the sequence for the corresponding primary accession.

        """
        self._index = collections.OrderedDict()
        ncbi_re = re.compile(b'(?:ref|gb)\\|([^|]+)')
        for ref in self.references:
            acs = [
             ref]
            if self.use_meta_index:
                acs += ncbi_re.findall(ref)
            for ac in acs:
                if ac not in self._index:
                    self._index[ac] = ref
                else:
                    files = [ e[0] for e in self.where_is(ac) ]
                    self._logger.debug((b'multiple entries found for {ac} in {files}').format(ac=ac, files=(b', ').join(files)))

    def where_is(self, ac):
        """return list of all (filename,pysam.Fastafile) pairs in which
        accession occurs

        TODO: This is broken for meta index lookups
        """
        return [ (fp, fh) for fp, fh in self._fastas.iteritems() if ac in fh
               ]

    @property
    def references(self):
        return list(itertools.chain.from_iterable([ fa.references for fa in self._fastas.values() ]))

    @property
    def lengths(self):
        return list(itertools.chain.from_iterable([ fa.lengths for fa in self._fastas.values() ]))

    def fetch(self, ac, start_i=None, end_i=None):
        """return a sequence, or subsequence if start_i and end_i are provided"""
        for fah in self._fastas.values():
            seq = fah.fetch(self._index[ac], start_i, end_i)
            if seq != b'':
                return seq

        return

    def __contains__(self, ac):
        return any([ ac in fh for fh in self._fastas.itervalues() ])

    def __getitem__(self, ac):
        if ac in self._index:
            return self.SequenceProxy(self, ac)
        else:
            return