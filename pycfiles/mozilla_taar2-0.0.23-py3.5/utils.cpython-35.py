# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/taar/recommenders/utils.py
# Compiled at: 2018-02-12 11:06:15
# Size of source mod 2**32: 1392 bytes
import boto3, json, logging, requests
from botocore.exceptions import ClientError
logger = logging.getLogger(__name__)

def fetch_json(uri):
    """ Perform an HTTP GET on the given uri, return the results as json.

    Args:
        uri: the string URI to fetch.

    Returns:
        A JSON object with the response or None if the status code of the
        response is an error code.
    """
    r = requests.get(uri)
    if r.status_code != requests.codes.ok:
        return
    return r.json()


def get_s3_json_content(s3_bucket, s3_key):
    """Download and parse a json file stored on AWS S3.

    The file is downloaded and then cached for future use.
    """
    raw_data = None
    try:
        s3 = boto3.resource('s3')
        raw_data = s3.Object(s3_bucket, s3_key).get()['Body'].read().decode('utf-8')
    except ClientError:
        logger.exception('Failed to download from S3', extra={'bucket': s3_bucket, 
         'key': s3_key})
        return

    try:
        return json.loads(raw_data)
    except ValueError:
        logging.error('Cannot parse JSON resource from S3', extra={'bucket': s3_bucket, 
         'key': s3_key})