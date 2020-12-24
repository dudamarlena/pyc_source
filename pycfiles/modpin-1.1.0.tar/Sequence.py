# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patricia/patricia/modppi/./src/SBI/sequence/Sequence.py
# Compiled at: 2018-02-02 06:38:50
"""
Sequence

author: jbonet
date:   05/2013

@oliva's lab
"""
import re, copy
from collections import Counter
AVAILABLE_FORMATS = set(['TAB', 'FASTA'])
gapdefinition = '[-x]'

class Sequence(object):

    def __init__(self, seqID='', sequence=''):
        global gapdefinition
        if bool(re.search('\\s', seqID)):
            self._seqID = seqID.split()[0]
            self._info = (' ').join(seqID.split()[1:])
        else:
            self._seqID = seqID
            self._info = ''
        self._sequence = sequence
        self._gapped = bool(re.search(gapdefinition, self._sequence))

    @property
    def id(self):
        return self._seqID

    @id.setter
    def id(self, value):
        if bool(re.search('\\s', value)):
            self._seqID = value.split()[0]
            self._info = (' ').join(value.split()[1:])
        else:
            self._seqID = value

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, value):
        self._sequence = value
        self._gapped = bool(re.search('-', self._sequence))

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, value):
        self._info = value

    @property
    def is_gapped(self):
        return self._gapped

    def contains(self, sequence):
        if isinstance(sequence, basestring):
            return bool(re.search(sequence, self.sequence))
        else:
            if isinstance(sequence, Sequence):
                return bool(re.search(sequence.sequence, self.sequence))
            return NotImplemented

    def contained(self, sequence):
        if isinstance(sequence, basestring):
            return bool(re.search(self.sequence, sequence))
        else:
            if isinstance(sequence, Sequence):
                return bool(re.search(self.sequence, sequence.sequence))
            return NotImplemented

    def format(self, format='TAB'):
        global AVAILABLE_FORMATS
        if format.upper() not in AVAILABLE_FORMATS:
            raise AttributeError('format option not available')
        if format.upper() == 'TAB':
            return ('{0.id}\t{0.sequence}').format(self)
        if format.upper() == 'FASTA':
            return ('>{0.id}\n{0.sequence}').format(self)

    def tokenize(self, token_coding=None):
        if token_coding is None:
            return copy.deepcopy(self._sequence)
        else:
            if token_coding is 'binary':
                tc = [
                 '\\D', '1', '-', '0']
                return re.sub(tc[0], tc[1], re.sub(tc[2], tc[3], self._sequence))
            return

    def aa_frequency(self):
        return dict([ (x, float(y) / len(self)) for x, y in Counter(re.sub(gapdefinition, '', self._sequence)).iteritems() ])

    def duplicate(self):
        return copy.deepcopy(self)

    def do_ungap(self):
        if self._gapped:
            self._sequence = re.sub(gapdefinition, '', self._sequence)

    def append(self, sequence):
        if isinstance(sequence, basestring):
            self._sequence += sequence
            if not self._gapped:
                self._gapped = bool(re.search('-', self._sequence))
        elif isinstance(sequence, (tuple, list)):
            self._sequence += ('').join(sequence)
            if not self._gapped:
                self._gapped = bool(re.search('-', self._sequence))
        else:
            raise AttributeError()

    def __len__(self):
        return len(self._sequence)

    def __eq__(self, other):
        if isinstance(other, Sequence):
            return self.sequence == other.sequence
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __lt__(self, other):
        if isinstance(other, Sequence):
            return len(self) < len(other)
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Sequence):
            return len(self) > len(other)
        return NotImplemented

    def __getitem__(self, key):
        try:
            int(key)
            return self._sequence[int(key)]
        except:
            if not isinstance(key, slice):
                raise TypeError
            else:
                return self._sequence[key]

    def __iter__(self):
        for s in self._sequence:
            yield s

    def __repr__(self):
        return ('<{0.__class__.__name__}: [{0.id}, {0.sequence}]>').format(self)

    def __str__(self):
        return ('{0.id}\t{0.sequence}').format(self)