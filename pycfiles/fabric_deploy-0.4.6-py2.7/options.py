# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fabric_deploy/options.py
# Compiled at: 2012-07-29 23:54:37
from __future__ import with_statement
import sys, os
from fabric.api import *
from fabric.decorators import *
import logging, time, scm, strategy

def fetch(key, default_val=None):
    val = env.get(key)
    if hasattr(val, '__call__'):
        val = val()
        set(key, val)
    if val is None:
        return default_val
    else:
        return val


def set(key, val=None):
    env[key] = val


def cset(key, val=None):
    if fetch(key) is None:
        set(key, val)
    return


cset('scm', 'git')
cset('application', 'app')
cset('repository', 'git@git:app.git')
cset('branch', 'master')
cset('remote', 'origin')
cset('git_enable_submodules', False)
cset('deploy_to', lambda : '/u/apps/%(name)s' % dict(name=fetch('application')))
cset('shared_path', lambda : '%(dir)s/shared' % dict(dir=fetch('deploy_to')))
cset('current_path', lambda : '%(dir)s/current' % dict(dir=fetch('deploy_to')))
cset('releases_path', lambda : '%(dir)s/releases' % dict(dir=fetch('deploy_to')))
cset('release_name', lambda : time.strftime('%Y%m%d%H%M%S'))
cset('release_path', lambda : '%(dir)s/%(name)s' % dict(dir=fetch('releases_path'), name=fetch('release_name')))
cset('latest_release', lambda : fetch('release_path'))
cset('releases', lambda : _get_releases())
cset('previous_release', lambda : _get_previous_release())
cset('current_release', lambda : _get_current_release())
cset('keep_releases', 5)
cset('cached_path', lambda : '%(dir)s/cached-copy' % dict(dir=fetch('shared_path')))

@task
@roles('app')
@runs_once
def _get_releases():
    releases = run('ls %(releases_path)s' % dict(releases_path=fetch('releases_path'))).split()
    releases.sort()
    return releases


@task
@roles('app')
@runs_once
def _get_previous_release():
    releases = fetch('releases')
    releases_path = fetch('releases_path')
    if 0 < len(releases):
        return os.path.join(releases_path, releases[(-2)])


@task
@roles('app')
@runs_once
def _get_current_release():
    releases = fetch('releases')
    releases_path = fetch('releases_path')
    if 0 < len(releases):
        return os.path.join(releases_path, releases[(-1)])


source_table = {'git': scm.Git, 
   'mercurial': scm.Mercurial}
cset('source', lambda : source_table.get(fetch('scm'))())
cset('revision', lambda : fetch('source').head())
cset('deploy_via', 'local_cache')
strategy_table = {'local_cache': strategy.LocalCacheStrategy, 
   'checkout': strategy.CheckoutStrategy}
cset('strategy', lambda : strategy_table.get(fetch('deploy_via'))())
set('user', 'deploy')
cset('runner', 'app')
cset('virtualenv', lambda : '%(dir)s/virtualenv' % dict(dir=fetch('shared_path')))
cset('pybundle_path', lambda : '/tmp/%(name)s.pybundle' % dict(name=fetch('application')))
cset('service_name', lambda : fetch('application'))
cset('maintenance_basename', 'maintenance')