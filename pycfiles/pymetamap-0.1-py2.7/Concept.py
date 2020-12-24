# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/pymetamap/Concept.py
# Compiled at: 2018-02-09 08:36:09
from collections import namedtuple
FIELD_NAMES_MMI = ('index', 'mm', 'score', 'preferred_name', 'cui', 'semtypes', 'trigger',
                   'location', 'pos_info', 'tree_codes')
FIELD_NAMES_AA = ('index', 'aa', 'short_form', 'long_form', 'num_tokens_short_form',
                  'num_chars_short_form', 'num_tokens_long_form', 'num_chars_long_form',
                  'pos_info')
FIELD_NAMES_UA = ('index', 'ua', 'short_form', 'long_form', 'num_tokens_short_form',
                  'num_chars_short_form', 'num_tokens_long_form', 'num_chars_long_form',
                  'pos_info')

class ConceptMMI(namedtuple('Concept', FIELD_NAMES_MMI)):

    def __repr__(self):
        items = [ (field, getattr(self, field, None)) for field in FIELD_NAMES_MMI ]
        fields = [ '%s=%r' % (k, v) for k, v in items if v is not None ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(fields))

    def as_mmi(self):
        return ('|').join([ get(field) for field in FIELD_NAMES_MMI ])

    @classmethod
    def from_mmi(this_class, line):
        fields = line.split('|')
        return this_class(**dict(zip(FIELD_NAMES_MMI, fields)))


class ConceptAA(namedtuple('Concept', FIELD_NAMES_AA)):

    def __repr__(self):
        items = [ (field, getattr(self, field, None)) for field in FIELD_NAMES_AA ]
        fields = [ '%s=%r' % (k, v) for k, v in items if v is not None ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(fields))

    def as_mmi(self):
        return ('|').join([ get(field) for field in FIELD_NAMES_AA ])

    @classmethod
    def from_mmi(this_class, line):
        fields = line.split('|')
        return this_class(**dict(zip(FIELD_NAMES_AA, fields)))


class ConceptUA(namedtuple('Concept', FIELD_NAMES_UA)):

    def __repr__(self):
        items = [ (field, getattr(self, field, None)) for field in FIELD_NAMES_UA ]
        fields = [ '%s=%r' % (k, v) for k, v in items if v is not None ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(fields))

    def as_mmi(self):
        return ('|').join([ get(field) for field in FIELD_NAMES_UA ])

    @classmethod
    def from_mmi(this_class, line):
        fields = line.split('|')
        return this_class(**dict(zip(FIELD_NAMES_UA, fields)))


class Corpus(list):

    @classmethod
    def load(this_class, stream):
        stream = iter(stream)
        corpus = this_class()
        for line in stream:
            fields = line.split('|')
            if fields[1] == 'MMI':
                corpus.append(ConceptMMI.from_mmi(line))
            elif fields[1] == 'AA':
                corpus.append(ConceptAA.from_mmi(line))
            else:
                corpus.append(ConceptUA.from_mmi(line))

        return corpus