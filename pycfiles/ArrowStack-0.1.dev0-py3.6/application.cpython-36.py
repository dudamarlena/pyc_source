# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arrow/application.py
# Compiled at: 2018-09-04 05:00:20
# Size of source mod 2**32: 789 bytes
from __future__ import unicode_literals
import multiprocessing, gunicorn.app.base
from gunicorn.six import iteritems

def number_of_workers():
    return multiprocessing.cpu_count() * 2 + 1


class Application(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.options['workers'] = number_of_workers()
        self.application = app
        super(Application, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options) if key in self.cfg.settings if value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application