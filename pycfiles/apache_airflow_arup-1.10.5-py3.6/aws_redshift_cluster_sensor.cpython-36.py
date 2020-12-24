# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/aws_redshift_cluster_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2109 bytes
from airflow.contrib.hooks.redshift_hook import RedshiftHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class AwsRedshiftClusterSensor(BaseSensorOperator):
    __doc__ = '\n    Waits for a Redshift cluster to reach a specific status.\n\n    :param cluster_identifier: The identifier for the cluster being pinged.\n    :type cluster_identifier: str\n    :param target_status: The cluster status desired.\n    :type target_status: str\n    '
    template_fields = ('cluster_identifier', 'target_status')

    @apply_defaults
    def __init__(self, cluster_identifier, target_status='available', aws_conn_id='aws_default', *args, **kwargs):
        (super(AwsRedshiftClusterSensor, self).__init__)(*args, **kwargs)
        self.cluster_identifier = cluster_identifier
        self.target_status = target_status
        self.aws_conn_id = aws_conn_id

    def poke(self, context):
        self.log.info('Poking for status : %s\nfor cluster %s', self.target_status, self.cluster_identifier)
        hook = RedshiftHook(aws_conn_id=(self.aws_conn_id))
        return hook.cluster_status(self.cluster_identifier) == self.target_status