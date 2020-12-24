# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = '\n    Copies data from a source S3 location to a temporary location on the\n    local filesystem. Runs a transformation on this file as specified by\n    the transformation script and uploads the output to a destination S3\n    location.\n\n    The locations of the source and the destination files in the local\n    filesystem is provided as an first and second arguments to the\n    transformation script. The transformation script is expected to read the\n    data from source, transform it and write the output to the local\n    destination file. The operator then takes over control and uploads the\n    local destination file to S3.\n\n    S3 Select is also available to filter the source contents. Users can\n    omit the transformation script if S3 Select expression is specified.\n\n    :param source_s3_key: The key to be retrieved from S3. (templated)\n    :type source_s3_key: str\n    :param source_aws_conn_id: source s3 connection\n    :type source_aws_conn_id: str\n    :param source_verify: Whether or not to verify SSL certificates for S3 connection.\n        By default SSL certificates are verified.\n        You can provide the following values:\n\n        - ``False``: do not validate SSL certificates. SSL will still be used\n             (unless use_ssl is False), but SSL certificates will not be\n             verified.\n        - ``path/to/cert/bundle.pem``: A filename of the CA cert bundle to uses.\n             You can specify this argument if you want to use a different\n             CA cert bundle than the one used by botocore.\n\n        This is also applicable to ``dest_verify``.\n    :type source_verify: bool or str\n    :param dest_s3_key: The key to be written from S3. (templated)\n    :type dest_s3_key: str\n    :param dest_aws_conn_id: destination s3 connection\n    :type dest_aws_conn_id: str\n    :param replace: Replace dest S3 key if it already exists\n    :type replace: bool\n    :param transform_script: location of the executable transformation script\n    :type transform_script: str\n    :param select_expression: S3 Select expression\n    :type select_expression: str\n    '
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
                    for line in iter(process.stdout.readline, b''):
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