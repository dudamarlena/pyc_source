# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/resgen/aws.py
# Compiled at: 2020-03-22 19:12:26
# Size of source mod 2**32: 1914 bytes
import logging, os, sys, threading, typing, boto3
from botocore.exceptions import ClientError

class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = self._seen_so_far / self._size * 100
            sys.stdout.write('\r%s  %s / %s  (%.2f%%)' % (
             self._filename, self._seen_so_far, self._size, percentage))
            sys.stdout.flush()


def upload_file(file_name: str, bucket: str, credentials: typing.Dict[(str, str)], object_name: str=None):
    """Upload a file to an S3 bucket

    Args:
        file_name: File to upload
        bucket: Bucket to upload to
        credentials: A dictionary containing the `awsAccessKeyId`,
            `secretAccessKey` and `sessionToken` entries
        object_name: S3 object name. If not specified then file_name is used

    Returns:
        True if file was uploaded, else False

    """
    if object_name is None:
        object_name = file_name
    s3_client = boto3.client('s3',
      aws_access_key_id=(credentials['accessKeyId']),
      aws_secret_access_key=(credentials['secretAccessKey']),
      aws_session_token=(credentials['sessionToken']))
    try:
        s3_client.upload_file(file_name,
          bucket, object_name, Callback=(ProgressPercentage(file_name)))
    except ClientError as client_error:
        try:
            logging.error(client_error)
            return False
        finally:
            client_error = None
            del client_error

    return True