# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ulutil/SeqRecordLite.py
# Compiled at: 2014-12-19 21:47:25
import copy
from Bio.Seq import Seq, UnknownSeq
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio.Alphabet import NucleotideAlphabet

class SeqRecordLite(object):
    """SeqRecord wrapper that allows simpler attribute access.
    
    The underlying data structure is actually a biopython `SeqRecord` object.
    This class wraps it in a way that maintains the simple-to-use interface to
    get at some common annotations. It also knows how to print out it's data
    as IMGT-flavored INSDC (e.g., GenBank/EMBL).
    """

    def __init__(self, biopython_object=None):
        if biopython_object == None:
            self._record = SeqRecord(seq=UnknownSeq(0, alphabet=NucleotideAlphabet()), id='', name='', description='')
        else:
            if isinstance(biopython_object, Seq):
                self._record = SeqRecord(seq=copy.deepcopy(biopython_object), id='', name='', description='')
            elif isinstance(biopython_object, SeqRecord):
                self._record = copy.deepcopy(biopython_object)
            self._features = {}
            for i, feature in enumerate(self._record.features):
                self._features.setdefault(feature.type, []).append(i)

        return

    def __getattr__(self, name):
        if name in self._record.annotations:
            return self._record.annotations[name]
        if name in self._features:
            return [ self._record.features[i] for i in self._features[name] ]
        raise AttributeError

    @property
    def seq(self):
        return self._record.seq

    @seq.setter
    def seq(self, s):
        self._record.seq = s

    @property
    def annotations(self):
        return self._record.annotations

    @property
    def id(self):
        return self._record.id

    @id.setter
    def id(self, i):
        self._record.id = i

    @property
    def description(self):
        return self._record.description

    @description.setter
    def description(self, d):
        self._record.description = d

    @property
    def name(self):
        return self._record.name

    @name.setter
    def name(self, n):
        self._record.name = n

    @property
    def features(self):
        return self._record.features

    def format(self, *args, **kw):
        return self._record.format(*args, **kw)

    def add_feature(self, start=None, end=None, type='', strand=None, qualifiers=None):
        if start == None or end == None:
            raise ValueError, 'if there is no spanning location...use an annotation?'
        location = FeatureLocation(start, end)
        feature = SeqFeature(location=location, type=type, strand=strand, qualifiers=qualifiers)
        self._record.features.append(feature)
        self._features.setdefault(feature.type, []).append(len(self._record.features) - 1)
        return self

    def has_feature(self, type):
        return type in self._features

    def del_feature(self, type):
        idxs = self._features.pop(type)
        idxs.sort(reverse=True)
        for i in idxs:
            self._record.features.pop(i)

        return self

    def __len__(self):
        return len(self.seq)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.format('imgt')