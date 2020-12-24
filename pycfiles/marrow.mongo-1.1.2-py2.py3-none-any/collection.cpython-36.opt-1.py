# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/trait/collection.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 9283 bytes
from __future__ import unicode_literals
from bson.binary import STANDARD
from bson.codec_options import CodecOptions
from bson.tz_util import utc
from pymongo.collection import Collection as PyMongoCollection
from pymongo.database import Database
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference
from pymongo.write_concern import WriteConcern
from ... import U, Update
from ...trait import Identified
__all__ = [
 'Collection']

class Collection(Identified):
    __doc__ = 'Allow this Document class to be bound to a real MongoDB database and collection.\n\t\n\tThis extracts all "active-record"-like patterns from basic Document classes, eliminates the need to declare as a\n\tsub-class of Identified (all top-level Collection objects are identified by default), and generally helps break\n\tthings apart into discrete groups of logical tasks.\n\t\n\tCurrently true Active Record pattern access is not supported, nor encouraged. This provides a shortcut, as\n\tmentioned above, and access to common collection-level activites in ways utilizing positional and parametric\n\thelpers. Not all collection manipulating methods are proxied here; only the ones benefitting from assistance\n\tfrom Marrow Mongo in terms of binding or index awareness.\n\t\n\tFor other operations (such as `drop`, `reindex`, etc.) it is recommended to `get_collection()` and explicitly\n\tutilize the PyMongo API. This helps reduce the liklihood of a given interface breaking with changes to PyMongo,\n\tavoids clutter, and allows you to use some of these method names yourself.\n\t'
    __bound__ = None
    __collection__ = None
    __projection__ = None
    __read_preference__ = ReadPreference.PRIMARY
    __read_concern__ = ReadConcern()
    __write_concern__ = WriteConcern(w=1)
    __capped__ = False
    __capped_count__ = None
    __engine__ = None
    __collation__ = None
    __validate__ = 'off'
    __validator__ = None

    @classmethod
    def __attributed__(cls):
        """Executed after each new subclass is constructed."""
        cls.__projection__ = cls._get_default_projection()

    @classmethod
    def bind(cls, target):
        """Bind a copy of the collection to the class, modified per our class' settings.
                
                The given target (and eventual collection returned) must be safe within the context the document sublcass
                being bound is constructed within. E.g. at the module scope this binding must be thread-safe.
                """
        if cls.__bound__ is not None:
            return cls
        else:
            cls.__bound__ = cls.get_collection(target)
            return cls

    @classmethod
    def get_collection(cls, target=None):
        """Retrieve a properly configured collection object as configured by this document class.
                
                If given an existing collection, will instead call `collection.with_options`.
                
                http://api.mongodb.com/python/current/api/pymongo/database.html#pymongo.database.Database.get_collection
                """
        if target is None:
            if cls.__bound__ is None:
                raise TypeError('Target required when document class not bound.')
            return cls.__bound__
        else:
            if isinstance(target, PyMongoCollection):
                return (target.with_options)(**cls._collection_configuration())
            if isinstance(target, Database):
                return (target.get_collection)((cls.__collection__), **cls._collection_configuration())
        raise TypeError('Can not retrieve collection from: ' + repr(target))

    @classmethod
    def create_collection(cls, target=None, drop=False, indexes=True):
        """Ensure the collection identified by this document class exists, creating it if not, also creating indexes.
                
                **Warning:** enabling the `recreate` option **will drop the collection, erasing all data within**.
                
                http://api.mongodb.com/python/current/api/pymongo/database.html#pymongo.database.Database.create_collection
                """
        if target is None:
            if cls.__bound__ is None:
                raise TypeError('Target required when document class not bound.')
            target = cls.__bound__
        else:
            if isinstance(target, PyMongoCollection):
                collection = target.name
                target = target.database
            else:
                if isinstance(target, Database):
                    collection = cls.__collection__
                else:
                    raise TypeError('Can not retrieve database from: ' + repr(target))
            if drop:
                target.drop_collection(collection)
            collection = (target.create_collection)(collection, **cls._collection_configuration(True))
            if indexes:
                cls.create_indexes(collection)
        return collection

    @classmethod
    def create_indexes(cls, target=None, recreate=False):
        """Iterate all known indexes and construct them.
                
                https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.create_indexes
                """
        results = []
        collection = cls.get_collection(target)
        if recreate:
            collection.drop_indexes()
        for index in cls.__indexes__.values():
            results.append(index.create(collection))

        return results

    @classmethod
    def _collection_configuration(cls, creation=False):
        config = {'codec_options':CodecOptions(document_class=cls.__store__,
           tz_aware=True,
           uuid_representation=STANDARD,
           tzinfo=utc), 
         'read_preference':cls.__read_preference__, 
         'read_concern':cls.__read_concern__, 
         'write_concern':cls.__write_concern__}
        if not creation:
            return config
        else:
            if cls.__capped__:
                config['size'] = cls.__capped__
                config['capped'] = True
                if cls.__capped_count__:
                    config['max'] = cls.__capped_count__
                if cls.__engine__:
                    config['storageEngine'] = cls.__engine__
            else:
                if cls.__validate__ != 'off':
                    config['validator'] = cls.__validator__
                    config['validationLevel'] = 'strict' if cls.__validate__ is True else cls.__validate__
                if cls.__collation__ is not None:
                    config['collation'] = cls.__collation__
            return config

    @classmethod
    def _get_default_projection(cls):
        """Construct the default projection document."""
        projected = []
        neutral = []
        omitted = False
        for name, field in cls.__fields__.items():
            if field.project is None:
                neutral.append(name)
            else:
                if field.project:
                    projected.append(name)
                else:
                    omitted = True

        if not projected:
            if not omitted:
                return
        if not projected:
            if omitted:
                projected = neutral
        return {field:True for field in projected}

    def insert_one(self, validate=True):
        """Insert this document.
                
                The `validate` argument translates to the inverse of the `bypass_document_validation` PyMongo option.
                
                https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.insert_one
                """
        kw = {}
        kw['bypass_document_validation'] = not validate
        collection = self.get_collection(kw.pop('source', None))
        return (collection.insert_one)(self, **kw)

    def update_one(self, update=None, validate=True, **kw):
        """Update this document in the database. Local representations will not be affected.
                
                A single positional parameter, `update`, may be provided as a mapping. Keyword arguments (other than those
                identified in UPDATE_MAPPING) are interpreted as parametric updates, added to any `update` passed in.
                
                https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.update_one
                """
        D = self.__class__
        collection = self.get_collection(kw.pop('source', None))
        update = Update(update or {})
        if kw:
            update &= U(D, **kw)
        if not update:
            raise TypeError('Must provide an update operation.')
        return collection.update_one((D.id == self), update, bypass_document_validation=(not validate))

    def delete_one(self, source=None, **kw):
        """Remove this document from the database, passing additional arguments through to PyMongo.
                
                https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.delete_one
                """
        collection = self.get_collection(source)
        return (collection.delete_one)((self.__class__.id == self), **kw)