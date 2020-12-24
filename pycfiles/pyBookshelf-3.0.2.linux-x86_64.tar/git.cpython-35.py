# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/bookshelf/api_v2/git.py
# Compiled at: 2016-08-21 18:37:21
# Size of source mod 2**32: 892 bytes
from fabric.api import sudo, run
from fabric.context_managers import cd
from fabric.contrib.files import exists

def install_recent_git_from_source(version='2.4.6', prefix='/usr/local', log=False):
    sudo('wget -c https://www.kernel.org/pub/software/scm/git/git-%s.tar.gz' % version)
    sudo('test -e git-%s || tar -zxf git-%s.tar.gz' % (version, version))
    with cd('git-%s' % version):
        sudo('test -e %s/bin/git || ./configure --prefix=%s' % (prefix, prefix))
        sudo('test -e %s/bin/git || make' % prefix)
        sudo('test -e %s/bin/git || make install' % prefix)


def git_clone(repo_url, repo_name):
    """ clones a git repository """
    if not exists(repo_name):
        run('git clone %s' % repo_url)