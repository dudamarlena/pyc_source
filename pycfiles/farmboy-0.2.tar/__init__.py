# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/termie/p/devacuda/contrail/farmboy/files/__init__.py
# Compiled at: 2013-11-19 19:21:09
import errno, os, pkg_resources
from fabric.api import env
from fabric.api import local
from fabric.api import puts
from fabric.api import task

def _makedir(p):
    try:
        os.mkdir(p)
        puts('[files] Making directory: %s' % p)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(p):
            pass


@task
def init(force=False):
    """Copy the template files to the local directory for easy modification."""
    _makedir('./files')
    top_level = pkg_resources.resource_listdir(__name__, '')
    for path in top_level:
        if not pkg_resources.resource_isdir(__name__, path):
            continue
        _makedir('./files/%s' % path)
        for sub in pkg_resources.resource_listdir(__name__, path):
            new_path = './files/%s/%s' % (path, sub)
            if not force and os.path.exists(new_path):
                continue
            old_path = pkg_resources.resource_filename(__name__, '%s/%s' % (path, sub))
            local('cp %s %s' % (old_path, new_path))