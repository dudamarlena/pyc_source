# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fabric_deploy/strategy.py
# Compiled at: 2012-07-29 23:54:37
from __future__ import with_statement
import sys, os
from fabric.api import *
from fabric.decorators import *
from fabric.contrib import project
from fabric.tasks import Task

def fetch(key, default_val=None):
    import options
    return options.fetch(key, default_val)


class Strategy(object):

    def deploy(self, *args, **kwargs):
        raise NotImplementedError()

    def _remote_cache_subdir(self, cached_path):
        deploy_subdir = fetch('deploy_subdir')
        if deploy_subdir is not None:
            while 0 < len(deploy_subdir) and deploy_subdir.startswith('/'):
                deploy_subdir = deploy_subdir[1:]

            cached_path = os.path.join(cached_path, deploy_subdir)
        return cached_path


class CheckoutStrategy(Strategy):

    def deploy(self):
        run(self.command() + '&&' + self.mark())

    def command(self):
        source = fetch('source')
        revision = fetch('revision')
        destination = fetch('release_path')
        return source.checkout(revision, destination, perform_fetch=False)

    def mark(self):
        kwargs = {'release_path': fetch('release_path'), 
           'revision': fetch('revision')}
        return 'echo %(revision)s > %(release_path)s/REVISION' % kwargs

    def __str__(self):
        return 'checkout'


class LocalCacheStrategy(Strategy):

    def deploy(self):
        cached_path = fetch('cached_path')
        if cached_path is None:
            abort('cached_path is None')
        source = fetch('source')
        revision = fetch('revision')
        local_repository = source.repository_path(os.path.realpath('.'))
        project.rsync_project(local_dir=local_repository + os.path.sep, remote_dir=cached_path, delete=True)
        run(source.checkout(revision, cached_path, perform_fetch=False))
        latest_release = fetch('latest_release')
        run('\n      rsync -lrpt --chmod=Du+rwx,Dgo+rx,Fu+rw,Fgo+r %(cached_path)s/* %(latest_release)s && (echo %(revision)s > %(release_path)s/REVISION)\n    ' % dict(cached_path=self._remote_cache_subdir(cached_path), latest_release=latest_release, revision=revision, release_path=fetch('release_path')))
        return

    def __str__(self):
        return 'local_cache'


class RemoteCacheStrategy(Strategy):

    def deploy(self):
        cached_path = fetch('cached_path')
        if cached_path is None:
            abort('cached_path is None')
        source = fetch('source')
        revision = fetch('revision')
        run(source.checkout(revision, cached_path))
        latest_release = fetch('latest_release')
        run('\n      rsync -lrpt --chmod=Du+rwx,Dgo+rx,Fu+rw,Fgo+r %(cached_path)s/* %(latest_release)s && (echo %(revision)s > %(release_path)s/REVISION)\n    ' % dict(cached_path=self._remote_cache_subdir(cached_path), latest_release=latest_release, revision=revision, release_path=fetch('release_path')))
        return

    def __str__(self):
        return 'remote_cache'