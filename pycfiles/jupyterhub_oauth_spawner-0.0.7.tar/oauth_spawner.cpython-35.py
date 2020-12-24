# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/diogo.munaro/workspace/jupyterhub_oauth_spawner/jupyterhub_oauth_spawner/oauth_spawner.py
# Compiled at: 2017-01-30 14:10:50
# Size of source mod 2**32: 1768 bytes
from jupyterhub.spawner import LocalProcessSpawner
from traitlets import Any
from tornado import gen

class OAuthSpawner(LocalProcessSpawner):
    __doc__ = 'Local spawner that runs single-user servers as the same user as the Hub itself.\n\n    Overrides user-specific env setup with no-ops.\n    '
    pre_start_hook = Any(None, config=True, help='Python callable thereof\n        to be called before the start of jupyter notebook.\n        ')
    post_start_hook = Any(None, config=True, help='Python callable thereof\n        to be called after the start of jupyter notebook.\n        ')
    pre_stop_hook = Any(None, config=True, help='Python callable thereof\n        to be called before the stop of jupyter notebook.\n        ')
    post_stop_hook = Any(None, config=True, help='Python callable thereof\n        to be called after the stop of jupyter notebook.\n        ')

    def make_preexec_fn(self, name):
        """no-op to avoid setuid"""
        pass

    def user_env(self, env):
        """no-op to avoid setting HOME dir, etc."""
        env['USER'] = self.user.name
        return env

    @gen.coroutine
    def start(self):
        if self.pre_start_hook:
            self.pre_start_hook(self.user, 'pre_start_hook')
        super(OAuthSpawner, self).start()
        if self.post_start_hook:
            self.post_start_hook(self.user, 'post_start_hook')
        return (
         self.ip or '127.0.0.1', self.port)

    @gen.coroutine
    def stop(self, now=False):
        if self.pre_stop_hook:
            self.pre_stop_hook(self.user, 'pre_stop_hook')
        super(OAuthSpawner, self).stop(now)
        if self.post_stop_hook:
            self.post_stop_hook(self.user, 'post_stop_hook')