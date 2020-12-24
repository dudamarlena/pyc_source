# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/gcs_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 12559 bytes
import os
from datetime import datetime
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class GoogleCloudStorageObjectSensor(BaseSensorOperator):
    """GoogleCloudStorageObjectSensor"""
    template_fields = ('bucket', 'object')
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, bucket, object, google_cloud_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        (super(GoogleCloudStorageObjectSensor, self).__init__)(*args, **kwargs)
        self.bucket = bucket
        self.object = object
        self.google_cloud_conn_id = google_cloud_conn_id
        self.delegate_to = delegate_to

    def poke(self, context):
        self.log.info('Sensor checks existence of : %s, %s', self.bucket, self.object)
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_conn_id),
          delegate_to=(self.delegate_to))
        return hook.exists(self.bucket, self.object)


def ts_function(context):
    """
    Default callback for the GoogleCloudStorageObjectUpdatedSensor. The default
    behaviour is check for the object being updated after execution_date +
    schedule_interval.
    """
    return context['dag'].following_schedule(context['execution_date'])


class GoogleCloudStorageObjectUpdatedSensor(BaseSensorOperator):
    """GoogleCloudStorageObjectUpdatedSensor"""
    template_fields = ('bucket', 'object')
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, bucket, object, ts_func=ts_function, google_cloud_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        (super(GoogleCloudStorageObjectUpdatedSensor, self).__init__)(*args, **kwargs)
        self.bucket = bucket
        self.object = object
        self.ts_func = ts_func
        self.google_cloud_conn_id = google_cloud_conn_id
        self.delegate_to = delegate_to

    def poke(self, context):
        self.log.info('Sensor checks existence of : %s, %s', self.bucket, self.object)
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_conn_id),
          delegate_to=(self.delegate_to))
        return hook.is_updated_after(self.bucket, self.object, self.ts_func(context))


class GoogleCloudStoragePrefixSensor(BaseSensorOperator):
    """GoogleCloudStoragePrefixSensor"""
    template_fields = ('bucket', 'prefix')
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, bucket, prefix, google_cloud_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        (super(GoogleCloudStoragePrefixSensor, self).__init__)(*args, **kwargs)
        self.bucket = bucket
        self.prefix = prefix
        self.google_cloud_conn_id = google_cloud_conn_id
        self.delegate_to = delegate_to

    def poke(self, context):
        self.log.info('Sensor checks existence of objects: %s, %s', self.bucket, self.prefix)
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_conn_id),
          delegate_to=(self.delegate_to))
        return bool(hook.list((self.bucket), prefix=(self.prefix)))


def get_time():
    """
    This is just a wrapper of datetime.datetime.now to simplify mocking in the
    unittests.
    """
    return datetime.now()


class GoogleCloudStorageUploadSessionCompleteSensor(BaseSensorOperator):
    """GoogleCloudStorageUploadSessionCompleteSensor"""
    template_fields = ('bucket', 'prefix')
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, bucket, prefix, inactivity_period=3600, min_objects=1, previous_num_objects=0, allow_delete=True, google_cloud_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        (super(GoogleCloudStorageUploadSessionCompleteSensor, self).__init__)(*args, **kwargs)
        self.bucket = bucket
        self.prefix = prefix
        self.inactivity_period = inactivity_period
        self.min_objects = min_objects
        self.previous_num_objects = previous_num_objects
        self.inactivity_seconds = 0
        self.allow_delete = allow_delete
        self.google_cloud_conn_id = google_cloud_conn_id
        self.delegate_to = delegate_to
        self.last_activity_time = None

    def is_bucket_updated(self, current_num_objects):
        """
        Checks whether new objects have been uploaded and the inactivity_period
        has passed and updates the state of the sensor accordingly.

        :param current_num_objects: number of objects in bucket during last poke.
        :type current_num_objects: int
        """
        if current_num_objects > self.previous_num_objects:
            self.log.info('\n                New objects found at {} resetting last_activity_time.\n                '.format(os.path.join(self.bucket, self.prefix)))
            self.last_activity_time = get_time()
            self.inactivity_seconds = 0
            self.previous_num_objects = current_num_objects
        else:
            if current_num_objects < self.previous_num_objects:
                if self.allow_delete:
                    self.previous_num_objects = current_num_objects
                    self.last_activity_time = get_time()
                    self.log.warning('\n                    Objects were deleted during the last\n                    poke interval. Updating the file counter and\n                    resetting last_activity_time.\n                    ')
                else:
                    raise RuntimeError('\n                    Illegal behavior: objects were deleted in {} between pokes.\n                    '.format(os.path.join(self.bucket, self.prefix)))
            else:
                if self.last_activity_time:
                    self.inactivity_seconds = (get_time() - self.last_activity_time).total_seconds()
                else:
                    self.last_activity_time = get_time()
                    self.inactivity_seconds = 0
                if self.inactivity_seconds >= self.inactivity_period:
                    if current_num_objects >= self.min_objects:
                        self.log.info('\n                        SUCCESS:\n                        Sensor found {} objects at {}.\n                        Waited at least {} seconds, with no new objects dropped.\n                        '.format(current_num_objects, os.path.join(self.bucket, self.prefix), self.inactivity_period))
                        return True
                    warn_msg = '\n                    FAILURE:\n                    Inactivity Period passed,\n                    not enough objects found in {}\n                    '.format(os.path.join(self.bucket, self.prefix))
                    self.log.warning(warn_msg)
                    return False
                else:
                    return False

    def poke(self, context):
        hook = GoogleCloudStorageHook()
        return self.is_bucket_updated(len(hook.list((self.bucket), prefix=(self.prefix))))