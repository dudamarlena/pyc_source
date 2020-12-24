# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Larco/Documents/Github/pyvenom/framework/venom/model/hybrid.py
# Compiled at: 2016-04-15 14:09:30
from google.appengine.api import search
from google.appengine.ext import ndb
import logging
__all__ = [
 'HybridModel']

def dynamic_ndb_model(kind, properties=None):

    class DynamicNDBModel(ndb.Model):

        @classmethod
        def _get_kind(cls):
            return kind

        @classmethod
        def property(cls, key, prop):
            prop._name = key
            prop._code_name = key
            cls._properties[key] = prop
            setattr(cls, key, prop)

    if properties:
        for key, prop in properties.items():
            DynamicNDBModel.property(key, prop)

    return DynamicNDBModel


class HybridModel(object):
    """
  PURPOSE
    A programatic model combining the
    search api and ndb Model
  """
    _prefix = 'VenomHybridModel'

    def __init__(self, name):
        self.name = name
        self._properties = {}
        self._code_name = ('{}.{}').format(self._prefix, self.name)
        self._index = search.Index(name=self._code_name)
        self._model_cls = dynamic_ndb_model(self._code_name)
        self._model = self._model_cls()
        self._search_fields = []

    def property(self, key, prop, value):
        self._properties[key] = prop
        if isinstance(prop, ndb.Property):
            self._model.property(key, prop)
            prop._set_value(self._model, value)
        elif issubclass(prop, ndb.Property):
            self.property(key, prop(), value)
        elif issubclass(prop, search.Field):
            self._search_fields.append(prop(name=key, value=value))

    def _to_search_document(self):
        return search.Document(fields=self._search_fields)

    def _to_ndb_model(self):
        return self._model

    def query_by_search(self, query_string):
        entities = []
        documents = self._index.search(query_string)
        for document in documents:
            ndb_urlsafe_key = document['venom_model_key'][0].value
            ndb_key = ndb.Key(urlsafe=ndb_urlsafe_key)
            entities.append(ndb_key)

        entities = ndb.get_multi(entities)
        return entities

    def query_by_ndb(self, query):
        if not query:
            return self._model.query()
        return self._model.query(query)

    def put(self):
        self._model.put()
        if self._search_fields:
            self.property('venom_model_key', search.TextField, self._model.key.urlsafe())
            results = self._index.put(self._to_search_document())
            search_id = results[0].id

    def delete(self):
        pass

    def get_by_id(self, identifier):
        if not isinstance(identifier, int):
            logging.warn('Ignoring identifier because it is not an int')
            return None
        else:
            return self._model_cls.get_by_id(identifier)