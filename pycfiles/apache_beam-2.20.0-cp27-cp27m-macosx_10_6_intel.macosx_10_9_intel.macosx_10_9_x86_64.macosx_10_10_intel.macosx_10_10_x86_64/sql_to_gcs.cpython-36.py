# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/sql_to_gcs.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 11144 bytes
__doc__ = '\nBase operator for SQL to GCS operators.\n'
import abc, json, sys
from tempfile import NamedTemporaryFile
import unicodecsv as csv
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
PY3 = sys.version_info[0] == 3

class BaseSQLToGoogleCloudStorageOperator(BaseOperator):
    """BaseSQLToGoogleCloudStorageOperator"""
    template_fields = ('sql', 'bucket', 'filename', 'schema_filename', 'schema', 'parameters')
    template_ext = ('.sql', )
    ui_color = '#a0e08c'

    def __init__(self, sql, bucket, filename, schema_filename=None, approx_max_file_size_bytes=1900000000, export_format='json', field_delimiter=',', gzip=False, schema=None, parameters=None, google_cloud_storage_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        (super(BaseSQLToGoogleCloudStorageOperator, self).__init__)(*args, **kwargs)
        self.sql = sql
        self.bucket = bucket
        self.filename = filename
        self.schema_filename = schema_filename
        self.approx_max_file_size_bytes = approx_max_file_size_bytes
        self.export_format = export_format.lower()
        self.field_delimiter = field_delimiter
        self.gzip = gzip
        self.schema = schema
        self.parameters = parameters
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.delegate_to = delegate_to
        self.parameters = parameters

    def execute(self, context):
        cursor = self.query()
        files_to_upload = self._write_local_data_files(cursor)
        if self.schema_filename:
            files_to_upload.append(self._write_local_schema_file(cursor))
        for tmp_file in files_to_upload:
            tmp_file['file_handle'].flush()

        self._upload_to_gcs(files_to_upload)
        for tmp_file in files_to_upload:
            tmp_file['file_handle'].close()

    def convert_types(self, schema, col_type_dict, row):
        """Convert values from DBAPI to output-friendly formats."""
        return [self.convert_type(value, col_type_dict.get(name)) for name, value in zip(schema, row)]

    def _write_local_data_files(self, cursor):
        """
        Takes a cursor, and writes results to a local file.

        :return: A dictionary where keys are filenames to be used as object
            names in GCS, and values are file handles to local files that
            contain the data for the GCS objects.
        """
        schema = list(map(lambda schema_tuple: schema_tuple[0], cursor.description))
        col_type_dict = self._get_col_type_dict()
        file_no = 0
        tmp_file_handle = NamedTemporaryFile(delete=True)
        if self.export_format == 'csv':
            file_mime_type = 'text/csv'
        else:
            file_mime_type = 'application/json'
        files_to_upload = [
         {'file_name':self.filename.format(file_no),  'file_handle':tmp_file_handle, 
          'file_mime_type':file_mime_type}]
        if self.export_format == 'csv':
            csv_writer = self._configure_csv_file(tmp_file_handle, schema)
        for row in cursor:
            row = self.convert_types(schema, col_type_dict, row)
            if self.export_format == 'csv':
                csv_writer.writerow(row)
            else:
                row_dict = dict(zip(schema, row))
                s = json.dumps(row_dict, sort_keys=True)
                if PY3:
                    s = s.encode('utf-8')
                tmp_file_handle.write(s)
                tmp_file_handle.write('\n')
            if tmp_file_handle.tell() >= self.approx_max_file_size_bytes:
                file_no += 1
                tmp_file_handle = NamedTemporaryFile(delete=True)
                files_to_upload.append({'file_name':self.filename.format(file_no), 
                 'file_handle':tmp_file_handle, 
                 'file_mime_type':file_mime_type})
                if self.export_format == 'csv':
                    csv_writer = self._configure_csv_file(tmp_file_handle, schema)

        return files_to_upload

    def _configure_csv_file(self, file_handle, schema):
        """Configure a csv writer with the file_handle and write schema
        as headers for the new file.
        """
        csv_writer = csv.writer(file_handle, encoding='utf-8', delimiter=(self.field_delimiter))
        csv_writer.writerow(schema)
        return csv_writer

    @abc.abstractmethod
    def query(self):
        """Execute DBAPI query."""
        pass

    @abc.abstractmethod
    def field_to_bigquery(self, field):
        """Convert a DBAPI field to BigQuery schema format."""
        pass

    @abc.abstractmethod
    def convert_type(self, value, schema_type):
        """Convert a value from DBAPI to output-friendly formats."""
        pass

    def _get_col_type_dict(self):
        """
        Return a dict of column name and column type based on self.schema if not None.
        """
        schema = []
        if isinstance(self.schema, str):
            schema = json.loads(self.schema)
        else:
            if isinstance(self.schema, list):
                schema = self.schema
            else:
                if self.schema is not None:
                    self.log.warning('Using default schema due to unexpected type.Should be a string or list.')
        col_type_dict = {}
        try:
            col_type_dict = {col['name']:col['type'] for col in schema}
        except KeyError:
            self.log.warning('Using default schema due to missing name or type. Please refer to: https://cloud.google.com/bigquery/docs/schemas#specifying_a_json_schema_file')

        return col_type_dict

    def _write_local_schema_file(self, cursor):
        """
        Takes a cursor, and writes the BigQuery schema for the results to a
        local file system.

        :return: A dictionary where key is a filename to be used as an object
            name in GCS, and values are file handles to local files that
            contains the BigQuery schema fields in .json format.
        """
        schema = [self.field_to_bigquery(field) for field in cursor.description]
        self.log.info('Using schema for %s: %s', self.schema_filename, schema)
        tmp_schema_file_handle = NamedTemporaryFile(delete=True)
        schema_str = json.dumps(schema, sort_keys=True)
        if PY3:
            schema_str = schema_str.encode('utf-8')
        tmp_schema_file_handle.write(schema_str)
        schema_file_to_upload = {'file_name':self.schema_filename, 
         'file_handle':tmp_schema_file_handle, 
         'file_mime_type':'application/json'}
        return schema_file_to_upload

    def _upload_to_gcs(self, files_to_upload):
        """
        Upload all of the file splits (and optionally the schema .json file) to
        Google cloud storage.
        """
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id),
          delegate_to=(self.delegate_to))
        for tmp_file in files_to_upload:
            hook.upload((self.bucket), (tmp_file.get('file_name')), (tmp_file.get('file_handle').name),
              mime_type=(tmp_file.get('file_mime_type')),
              gzip=(self.gzip if tmp_file.get('file_name') == self.schema_filename else False))