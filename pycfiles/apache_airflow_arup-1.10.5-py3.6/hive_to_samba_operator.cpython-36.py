# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/hive_to_samba_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2617 bytes
import tempfile
from airflow.hooks.hive_hooks import HiveServer2Hook
from airflow.hooks.samba_hook import SambaHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.utils.operator_helpers import context_to_airflow_vars

class Hive2SambaOperator(BaseOperator):
    __doc__ = '\n    Executes hql code in a specific Hive database and loads the\n    results of the query as a csv to a Samba location.\n\n    :param hql: the hql to be exported. (templated)\n    :type hql: str\n    :param hiveserver2_conn_id: reference to the hiveserver2 service\n    :type hiveserver2_conn_id: str\n    :param samba_conn_id: reference to the samba destination\n    :type samba_conn_id: str\n    '
    template_fields = ('hql', 'destination_filepath')
    template_ext = ('.hql', '.sql')

    @apply_defaults
    def __init__(self, hql, destination_filepath, samba_conn_id='samba_default', hiveserver2_conn_id='hiveserver2_default', *args, **kwargs):
        (super(Hive2SambaOperator, self).__init__)(*args, **kwargs)
        self.hiveserver2_conn_id = hiveserver2_conn_id
        self.samba_conn_id = samba_conn_id
        self.destination_filepath = destination_filepath
        self.hql = hql.strip().rstrip(';')

    def execute(self, context):
        samba = SambaHook(samba_conn_id=(self.samba_conn_id))
        hive = HiveServer2Hook(hiveserver2_conn_id=(self.hiveserver2_conn_id))
        tmpfile = tempfile.NamedTemporaryFile()
        self.log.info('Fetching file from Hive')
        hive.to_csv(hql=(self.hql), csv_filepath=(tmpfile.name), hive_conf=(context_to_airflow_vars(context)))
        self.log.info('Pushing to samba')
        samba.push_from_local(self.destination_filepath, tmpfile.name)