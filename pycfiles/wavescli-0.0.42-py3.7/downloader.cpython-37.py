# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/wavescli/downloader.py
# Compiled at: 2019-12-04 17:33:36
# Size of source mod 2**32: 813 bytes
import os, urllib.parse, urllib.request
from wavescli import awsadapter

def get_file(remote_uri, local_target_dir, basename=None):
    if remote_uri.startswith('s3://'):
        return awsadapter.get_file(remote_uri, local_target_dir, basename)
    if remote_uri.startswith('http://') or remote_uri.startswith('https://'):
        if not basename:
            schema = urllib.parse.urlparse(remote_uri)
            basename = os.path.basename(schema.path)
        target_path = os.path.join(local_target_dir, basename)
        response = urllib.request.urlopen(remote_uri)
        with open(target_path, 'wb') as (localfile):
            localfile.write(response.read())
        return target_path
    raise RuntimeError("Couldn't download the URL: {}".format(repr(remote_uri)))