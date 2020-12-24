# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/emr_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2054 bytes
from airflow.exceptions import AirflowException
from airflow.contrib.hooks.aws_hook import AwsHook

class EmrHook(AwsHook):
    __doc__ = '\n    Interact with AWS EMR. emr_conn_id is only necessary for using the\n    create_job_flow method.\n    '

    def __init__(self, emr_conn_id=None, region_name=None, *args, **kwargs):
        self.emr_conn_id = emr_conn_id
        self.region_name = region_name
        (super(EmrHook, self).__init__)(*args, **kwargs)

    def get_conn(self):
        self.conn = self.get_client_type('emr', self.region_name)
        return self.conn

    def create_job_flow(self, job_flow_overrides):
        """
        Creates a job flow using the config from the EMR connection.
        Keys of the json extra hash may have the arguments of the boto3
        run_job_flow method.
        Overrides for this config may be passed as the job_flow_overrides.
        """
        if not self.emr_conn_id:
            raise AirflowException('emr_conn_id must be present to use create_job_flow')
        emr_conn = self.get_connection(self.emr_conn_id)
        config = emr_conn.extra_dejson.copy()
        config.update(job_flow_overrides)
        response = (self.get_conn().run_job_flow)(**config)
        return response