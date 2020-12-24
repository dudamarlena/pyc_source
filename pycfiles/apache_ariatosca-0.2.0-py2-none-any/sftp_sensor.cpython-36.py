# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/sftp_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1856 bytes
from paramiko import SFTP_NO_SUCH_FILE
from airflow.contrib.hooks.sftp_hook import SFTPHook
from airflow.operators.sensors import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class SFTPSensor(BaseSensorOperator):
    """SFTPSensor"""
    template_fields = ('path', )

    @apply_defaults
    def __init__(self, path, sftp_conn_id='sftp_default', *args, **kwargs):
        (super(SFTPSensor, self).__init__)(*args, **kwargs)
        self.path = path
        self.hook = SFTPHook(sftp_conn_id)

    def poke(self, context):
        self.log.info('Poking for %s', self.path)
        try:
            self.hook.get_mod_time(self.path)
        except IOError as e:
            if e.errno != SFTP_NO_SUCH_FILE:
                raise e
            return False

        self.hook.close_conn()
        return True