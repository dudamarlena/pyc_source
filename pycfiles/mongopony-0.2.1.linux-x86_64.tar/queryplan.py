# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/envs/conversocial/lib/python2.7/site-packages/mongopony/queryplan.py
# Compiled at: 2015-11-17 06:33:46


class QueryPlan(object):

    def __init__(self, db, collection_cls):
        self.db = db
        self.collection_cls = collection_cls
        self.collection_name = collection_cls.collection_name
        self.filters = {}
        self.ordering = None
        self.only_fields = None
        self._read_preference = None
        return

    def _apply_aliasing(self, filters):
        if not hasattr(self.collection_cls, 'document_strategy'):
            return filters
        new_filters = {}
        for clause, expr in filters.iteritems():
            clause = self.collection_cls.document_strategy.get_alias(clause)
            new_filters[clause] = expr

        return new_filters

    def _cursor(self):
        coll = getattr(self.db, self.collection_name)
        filters = self._apply_aliasing(self.filters)
        if self._read_preference:
            coll = coll.with_options(read_preference=self._read_preference)
        cursor = coll.find(filters, projection=self.only_fields)
        if self.ordering:
            cursor = cursor.sort(self.ordering)
        return cursor

    def filter(self, filters):
        self.filters = filters

    def only(self, fields):
        self.only_fields = fields

    def as_list(self):
        return [ self._dict_to_object(doc) for doc in self._cursor() ]

    def as_generator(self):
        for doc in self._cursor():
            yield self._dict_to_object(doc)

    def _dict_to_object(self, doc):
        return self.collection_cls.dict_to_object(doc, self.only_fields)

    def count(self):
        return self._cursor().count()

    def order_by(self, *ordering):
        self.ordering = list(ordering)

    def read_preference(self, read_preference):
        self._read_preference = read_preference