# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/model/morphemelanguagemodelbackup.py
# Compiled at: 2016-09-19 13:27:02
"""Morpheme language model backup model"""
from sqlalchemy import Column, Sequence
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime, Boolean, Float
from onlinelinguisticdatabase.model.meta import Base, now
import simplejson as json, logging
log = logging.getLogger(__file__)

class MorphemeLanguageModelBackup(Base):
    __tablename__ = 'morphemelanguagemodelbackup'

    def __repr__(self):
        return '<MorphemeLanguageModelBackup (%s)>' % self.id

    id = Column(Integer, Sequence('morphemelanguagemodelbackup_seq_id', optional=True), primary_key=True)
    morphemelanguagemodel_id = Column(Integer)
    UUID = Column(Unicode(36))
    name = Column(Unicode(255))
    description = Column(UnicodeText)
    corpus = Column(UnicodeText)
    enterer = Column(UnicodeText)
    modifier = Column(UnicodeText)
    datetime_entered = Column(DateTime)
    datetime_modified = Column(DateTime, default=now)
    generate_succeeded = Column(Boolean, default=False)
    generate_message = Column(Unicode(255))
    generate_attempt = Column(Unicode(36))
    perplexity = Column(Float, default=0.0)
    perplexity_attempt = Column(Unicode(36))
    perplexity_computed = Column(Boolean, default=False)
    toolkit = Column(Unicode(10))
    order = Column(Integer)
    smoothing = Column(Unicode(30))
    vocabulary_morphology = Column(UnicodeText)
    restricted = Column(Boolean)
    categorial = Column(Boolean)

    def vivify(self, morpheme_language_model_dict):
        """The vivify method gives life to a morpheme language model backup by specifying its
        attributes using the to-be-backed-up morpheme language model (morpheme_language_model_dict)
        The relational attributes of the to-be-backed-up morpheme language model are converted into (truncated) JSON objects.

        """
        self.UUID = morpheme_language_model_dict['UUID']
        self.morphemelanguagemodel_id = morpheme_language_model_dict['id']
        self.name = morpheme_language_model_dict['name']
        self.description = morpheme_language_model_dict['description']
        self.corpus = unicode(json.dumps(morpheme_language_model_dict['corpus']))
        self.enterer = unicode(json.dumps(morpheme_language_model_dict['enterer']))
        self.modifier = unicode(json.dumps(morpheme_language_model_dict['modifier']))
        self.datetime_entered = morpheme_language_model_dict['datetime_entered']
        self.datetime_modified = morpheme_language_model_dict['datetime_modified']
        self.generate_succeeded = morpheme_language_model_dict['generate_succeeded']
        self.generate_message = morpheme_language_model_dict['generate_message']
        self.generate_attempt = morpheme_language_model_dict['generate_attempt']
        self.perplexity = morpheme_language_model_dict['perplexity']
        self.perplexity_attempt = morpheme_language_model_dict['perplexity_attempt']
        self.perplexity_computed = morpheme_language_model_dict['perplexity_computed']
        self.toolkit = morpheme_language_model_dict['toolkit']
        self.order = morpheme_language_model_dict['order']
        self.smoothing = morpheme_language_model_dict['smoothing']
        self.vocabulary_morphology = unicode(json.dumps(morpheme_language_model_dict['vocabulary_morphology']))
        self.restricted = morpheme_language_model_dict['restricted']
        self.categorial = morpheme_language_model_dict['categorial']

    def get_dict(self):
        return {'id': self.id, 
           'morphemelanguagemodel_id': self.morphemelanguagemodel_id, 
           'UUID': self.UUID, 
           'name': self.name, 
           'corpus': self.json_loads(self.corpus), 
           'description': self.description, 
           'enterer': self.json_loads(self.enterer), 
           'modifier': self.json_loads(self.modifier), 
           'datetime_entered': self.datetime_entered, 
           'datetime_modified': self.datetime_modified, 
           'generate_succeeded': self.generate_succeeded, 
           'generate_message': self.generate_message, 
           'perplexity': self.perplexity, 
           'perplexity_attempt': self.perplexity_attempt, 
           'perplexity_computed': self.perplexity_computed, 
           'generate_attempt': self.generate_attempt, 
           'toolkit': self.toolkit, 
           'order': self.order, 
           'smoothing': self.smoothing, 
           'vocabulary_morphology': self.json_loads(self.vocabulary_morphology), 
           'restricted': self.restricted, 
           'categorial': self.categorial}