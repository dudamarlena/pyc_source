# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/mongo_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2373 bytes
from airflow.contrib.hooks.mongo_hook import MongoHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class MongoSensor(BaseSensorOperator):
    __doc__ = '\n    Checks for the existence of a document which\n    matches the given query in MongoDB. Example:\n\n    >>> mongo_sensor = MongoSensor(collection="coll",\n    ...                            query={"key": "value"},\n    ...                            mongo_conn_id="mongo_default",\n    ...                            task_id="mongo_sensor")\n    '
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