# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\tools\extension_dependency.py
# Compiled at: 2020-05-08 11:04:15
# Size of source mod 2**32: 1267 bytes
import functools
from reapy.errors import ExtensionNotFoundError

def depends_on_extension(extension, url):
    """Return a decorator to indicate dependency to an extension.

    If the extension is not available, an `ExtensionNotFoundError`
    will be raised when calling the decorated function.

    Parameters
    ----------
    extension : str
        Extension name.
    url : str
        URL of the download page or installation instructions of
        the extension.
    """
    message = "module 'reapy.reascript_api' has no attribute"

    def decorator(f):

        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except AttributeError as exc:
                try:
                    if exc.args[0].startswith(message):
                        raise ExtensionNotFoundError(extension, url)
                    else:
                        raise exc
                finally:
                    exc = None
                    del exc

        return wrapped

    return decorator


depends_on_sws = depends_on_extension('SWS', 'www.sws-extension.org')