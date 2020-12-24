# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/anaconda3/lib/python3.6/site-packages/vnlp/utils/files.py
# Compiled at: 2018-06-21 18:30:13
# Size of source mod 2**32: 472 bytes
import os, logging, requests

def download(url, fname, skip_if_exists=True, chunk_size=1024):
    """
    Downloads a file from an URL.
    """
    if os.path.isfile(fname):
        if skip_if_exists:
            return
    logging.info('Downloading from {} to {}'.format(url, fname))
    r = requests.get(url, stream=True)
    with open(fname, 'wb') as (f):
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)