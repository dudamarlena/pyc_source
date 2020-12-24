# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/sftp_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1856 bytes
from paramiko import SFTP_NO_SUCH_FILE
from airflow.contrib.hooks.sftp_hook import SFTPHook
from airflow.operators.sensors import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class SFTPSensor(BaseSensorOperator):
    __doc__ = '\n    Waits for a file or directory to be present on SFTP.\n\n    :param path: Remote file or directory path\n    :type path: str\n    :param sftp_conn_id: The connection to run the sensor against\n    :type sftp_conn_id: str\n    '
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