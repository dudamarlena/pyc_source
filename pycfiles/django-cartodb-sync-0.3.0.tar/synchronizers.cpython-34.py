# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eric/Documents/code/django-cartodb-sync/cartodbsync/synchronizers.py
# Compiled at: 2015-09-09 11:26:06
# Size of source mod 2**32: 6050 bytes
from datetime import datetime
import traceback
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from cartodb import CartoDBAPIKey, CartoDBException
from .models import SyncEntry

class BaseSynchronizer(object):
    __doc__ = '\n    The base class for synchronizing a model with a CartoDB table.\n\n    The general outline for this process is:\n    * Get model instances to synchronize\n    * Synchronize using\n    * Mark as not needing to be synchronized anymore\n\n    INSERT and UPDATE statements inspired by:\n     http://blog.cartodb.com/post/53301057653/faster-data-updates-with-cartodb\n    '

    def __init__(self, model, cartodb_table, batch_size=500):
        self.model = model
        self.cartodb_table = cartodb_table
        self.batch_size = batch_size

    def synchronize(self):
        entries = self.get_entries_to_synchronize()
        try:
            self.synchronize_entries(entries)
            entries.mark_as_success()
        except Exception as e:
            traceback.print_exc()
            print('Exception while synchronizing:', e)
            entries.mark_as_failed()

    def get_entries_to_synchronize(self):
        entries = SyncEntry.objects.for_model(self.model).to_synchronize()
        entries = entries.order_by('-updated')
        if entries.count() > self.batch_size:
            entries = entries[:self.batch_size]
        return entries

    def synchronize_entries(self, entries):
        cl = CartoDBAPIKey(settings.CARTODB_SYNC['API_KEY'], settings.CARTODB_SYNC['DOMAIN'])
        inserts = [self.get_cartodb_mapping(e.content_object) for e in entries if e.status == SyncEntry.PENDING_INSERT]
        if inserts:
            insert_statement = self.get_insert_statement(inserts)
            try:
                print(cl.sql(insert_statement))
            except CartoDBException as e:
                traceback.print_exc()
                print('Exception while inserting:', e)

        updates = [self.get_cartodb_mapping(e.content_object) for e in entries if e.status == SyncEntry.PENDING_UPDATE]
        if updates:
            statement = self.get_update_statement(updates)
            print(statement)
            try:
                print(cl.sql(statement))
            except CartoDBException as e:
                traceback.print_exc()
                print('Exception while updating:', e)

        deletes = [e for e in entries if e.status == SyncEntry.PENDING_DELETE]
        if deletes:
            statement = self.get_delete_statement(deletes)
            try:
                print(cl.sql(statement))
            except CartoDBException as e:
                traceback.print_exc()
                print('Exception while deleting:', e)

    def format_value(self, value):
        if value is None:
            return 'NULL'
        if isinstance(value, (int, float, complex)):
            return str(value)
        if isinstance(value, datetime):
            return "to_timestamp('%s', 'YYYY-MM-DD HH24:MI:SS')" % (
             value.strftime('%Y-%m-%d %H:%M:%S%z'),)
        try:
            float(value)
            return str(value)
        except Exception:
            pass

        if isinstance(value, GEOSGeometry):
            return "'%s'" % value.ewkt
        return "'%s'" % str(value)

    def get_column_names(self):
        raise NotImplementedError('Implement get_column_names')

    def get_cartodb_mapping(self, instance):
        raise NotImplementedError('Implement get_cartodb_mapping')

    def get_delete_statement(self, delete_entries):
        """
        Consolidate the given instances into one large and efficient delete
        statement.

        DELETE FROM <table name> WHERE id in (<ids>)
        """
        sql = 'DELETE FROM %s WHERE id in (%s)' % (
         self.cartodb_table,
         ','.join([str(e.object_id) for e in delete_entries]))
        return sql

    def get_insert_statement(self, insert_instances):
        """
        Consolidate the given instances into one large and efficient insert
        statement.

        INSERT INTO <table name> (<column names>) VALUES <values>
        """
        column_names = self.get_column_names()
        values = []
        for instance in insert_instances:
            formatted_values = [self.format_value(instance[c]) for c in column_names]
            values.append(','.join(formatted_values))

        sql = 'INSERT INTO %s (%s) VALUES %s' % (
         self.cartodb_table,
         ','.join(column_names),
         ','.join(['(%s)' % v for v in values]))
        return sql

    def get_update_statement(self, instances):
        """
        Consolidate the given instances into one large and efficient update
        statement.

        UPDATE <table name> o
        SET <column 1>=n.<column 1>, <column 2>=n.<column 2>
        FROM (VALUES
            (<values in order for row 1>),
            (<values in order for row 2>),
            (<values in order for row 3>)
        ) n(id, <column 1>, <column 2>)
        WHERE o.id = n.id;
        """
        column_names = self.get_column_names()
        values = []
        for instance in instances:
            formatted_values = [self.format_value(instance[c]) for c in column_names]
            values.append(','.join(formatted_values))

        sql = 'UPDATE %s o SET %s FROM (VALUES %s) n(%s) WHERE o.id = n.id' % (
         self.cartodb_table,
         ','.join(['%s=n.%s' % (c, c) for c in column_names]),
         ','.join(['(%s)' % v for v in values]),
         ','.join(column_names))
        return sql