# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/project/znbdownload/fields.py
# Compiled at: 2019-07-04 10:24:59
# Size of source mod 2**32: 661 bytes
import logging
from django.db import models
from .storage import S3PrivateStorage
logger = logging.getLogger(__name__)

class S3PrivateFileField(models.FileField):
    __doc__ = "\n    A FileField with a default 'private' ACL to the files it uploads to S3, instead of the default ACL.\n    You can pass also pass 'public-read' for testing but it may be confusing.\n    "

    def __init__(self, verbose_name=None, name=None, upload_to='', storage=None, default_acl='private', **kwargs):
        self.storage = storage or S3PrivateStorage(default_acl)
        (super().__init__)(verbose_name=verbose_name, name=name, upload_to=upload_to, storage=self.storage, **kwargs)