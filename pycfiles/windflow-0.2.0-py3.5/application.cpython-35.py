# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/windflow/web/application.py
# Compiled at: 2018-04-18 11:33:58
# Size of source mod 2**32: 1048 bytes
import tornado.web, os.path

class ApplicationFactory:
    __doc__ = '\n    TODO change this, the API does not feel good.\n\n    XXX API will change\n    '

    def __init__(self, factory=tornado.web.Application):
        self.factory = factory
        self.mounts = []
        self.configured = False

    def configure(self, configurator=None):
        self.configured = True
        configured = None
        if configurator:
            configured = configurator(self) or configured
        return configured or self

    def mount(self, prefix, config):
        self.mounts.append((prefix, config))
        return self

    def __call__(self, *args, **kwargs):
        if not self.configured:
            return self.configure(*args, **kwargs)
        app = self.factory(*args, **kwargs)
        for prefix, config in reversed(self.mounts):
            app.add_handlers('.*$', [(os.path.join(prefix, handler[0].lstrip('/')), *handler[1:]) for handler in config.get_handlers()])

        return app