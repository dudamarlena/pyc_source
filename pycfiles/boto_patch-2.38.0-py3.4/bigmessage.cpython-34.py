# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/sqs/bigmessage.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 4729 bytes
import uuid, boto
from boto.sqs.message import RawMessage
from boto.exception import SQSDecodeError

class BigMessage(RawMessage):
    __doc__ = "\n    The BigMessage class provides large payloads (up to 5GB)\n    by storing the payload itself in S3 and then placing a reference\n    to the S3 object in the actual SQS message payload.\n\n    To create a BigMessage, you should create a BigMessage object\n    and pass in a file-like object as the ``body`` param and also\n    pass in the an S3 URL specifying the bucket in which to store\n    the message body::\n\n        import boto.sqs\n        from boto.sqs.bigmessage import BigMessage\n\n        sqs = boto.sqs.connect_to_region('us-west-2')\n        queue = sqs.get_queue('myqueue')\n        fp = open('/path/to/bigmessage/data')\n        msg = BigMessage(queue, fp, 's3://mybucket')\n        queue.write(msg)\n\n    Passing in a fully-qualified S3 URL (e.g. s3://mybucket/foo)\n    is interpreted to mean that the body of the message is already\n    stored in S3 and the that S3 URL is then used directly with no\n    content uploaded by BigMessage.\n    "

    def __init__(self, queue=None, body=None, s3_url=None):
        self.s3_url = s3_url
        super(BigMessage, self).__init__(queue, body)

    def _get_bucket_key(self, s3_url):
        bucket_name = key_name = None
        if s3_url:
            if s3_url.startswith('s3://'):
                s3_components = s3_url[5:].split('/', 1)
                bucket_name = s3_components[0]
                if len(s3_components) > 1:
                    if s3_components[1]:
                        key_name = s3_components[1]
            else:
                msg = 's3_url parameter should start with s3://'
                raise SQSDecodeError(msg, self)
        return (
         bucket_name, key_name)

    def encode(self, value):
        """
        :type value: file-like object
        :param value: A file-like object containing the content
            of the message.  The actual content will be stored
            in S3 and a link to the S3 object will be stored in
            the message body.
        """
        bucket_name, key_name = self._get_bucket_key(self.s3_url)
        if bucket_name and key_name:
            return self.s3_url
        key_name = uuid.uuid4()
        s3_conn = boto.connect_s3()
        s3_bucket = s3_conn.get_bucket(bucket_name)
        key = s3_bucket.new_key(key_name)
        key.set_contents_from_file(value)
        self.s3_url = 's3://%s/%s' % (bucket_name, key_name)
        return self.s3_url

    def _get_s3_object(self, s3_url):
        bucket_name, key_name = self._get_bucket_key(s3_url)
        if bucket_name and key_name:
            s3_conn = boto.connect_s3()
            s3_bucket = s3_conn.get_bucket(bucket_name)
            key = s3_bucket.get_key(key_name)
            return key
        msg = 'Unable to decode S3 URL: %s' % s3_url
        raise SQSDecodeError(msg, self)

    def decode(self, value):
        self.s3_url = value
        key = self._get_s3_object(value)
        return key.get_contents_as_string()

    def delete(self):
        if self.s3_url:
            key = self._get_s3_object(self.s3_url)
            key.delete()
        super(BigMessage, self).delete()