# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/cassandra_to_gcs.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 13742 bytes
from __future__ import unicode_literals
import json
from builtins import str
from base64 import b64encode
from cassandra.util import Date, Time, SortedSet, OrderedMapSerializedKey
from datetime import datetime
from decimal import Decimal
from six import text_type, binary_type, PY3
from tempfile import NamedTemporaryFile
from uuid import UUID
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.contrib.hooks.cassandra_hook import CassandraHook
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CassandraToGoogleCloudStorageOperator(BaseOperator):
    """CassandraToGoogleCloudStorageOperator"""
    template_fields = ('cql', 'bucket', 'filename', 'schema_filename')
    template_ext = ('.cql', )
    ui_color = '#a0e08c'

    @apply_defaults
    def __init__(self, cql, bucket, filename, schema_filename=None, approx_max_file_size_bytes=1900000000, cassandra_conn_id='cassandra_default', google_cloud_storage_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        (super(CassandraToGoogleCloudStorageOperator, self).__init__)(*args, **kwargs)
        self.cql = cql
        self.bucket = bucket
        self.filename = filename
        self.schema_filename = schema_filename
        self.approx_max_file_size_bytes = approx_max_file_size_bytes
        self.cassandra_conn_id = cassandra_conn_id
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.delegate_to = delegate_to
        self.hook = None

    CQL_TYPE_MAP = {'BytesType':'BYTES', 
     'DecimalType':'FLOAT', 
     'UUIDType':'BYTES', 
     'BooleanType':'BOOL', 
     'ByteType':'INTEGER', 
     'AsciiType':'STRING', 
     'FloatType':'FLOAT', 
     'DoubleType':'FLOAT', 
     'LongType':'INTEGER', 
     'Int32Type':'INTEGER', 
     'IntegerType':'INTEGER', 
     'InetAddressType':'STRING', 
     'CounterColumnType':'INTEGER', 
     'DateType':'TIMESTAMP', 
     'SimpleDateType':'DATE', 
     'TimestampType':'TIMESTAMP', 
     'TimeUUIDType':'BYTES', 
     'ShortType':'INTEGER', 
     'TimeType':'TIME', 
     'DurationType':'INTEGER', 
     'UTF8Type':'STRING', 
     'VarcharType':'STRING'}

    def execute(self, context):
        cursor = self._query_cassandra()
        files_to_upload = self._write_local_data_files(cursor)
        if self.schema_filename:
            files_to_upload.update(self._write_local_schema_file(cursor))
        for file_handle in files_to_upload.values():
            file_handle.flush()

        self._upload_to_gcs(files_to_upload)
        for file_handle in files_to_upload.values():
            file_handle.close()

        self.hook.shutdown_cluster()

    def _query_cassandra(self):
        """
        Queries cassandra and returns a cursor to the results.
        """
        self.hook = CassandraHook(cassandra_conn_id=(self.cassandra_conn_id))
        session = self.hook.get_conn()
        cursor = session.execute(self.cql)
        return cursor

    def _write_local_data_files(self, cursor):
        """
        Takes a cursor, and writes results to a local file.

        :return: A dictionary where keys are filenames to be used as object
            names in GCS, and values are file handles to local files that
            contain the data for the GCS objects.
        """
        file_no = 0
        tmp_file_handle = NamedTemporaryFile(delete=True)
        tmp_file_handles = {self.filename.format(file_no): tmp_file_handle}
        for row in cursor:
            row_dict = self.generate_data_dict(row._fields, row)
            s = json.dumps(row_dict)
            if PY3:
                s = s.encode('utf-8')
            tmp_file_handle.write(s)
            tmp_file_handle.write('\n')
            if tmp_file_handle.tell() >= self.approx_max_file_size_bytes:
                file_no += 1
                tmp_file_handle = NamedTemporaryFile(delete=True)
                tmp_file_handles[self.filename.format(file_no)] = tmp_file_handle

        return tmp_file_handles

    def _write_local_schema_file(self, cursor):
        """
        Takes a cursor, and writes the BigQuery schema for the results to a
        local file system.

        :return: A dictionary where key is a filename to be used as an object
            name in GCS, and values are file handles to local files that
            contains the BigQuery schema fields in .json format.
        """
        schema = []
        tmp_schema_file_handle = NamedTemporaryFile(delete=True)
        for name, type in zip(cursor.column_names, cursor.column_types):
            schema.append(self.generate_schema_dict(name, type))

        json_serialized_schema = json.dumps(schema)
        if PY3:
            json_serialized_schema = json_serialized_schema.encode('utf-8')
        tmp_schema_file_handle.write(json_serialized_schema)
        return {self.schema_filename: tmp_schema_file_handle}

    def _upload_to_gcs(self, files_to_upload):
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id),
          delegate_to=(self.delegate_to))
        for object, tmp_file_handle in files_to_upload.items():
            hook.upload(self.bucket, object, tmp_file_handle.name, 'application/json')

    @classmethod
    def generate_data_dict(cls, names, values):
        row_dict = {}
        for name, value in zip(names, values):
            row_dict.update({name: cls.convert_value(name, value)})

        return row_dict

    @classmethod
    def convert_value(cls, name, value):
        if not value:
            return value
        else:
            if isinstance(value, (text_type, int, float, bool, dict)):
                return value
            else:
                if isinstance(value, binary_type):
                    return b64encode(value).decode('ascii')
                else:
                    if isinstance(value, UUID):
                        return b64encode(value.bytes).decode('ascii')
                    else:
                        if isinstance(value, (datetime, Date)):
                            return str(value)
                        else:
                            if isinstance(value, Decimal):
                                return float(value)
                            if isinstance(value, Time):
                                return str(value).split('.')[0]
                        if isinstance(value, (list, SortedSet)):
                            return cls.convert_array_types(name, value)
                    if hasattr(value, '_fields'):
                        return cls.convert_user_type(name, value)
                if isinstance(value, tuple):
                    return cls.convert_tuple_type(name, value)
            if isinstance(value, OrderedMapSerializedKey):
                return cls.convert_map_type(name, value)
        raise AirflowException('unexpected value: ' + str(value))

    @classmethod
    def convert_array_types(cls, name, value):
        return [cls.convert_value(name, nested_value) for nested_value in value]

    @classmethod
    def convert_user_type(cls, name, value):
        """
        Converts a user type to RECORD that contains n fields, where n is the
        number of attributes. Each element in the user type class will be converted to its
        corresponding data type in BQ.
        """
        names = value._fields
        values = [cls.convert_value(name, getattr(value, name)) for name in names]
        return cls.generate_data_dict(names, values)

    @classmethod
    def convert_tuple_type(cls, name, value):
        """
        Converts a tuple to RECORD that contains n fields, each will be converted
        to its corresponding data type in bq and will be named 'field_<index>', where
        index is determined by the order of the tuple elements defined in cassandra.
        """
        names = ['field_' + str(i) for i in range(len(value))]
        values = [cls.convert_value(name, value) for name, value in zip(names, value)]
        return cls.generate_data_dict(names, values)

    @classmethod
    def convert_map_type(cls, name, value):
        """
        Converts a map to a repeated RECORD that contains two fields: 'key' and 'value',
        each will be converted to its corresponding data type in BQ.
        """
        converted_map = []
        for k, v in zip(value.keys(), value.values()):
            converted_map.append({'key':cls.convert_value('key', k), 
             'value':cls.convert_value('value', v)})

        return converted_map

    @classmethod
    def generate_schema_dict(cls, name, type):
        field_schema = dict()
        field_schema.update({'name': name})
        field_schema.update({'type': cls.get_bq_type(type)})
        field_schema.update({'mode': cls.get_bq_mode(type)})
        fields = cls.get_bq_fields(name, type)
        if fields:
            field_schema.update({'fields': fields})
        return field_schema

    @classmethod
    def get_bq_fields(cls, name, type):
        fields = []
        if not cls.is_simple_type(type):
            names, types = [], []
            if cls.is_array_type(type):
                if cls.is_record_type(type.subtypes[0]):
                    names = type.subtypes[0].fieldnames
                    types = type.subtypes[0].subtypes
            if cls.is_record_type(type):
                names = type.fieldnames
                types = type.subtypes
            if types:
                if not names:
                    if type.cassname == 'TupleType':
                        names = ['field_' + str(i) for i in range(len(types))]
            if types:
                if not names:
                    if type.cassname == 'MapType':
                        names = [
                         'key', 'value']
            for name, type in zip(names, types):
                field = cls.generate_schema_dict(name, type)
                fields.append(field)

        return fields

    @classmethod
    def is_simple_type(cls, type):
        return type.cassname in CassandraToGoogleCloudStorageOperator.CQL_TYPE_MAP

    @classmethod
    def is_array_type(cls, type):
        return type.cassname in ('ListType', 'SetType')

    @classmethod
    def is_record_type(cls, type):
        return type.cassname in ('UserType', 'TupleType', 'MapType')

    @classmethod
    def get_bq_type(cls, type):
        if cls.is_simple_type(type):
            return CassandraToGoogleCloudStorageOperator.CQL_TYPE_MAP[type.cassname]
        else:
            if cls.is_record_type(type):
                return 'RECORD'
            if cls.is_array_type(type):
                return cls.get_bq_type(type.subtypes[0])
        raise AirflowException('Not a supported type: ' + type.cassname)

    @classmethod
    def get_bq_mode(cls, type):
        if cls.is_array_type(type) or type.cassname == 'MapType':
            return 'REPEATED'
        if cls.is_record_type(type) or cls.is_simple_type(type):
            return 'NULLABLE'
        raise AirflowException('Not a supported type: ' + type.cassname)