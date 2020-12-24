# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/mongo_to_s3.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4313 bytes
import json
from airflow.contrib.hooks.mongo_hook import MongoHook
from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from bson import json_util

class MongoToS3Operator(BaseOperator):
    """MongoToS3Operator"""
    template_fields = [
     's3_key', 'mongo_query']

    @apply_defaults
    def __init__(self, mongo_conn_id, s3_conn_id, mongo_collection, mongo_query, s3_bucket, s3_key, mongo_db=None, replace=False, *args, **kwargs):
        (super(MongoToS3Operator, self).__init__)(*args, **kwargs)
        self.mongo_conn_id = mongo_conn_id
        self.s3_conn_id = s3_conn_id
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.mongo_query = mongo_query
        self.is_pipeline = True if isinstance(self.mongo_query, list) else False
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.replace = replace

    def execute(self, context):
        """
        Executed by task_instance at runtime
        """
        s3_conn = S3Hook(self.s3_conn_id)
        if self.is_pipeline:
            results = MongoHook(self.mongo_conn_id).aggregate(mongo_collection=(self.mongo_collection),
              aggregate_query=(self.mongo_query),
              mongo_db=(self.mongo_db))
        else:
            results = MongoHook(self.mongo_conn_id).find(mongo_collection=(self.mongo_collection),
              query=(self.mongo_query),
              mongo_db=(self.mongo_db))
        docs_str = self._stringify(self.transform(results))
        s3_conn.load_string(string_data=docs_str,
          key=(self.s3_key),
          bucket_name=(self.s3_bucket),
          replace=(self.replace))
        return True

    @staticmethod
    def _stringify(iterable, joinable='\n'):
        """
        Takes an iterable (pymongo Cursor or Array) containing dictionaries and
        returns a stringified version using python join
        """
        return joinable.join([json.dumps(doc, default=(json_util.default)) for doc in iterable])

    @staticmethod
    def transform(docs):
        """
        Processes pyMongo cursor and returns an iterable with each element being
                a JSON serializable dictionary

        Base transform() assumes no processing is needed
        ie. docs is a pyMongo cursor of documents and cursor just
        needs to be passed through

        Override this method for custom transformations
        """
        return docs