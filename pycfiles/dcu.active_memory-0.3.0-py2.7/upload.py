# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dcu/active_memory/upload.py
# Compiled at: 2017-06-30 09:17:22
import mimetypes, boto3
from boto3.s3.transfer import S3Transfer

def upload(source_path, bucketname, keyname, acl='private', guess_mimetype=True, aws_access_key_id=None, aws_secret_access_key=None):
    client = boto3.client('s3', 'us-west-2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    transfer = S3Transfer(client)
    extra_args = {'ACL': acl}
    if guess_mimetype:
        mtype = mimetypes.guess_type(keyname)[0] or 'application/octet-stream'
        extra_args['ContentType'] = mtype
    transfer.upload_file(source_path, bucketname, keyname, extra_args=extra_args)