# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/s3_to_hive_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 12496 bytes
from builtins import next
from builtins import zip
from tempfile import NamedTemporaryFile
from airflow.utils.file import TemporaryDirectory
import gzip, bz2, tempfile, os
from airflow.exceptions import AirflowException
from airflow.hooks.S3_hook import S3Hook
from airflow.hooks.hive_hooks import HiveCliHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.utils.compression import uncompress_file

class S3ToHiveTransfer(BaseOperator):
    """S3ToHiveTransfer"""
    template_fields = ('s3_key', 'partition', 'hive_table')
    template_ext = ()
    ui_color = '#a0e08c'

    @apply_defaults
    def __init__(self, s3_key, field_dict, hive_table, delimiter=',', create=True, recreate=False, partition=None, headers=False, check_headers=False, wildcard_match=False, aws_conn_id='aws_default', verify=None, hive_cli_conn_id='hive_cli_default', input_compressed=False, tblproperties=None, select_expression=None, *args, **kwargs):
        (super(S3ToHiveTransfer, self).__init__)(*args, **kwargs)
        self.s3_key = s3_key
        self.field_dict = field_dict
        self.hive_table = hive_table
        self.delimiter = delimiter
        self.create = create
        self.recreate = recreate
        self.partition = partition
        self.headers = headers
        self.check_headers = check_headers
        self.wildcard_match = wildcard_match
        self.hive_cli_conn_id = hive_cli_conn_id
        self.aws_conn_id = aws_conn_id
        self.verify = verify
        self.input_compressed = input_compressed
        self.tblproperties = tblproperties
        self.select_expression = select_expression
        if self.check_headers:
            if not (self.field_dict is not None and self.headers):
                raise AirflowException('To check_headers provide field_dict and headers')

    def execute(self, context):
        self.s3 = S3Hook(aws_conn_id=(self.aws_conn_id), verify=(self.verify))
        self.hive = HiveCliHook(hive_cli_conn_id=(self.hive_cli_conn_id))
        self.log.info('Downloading S3 file')
        if self.wildcard_match:
            if not self.s3.check_for_wildcard_key(self.s3_key):
                raise AirflowException('No key matches {0}'.format(self.s3_key))
            s3_key_object = self.s3.get_wildcard_key(self.s3_key)
        else:
            if not self.s3.check_for_key(self.s3_key):
                raise AirflowException('The key {0} does not exists'.format(self.s3_key))
            s3_key_object = self.s3.get_key(self.s3_key)
        root, file_ext = os.path.splitext(s3_key_object.key)
        if self.select_expression:
            if self.input_compressed:
                if file_ext.lower() != '.gz':
                    raise AirflowException('GZIP is the only compression format Amazon S3 Select supports')
        with TemporaryDirectory(prefix='tmps32hive_') as (tmp_dir):
            with NamedTemporaryFile(mode='wb', dir=tmp_dir,
              suffix=file_ext) as (f):
                self.log.info('Dumping S3 key %s contents to local file %s', s3_key_object.key, f.name)
                if self.select_expression:
                    option = {}
                    if self.headers:
                        option['FileHeaderInfo'] = 'USE'
                    if self.delimiter:
                        option['FieldDelimiter'] = self.delimiter
                    input_serialization = {'CSV': option}
                    if self.input_compressed:
                        input_serialization['CompressionType'] = 'GZIP'
                    content = self.s3.select_key(bucket_name=(s3_key_object.bucket_name),
                      key=(s3_key_object.key),
                      expression=(self.select_expression),
                      input_serialization=input_serialization)
                    f.write(content.encode('utf-8'))
                else:
                    s3_key_object.download_fileobj(f)
                f.flush()
                if self.select_expression or not self.headers:
                    self.log.info('Loading file %s into Hive', f.name)
                    self.hive.load_file((f.name),
                      (self.hive_table),
                      field_dict=(self.field_dict),
                      create=(self.create),
                      partition=(self.partition),
                      delimiter=(self.delimiter),
                      recreate=(self.recreate),
                      tblproperties=(self.tblproperties))
                else:
                    if self.input_compressed:
                        self.log.info('Uncompressing file %s', f.name)
                        fn_uncompressed = uncompress_file(f.name, file_ext, tmp_dir)
                        self.log.info('Uncompressed to %s', fn_uncompressed)
                        f.close()
                    else:
                        fn_uncompressed = f.name
                    if self.check_headers:
                        self.log.info('Matching file header against field_dict')
                        header_list = self._get_top_row_as_list(fn_uncompressed)
                        if not self._match_headers(header_list):
                            raise AirflowException('Header check failed')
                    self.log.info('Removing header from file %s', fn_uncompressed)
                    headless_file = self._delete_top_row_and_compress(fn_uncompressed, file_ext, tmp_dir)
                    self.log.info('Headless file %s', headless_file)
                    self.log.info('Loading file %s into Hive', headless_file)
                    self.hive.load_file(headless_file, (self.hive_table),
                      field_dict=(self.field_dict),
                      create=(self.create),
                      partition=(self.partition),
                      delimiter=(self.delimiter),
                      recreate=(self.recreate),
                      tblproperties=(self.tblproperties))

    def _get_top_row_as_list(self, file_name):
        with open(file_name, 'rt') as (f):
            header_line = f.readline().strip()
            header_list = header_line.split(self.delimiter)
            return header_list

    def _match_headers(self, header_list):
        if not header_list:
            raise AirflowException('Unable to retrieve header row from file')
        field_names = self.field_dict.keys()
        if len(field_names) != len(header_list):
            self.log.warning('Headers count mismatch File headers:\n %s\nField names: \n %s\n', header_list, field_names)
            return False
        else:
            test_field_match = [h1.lower() == h2.lower() for h1, h2 in zip(header_list, field_names)]
            if not all(test_field_match):
                self.log.warning('Headers do not match field names File headers:\n %s\nField names: \n %s\n', header_list, field_names)
                return False
            return True

    @staticmethod
    def _delete_top_row_and_compress(input_file_name, output_file_ext, dest_dir):
        open_fn = open
        if output_file_ext.lower() == '.gz':
            open_fn = gzip.GzipFile
        else:
            if output_file_ext.lower() == '.bz2':
                open_fn = bz2.BZ2File
        os_fh_output, fn_output = tempfile.mkstemp(suffix=output_file_ext, dir=dest_dir)
        with open(input_file_name, 'rb') as (f_in):
            with open_fn(fn_output, 'wb') as (f_out):
                f_in.seek(0)
                next(f_in)
                for line in f_in:
                    f_out.write(line)

        return fn_output