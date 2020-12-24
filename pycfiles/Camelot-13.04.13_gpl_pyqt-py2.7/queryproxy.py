# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/proxy/queryproxy.py
# Compiled at: 2013-04-11 17:47:52
"""Proxies representing the results of a query"""
import functools, logging
logger = logging.getLogger('camelot.view.proxy.queryproxy')
from collection_proxy import CollectionProxy, strip_data_from_object
from camelot.view.model_thread import model_function, object_thread, post

class QueryTableProxy(CollectionProxy):
    """The QueryTableProxy contains a limited copy of the data in the SQLAlchemy
    model, which is fetched from the database to be used as the model for a
    QTableView
    """

    def __init__(self, admin, query_getter, columns_getter, max_number_of_rows=10, cache_collection_proxy=None):
        """@param query_getter: a model_thread function that returns a query, can be None at construction time and set later"""
        logger.debug('initialize query table')
        self._query_getter = query_getter
        self._sort_decorator = None
        self._mapper = admin.mapper
        self._appended_rows = []
        super(QueryTableProxy, self).__init__(admin, lambda : [], columns_getter, max_number_of_rows=max_number_of_rows, cache_collection_proxy=cache_collection_proxy)
        return

    def get_query_getter(self):
        if self._query_getter == None:
            return
        else:
            if self._sort_decorator == None:
                self._set_sort_decorator()

            def sorted_query_getter(query_getter, sort_decorator):
                return sort_decorator(query_getter())

            return functools.partial(sorted_query_getter, self._query_getter, self._sort_decorator)

    def _update_unflushed_rows(self):
        """Does nothing since all rows returned by a query are flushed"""
        pass

    @model_function
    def _clean_appended_rows(self):
        """Remove those rows from appended rows that have been flushed"""
        flushed_rows = []
        for o in self._appended_rows:
            primary_key = self._mapper.primary_key_from_instance(o)
            if None not in primary_key:
                flushed_rows.append(o)

        for o in flushed_rows:
            self._appended_rows.remove(o)

        return

    @model_function
    def getRowCount(self):
        self._clean_appended_rows()
        if not self._query_getter:
            return 0
        query = self.get_query_getter()()
        return query.count() + len(self._appended_rows)

    def setQuery(self, query_getter):
        """Set the query and refresh the view"""
        assert object_thread(self)
        self._query_getter = query_getter
        self.refresh()

    def get_collection(self):
        """In case the collection is requested of a QueryProxy, we will return
        a collection getter for a collection that reuses the data already queried by
        the collection proxy, and available in the cache.
         
        We do this to :
        
        1. Prevent an unneeded query when the collection is used to fetch an object already
           fetched by the query proxy (eg when a form is opened on a table view)
           
        2. To make sure the index of an object in the query proxy is the same as the index
           in the returned collection.  Should we do the same query twice (once to fill the
           query proxy, and once to fill the returned collection), the same object might appear
           in a different row.  eg when a form is opened in a table view, the form contains 
           another record than the selected row in the table.
        """
        if not self._query_getter:
            return []
        return self.get_query_getter()().all()

    @model_function
    def _set_sort_decorator(self, column=None, order=None):
        """set the sort decorator attribute of this model to a function that
        sorts a query by the given column using the given order.  When no
        arguments are given, use the default sorting, which is according to
        the primary keys of the model.  This to impose a string ordening of
        the rows in the model.
        """
        from sqlalchemy import orm
        from sqlalchemy.exc import InvalidRequestError
        class_attributes_to_sort_by, join = [], None
        mapper = orm.class_mapper(self.admin.entity)
        if column != None and order != None:
            property = None
            field_name = self._columns[column][0]
            class_attribute = getattr(self.admin.entity, field_name)
            try:
                property = mapper.get_property(field_name)
            except InvalidRequestError:
                pass

            if property and isinstance(property, orm.properties.PropertyLoader):
                target = property.mapper
                if target:
                    if target.order_by:
                        join = field_name
                        class_attribute = target.order_by[0]
                    elif hasattr(property, '_foreign_keys'):
                        class_attribute = list(property._foreign_keys)[0]
                    else:
                        class_attribute = list(property._calculated_foreign_keys)[0]
            if property:
                if order:
                    class_attributes_to_sort_by.append(class_attribute.desc())
                else:
                    class_attributes_to_sort_by.append(class_attribute)
        if mapper.order_by:
            class_attributes_to_sort_by.extend(mapper.order_by)
        class_attributes_to_sort_by.extend(mapper.primary_key)

        def sort_decorator(class_attributes_to_sort_by, join, query):
            if join:
                query = query.outerjoin(join)
            if class_attributes_to_sort_by:
                return query.order_by(*class_attributes_to_sort_by)
            else:
                return query

        self._sort_decorator = functools.partial(sort_decorator, class_attributes_to_sort_by, join)
        return self._rows

    def sort(self, column, order):
        """Overwrites the :meth:`QAbstractItemModel.sort` method
        """
        assert object_thread(self)
        post(functools.update_wrapper(functools.partial(self._set_sort_decorator, column, order), self._set_sort_decorator), self._refresh_content)

    def append(self, o):
        """Add an object to this collection, used when inserting a new
        row, overwrite this method for specific behaviour in subclasses"""
        primary_key = self._mapper.primary_key_from_instance(o)
        if None in primary_key:
            self._appended_rows.append(o)
        return

    def remove(self, o):
        if o in self._appended_rows:
            self._appended_rows.remove(o)
        self._rows = self._rows - 1

    @model_function
    def getData(self):
        """Generator for all the data queried by this proxy"""
        if self._query_getter:
            for _i, o in enumerate(self.get_query_getter()().all()):
                yield strip_data_from_object(o, self._columns)

    @model_function
    def _get_collection_range(self, offset, limit):
        """Get the objects in a certain range of the collection
        :return: an iterator over the objects in the collection, starting at 
        offset, until limit
        """
        from sqlalchemy import orm
        from sqlalchemy.exc import InvalidRequestError
        query = self.get_query_getter()().offset(offset).limit(limit)
        columns_to_undefer = []
        for field_name, _field_attributes in self._columns:
            property = None
            try:
                property = self.admin.mapper.get_property(field_name)
            except InvalidRequestError:
                pass

            if property and isinstance(property, orm.properties.ColumnProperty):
                columns_to_undefer.append(field_name)

        if columns_to_undefer:
            options = [ orm.undefer(field_name) for field_name in columns_to_undefer ]
            query = query.options(*options)
        return query.all()

    @model_function
    def _extend_cache(self):
        """Extend the cache around the rows under request"""
        if self._query_getter:
            offset, limit = self._offset_and_limit_rows_to_get()
            if limit:
                columns = self._columns
                rows_in_cache = 0
                for row in range(offset, offset + limit):
                    try:
                        cached_obj = self.edit_cache.get_entity_at_row(row)
                        self._add_data(columns, row, cached_obj)
                        rows_in_cache += 1
                    except KeyError:
                        break

                query_offset = offset + rows_in_cache
                query_limit = limit - rows_in_cache
                if query_limit > 0:
                    for i, obj in enumerate(self._get_collection_range(query_offset, query_limit)):
                        row = i + query_offset
                        try:
                            previous_obj = self.edit_cache.get_entity_at_row(row)
                            if previous_obj != obj:
                                continue
                        except KeyError:
                            pass

                        if self._skip_row(row, obj) == False:
                            self._add_data(columns, row, obj)

                rows_in_query = self._rows - len(self._appended_rows)
                if offset + limit >= rows_in_query:
                    for row in range(max(rows_in_query, offset), min(offset + limit, self._rows)):
                        obj = self._get_object(row)
                        self._add_data(columns, row, obj)

            return (
             offset, limit)

    @model_function
    def _get_object(self, row):
        """Get the object corresponding to row.  If row is smaller than 0
        (in case of an invalid widget mapper), None is returned as an object"""
        if self._rows > 0 and self._rows > row >= 0:
            self._clean_appended_rows()
            rows_in_query = self._rows - len(self._appended_rows)
            if row >= rows_in_query:
                return self._appended_rows[(row - rows_in_query)]
            try:
                return self.edit_cache.get_entity_at_row(row)
            except KeyError:
                pass

            if self._query_getter:
                res = self.get_query_getter()().offset(row)
                if isinstance(res, list):
                    res = res[0]
                try:
                    return res.limit(1).first()
                except:
                    pass