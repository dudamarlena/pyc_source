# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/dispatch.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = '\n\n  dispatch\n  ~~~~~~~~\n\n  WSGI dispatch entrypoint. INCEPTION.\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n'
import os
app = None

def spawn(app, config=None):
    """ Spawn a Canteen app, suitable for dispatch
      as a WSGI application.

      :param app: Canteen application to be spawned,
        usually passed as a Python module.

      :param config: Application configuration, in
        the form of a ``canteen.util.Config`` instance
        wrapping a dictionary of application config.

      :returns: Instance of ``canteen.Runtime`` that
        can be dispatched via WSGI and wraps the target
        ``app`` object.  """
    from canteen.core import runtime
    from canteen.util import config as cfg
    if not config:
        config = cfg.Config()
    return runtime.Runtime.spawn(app).configure(config)


def run(app=None, interface='127.0.0.1', port=8080, dev=True, config=None):
    """ Run a lightweight development server via the
      currently-active runtime. Suitable for use
      locally, with no required parameters at all.

      :param app: Canteen application to be spawned,
        usually passed as a Python module.

      :param root: Unused. No fucking clue what this
        is but I'd guess it's the root filepath to the
        application. I hope it's not that, though,
        because that would break App Engine.

      :param interface: Network interface that should
        be bound to for the resulting lightweight HTTP
        server. Defaults to ``127.0.0.1``.

      :param port: Integer port number that should be
        bound to for the resulting lightweight HTTP
        server. Defaults to ``8080``.

      :param dev: Boolean flag indicating whether we
        should be running in debug mode or not. Controls
        various things like log output. Defaults to
        ``True`` as this method is only meant to be an
        easy way to put up a dev server.

      :returns: Nothing useful, as this blocks to
        serve requests forever and ever. """
    if 'CANTEEN_TESTING' in os.environ and os.environ['CANTEEN_TESTING'] in ('yep',
                                                                             '1',
                                                                             'sure',
                                                                             'ofcourse',
                                                                             'whynot',
                                                                             'yes',
                                                                             'on'):
        return spawn(app, config or {})
    return spawn(app, config or {}).serve(interface, port)