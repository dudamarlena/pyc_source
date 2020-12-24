# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/firestore/containers/collection.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 11585 bytes
"""
    firestore.containers.document
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    John Cleese (Commentator): Ah no, they're not. No they didn't realize
    they were supposed to start. Never mind, we'll soon sort that out, the
    judge is explaining it to them now. I think Nigel and Gervaise have
    got the idea. All set to go.

    :copyright: 2019 Workhamper
    :license: MIT
"""
from firestore.db import Connection
from firestore.errors import InvalidDocumentError, UnknownFieldError, ValidationError, OfflineDocumentError
from google.cloud.firestore_v1 import DocumentReference
STOP_WORDS = ('the', 'is')
DOT = '.'
SLASH = '/'
UID = '{}/{}'
METADATA = ('__module__', '__doc__', '__collection__', '__private__', '__exclude__')

class Cache(dict):
    __doc__ = '\n    A class to make attribute lookup and writing\n    swift and fast without the need for attribute access\n    notation instead defaulting to object access notation\n    '

    def __init__(self, *args, **kwargs):
        self._pk = False
        (dict.__init__)(self, *args, **kwargs)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def add(self, key, value):
        self.__setattr__(key, value)


class Collection(object):
    __doc__ = 'Collections are recommended to be used when saving objects\n    to firestore. They ensure a schema exists under which data can be\n    stored i.e. reducing the error of typing name and naame across\n    two different documents.\n\n    They also help to group together commonly used actions across documents\n    i.e. setting and saving, querying, and updating document instances.\n    '
    __collection__ = None
    __schema__ = None

    @classmethod
    def __autospector__(cls, *args, **kwargs):
        return {k:v for k, v in cls.__dict__.items() if k not in METADATA if k not in METADATA}

    def __deref__(self, doc_ref):
        """
        Deref string based document references into classes
        upon instance assignment by looking up the doc_ref
        first in the globals of this module then walking
        up the directory tree until an instance is found
        or an error is thrown
        """
        self.get(doc_ref)

    def __eq__(self, comparator):
        try:
            comparator.__loaded__
        except:
            return False
            if not self.__loaded__:
                return False
            a = self.__loaded__.get().to_dict()
            b = comparator.__loaded__.get().to_dict()
            return a == b

    def __getattr__(self, key):
        return self._data[key]

    def __init__(self, *args, **kwargs):
        """
        Root document holding all the utility methods
        needed for persistence to cloud firestore
        """
        self._uniques = {}
        self._data = Cache()
        self._parent = self.__collection__
        self.__loaded__ = False
        self.__mutated__ = True
        self.fields_cache = self.__autospector__()
        for k in kwargs:
            if k in ('_pk', '_id'):
                self._data.add(k, kwargs.get(k))
                continue
            if k not in self.fields_cache.keys():
                raise UnknownFieldError(f"Key {k} not found in document {type(self).__name__}")
            self._data.add(k, self.fields_cache.get(k).cast(self, kwargs.get(k)))

    def add_field(self, field, value):
        """
        Add a field to this instance's data for persistence after
        taking into cognizance all the validations present on the field
        """
        self._data.add(field._name, value)

    @classmethod
    def bases(cls):
        _b = list(cls.__bases__)
        for _Collection__b in _b:
            _b.extend(_Collection__b.__bases__)

        return _b

    @property
    def collection(self):
        """
        Return the class variable
        """
        cls = type(self)
        if not cls.__collection__:
            return cls.__name__.lower()
        return type(self).__collection__.replace(DOT, SLASH)

    @collection.setter
    def collection(self, value):
        """
        Note this changes the class variable
        """
        type(self).__collection__ = value.replace(DOT, SLASH)

    @classmethod
    def count(cls, **kwargs):
        """
        Count the number of records that exist on firestore
        up until 5000 then return 5k+ if records
        exceed that number. The implmentation of this
        method might (will!) change
        """
        pass

    @property
    def dbpath(self):
        if self.__loaded__:
            return self.__loaded__.path
        if self._pk:
            return UID.format(self.collection, self._pk.value)
        raise OfflineDocumentError('')

    def delete(self):
        """
        Delete this account by using it's primary key
        or a unique identifier
        """
        conn = Connection.get_connection()
        conn.delete(self)

    @classmethod
    def get(cls, document_id):
        """
        Get a document by its unique identifier on firebase
        """
        conn = Connection.get_connection()
        return conn.get(cls, UID.format(cls().collection, document_id))

    def get_field(self, field):
        """
        Get a field form the internal _data store of field values
        """
        return self._data.get(field._name)

    @classmethod
    def get_json_data(cls, exclude=None, minimize=True):
        """
        Get json representation of this document.

        If there is data from the server then the last fetched
        data is used otherwise the untethered version of the data
        is used to create the json document. To ensure you get
        the latest data refresh the document.

        @exclude: (list)    A list of key names to additionally
        exclude from the returned json data. This is merged
        with __exclude__ if present

        @minimize: (bool)  A boolean (True/False) value depicting
        if references should be expanded into full blown JSON objects
        or left as uids.
        """
        pass

    @classmethod
    def get_json_schema(cls):
        """
        Get a json schema of this document with datatypes and required
        status
        """
        if cls.__schema__:
            return cls.__schema__

    @classmethod
    def find(cls, *args, **kwargs):
        """
        Find a document using the keyward value pairs and limit to
        20 results if no limit key is passed in
        """
        conn = Connection.get_connection()
        return (conn.find)(cls, *args, **kwargs)

    def load_json_data(self, json_data):
        pass

    def persist(self):
        """Save changes made to this document and any children of this
        document to cloud firestore
        """
        pass

    @property
    def pk(self):
        return self._data.get(self._data._pk)

    @pk.setter
    def pk(self, value):
        """
        Sets what field is the pk
        """
        if self._data._pk:
            raise InvalidDocumentError(f"Duplicate primary key `{value._name}` assigned on document with existing pk `{self._data._pk}`")
        elif isinstance(value, DocumentReference):
            self._data._pk = '_id'
            self._data.add('_id', value.id)
        else:
            self._data._pk = value._name
        self._pk = value

    def _presave(self):
        """
        Validates inputs and ensures all required fields and other
        constraints are present before the save operation is called
        """
        for k in self.fields_cache:
            f = self.fields_cache.get(k)
            v = self._data.get(k)
            if v or f.default:
                self._data.add(k, f.default)
                if callable(f.default):
                    self._data.add(k, f.default())
                elif f.required or f.pk:
                    raise ValidationError(f"{f._name} is a required field of {type(self).__name__}")

    def save(self):
        """
        Save changes made to document to cloud firestore.
        """
        if not self.__mutated__:
            return
        self._presave()
        conn = Connection.get_connection()
        res = conn.post(self)
        self.__mutated__ = False
        return res

    @classmethod
    def search(cls, query_string, compound_search=False):
        """
        Search for a document using text values. Note this
        is not supported locally by firebase and this library
        uses a read hack to implement text search.
        It is production ready but your mileage might vary.

        @param: query_string {str}
        --------------------------
        This is the text data, search text, or query to use
        as input for the actual search to be done on firestore

        @param: compound_search {bool}
        ------------------------------
        If compound search is enabled then the search terms
        i.e. text used for lookup will be flagged as compound
        before a search is submitted.
        This means all matching documents must have all the words
        in the search text before it returns.
        e.g. red car - only documents with both red and car will be
        returned, documents with only red or only car will
        be ignored

        @return: results {firestore.db.result.Results}
        ----------------------------------------------
        A collection of traversable result documents limited by
        the paginate field which maxes out at 100
        """
        pass

    def to_firestore_dict(self):
        """
        Convert this object into a firestore update compatible
        dict i.e. nested maps have root elements with the key
        document.nested
        """
        pass

    def transaction(self):
        """
        Perform a transaction i.e. persist all changes or roll back
        entire transaction
        """
        pass

    @property
    def uniques(self):
        """
        Unique fields only hold true if the value is not empty
        i.e. null.
        To prevent null mark the field as required, only fields
        that have a value will be used for the unique evaluation
        """
        return self._uniques

    @uniques.setter
    def uniques(self, values):
        k, v = values
        self._uniques[k] = v