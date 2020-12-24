# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/test/test.py
# Compiled at: 2013-09-16 06:14:55
import os
from avoid_disaster import S3Uploader, gunzip_dir, generate_file_key
AWS_KEY = 'YOUR AWS KEY'
AWS_SECRET = 'YOUR AWS SECRET'
s3_uploader = S3Uploader(AWS_KEY, AWS_SECRET, 'backups.your_domain.com')
s3_uploader.compress_and_upload('test_dir/', 'test_dir.%(weekday)s.tgz', replace_old=True)
s3_uploader.compress_and_upload('test_dir/', 'test_dir.%(month_name)s.tgz', replace_old=True)
s3_uploader.compress_and_upload('test_dir/', 'test_dir.%(week_number)s.tgz', replace_old=True)
file_key = generate_file_key('test_dir.%(weekday)s.tgz')
gz_filename = gunzip_dir('test_dir/', file_key)
s3_uploader.upload(file_key, gz_filename, replace_old=True)
os.remove(gz_filename)