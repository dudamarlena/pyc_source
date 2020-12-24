# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/file_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2439 bytes
import os, stat
from airflow.contrib.hooks.fs_hook import FSHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class FileSensor(BaseSensorOperator):
    __doc__ = '\n    Waits for a file or folder to land in a filesystem.\n\n    If the path given is a directory then this sensor will only return true if\n    any files exist inside it (either directly, or within a subdirectory)\n\n    :param fs_conn_id: reference to the File (path)\n        connection id\n    :type fs_conn_id: str\n    :param filepath: File or folder name (relative to\n        the base path set within the connection)\n    :type fs_conn_id: str\n    '
    template_fields = ('filepath', )
    ui_color = '#91818a'

    @apply_defaults
    def __init__(self, filepath, fs_conn_id='fs_default', *args, **kwargs):
        (super(FileSensor, self).__init__)(*args, **kwargs)
        self.filepath = filepath
        self.fs_conn_id = fs_conn_id

    def poke(self, context):
        hook = FSHook(self.fs_conn_id)
        basepath = hook.get_path()
        full_path = os.path.join(basepath, self.filepath)
        self.log.info('Poking for file %s', full_path)
        try:
            if stat.S_ISDIR(os.stat(full_path).st_mode):
                for root, dirs, files in os.walk(full_path):
                    if len(files):
                        return True

            else:
                return True
        except OSError:
            return False
        else:
            return False