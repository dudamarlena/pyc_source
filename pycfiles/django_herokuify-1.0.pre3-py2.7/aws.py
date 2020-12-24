# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\herokuify\aws.py
# Compiled at: 2012-10-24 18:45:29
from __future__ import unicode_literals
import os
__all__ = [
 b'AWS_ACCESS_KEY_ID', b'AWS_SECRET_ACCESS_KEY', b'AWS_STORAGE_BUCKET_NAME']
AWS_ACCESS_KEY_ID = os.environ.get(b'AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get(b'AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get(b'AWS_STORAGE_BUCKET_NAME')