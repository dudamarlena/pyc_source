# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sovereign/server.py
# Compiled at: 2020-04-29 02:35:50
# Size of source mod 2**32: 664 bytes
import gunicorn.app.base
from sovereign import asgi_config
import sovereign.app as app

class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, application, options=None):
        self.options = options or {}
        self.application = application
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def main():
    asgi = StandaloneApplication(application=app,
      options=(asgi_config.as_gunicorn_conf()))
    asgi.run()


if __name__ == '__main__':
    main()