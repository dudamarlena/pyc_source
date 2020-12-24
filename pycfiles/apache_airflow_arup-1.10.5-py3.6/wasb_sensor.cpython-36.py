# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/wasb_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3611 bytes
from airflow.contrib.hooks.wasb_hook import WasbHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class WasbBlobSensor(BaseSensorOperator):
    __doc__ = '\n    Waits for a blob to arrive on Azure Blob Storage.\n\n    :param container_name: Name of the container.\n    :type container_name: str\n    :param blob_name: Name of the blob.\n    :type blob_name: str\n    :param wasb_conn_id: Reference to the wasb connection.\n    :type wasb_conn_id: str\n    :param check_options: Optional keyword arguments that\n        `WasbHook.check_for_blob()` takes.\n    :type check_options: dict\n    '
    template_fields = ('container_name', 'blob_name')

    @apply_defaults
    def __init__(self, container_name, blob_name, wasb_conn_id='wasb_default', check_options=None, *args, **kwargs):
        (super(WasbBlobSensor, self).__init__)(*args, **kwargs)
        if check_options is None:
            check_options = {}
        self.wasb_conn_id = wasb_conn_id
        self.container_name = container_name
        self.blob_name = blob_name
        self.check_options = check_options

    def poke(self, context):
        self.log.info('Poking for blob: %s\nin wasb://%s', self.blob_name, self.container_name)
        hook = WasbHook(wasb_conn_id=(self.wasb_conn_id))
        return (hook.check_for_blob)((self.container_name), (self.blob_name), **self.check_options)


class WasbPrefixSensor(BaseSensorOperator):
    __doc__ = '\n    Waits for blobs matching a prefix to arrive on Azure Blob Storage.\n\n    :param container_name: Name of the container.\n    :type container_name: str\n    :param prefix: Prefix of the blob.\n    :type prefix: str\n    :param wasb_conn_id: Reference to the wasb connection.\n    :type wasb_conn_id: str\n    :param check_options: Optional keyword arguments that\n        `WasbHook.check_for_prefix()` takes.\n    :type check_options: dict\n    '
    template_fields = ('container_name', 'prefix')

    @apply_defaults
    def __init__(self, container_name, prefix, wasb_conn_id='wasb_default', check_options=None, *args, **kwargs):
        (super(WasbPrefixSensor, self).__init__)(*args, **kwargs)
        if check_options is None:
            check_options = {}
        self.wasb_conn_id = wasb_conn_id
        self.container_name = container_name
        self.prefix = prefix
        self.check_options = check_options

    def poke(self, context):
        self.log.info('Poking for prefix: %s in wasb://%s', self.prefix, self.container_name)
        hook = WasbHook(wasb_conn_id=(self.wasb_conn_id))
        return (hook.check_for_prefix)((self.container_name), (self.prefix), **self.check_options)