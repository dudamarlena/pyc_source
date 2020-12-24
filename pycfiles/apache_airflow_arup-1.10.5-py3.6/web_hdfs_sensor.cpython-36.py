# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/web_hdfs_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1641 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class WebHdfsSensor(BaseSensorOperator):
    __doc__ = '\n    Waits for a file or folder to land in HDFS\n    '
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