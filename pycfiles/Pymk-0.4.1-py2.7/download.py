# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymk/download.py
# Compiled at: 2013-12-18 01:24:56
import os, shutil, urllib2, urlparse
from zipfile import ZipFile

def download(url, fileName=None):

    def getFileName(url, openUrl):
        if 'Content-Disposition' in openUrl.info():
            cd = dict(map(lambda x: x.strip().split('=') if '=' in x else (x.strip(), ''), openUrl.info()['Content-Disposition'].split(';')))
            if 'filename' in cd:
                filename = cd['filename'].strip('"\'')
                if filename:
                    return filename
        return os.path.basename(urlparse.urlsplit(openUrl.url)[2])

    r = urllib2.urlopen(urllib2.Request(url))
    try:
        fileName = fileName or getFileName(url, r)
        with open(fileName, 'wb') as (f):
            shutil.copyfileobj(r, f)
    finally:
        r.close()


def extract_egg(source_path, destination_path):
    zipfile = ZipFile(source_path)
    zipfile.extractall(destination_path)
    zipfile.close()
    os.unlink(source_path)