# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/greins/app.py
# Compiled at: 2011-10-12 00:10:32
import glob, inspect, logging, os.path, sys, textwrap, traceback
from gunicorn.app.wsgiapp import WSGIApplication
from gunicorn.config import make_settings
from gunicorn.util import import_app
from greins.reloader import Reloader
from greins.router import Router
from greins.synchronization import synchronized

class GreinsApplication(WSGIApplication):
    synchronize_hooks = synchronized('_hooks_lock')

    def init(self, parser, opts, args):
        if len(args) != 1:
            parser.error('No configuration directory specified.')
        if not os.path.isdir(args[0]):
            parser.error('APP_DIR must refer to an existing directory.')
        self.cfg.set('default_proc_name', parser.get_prog_name())
        self.app_dir = os.path.abspath(args[0])
        self.logger = logging.getLogger('gunicorn.error')
        self._use_reloader = opts.reloader
        self._hooks = {}
        self._hooks_lock = None
        return

    def setup_hooks(self):
        """
        Set up server hook proxies

        Rather than explicitly referring to defined Gunicorn server hooks,
        which may change in future versions of Gunicorn, take configuration
        settings from gunicorn.config.make_settings().

        For each setting in the "Server Hooks" category, create a proxy
        function (with matching arity in order to pass validation), which
        calls the hook for every loaded app that defines it.
        """
        hook_proxy_template = textwrap.dedent('\n        def proxy%(spec)s:\n            greins._do_hook(name, %(spec)s)\n        ')
        for name, obj in make_settings().items():
            if obj.section == 'Server Hooks':
                self._hooks[name] = {'handlers': [], 'validator': obj.validator}
                spec = inspect.formatargspec(*inspect.getargspec(obj.default))
                proxy_env = {'greins': self, 
                   'name': name}
                exec hook_proxy_template % {'spec': spec} in proxy_env
                self.cfg.set(name, proxy_env['proxy'])

    def load_file(self, cf):
        cf_name = os.path.splitext(os.path.basename(cf))[0]
        cfg = {'__builtins__': __builtins__, 
           '__name__': '__config__', 
           '__file__': os.path.abspath(cf), 
           '__doc__': None, 
           '__package__': None, 
           'mounts': {}}
        try:
            self.logger.info('Loading configuration for %s' % cf_name)
            execfile(cf, cfg, cfg)
            if not cfg['mounts']:
                app_name, ext = os.path.splitext(os.path.basename(cf))
                cfg['mounts']['/' + app_name] = import_app(app_name)
            for r, a in cfg['mounts'].iteritems():

                def wrap(app):

                    def app_with_env(env, start_response):
                        return app(env, start_response)

                    app_with_env.__name__ = app.__name__
                    return app_with_env

                wrapped = wrap(a)
                if not r.startswith('/'):
                    self.logger.warning("Adding leading '/' to '%s'" % r)
                    r = '/' + r
                if self._router.add_mount(r, wrapped) != wrapped:
                    self.logger.error("Found conflicting routes for '%s'" % r)
                    sys.exit(1)

            self._setup_hooks(cfg)
        except Exception as e:
            if self._use_reloader:
                for fname, _, _, _ in traceback.extract_tb(sys.exc_info()[2]):
                    self._reloader.add_extra_file(fname)

                if isinstance(e, SyntaxError):
                    self._reloader.add_extra_file(e.filename)
            self.logger.exception('Exception reading config for %s:' % cf_name)

        return

    def load(self):
        import threading
        self._router = Router()
        self._hooks_lock = threading.RLock()
        self.setup_hooks()
        if self._use_reloader:
            self._reloader = Reloader()
            self._reloader.start()
        for cf in glob.glob(os.path.join(self.app_dir, '*.py')):
            if self._use_reloader:
                self._reloader.add_extra_file(cf)
            t = threading.Thread(target=self.load_file, args=[cf])
            t.start()

        self.logger.info('Greins booted successfully.')
        self.logger.debug('Routes:\n%s' % self._router)
        return self._router

    @synchronize_hooks
    def _setup_hooks(self, cfg):
        for name, hook in self._hooks.items():
            handler = cfg.get(name)
            if handler:
                hook['validator'](handler)
                hook['handlers'].append(handler)

    @synchronize_hooks
    def _do_hook(self, name, argtuple):
        for handler in self._hooks[name]['handlers']:
            handler(*argtuple)


def run():
    """    The ``greins`` command line runner for launching Gunicorn with
    a greins configuration directory.
    """
    from greins.app import GreinsApplication
    GreinsApplication('%prog [OPTIONS] APP_DIR').run()