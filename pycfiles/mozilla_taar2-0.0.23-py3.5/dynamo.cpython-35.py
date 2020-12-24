# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/taar/adapters/dynamo.py
# Compiled at: 2018-02-21 10:25:08
# Size of source mod 2**32: 2070 bytes
import boto3, json, logging, zlib
logger = logging.getLogger(__name__)

class ProfileController:
    __doc__ = '\n    This class provides basic read/write access into a AWS DynamoDB\n    backed datastore.  The profile controller and profile fetcher code\n    should eventually be merged as individually they don\'t "pull their\n    weight".\n    '

    def __init__(self, region_name, table_name):
        """
        Configure access to the DynamoDB instance
        """
        self._ddb = boto3.resource('dynamodb', region_name=region_name)
        self._table = self._ddb.Table(table_name)

    def get_client_profile(self, client_id):
        """This fetches a single client record out of DynamoDB
        """
        try:
            response = self._table.get_item(Key={'client_id': client_id})
            compressed_bytes = response['Item']['json_payload'].value
            json_byte_data = zlib.decompress(compressed_bytes)
            json_str_data = json_byte_data.decode('utf8')
            return json.loads(json_str_data)
        except Exception:
            return

    def put_client_profile(self, json_blob):
        """Store a single data record
        """
        return self._table.put_item(Item=json_blob)

    def delete(self, client_id):
        self._table.delete_item(Key={'client_id': client_id})

    def batch_delete(self, *client_ids):
        with self._table.batch_writer() as (batch):
            for client_id in client_ids:
                batch.delete_item(Key={'client_id': client_id})

    def batch_put_clients(self, records):
        """Batch fill the DynamoDB instance with
        """
        with self._table.batch_writer() as (batch):
            for rec in records:
                batch.put_item(Item=rec)