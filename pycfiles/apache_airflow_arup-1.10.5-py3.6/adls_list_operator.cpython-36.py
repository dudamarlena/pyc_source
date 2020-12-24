# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/adls_list_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2598 bytes
from typing import Iterable
from airflow.contrib.hooks.azure_data_lake_hook import AzureDataLakeHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class AzureDataLakeStorageListOperator(BaseOperator):
    __doc__ = "\n    List all files from the specified path\n\n    This operator returns a python list with the names of files which can be used by\n     `xcom` in the downstream tasks.\n\n    :param path: The Azure Data Lake path to find the objects. Supports glob\n        strings (templated)\n    :type path: str\n    :param azure_data_lake_conn_id: The connection ID to use when\n        connecting to Azure Data Lake Storage.\n    :type azure_data_lake_conn_id: str\n\n    **Example**:\n        The following Operator would list all the Parquet files from ``folder/output/``\n        folder in the specified ADLS account ::\n\n            adls_files = AzureDataLakeStorageListOperator(\n                task_id='adls_files',\n                path='folder/output/*.parquet',\n                azure_data_lake_conn_id='azure_data_lake_default'\n            )\n    "
    template_fields = ('path', )
    ui_color = '#901dd2'

    @apply_defaults
    def __init__(self, path, azure_data_lake_conn_id='azure_data_lake_default', *args, **kwargs):
        (super(AzureDataLakeStorageListOperator, self).__init__)(*args, **kwargs)
        self.path = path
        self.azure_data_lake_conn_id = azure_data_lake_conn_id

    def execute(self, context):
        hook = AzureDataLakeHook(azure_data_lake_conn_id=(self.azure_data_lake_conn_id))
        self.log.info('Getting list of ADLS files in path: %s', self.path)
        return hook.list(path=(self.path))