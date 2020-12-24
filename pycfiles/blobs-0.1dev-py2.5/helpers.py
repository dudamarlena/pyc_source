# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/blobs/helpers.py
# Compiled at: 2008-02-19 12:19:12
"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *
import datetime, re, os, logging, shutil
from pylons import config
log = logging.getLogger(__name__)
now = datetime.datetime.now

def getBlobPath(hash):
    if not re.match('^[a-f0-9]{40}$', hash):
        assert ValueError('Invalid hash')
    path = os.path.join(config['app_conf']['blobs.data_dir'], 'blobs', hash[0], hash[1], hash)
    return path


def saveBlob(hash, data):
    dest = getBlobPath(hash)
    destDir = os.path.dirname(dest)
    log.info('Saving to %s', dest)
    if not os.path.exists(destDir):
        os.makedirs(destDir)
    dst = open(dest, 'w')
    if type(data) in (str, unicode):
        dst.write(data)
    elif hasattr(data, 'read'):
        shutil.copyfileobj(data, dst)
    else:
        raise TypeError("Don't know how to save blob of type %s" % type(data))