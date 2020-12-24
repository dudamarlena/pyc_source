# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/firestore/db/connection.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 5571 bytes
import os
from collections import deque
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firestore.errors import InvalidDocumentError, DuplicateError, NotFoundError
from google.cloud.firestore_v1.document import DocumentReference
_dbs = {}
_connections = {}
DEFAULT = 'default'
SLASH = '/'
EQUALS = '=='

class ResultSet(object):

    def __init__(self, *args, **kwargs):
        self.__data__ = deque(*args)

    def append(self, result):
        if not isinstance(result, DocumentReference):
            raise InvalidDocumentError('Only documents can be added to a results set')
        self.__data__.append(result)

    def first(self):
        if self.__data__:
            return self.__data__.popleft()

    def next(self):
        return self.first()

    def __bool__(self):
        return bool(self.__data__)

    def __len__(self):
        return len(self.__data__)


class Connection(object):
    __doc__ = '\n    A connection is the link between your project and\n    Google Cloud Firestore\n\n    :param connection_string {str}:\n    '

    def __init__(self, certificate, collection=False):
        _conn = _connections.get(DEFAULT)
        if _conn:
            self._db = _conn._db
        else:
            if not certificate:
                raise ConnectionError('Firestore configuration object or json file required')
            self.certificate = credentials.Certificate(certificate)
            firebase_admin.initialize_app(self.certificate)
            self._db = firestore.client()
            _connections[DEFAULT] = self
        self.collection = collection

    def delete(self, doc):
        """
        Remove the doc or the doc with the provided id from
        firestore cloud db if it exists
        """
        ref = doc.__loaded__
        if ref:
            if isinstance(ref, DocumentReference):
                return doc.__loaded__.delete()
        raise NotFoundError('Document does not exist')

    def find(self, *args, **kwargs):
        """Perform a query on cloud firestore using key names
        and values present in the default args dict"""
        limit = kwargs.get('limit', 10)
        coll_cls = args[0]
        args = list(args[1:])[::-1]
        if limit > 100:
            limit = 100
        query = self._db.collection(coll_cls().collection)
        while len(args) > 0:
            field, operand, value = args.pop()
            query = query.where(field, operand, value)

        query = query.limit(limit)
        rs = ResultSet([coll_cls(doc.to_dict()) for doc in query.stream()])
        return rs

    def get(self, cls, uid):
        """
        Get an instance of the document from firestore if it
        exists and return a result set of the wrapped
        document or an empty result set otherwise
        """
        docref = self._db.document(uid)
        _doc = docref.get()
        if _doc.exists:
            dwargs = _doc.to_dict()
            doc = cls(**dwargs)
            doc.__loaded__ = docref
            return ResultSet([doc])
        return ResultSet()

    @staticmethod
    def get_connection():
        __connection__ = _connections.get(DEFAULT)
        if not __connection__:
            raise ConnectionError('No connection object found, are you sure youhave created a connection with `conn = Connection(firestore_cert)`')
        return __connection__

    def patch(self, doc):
        pass

    def post(self, doc):
        collection_string = doc.collection
        if not len(collection_string.split(SLASH)) % 2:
            raise InvalidDocumentError('Invalid collection name, looks like collection ends in a document')
        else:
            colref = self._db.collection(collection_string)
            for k in doc.uniques:
                v = doc.uniques.get(k)
                if v and [res for res in colref.where(k, EQUALS, v).limit(1).get()]:
                    raise DuplicateError(f"Document found in firestore for unique field `{k}` with value `{v}`")

            if doc.__loaded__:
                doc.__loaded__.update(doc._data)
            else:
                if doc.pk:
                    if colref.document(doc.pk).get().exists:
                        raise DuplicateError(f"Document with primary key {doc.pk}=`{doc._pk.value}` already exists")
                    identifier = colref.document(doc.pk)
                    identifier.set(doc._data)
                    doc.__loaded__ = identifier
                else:
                    identifier = colref.document()
                    doc.pk = identifier
                    identifier.set(doc._data)
                    doc.__loaded__ = identifier
        return doc