# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/file_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2439 bytes
import os, stat
from airflow.contrib.hooks.fs_hook import FSHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class FileSensor(BaseSensorOperator):
    """FileSensor"""
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