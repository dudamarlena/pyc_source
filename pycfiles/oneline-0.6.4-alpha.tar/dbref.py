# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: bson/dbref.py
# Compiled at: 2014-07-29 17:29:28
"""Tools for manipulating DBRefs (references to MongoDB documents)."""
from copy import deepcopy
from bson.son import SON

class DBRef(object):
    """A reference to a document stored in MongoDB.
    """
    _type_marker = 100

    def __init__(self, collection, id, database=None, _extra={}, **kwargs):
        """Initialize a new :class:`DBRef`.

        Raises :class:`TypeError` if `collection` or `database` is not
        an instance of :class:`basestring` (:class:`str` in python 3).
        `database` is optional and allows references to documents to work
        across databases. Any additional keyword arguments will create
        additional fields in the resultant embedded document.

        :Parameters:
          - `collection`: name of the collection the document is stored in
          - `id`: the value of the document's ``"_id"`` field
          - `database` (optional): name of the database to reference
          - `**kwargs` (optional): additional keyword arguments will
            create additional, custom fields

        .. versionchanged:: 1.8
           Now takes keyword arguments to specify additional fields.
        .. versionadded:: 1.1.1
           The `database` parameter.

        .. mongodoc:: dbrefs
        """
        if not isinstance(collection, basestring):
            raise TypeError('collection must be an instance of %s' % (
             basestring.__name__,))
        if database is not None and not isinstance(database, basestring):
            raise TypeError('database must be an instance of %s' % (
             basestring.__name__,))
        self.__collection = collection
        self.__id = id
        self.__database = database
        kwargs.update(_extra)
        self.__kwargs = kwargs
        return

    @property
    def collection(self):
        """Get the name of this DBRef's collection as unicode.
        """
        return self.__collection

    @property
    def id(self):
        """Get this DBRef's _id.
        """
        return self.__id

    @property
    def database(self):
        """Get the name of this DBRef's database.

        Returns None if this DBRef doesn't specify a database.

        .. versionadded:: 1.1.1
        """
        return self.__database

    def __getattr__(self, key):
        try:
            return self.__kwargs[key]
        except KeyError:
            raise AttributeError(key)

    def __setstate__(self, state):
        self.__dict__.update(state)

    def as_doc(self):
        """Get the SON document representation of this DBRef.

        Generally not needed by application developers
        """
        doc = SON([('$ref', self.collection),
         (
          '$id', self.id)])
        if self.database is not None:
            doc['$db'] = self.database
        doc.update(self.__kwargs)
        return doc

    def __repr__(self):
        extra = ('').join([ ', %s=%r' % (k, v) for k, v in self.__kwargs.iteritems()
                          ])
        if self.database is None:
            return 'DBRef(%r, %r%s)' % (self.collection, self.id, extra)
        else:
            return 'DBRef(%r, %r, %r%s)' % (self.collection, self.id,
             self.database, extra)

    def __eq__(self, other):
        if isinstance(other, DBRef):
            us = (
             self.__database, self.__collection,
             self.__id, self.__kwargs)
            them = (other.__database, other.__collection,
             other.__id, other.__kwargs)
            return us == them
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        """Get a hash value for this :class:`DBRef`.

        .. versionadded:: 1.1
        """
        return hash((self.__collection, self.__id, self.__database,
         tuple(sorted(self.__kwargs.items()))))

    def __deepcopy__(self, memo):
        """Support function for `copy.deepcopy()`.

        .. versionadded:: 1.10
        """
        return DBRef(deepcopy(self.__collection, memo), deepcopy(self.__id, memo), deepcopy(self.__database, memo), deepcopy(self.__kwargs, memo))