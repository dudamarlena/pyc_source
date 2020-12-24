# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/s3iotools-project/s3iotools/tests/moto_compat.py
# Compiled at: 2019-05-19 22:48:53
"""
moto3 requires a ~/.aws/credentials file exists, so we create a fake one dynamically.
"""
import os
src = os.path.join(os.path.dirname(__file__), 'credentials')
dst = os.path.join(os.path.expanduser('~'), '.aws', 'credentials')
dst_dir = os.path.dirname(dst)
if not os.path.exists(dst_dir):
    os.mkdir(dst_dir)
if not os.path.exists(dst):
    with open(src, 'rb') as (f1):
        with open(dst, 'wb') as (f2):
            s = f1.read().decode('utf-8').format(field1='aws_access_key_id', field2='aws_secret_access_key')
            f2.write(s.encode('utf-8'))