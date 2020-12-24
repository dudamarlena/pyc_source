# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/package/s3_uploader.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 6841 bytes
"""
Client for uploading packaged artifacts to s3
"""
import hashlib, logging, threading, os, sys
from collections import abc
import botocore, botocore.exceptions
from boto3.s3 import transfer
from samcli.commands.package.exceptions import NoSuchBucketError, BucketNotSpecifiedError
from samcli.lib.utils.hash import file_checksum
LOG = logging.getLogger(__name__)

class S3Uploader:
    __doc__ = '\n    Class to upload objects to S3 bucket that use versioning. If bucket\n    does not already use versioning, this class will turn on versioning.\n    '

    @property
    def artifact_metadata(self):
        """
        Metadata to attach to the object(s) uploaded by the uploader.
        """
        return self._artifact_metadata

    @artifact_metadata.setter
    def artifact_metadata(self, val):
        if val is not None:
            if not isinstance(val, abc.Mapping):
                raise TypeError('Artifact metadata should be in dict type')
        self._artifact_metadata = val

    def __init__(self, s3_client, bucket_name, prefix=None, kms_key_id=None, force_upload=False):
        self.s3 = s3_client
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.kms_key_id = kms_key_id or None
        self.force_upload = force_upload
        self.transfer_manager = transfer.create_transfer_manager(self.s3, transfer.TransferConfig())
        self._artifact_metadata = None

    def upload(self, file_name, remote_path):
        """
        Uploads given file to S3
        :param file_name: Path to the file that will be uploaded
        :param remote_path:  be uploaded
        :return: VersionId of the latest upload
        """
        if self.prefix:
            remote_path = '{0}/{1}'.format(self.prefix, remote_path)
        else:
            if not self.force_upload:
                if self.file_exists(remote_path):
                    LOG.debug('File with same data is already exists at %s. Skipping upload', remote_path)
                    return self.make_url(remote_path)
            try:
                additional_args = {'ServerSideEncryption': 'AES256'}
                if self.kms_key_id:
                    additional_args['ServerSideEncryption'] = 'aws:kms'
                    additional_args['SSEKMSKeyId'] = self.kms_key_id
                if self.artifact_metadata:
                    additional_args['Metadata'] = self.artifact_metadata
                print_progress_callback = ProgressPercentage(file_name, remote_path)
                if not self.bucket_name:
                    raise BucketNotSpecifiedError()
                future = self.transfer_manager.upload(file_name, self.bucket_name, remote_path, additional_args, [print_progress_callback])
                future.result()
                return self.make_url(remote_path)
            except botocore.exceptions.ClientError as ex:
                try:
                    error_code = ex.response['Error']['Code']
                    if error_code == 'NoSuchBucket':
                        raise NoSuchBucketError(bucket_name=(self.bucket_name))
                    raise ex
                finally:
                    ex = None
                    del ex

    def upload_with_dedup(self, file_name, extension=None, precomputed_md5=None):
        """
        Makes and returns name of the S3 object based on the file's MD5 sum

        :param file_name: file to upload
        :param extension: String of file extension to append to the object
        :param precomputed_md5: Specified md5 hash for the file to be uploaded.
        :return: S3 URL of the uploaded object
        """
        filemd5 = precomputed_md5 or file_checksum(file_name)
        remote_path = filemd5
        if extension:
            remote_path = remote_path + '.' + extension
        return self.upload(file_name, remote_path)

    def file_exists(self, remote_path):
        """
        Check if the file we are trying to upload already exists in S3

        :param remote_path:
        :return: True, if file exists. False, otherwise
        """
        try:
            if not self.bucket_name:
                raise BucketNotSpecifiedError()
            self.s3.head_object(Bucket=(self.bucket_name), Key=remote_path)
            return True
        except botocore.exceptions.ClientError:
            return False

    def make_url(self, obj_path):
        if not self.bucket_name:
            raise BucketNotSpecifiedError()
        return 's3://{0}/{1}'.format(self.bucket_name, obj_path)

    def to_path_style_s3_url(self, key, version=None):
        """
            This link describes the format of Path Style URLs
            http://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html#access-bucket-intro
        """
        base = self.s3.meta.endpoint_url
        result = '{0}/{1}/{2}'.format(base, self.bucket_name, key)
        if version:
            result = '{0}?versionId={1}'.format(result, version)
        return result


class ProgressPercentage:

    def __init__(self, filename, remote_path):
        self._filename = filename
        self._remote_path = remote_path
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def on_progress(self, bytes_transferred, **kwargs):
        with self._lock:
            self._seen_so_far += bytes_transferred
            percentage = self._seen_so_far / self._size * 100
            sys.stderr.write('\rUploading to %s  %s / %s  (%.2f%%)' % (self._remote_path, self._seen_so_far, self._size, percentage))
            sys.stderr.flush()
            if int(percentage) == 100:
                sys.stderr.write('\n')