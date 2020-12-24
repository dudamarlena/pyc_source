# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/trait/queryable.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 11524 bytes
from __future__ import unicode_literals
from collections import Mapping
from functools import reduce
from operator import and_
from pymongo.cursor import CursorType
from ... import F, Filter, P, S
from ...trait import Collection
from ....schema.compat import odict
from ....package.loader import traverse

class Queryable(Collection):
    __doc__ = 'EXPERIMENTAL: Extend active collection behaviours to include querying.'
    UNIVERSAL_OPTIONS = {
     'collation',
     'limit',
     'projection',
     'skip',
     'sort'}
    FIND_OPTIONS = UNIVERSAL_OPTIONS | {
     'allow_partial_results',
     'await',
     'batch_size',
     'cursor_type',
     'max_time_ms',
     'modifiers',
     'no_cursor_timeout',
     'oplog_replay',
     'tail',
     'wait',
     'await'}
    FIND_MAPPING = {'allowPartialResults':'allow_partial_results', 
     'batchSize':'batch_size', 
     'cursorType':'cursor_type', 
     'maxTimeMS':'max_time_ms', 
     'maxTimeMs':'max_time_ms', 
     'noCursorTimeout':'no_cursor_timeout', 
     'oplogReplay':'oplog_replay'}
    AGGREGATE_OPTIONS = UNIVERSAL_OPTIONS | {
     'allowDiskUse',
     'batchSize',
     'maxTimeMS',
     'useCursor'}
    AGGREGATE_MAPPING = {'allow_disk_use':'allowDiskUse', 
     'batch_size':'batchSize', 
     'maxTimeMs':'maxTimeMS', 
     'max_time_ms':'maxTimeMS', 
     'use_cursor':'useCursor'}

    @classmethod
    def _prepare_query(cls, mapping, valid, *args, **kw):
        """Process arguments to query methods. For internal use only.
                
                Positional arguments are treated as query components, combined using boolean AND reduction.
                
                Keyword arguments are processed depending on the passed in mapping and set of valid options, with non-
                option arguments treated as parametric query components, also ANDed with any positionally passed query
                components.
                
                Parametric querying with explicit `__eq` against these "reserved words" is possible to work around their
                reserved-ness.
                
                Querying options for find and aggregate may differ in use of under_score or camelCase formatting; this
                helper removes the distinction and allows either.
                """
        collection = cls.get_collection(kw.pop('source', None))
        query = Filter(document=cls, collection=collection)
        options = {}
        if args:
            query &= reduce(and_, args)
        for key in tuple(kw):
            name = mapping.get(key, key)
            if name in valid:
                options[name] = kw.pop(key)

        if 'projection' in options:
            if not isinstance(options['projection'], Mapping):
                options['projection'] = P(cls, *options['projection'])
        if 'sort' in options:
            options['sort'] = S(cls, *options['sort'])
        if kw:
            query &= F(cls, **kw)
        return (cls, collection, query, options)

    @classmethod
    def _prepare_find(cls, *args, **kw):
        """Execute a find and return the resulting queryset using combined plain and parametric query generation.
                
                Additionally, performs argument case normalization, refer to the `_prepare_query` method's docstring.
                """
        cls, collection, query, options = (cls._prepare_query)(
 cls.FIND_MAPPING,
 cls.FIND_OPTIONS, *args, **kw)
        if 'await' in options:
            raise TypeError('Await is hard-deprecated as reserved keyword in Python 3.7, use wait instead.')
        if 'cursor_type' in options:
            if {'tail', 'wait'} & set(options):
                raise TypeError('Can not combine cursor_type and tail/wait arguments.')
        if options.pop('tail', False):
            options['cursor_type'] = CursorType.TAILABLE_AWAIT if options.pop('wait', True) else CursorType.TAILABLE
        else:
            if 'wait' in options:
                raise TypeError('Wait option only applies to tailing cursors.')
        modifiers = options.get('modifiers', dict())
        if 'max_time_ms' in options:
            modifiers['$maxTimeMS'] = options.pop('max_time_ms')
        if modifiers:
            options['modifiers'] = modifiers
        return (cls, collection, query, options)

    @classmethod
    def _prepare_aggregate(cls, *args, **kw):
        """Generate and execute an aggregate query pipline using combined plain and parametric query generation.
                
                Additionally, performs argument case normalization, refer to the `_prepare_query` method's docstring.
                
                This provides a find-like interface for generating aggregate pipelines with a few shortcuts that make
                aggregates behave more like "find, optionally with more steps". Positional arguments that are not Filter
                instances are assumed to be aggregate pipeline stages.
                
                https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.aggregate
                """
        stages = []
        stage_args = []
        fragments = []
        for arg in args:
            (fragments if isinstance(arg, Filter) else stage_args).append(arg)

        cls, collection, query, options = (cls._prepare_query)(
 cls.AGGREGATE_MAPPING,
 cls.AGGREGATE_OPTIONS, *fragments, **kw)
        if query:
            stages.append({'$match': query})
        stages.extend(stage_args)
        if 'sort' in options:
            stages.append({'$sort': odict(options.pop('sort'))})
        if 'skip' in options:
            stages.append({'$skip': options.pop('skip')})
        if 'limit' in options:
            stages.append({'$limit': options.pop('limit')})
        if 'projection' in options:
            stages.append({'$project': options.pop('projection')})
        return (cls, collection, stages, options)

    @classmethod
    def find(cls, *args, **kw):
        """Query the collection this class is bound to.
                
                Additional arguments are processed according to `_prepare_find` prior to passing to PyMongo, where positional
                parameters are interpreted as query fragments, parametric keyword arguments combined, and other keyword
                arguments passed along with minor transformation.
                
                https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.find
                """
        Doc, collection, query, options = (cls._prepare_find)(*args, **kw)
        return (collection.find)(query, **options)

    @classmethod
    def find_one(cls, *args, **kw):
        """Get a single document from the collection this class is bound to.
                
                Additional arguments are processed according to `_prepare_find` prior to passing to PyMongo, where positional
                parameters are interpreted as query fragments, parametric keyword arguments combined, and other keyword
                arguments passed along with minor transformation.
                
                Automatically calls `to_mongo` with the retrieved data.
                
                https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.find_one
                """
        if len(args) == 1:
            if not isinstance(args[0], Filter):
                args = (
                 getattr(cls, cls.__pk__) == args[0],)
        Doc, collection, query, options = (cls._prepare_find)(*args, **kw)
        result = Doc.from_mongo((collection.find_one)(query, **options))
        return result

    @classmethod
    def find_in_sequence(cls, field, order, *args, **kw):
        """Return a QuerySet iterating the results of a query in a defined order. Technically an aggregate.
                
                To be successful one must be running MongoDB 3.4 or later. Document order will not be represented otherwise.
                
                Based on the technique described here: http://s.webcore.io/2O3i0N2E3h0r
                See also: https://jira.mongodb.org/browse/SERVER-7528
                """
        field = traverse(cls, field)
        order = list(order)
        kw['sort'] = {'__order': 1}
        kw.setdefault('projection', {'__order': 0})
        cls, collection, stages, options = (cls._prepare_aggregate)(
 field.any(order),
 {'$addFields': {'__order': {'$indexOfArray': [order, '$' + ~field]}}}, *args, **kw)
        if tuple(collection.database.client.server_info()['versionArray'][:2]) < (3,
                                                                                  4):
            raise RuntimeError('Queryable.find_in_sequence only works against MongoDB server versions 3.4 or newer.')
        return (collection.aggregate)(stages, **options)

    def reload(self, *fields, **kw):
        """Reload the entire document from the database, or refresh specific named top-level fields."""
        Doc, collection, query, options = (self._prepare_find)(id=self.id, projection=fields, **kw)
        result = (collection.find_one)(query, **options)
        if fields:
            for k in result:
                if k == ~Doc.id:
                    pass
                else:
                    self.__data__[k] = result[k]

        else:
            self.__data__ = result
        return self