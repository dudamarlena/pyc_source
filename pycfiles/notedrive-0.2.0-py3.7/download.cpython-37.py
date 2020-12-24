# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notedrive/utils/download.py
# Compiled at: 2020-04-19 10:34:23
# Size of source mod 2**32: 496 bytes
import os, pycurl
from notedrive.baidu.drive import BaiDuDrive

def download(url, path):
    with open(path, 'wb') as (f):
        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.WRITEDATA, f)
        c.perform()
        c.close()


def download_from_url(url, bduss=None, save_path='/drive/temp/'):
    client = BaiDuDrive(bduss)
    filename = os.path.basename(url)
    download(url, filename)
    client.upload(filename, (save_path + filename), overwrite=True)