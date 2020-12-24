# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/ftp_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3356 bytes
import ftplib, re
from airflow.contrib.hooks.ftp_hook import FTPHook, FTPSHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class FTPSensor(BaseSensorOperator):
    """FTPSensor"""
    template_fields = ('path', )
    transient_errors = [
     421, 425, 426, 434, 450, 451, 452]
    error_code_pattern = re.compile('([\\d]+)')

    @apply_defaults
    def __init__(self, path, ftp_conn_id='ftp_default', fail_on_transient_errors=True, *args, **kwargs):
        """
        Create a new FTP sensor

        :param path: Remote file or directory path
        :type path: str
        :param fail_on_transient_errors: Fail on all errors,
            including 4xx transient errors. Default True.
        :type fail_on_transient_errors: bool
        :param ftp_conn_id: The connection to run the sensor against
        :type ftp_conn_id: str
        """
        (super(FTPSensor, self).__init__)(*args, **kwargs)
        self.path = path
        self.ftp_conn_id = ftp_conn_id
        self.fail_on_transient_errors = fail_on_transient_errors

    def _create_hook(self):
        """Return connection hook."""
        return FTPHook(ftp_conn_id=(self.ftp_conn_id))

    def _get_error_code(self, e):
        """Extract error code from ftp exception"""
        try:
            matches = self.error_code_pattern.match(str(e))
            code = int(matches.group(0))
            return code
        except ValueError:
            return e

    def poke(self, context):
        with self._create_hook() as (hook):
            self.log.info('Poking for %s', self.path)
            try:
                hook.get_mod_time(self.path)
            except ftplib.error_perm as e:
                self.log.info('Ftp error encountered: %s', str(e))
                error_code = self._get_error_code(e)
                if error_code != 550:
                    if self.fail_on_transient_errors or error_code not in self.transient_errors:
                        raise e
                return False

            return True


class FTPSSensor(FTPSensor):
    """FTPSSensor"""

    def _create_hook(self):
        """Return connection hook."""
        return FTPSHook(ftp_conn_id=(self.ftp_conn_id))