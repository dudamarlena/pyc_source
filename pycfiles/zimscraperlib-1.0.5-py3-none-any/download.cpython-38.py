# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/zimscraperlib/src/zimscraperlib/download.py
# Compiled at: 2020-02-03 10:50:32
# Size of source mod 2**32: 817 bytes
import os, subprocess, requests
WGET_BINARY = os.getenv('WGET_BINARY', '/usr/bin/wget')

def save_file(url, fpath):
    """ download a binary file from its URL """
    req = requests.get(url)
    req.raise_for_status()
    if not fpath.parent.exists():
        fpath.parent.mkdir(exist_ok=True)
    with open(fpath, 'wb') as (fp):
        fp.write(req.content)


def save_large_file(url, fpath):
    """ download a binary file from its URL, using wget """
    subprocess.run([
     WGET_BINARY,
     '-t',
     '5',
     '--retry-connrefused',
     '--random-wait',
     '-O',
     str(fpath),
     '-c',
     url],
      check=True)