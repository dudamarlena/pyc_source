# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notecode/data/download.py
# Compiled at: 2019-05-23 07:01:02
# Size of source mod 2**32: 562 bytes
import os, pycurl
__all__ = [
 'download_file']

def download_file(url, path):
    if not os.path.exists(path):
        print('downloading from ' + url + ' to ' + path)
        with open(path, 'wb') as (f):
            c = pycurl.Curl()
            c.setopt(pycurl.URL, url)
            c.setopt(pycurl.WRITEDATA, f)
            c.perform()
            c.close()
        print('download success')