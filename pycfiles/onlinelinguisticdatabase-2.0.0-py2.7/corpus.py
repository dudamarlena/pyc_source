# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/model/corpus.py
# Compiled at: 2016-09-19 13:27:02
"""Corpus model"""
from sqlalchemy import Column, Sequence, ForeignKey
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime, Boolean
from sqlalchemy.orm import relation
from onlinelinguisticdatabase.model.meta import Base, now
import logging
log = logging.getLogger(name=__name__)

class CorpusForm(Base):
    __tablename__ = 'corpusform'
    id = Column(Integer, Sequence('corpusform_seq_id', optional=True), primary_key=True)
    corpus_id = Column(Integer, ForeignKey('corpus.id'))
    form_id = Column(Integer, ForeignKey('form.id'))
    datetime_modified = Column(DateTime(), default=now)


class CorpusTag(Base):
    __tablename__ = 'corpustag'
    id = Column(Integer, Sequence('corpustag_seq_id', optional=True), primary_key=True)
    corpus_id = Column(Integer, ForeignKey('corpus.id'))
    tag_id = Column(Integer, ForeignKey('tag.id'))
    datetime_modified = Column(DateTime(), default=now)


class Keeper(object):
    """Filters everything from a unicode string except the characters in ``keep``."""

    def __init__(self, keep):
        self.keep = set(map(ord, keep))

    def __getitem__(self, n):
        if n not in self.keep:
            return None
        else:
            return unichr(n)

    def __call__(self, s):
        return unicode(s).translate(self)


class Corpus(Base):
    __tablename__ = 'corpus'

    def __repr__(self):
        return '<Corpus (%s)>' % self.id

    id = Column(Integer, Sequence('corpus_seq_id', optional=True), primary_key=True)
    UUID = Column(Unicode(36))
    name = Column(Unicode(255))
    description = Column(UnicodeText)
    content = Column(UnicodeText(length=2147483648))
    enterer_id = Column(Integer, ForeignKey('user.id', ondelete='SET NULL'))
    enterer = relation('User', primaryjoin='Corpus.enterer_id==User.id')
    modifier_id = Column(Integer, ForeignKey('user.id', ondelete='SET NULL'))
    modifier = relation('User', primaryjoin='Corpus.modifier_id==User.id')
    form_search_id = Column(Integer, ForeignKey('formsearch.id', ondelete='SET NULL'))
    form_search = relation('FormSearch')
    datetime_entered = Column(DateTime)
    datetime_modified = Column(DateTime, default=now)
    tags = relation('Tag', secondary=CorpusTag.__table__)
    forms = relation('Form', secondary=CorpusForm.__table__, backref='corpora')
    files = relation('CorpusFile', backref='corpus', cascade='all, delete, delete-orphan')

    def get_dict(self):
        """Return a Python dictionary representation of the Corpus.  This
        facilitates JSON-stringification, cf. utils.JSONOLDEncoder.  Relational
        data are truncated, e.g., corpus_dict['elicitor'] is a dict with keys
        for 'id', 'first_name' and 'last_name' (cf. get_mini_user_dict above) and
        lacks keys for other attributes such as 'username',
        'personal_page_content', etc.
        """
        return {'id': self.id, 
           'UUID': self.UUID, 
           'name': self.name, 
           'description': self.description, 
           'content': self.content, 
           'enterer': self.get_mini_user_dict(self.enterer), 
           'modifier': self.get_mini_user_dict(self.modifier), 
           'form_search': self.get_mini_form_search_dict(self.form_search), 
           'datetime_entered': self.datetime_entered, 
           'datetime_modified': self.datetime_modified, 
           'tags': self.get_tags_list(self.tags), 
           'files': self.get_corpus_files_list(self.files)}

    def get_full_dict(self):
        result = self.get_dict()
        result['forms'] = self.get_forms_list(self.forms)
        return result

    makefilter = Keeper

    @classmethod
    def get_int(cls, input_):
        try:
            return int(input_)
        except Exception:
            return

        return

    @classmethod
    def get_form_references(cls, content):
        """Similar to ``get_ids_of_forms_referenced`` except that references are
        assumed to be comma-delimited strings of digits -- all other text is
        filtered out.
        """
        digits_comma_only = cls.makefilter('1234567890,')
        return filter(None, map(cls.get_int, digits_comma_only(content).split(',')))


class CorpusFile(Base):
    """Represents a corpus' forms written to disk in a certain format."""
    __tablename__ = 'corpusfile'

    def __repr__(self):
        return '<CorpusFile (%s)>' % self.id

    id = Column(Integer, Sequence('corpusfile_seq_id', optional=True), primary_key=True)
    corpus_id = Column(Integer, ForeignKey('corpus.id', ondelete='SET NULL'))
    filename = Column(Unicode(255))
    format = Column(Unicode(255))
    creator_id = Column(Integer, ForeignKey('user.id', ondelete='SET NULL'))
    creator = relation('User', primaryjoin='CorpusFile.creator_id==User.id')
    modifier_id = Column(Integer, ForeignKey('user.id', ondelete='SET NULL'))
    modifier = relation('User', primaryjoin='CorpusFile.modifier_id==User.id')
    datetime_modified = Column(DateTime, default=now)
    datetime_created = Column(DateTime)
    restricted = Column(Boolean)

    def get_dict(self):
        """Return a Python dictionary representation of the corpus file."""
        return {'id': self.id, 
           'corpus_id': self.corpus_id, 
           'filename': self.filename, 
           'format': self.format, 
           'creator': self.get_mini_user_dict(self.creator), 
           'modifier': self.get_mini_user_dict(self.modifier), 
           'datetime_modified': self.datetime_modified, 
           'datetime_entered': self.datetime_entered, 
           'restricted': self.restricted}