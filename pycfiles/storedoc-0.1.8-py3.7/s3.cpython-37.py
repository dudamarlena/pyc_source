# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/storedoc/s3.py
# Compiled at: 2019-08-22 07:45:56
# Size of source mod 2**32: 3141 bytes
import os, re, boto3, urllib, mimetypes
from hashlib import md5
from time import localtime
from werkzeug.datastructures import FileStorage

class S3Service(object):
    data_uri_pat = '^data:(?P<content_type>[A-Za-z\\/\\-\\+.]*);base64,(?P<bytes>.*)$'

    def __init__(self, region_name, endpoint_url, aws_access_key_id, aws_secret_access_key):
        self.description = 'Amazon S3 or Amazon Simple Storage Service isa "simple storage service" offered by Amazon Web Services that provides object storage through a web service interface.'
        self.conn = boto3.resource('s3', region_name=region_name,
          endpoint_url=endpoint_url,
          aws_access_key_id=aws_access_key_id,
          aws_secret_access_key=aws_secret_access_key)

    def _upload_file_to_cloud(self, file, file_key, bucket, mime, guess_mime, acl):
        buck = self.conn.Bucket(bucket)
        params = dict(Key=file_key,
          Body=file,
          ACL=acl)
        if mime:
            params['ContentType'] = mime
        else:
            if guess_mime:
                guess_mime = mimetypes.guess_type(file_key)[0]
                if guess_mime:
                    params['ContentType'] = guess_mime
        (buck.put_object)(**params)
        return '{}/{}/{}'.format(self.base_url, bucket, file_key)

    def _is_data_uri(self, file):
        return bool(re.match(self.data_uri_pat, file))

    def _get_file_bytes(self, data_uri):
        match = re.match(self.data_uri_pat, data_uri)
        if match:
            return match.groups()
        raise ValueError('Invalid file provided')

    def _get_filename(self, file):
        *_, filename = file.filename.split('/')
        return filename

    def _get_random_filename(self, content_type):
        ext = mimetypes.guess_extension(content_type)
        filename = '{}{}'.format(md5(str(localtime()).encode('utf-8')).hexdigest(), ext)
        return filename

    def upload_file(self, file, bucket, folder='', filename=None, mime=None, guess_mime=False, acl='private'):
        if type(file) == FileStorage:
            _filename = self._get_filename(file)
        else:
            if type(file) == str and self._is_data_uri(file):
                mime, file_bytes = self._get_file_bytes(file)
                _filename = self._get_random_filename(mime)
                response = urllib.request.urlopen(file)
                file = response.file.read()
            else:
                raise ValueError('Invalid file provided')
        filename = filename if filename else _filename
        file_key = filename
        if folder:
            file_key = '{}/{}'.format(folder, filename)
        file_url = self._upload_file_to_cloud(file, file_key, bucket, mime, guess_mime, acl)
        return file_url