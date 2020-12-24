# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/minio_storage/policy.py
# Compiled at: 2019-10-18 04:18:30
# Size of source mod 2**32: 4048 bytes
import enum, json, typing as T

class Policy(enum.Enum):
    none = 'NONE'
    get = 'GET_ONLY'
    read = 'READ_ONLY'
    write = 'WRITE_ONLY'
    read_write = 'READ_WRITE'

    def bucket(self, bucket_name: str, *, json_encode: bool=True) -> T.Union[(str, T.Dict[(str, T.Any)])]:
        policies = {Policy.get: _get, 
         Policy.read: _read, 
         Policy.write: _write, 
         Policy.read_write: _read_write, 
         Policy.none: _none}
        pol = policies[self](bucket_name)
        if json_encode:
            return json.dumps(pol)
        return pol


def _none(bucket_name: str) -> T.Dict:
    return {'Version':'2012-10-17',  'Statement':[]}


def _get(bucket_name: str) -> T.Dict:
    return {'Version':'2012-10-17', 
     'Statement':[
      {'Effect':'Allow', 
       'Principal':{'AWS': ['*']}, 
       'Action':[
        's3:GetObject'], 
       'Resource':[
        f"arn:aws:s3:::{bucket_name}/*"]}]}


def _read(bucket_name: str) -> T.Dict:
    return {'Version':'2012-10-17', 
     'Statement':[
      {'Effect':'Allow', 
       'Principal':{'AWS': ['*']}, 
       'Action':[
        's3:GetBucketLocation'], 
       'Resource':[
        f"arn:aws:s3:::{bucket_name}"]},
      {'Effect':'Allow', 
       'Principal':{'AWS': ['*']}, 
       'Action':[
        's3:ListBucket'], 
       'Resource':[
        f"arn:aws:s3:::{bucket_name}"]},
      {'Effect':'Allow', 
       'Principal':{'AWS': ['*']}, 
       'Action':[
        's3:GetObject'], 
       'Resource':[
        f"arn:aws:s3:::{bucket_name}/*"]}]}


def _write(bucket_name: str) -> T.Dict:
    return {'Version':'2012-10-17', 
     'Statement':[
      {'Effect':'Allow', 
       'Principal':{'AWS': ['*']}, 
       'Action':[
        's3:GetBucketLocation'], 
       'Resource':[
        f"arn:aws:s3:::{bucket_name}"]},
      {'Effect':'Allow', 
       'Principal':{'AWS': ['*']}, 
       'Action':[
        's3:ListBucketMultipartUploads'], 
       'Resource':[
        f"arn:aws:s3:::{bucket_name}"]},
      {'Effect':'Allow', 
       'Principal':{'AWS': ['*']}, 
       'Action':[
        's3:ListMultipartUploadParts',
        's3:AbortMultipartUpload',
        's3:DeleteObject',
        's3:PutObject'], 
       'Resource':[
        f"arn:aws:s3:::{bucket_name}/*"]}]}


def _read_write(bucket_name: str) -> T.Dict:
    return {'Version':'2012-10-17', 
     'Statement':[
      {'Effect':'Allow', 
       'Principal':{'AWS': ['*']}, 
       'Action':[
        's3:GetBucketLocation'], 
       'Resource':[
        f"arn:aws:s3:::{bucket_name}"]},
      {'Effect':'Allow', 
       'Principal':{'AWS': ['*']}, 
       'Action':[
        's3:ListBucket'], 
       'Resource':[
        f"arn:aws:s3:::{bucket_name}"]},
      {'Effect':'Allow', 
       'Principal':{'AWS': ['*']}, 
       'Action':[
        's3:ListBucketMultipartUploads'], 
       'Resource':[
        f"arn:aws:s3:::{bucket_name}"]},
      {'Effect':'Allow', 
       'Principal':{'AWS': ['*']}, 
       'Action':[
        's3:AbortMultipartUpload',
        's3:DeleteObject',
        's3:GetObject',
        's3:ListMultipartUploadParts',
        's3:PutObject'], 
       'Resource':[
        f"arn:aws:s3:::{bucket_name}/*"]}]}