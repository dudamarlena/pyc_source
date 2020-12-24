# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/eggproxy/update_script.py
# Compiled at: 2008-09-22 04:57:28
import os
from os.path import getmtime
from time import time
from iw.eggproxy import eggs_index_proxy
from iw.eggproxy import PackageNotFound
from iw.eggproxy.config import config, EGGS_DIR
UPDATE_INTERVAL = int(config.get('default', 'update_interval')) * 3600
TIME_LIMIT = int(time()) - UPDATE_INTERVAL

def isOutDated(file_path):
    """A file is outdated if it does not exists or if its modification date is
    older than now - update_interval
    """
    if os.path.exists(file_path):
        mtime = getmtime(file_path)
        return mtime < TIME_LIMIT
    return True


def updateCache(*args):
    """
    """
    isDir = os.path.isdir
    pathJoin = os.path.join
    update = False
    index_file = pathJoin(EGGS_DIR, 'index.html')
    if isOutDated(index_file):
        eggs_index_proxy.updateBaseIndex()
    for package_name in os.listdir(EGGS_DIR):
        dir_path = pathJoin(EGGS_DIR, package_name)
        if not isDir(dir_path):
            continue
        index_file = pathJoin(dir_path, 'index.html')
        if isOutDated(index_file):
            try:
                eggs_index_proxy.updatePackageIndex(package_name)
            except PackageNotFound, msg:
                print msg