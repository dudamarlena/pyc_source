# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/gunicorn/gunicorn/app/wsgiapp.py
# Compiled at: 2019-02-14 00:35:18
import os
from gunicorn.errors import ConfigError
from gunicorn.app.base import Application
from gunicorn import util

class WSGIApplication(Application):

    def init(self, parser, opts, args):
        if opts.paste:
            app_name = 'main'
            path = opts.paste
            if '#' in path:
                path, app_name = path.split('#')
            path = os.path.abspath(os.path.normpath(os.path.join(util.getcwd(), path)))
            if not os.path.exists(path):
                raise ConfigError('%r not found' % path)
            self.cfgurl = 'config:%s#%s' % (path, app_name)
            self.relpath = os.path.dirname(path)
            from .pasterapp import paste_config
            return paste_config(self.cfg, self.cfgurl, self.relpath)
        if len(args) < 1:
            parser.error('No application module specified.')
        self.cfg.set('default_proc_name', args[0])
        self.app_uri = args[0]

    def load_wsgiapp(self):
        return util.import_app(self.app_uri)

    def load_pasteapp(self):
        from .pasterapp import load_pasteapp
        return load_pasteapp(self.cfgurl, self.relpath, global_conf=self.cfg.paste_global_conf)

    def load(self):
        if self.cfg.paste is not None:
            return self.load_pasteapp()
        else:
            return self.load_wsgiapp()
            return


def run():
    """    The ``gunicorn`` command line runner for launching Gunicorn with
    generic WSGI applications.
    """
    from gunicorn.app.wsgiapp import WSGIApplication
    WSGIApplication('%(prog)s [OPTIONS] [APP_MODULE]').run()


if __name__ == '__main__':
    run()