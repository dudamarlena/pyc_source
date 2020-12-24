# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/file_to_wasb.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2513 bytes
from airflow.contrib.hooks.wasb_hook import WasbHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class FileToWasbOperator(BaseOperator):
    __doc__ = '\n    Uploads a file to Azure Blob Storage.\n\n    :param file_path: Path to the file to load. (templated)\n    :type file_path: str\n    :param container_name: Name of the container. (templated)\n    :type container_name: str\n    :param blob_name: Name of the blob. (templated)\n    :type blob_name: str\n    :param wasb_conn_id: Reference to the wasb connection.\n    :type wasb_conn_id: str\n    :param load_options: Optional keyword arguments that\n        `WasbHook.load_file()` takes.\n    :type load_options: dict\n    '
    template_fields = ('file_path', 'container_name', 'blob_name')

    @apply_defaults
    def __init__(self, file_path, container_name, blob_name, wasb_conn_id='wasb_default', load_options=None, *args, **kwargs):
        (super(FileToWasbOperator, self).__init__)(*args, **kwargs)
        if load_options is None:
            load_options = {}
        self.file_path = file_path
        self.container_name = container_name
        self.blob_name = blob_name
        self.wasb_conn_id = wasb_conn_id
        self.load_options = load_options

    def execute(self, context):
        """Upload a file to Azure Blob Storage."""
        hook = WasbHook(wasb_conn_id=(self.wasb_conn_id))
        self.log.info('Uploading %s to wasb://%s as %s'.format(self.file_path, self.container_name, self.blob_name))
        (hook.load_file)((self.file_path), (self.container_name), 
         (self.blob_name), **self.load_options)