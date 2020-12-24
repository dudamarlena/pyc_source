# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/harley/projects/django-fab/examples/fabfile-git.py
# Compiled at: 2009-09-21 23:27:53
from djangofab.api import *
from djangofab.vcs.git import update_remote, update_local, push, commit, add
env.capture_default = False
apply_settings()

@user_settings()
def prod():
    """Production settings"""
    env.hosts = [
     'server1']
    env.path = '%(prod_path)s'
    env.giturl = '%(giturl)s'
    env.site_user = 'owner'
    env.site_group = 'group'


@user_settings()
def dev():
    """Development settings"""
    env.hosts = [
     'server1']
    env.path = '%(dev_path)s'
    env.giturl = '%(giturl)s'
    env.site_user = 'owner'
    env.site_group = 'group'


@user_settings('fab.cfg', 'local')
def localhost():
    """Local settings"""
    env.path = '%(dev_path)s'
    env.giturl = '%(giturl)s'


def deploy():
    """Push local changes and update checkout on the remote host"""
    push()
    update_remote()
    change_ownership()
    touch_wsgi()


def test():
    print 'website using database %s ' % (settings.DATABASE_NAME,)