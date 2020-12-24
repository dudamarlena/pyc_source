# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/web_hdfs_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1641 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class WebHdfsSensor(BaseSensorOperator):
    """WebHdfsSensor"""
    template_fields = ('filepath', )

    @apply_defaults
    def __init__(self, filepath, webhdfs_conn_id='webhdfs_default', *args, **kwargs):
        (super(WebHdfsSensor, self).__init__)(*args, **kwargs)
        self.filepath = filepath
        self.webhdfs_conn_id = webhdfs_conn_id

    def poke(self, context):
        from airflow.hooks.webhdfs_hook import WebHDFSHook
        c = WebHDFSHook(self.webhdfs_conn_id)
        self.log.info('Poking for file %s', self.filepath)
        return c.check_for_path(hdfs_path=(self.filepath))