# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/app/_default_app.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 2422 bytes
from .application import Application
default_app = None

def use_app(backend_name=None, call_reuse=True):
    """ Get/create the default Application object

    It is safe to call this function multiple times, as long as
    backend_name is None or matches the already selected backend.

    Parameters
    ----------
    backend_name : str | None
        The name of the backend application to use. If not specified, Vispy
        tries to select a backend automatically. See ``vispy.use()`` for
        details.
    call_reuse : bool
        Whether to call the backend's `reuse()` function (True by default).
        Not implemented by default, but some backends need it. For example,
        the notebook backends need to inject some JavaScript in a notebook as
        soon as `use_app()` is called.

    """
    global default_app
    if default_app is not None:
        names = default_app.backend_name.lower().replace('(', ' ').strip(') ')
        names = [name for name in names.split(' ') if name]
        if backend_name and backend_name.lower() not in names:
            raise RuntimeError('Can only select a backend once, already using %s.' % names)
        else:
            if call_reuse:
                default_app.reuse()
            return default_app
        default_app = Application(backend_name)
        return default_app


def create():
    """Create the native application.
    """
    use_app(call_reuse=False)
    return default_app.create()


def run():
    """Enter the native GUI event loop.
    """
    use_app(call_reuse=False)
    return default_app.run()


def quit():
    """Quit the native GUI event loop.
    """
    use_app(call_reuse=False)
    return default_app.quit()


def process_events():
    """Process all pending GUI events

    If the mainloop is not running, this should be done regularly to
    keep the visualization interactive and to keep the event system going.
    """
    use_app(call_reuse=False)
    return default_app.process_events()