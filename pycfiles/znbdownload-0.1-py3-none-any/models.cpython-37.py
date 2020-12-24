# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/project/znbdownload/models.py
# Compiled at: 2019-07-04 12:33:17
# Size of source mod 2**32: 1747 bytes
import logging, boto3
from django.db import models
from django.conf import settings
from .storage import S3PrivateStorage
from .fields import S3PrivateFileField
logger = logging.getLogger(__name__)
storage = S3PrivateStorage()

class PrivateDownload(models.Model):
    __doc__ = "\n    By using a S3PrivateFileField field, using default_acl='private',\n    the file is private by default.\n    You can pass default_acl='public-read' for testing but it may be confusing.\n    "
    title = models.CharField(max_length=200)
    private_file = S3PrivateFileField(blank=True, null=True, upload_to='secret')

    def __str__(self):
        return self.title


class Download(models.Model):
    __doc__ = '\n    The private_file field can be switched to public-read or private with\n    the private boolean field.\n    '
    title = models.CharField(max_length=200)
    private_file = models.FileField(blank=True, null=True, storage=storage)
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        (super().save)(*args, **kwargs)
        bucket_name = getattr(settings, 'AWS_STORAGE_PRIVATE_BUCKET_NAME')
        session = boto3.Session(aws_access_key_id=(getattr(settings, 'AWS_ACCESS_KEY_ID')),
          aws_secret_access_key=(getattr(settings, 'AWS_SECRET_ACCESS_KEY')))
        s3 = session.resource('s3')
        object_acl = s3.ObjectAcl(bucket_name, self.private_file.name)
        if self.private:
            object_acl.put(ACL='private')
        else:
            object_acl.put(ACL='public-read')