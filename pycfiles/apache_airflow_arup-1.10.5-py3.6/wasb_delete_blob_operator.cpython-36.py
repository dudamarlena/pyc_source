# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/wasb_delete_blob_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2731 bytes
from airflow.contrib.hooks.wasb_hook import WasbHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class WasbDeleteBlobOperator(BaseOperator):
    __doc__ = '\n    Deletes blob(s) on Azure Blob Storage.\n\n    :param container_name: Name of the container. (templated)\n    :type container_name: str\n    :param blob_name: Name of the blob. (templated)\n    :type blob_name: str\n    :param wasb_conn_id: Reference to the wasb connection.\n    :type wasb_conn_id: str\n    :param check_options: Optional keyword arguments that\n        `WasbHook.check_for_blob()` takes.\n    :param is_prefix: If blob_name is a prefix, delete all files matching prefix.\n    :type is_prefix: bool\n    :param ignore_if_missing: if True, then return success even if the\n        blob does not exist.\n    :type ignore_if_missing: bool\n    '
    template_fields = ('container_name', 'blob_name')

    @apply_defaults
    def __init__(self, container_name, blob_name, wasb_conn_id='wasb_default', check_options=None, is_prefix=False, ignore_if_missing=False, *args, **kwargs):
        (super(WasbDeleteBlobOperator, self).__init__)(*args, **kwargs)
        if check_options is None:
            check_options = {}
        self.wasb_conn_id = wasb_conn_id
        self.container_name = container_name
        self.blob_name = blob_name
        self.check_options = check_options
        self.is_prefix = is_prefix
        self.ignore_if_missing = ignore_if_missing

    def execute(self, context):
        self.log.info('Deleting blob: %s\nin wasb://%s', self.blob_name, self.container_name)
        hook = WasbHook(wasb_conn_id=(self.wasb_conn_id))
        (hook.delete_file)((self.container_name), (self.blob_name), 
         (self.is_prefix), (self.ignore_if_missing), **self.check_options)