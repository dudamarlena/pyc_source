# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/index.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 3390 bytes
from __future__ import unicode_literals
from pymongo import ASCENDING, DESCENDING, GEO2D, GEOHAYSTACK, GEOSPHERE, HASHED, TEXT
from ...package.loader import traverse
from ...schema import Attribute
from ...schema.compat import unicode

class Index(Attribute):
    PREFIX_MAP = {'':ASCENDING, 
     '-':DESCENDING, 
     '+':ASCENDING, 
     '@':GEO2D, 
     '%':GEOHAYSTACK, 
     '*':GEOSPHERE, 
     '#':HASHED, 
     '$':TEXT}
    fields = Attribute(default=None)
    unique = Attribute(default=False)
    background = Attribute(default=True)
    sparse = Attribute(default=False)
    expire = Attribute(default=None)
    partial = Attribute(default=None)
    bucket = Attribute(default=None)
    min = Attribute(default=None)
    max = Attribute(default=None)

    def __init__(self, *args, **kw):
        if args:
            kw['fields'] = self.process_fields(args)
        (super(Index, self).__init__)(**kw)

    def __fixup__(self, document):
        """Process the fact that we've been bound to a document; transform field references to DB field names."""
        self.fields = [(unicode(traverse(document, i[0], i[0])), i[1]) for i in self.fields]

    def adapt(self, *args, **kw):
        if args:
            kw['fields'] = self.fields + self.process_fields(args)
        instance = self.__class__()
        instance.__data__ = self.__data__.copy()
        for k, v in kw.items():
            setattr(instance, k, v)

        return instance

    def process_fields(self, fields):
        """Process a list of simple string field definitions and assign their order based on prefix."""
        result = []
        strip = ''.join(self.PREFIX_MAP)
        for field in fields:
            direction = self.PREFIX_MAP['']
            if field[0] in self.PREFIX_MAP:
                direction = self.PREFIX_MAP[field[0]]
                field = field.lstrip(strip)
            result.append((field, direction))

        return result

    def create(self, collection, **kw):
        """Create this index in the specified collection; keyword arguments are passed to PyMongo.
                
                http://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.create_index
                """
        options = dict(name=(self.__name__),
          unique=(self.unique),
          background=(self.background),
          sparse=(self.sparse),
          expireAfterSeconds=(self.expire),
          partialFilterExpression=(self.partial),
          bucketSize=(self.bucket),
          min=(self.min),
          max=(self.max))
        options.update(kw)
        for key in list(options):
            if options[key] is None:
                del options[key]

        return (collection.create_index)((self.fields), **options)

    create_index = create

    def drop(self, collection):
        """Drop this index from the specified collection.
                
                https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.drop_index
                """
        collection.drop_index(self.__name__)

    drop_index = drop