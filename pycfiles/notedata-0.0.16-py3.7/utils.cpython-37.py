# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notedata/utils.py
# Compiled at: 2019-06-12 04:57:09
# Size of source mod 2**32: 1104 bytes
import logging, os, pycurl
logger = logging.getLogger(__name__)
__all__ = [
 'utils']
data_root = '/content/tmp/'
raw_root = 'https://raw.githubusercontent.com/1007530194/data/master/'

def download_file(url, path, overwrite=False):
    if exists(path, overwrite=overwrite):
        return
    logger.info('downloading from ' + url + ' to ' + path)
    with open(path, 'wb') as (f):
        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.WRITEDATA, f)
        c.perform()
        c.close()
        logger.info('download success')


def exists(path, overwrite=False):
    filename = os.path.basename(path)
    if os.path.exists(path):
        if overwrite:
            logger.info('file:{} exists, overwrite it'.format(filename))
            os.remove(path)
            return False
        logger.info('file:{} exists, return'.format(filename))
        return True
    return False