# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/mongo_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2373 bytes
from airflow.contrib.hooks.mongo_hook import MongoHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class MongoSensor(BaseSensorOperator):
    """MongoSensor"""
    template_fields = ('collection', 'query')

    @apply_defaults
    def __init__(self, collection, query, mongo_conn_id='mongo_default', *args, **kwargs):
        """
        Create a new MongoSensor

        :param collection: Target MongoDB collection.
        :type collection: str
        :param query: The query to find the target document.
        :type query: dict
        :param mongo_conn_id: The connection ID to use
                              when connecting to MongoDB.
        :type mongo_conn_id: str
        """
        (super(MongoSensor, self).__init__)(*args, **kwargs)
        self.mongo_conn_id = mongo_conn_id
        self.collection = collection
        self.query = query

    def poke(self, context):
        self.log.info('Sensor check existence of the document that matches the following query: %s', self.query)
        hook = MongoHook(self.mongo_conn_id)
        return hook.find((self.collection), (self.query), find_one=True) is not None