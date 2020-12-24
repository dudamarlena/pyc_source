# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/model.py
# Compiled at: 2016-12-03 23:01:42
# Size of source mod 2**32: 2296 bytes
"""Note: experimental thingamabob."""
from __future__ import unicode_literals
__all__ = [
 'Model']

class Model(object):
    __doc__ = 'Lazy access to MongoDB database collections via the WebCore request context.\n\t\n\tAssign instances of this lazy loader to your endpoint classes and make sure your endpoint class stores the request\n\tcontext as `self._ctx` as per convention.  For example:\n\t\t\n\t\tclass Hello:\n\t\t\t_people = Model(\'people\', cache=\'_people\')\n\t\t\t\n\t\t\tdef __init__(self, context):\n\t\t\t\tself._ctx = context\n\t\t\t\n\t\t\tdef __call__(self, id):\n\t\t\t\treturn "Hello " + self._people.find_one({\'_id\': ObjectId(id)})[\'name\'] + "!"\n\t\n\tBecause the WebCore dispatch process constructs new instances on each request, we can safely cache the result and\n\toverwrite the descriptor on the instance. (This is only possible because we do not provide a `__set__` descriptor\n\tmethod!)\n\t'
    __slots__ = ('database', 'collection', 'model', 'cache')

    def __init__(self, collection, model=None, database='default', cache=None):
        """Construct a new lazy loader for MongoDB collections.
                
                Pass in the string name of the collection as the first positional argument, optionally pass in a marrow.mongo
                document class to remember for later, and the name of the database connection to access may be passed as a
                keyword arguemnt appropriately called `database`.
                
                If you want to utilize the cache (to save on repeated calls) you'll need to pass in the name of the attribute
                you wish to assign to on the instance as `cache`.
                """
        self.database = database
        self.collection = collection
        self.model = model
        self.cache = cache

    def resolve(self, context):
        """Given a WebCore request context, load our named collection out of the appropriate database connection."""
        return context.db[self.database][self.collection]

    def __get__(self, instance, cls=None):
        """Descriptor protocol getter."""
        if instance is None:
            return self
        else:
            collection = self.resolve(instance._ctx)
            if self.cache:
                setattr(instance, self.cache, collection)
            return collection