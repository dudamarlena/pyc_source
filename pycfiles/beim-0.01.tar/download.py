# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/linjiao/dv/beim/beim/installers/download.py
# Compiled at: 2013-12-08 21:45:16


def download_cmd(link):
    if link.startswith('http:') or link.startswith('ftp:'):
        return ['wget %s' % link]
    if link.startswith('svn:'):
        return download_using_svn(link)
    raise NotImplementedError


def download_using_svn(link):
    import tempfile
    tempdir = tempfile.mkdtemp()
    import os
    path, filename = os.path.split(link)
    dirname = os.path.split(path)[(-1)]
    cmds = [
     'tempvar_current_path=$PWD',
     'cd %s' % tempdir,
     'svn co -N %s' % path,
     'cd %s' % dirname,
     'svn up %s' % filename,
     'mv %s $tempvar_current_path' % filename,
     'cd $tempvar_current_path',
     'rm -rf %s' % tempdir]
    return cmds


__id__ = '$Id$'