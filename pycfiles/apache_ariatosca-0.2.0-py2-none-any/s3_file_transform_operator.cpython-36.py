# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/s3_file_transform_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6855 bytes
from tempfile import NamedTemporaryFile
import subprocess, sys
from airflow.exceptions import AirflowException
from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class S3FileTransformOperator(BaseOperator):
    """S3FileTransformOperator"""
    template_fields = ('source_s3_key', 'dest_s3_key')
    template_ext = ()
    ui_color = '#f9c915'

    @apply_defaults
    def __init__(self, source_s3_key, dest_s3_key, transform_script=None, select_expression=None, source_aws_conn_id='aws_default', source_verify=None, dest_aws_conn_id='aws_default', dest_verify=None, replace=False, *args, **kwargs):
        (super(S3FileTransformOperator, self).__init__)(*args, **kwargs)
        self.source_s3_key = source_s3_key
        self.source_aws_conn_id = source_aws_conn_id
        self.source_verify = source_verify
        self.dest_s3_key = dest_s3_key
        self.dest_aws_conn_id = dest_aws_conn_id
        self.dest_verify = dest_verify
        self.replace = replace
        self.transform_script = transform_script
        self.select_expression = select_expression
        self.output_encoding = sys.getdefaultencoding()

    def execute(self, context):
        if self.transform_script is None:
            if self.select_expression is None:
                raise AirflowException('Either transform_script or select_expression must be specified')
        source_s3 = S3Hook(aws_conn_id=(self.source_aws_conn_id), verify=(self.source_verify))
        dest_s3 = S3Hook(aws_conn_id=(self.dest_aws_conn_id), verify=(self.dest_verify))
        self.log.info('Downloading source S3 file %s', self.source_s3_key)
        if not source_s3.check_for_key(self.source_s3_key):
            raise AirflowException('The source key {0} does not exist'.format(self.source_s3_key))
        source_s3_key_object = source_s3.get_key(self.source_s3_key)
        with NamedTemporaryFile('wb') as (f_source):
            with NamedTemporaryFile('wb') as (f_dest):
                self.log.info('Dumping S3 file %s contents to local file %s', self.source_s3_key, f_source.name)
                if self.select_expression is not None:
                    content = source_s3.select_key(key=(self.source_s3_key),
                      expression=(self.select_expression))
                    f_source.write(content.encode('utf-8'))
                else:
                    source_s3_key_object.download_fileobj(Fileobj=f_source)
                f_source.flush()
                if self.transform_script is not None:
                    process = subprocess.Popen([
                     self.transform_script, f_source.name, f_dest.name],
                      stdout=(subprocess.PIPE),
                      stderr=(subprocess.STDOUT),
                      close_fds=True)
                    self.log.info('Output:')
                    for line in iter(process.stdout.readline, ''):
                        self.log.info(line.decode(self.output_encoding).rstrip())

                    process.wait()
                    if process.returncode > 0:
                        raise AirflowException('Transform script failed: {0}'.format(process.returncode))
                    else:
                        self.log.info('Transform script successful. Output temporarily located at %s', f_dest.name)
                self.log.info('Uploading transformed file to S3')
                f_dest.flush()
                dest_s3.load_file(filename=(f_dest.name),
                  key=(self.dest_s3_key),
                  replace=(self.replace))
                self.log.info('Upload successful')