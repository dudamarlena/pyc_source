# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/app/application.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 9052 bytes
"""
Implements the global singleton app object.

"""
from __future__ import division
import os, sys
from . import backends, inputhook
from .backends import CORE_BACKENDS, BACKEND_NAMES, BACKENDMAP, TRIED_BACKENDS
from .. import config
from .base import BaseApplicationBackend as ApplicationBackend
from ..util import logger
from ..ext import six

class Application(object):
    __doc__ = 'Representation of the vispy application\n\n    This wraps a native GUI application instance. Vispy has a default\n    instance of this class that can be created/obtained via\n    `vispy.app.use_app()`.\n\n    Parameters\n    ----------\n    backend_name : str | None\n        The name of the backend application to use. If not specified,\n        Vispy tries to select a backend automatically. See ``vispy.use()``\n        for details.\n\n    Notes\n    -----\n    Upon creating an Application object, a backend is selected, but the\n    native backend application object is only created when `create()`\n    is called or `native` is used. The Canvas and Timer do this\n    automatically.\n\n    '

    def __init__(self, backend_name=None):
        self._backend_module = None
        self._backend = None
        self._use(backend_name)

    def __repr__(self):
        name = self.backend_name
        if not name:
            return '<Vispy app with no backend>'
        else:
            return '<Vispy app, wrapping the %s GUI toolkit>' % name

    @property
    def backend_name(self):
        """ The name of the GUI backend that this app wraps.
        """
        if self._backend is not None:
            return self._backend._vispy_get_backend_name()
        else:
            return ''

    @property
    def backend_module(self):
        """ The module object that defines the backend.
        """
        return self._backend_module

    def process_events(self):
        """ Process all pending GUI events. If the mainloop is not
        running, this should be done regularly to keep the visualization
        interactive and to keep the event system going.
        """
        return self._backend._vispy_process_events()

    def sleep(self, duration_sec):
        """ Sleep for the given duration in seconds.

        This is used to reduce
        CPU stress when VisPy is run in interactive mode.
        see inputhook.py for details

        Parameters
        ----------
        duration_sec: float
            Time to sleep in seconds
        """
        self._backend._vispy_sleep(duration_sec)

    def create(self):
        """ Create the native application.
        """
        self.native

    def is_interactive(self):
        """ Determine if the user requested interactive mode.
        """
        if sys.flags.interactive:
            return True
        if '__IPYTHON__' not in dir(six.moves.builtins):
            return False
        try:
            from IPython.config.application import Application as App
            return App.initialized() and App.instance().interact
        except (ImportError, AttributeError):
            return False

    def run(self, allow_interactive=True):
        """ Enter the native GUI event loop.

        Parameters
        ----------
        allow_interactive : bool
            Is the application allowed to handle interactive mode for console
            terminals?  By default, typing ``python -i main.py`` results in
            an interactive shell that also regularly calls the VisPy event
            loop.  In this specific case, the run() function will terminate
            immediately and rely on the interpreter's input loop to be run
            after script execution.
        """
        if allow_interactive and self.is_interactive():
            inputhook.set_interactive(enabled=True, app=self)
        else:
            return self._backend._vispy_run()

    def reuse(self):
        """ Called when the application is reused in an interactive session.
        This allow the backend to do stuff in the client when `use_app()` is
        called multiple times by the user. For example, the notebook backends
        need to inject JavaScript code as soon as `use_app()` is called.
        """
        return self._backend._vispy_reuse()

    def quit(self):
        """ Quit the native GUI event loop.
        """
        return self._backend._vispy_quit()

    @property
    def native(self):
        """ The native GUI application instance.
        """
        return self._backend._vispy_get_native_app()

    def _use(self, backend_name=None):
        """Select a backend by name. See class docstring for details.
        """
        test_name = os.getenv('_VISPY_TESTING_APP', None)
        if backend_name is not None:
            if backend_name.lower() == 'default':
                backend_name = None
            elif backend_name.lower() not in BACKENDMAP:
                raise ValueError('backend_name must be one of %s or None, not %r' % (
                 BACKEND_NAMES, backend_name))
        elif test_name is not None:
            backend_name = test_name.lower()
        assert backend_name in BACKENDMAP
        try_others = backend_name is None
        imported_toolkits = []
        backends_to_try = []
        if not try_others:
            assert backend_name.lower() in BACKENDMAP.keys()
            backends_to_try.append(backend_name.lower())
        else:
            for name, module_name, native_module_name in CORE_BACKENDS:
                if native_module_name and native_module_name in sys.modules:
                    imported_toolkits.append(name.lower())
                    backends_to_try.append(name.lower())

            default_backend = config['default_backend'].lower()
            if default_backend.lower() in BACKENDMAP.keys() and default_backend not in backends_to_try:
                backends_to_try.append(default_backend)
            for name, module_name, native_module_name in CORE_BACKENDS:
                name = name.lower()
                if name not in backends_to_try:
                    backends_to_try.append(name)

        for key in backends_to_try:
            name, module_name, native_module_name = BACKENDMAP[key]
            TRIED_BACKENDS.append(name)
            mod_name = 'backends.' + module_name
            __import__(mod_name, globals(), level=1)
            mod = getattr(backends, module_name)
            if not mod.available:
                msg = 'Could not import backend "%s":\n%s' % (
                 name, str(mod.why_not))
                if not try_others:
                    raise RuntimeError(msg)
                else:
                    if key in imported_toolkits:
                        msg = 'Although %s is already imported, the %s backend could not\nbe used ("%s"). \nNote that running multiple GUI toolkits simultaneously can cause side effects.' % (
                         native_module_name, name, str(mod.why_not))
                        logger.warning(msg)
                    else:
                        logger.info(msg)
            else:
                self._backend_module = mod
                logger.debug('Selected backend %s' % module_name)
                break
        else:
            raise RuntimeError('Could not import any of the backends. You need to install any of %s. We recommend PyQt' % [b[0] for b in CORE_BACKENDS])

        self._backend = self.backend_module.ApplicationBackend()