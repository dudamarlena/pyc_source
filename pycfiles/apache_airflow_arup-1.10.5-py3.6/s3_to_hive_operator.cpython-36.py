# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = "\n    Moves data from S3 to Hive. The operator downloads a file from S3,\n    stores the file locally before loading it into a Hive table.\n    If the ``create`` or ``recreate`` arguments are set to ``True``,\n    a ``CREATE TABLE`` and ``DROP TABLE`` statements are generated.\n    Hive data types are inferred from the cursor's metadata from.\n\n    Note that the table generated in Hive uses ``STORED AS textfile``\n    which isn't the most efficient serialization format. If a\n    large amount of data is loaded and/or if the tables gets\n    queried considerably, you may want to use this operator only to\n    stage the data into a temporary table before loading it into its\n    final destination using a ``HiveOperator``.\n\n    :param s3_key: The key to be retrieved from S3. (templated)\n    :type s3_key: str\n    :param field_dict: A dictionary of the fields name in the file\n        as keys and their Hive types as values\n    :type field_dict: dict\n    :param hive_table: target Hive table, use dot notation to target a\n        specific database. (templated)\n    :type hive_table: str\n    :param create: whether to create the table if it doesn't exist\n    :type create: bool\n    :param recreate: whether to drop and recreate the table at every\n        execution\n    :type recreate: bool\n    :param partition: target partition as a dict of partition columns\n        and values. (templated)\n    :type partition: dict\n    :param headers: whether the file contains column names on the first\n        line\n    :type headers: bool\n    :param check_headers: whether the column names on the first line should be\n        checked against the keys of field_dict\n    :type check_headers: bool\n    :param wildcard_match: whether the s3_key should be interpreted as a Unix\n        wildcard pattern\n    :type wildcard_match: bool\n    :param delimiter: field delimiter in the file\n    :type delimiter: str\n    :param aws_conn_id: source s3 connection\n    :type aws_conn_id: str\n    :param verify: Whether or not to verify SSL certificates for S3 connection.\n        By default SSL certificates are verified.\n        You can provide the following values:\n\n        - ``False``: do not validate SSL certificates. SSL will still be used\n                 (unless use_ssl is False), but SSL certificates will not be\n                 verified.\n        - ``path/to/cert/bundle.pem``: A filename of the CA cert bundle to uses.\n                 You can specify this argument if you want to use a different\n                 CA cert bundle than the one used by botocore.\n    :type verify: bool or str\n    :param hive_cli_conn_id: destination hive connection\n    :type hive_cli_conn_id: str\n    :param input_compressed: Boolean to determine if file decompression is\n        required to process headers\n    :type input_compressed: bool\n    :param tblproperties: TBLPROPERTIES of the hive table being created\n    :type tblproperties: dict\n    :param select_expression: S3 Select expression\n    :type select_expression: str\n    "
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