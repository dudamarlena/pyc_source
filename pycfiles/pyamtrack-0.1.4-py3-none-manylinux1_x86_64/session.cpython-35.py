# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/session.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 3533 bytes
__doc__ = 'PyAMS_utils session module\n\nThis helper module is used to add a "session_property" method decorator, which can be used to\nstore method result into user\'s session.\n\nIt also adds to function to get and set session data.\n'
from pyams_utils.request import check_request
__docformat__ = 'restructuredtext'

def get_session_data(request, app, key, default=None):
    """Get data associated with current user session

    PyAMS session management is based on :py:mod:`Beaker` package session management.

    :param request: the request from which session is extracted
    :param str app: application name
    :param str key: session data key for given application
    :param default: object; requested session data, or *default* if it can't be found

    .. code-block:: python

        APPLICATION_KEY = 'MyApp'
        SESSION_KEY = 'MyFunction'

        def my_function(request):
            return get_session_data(request, APPLICATION_KEY, SESSION_KEY)
    """
    session = request.session
    return session.get('{0}::{1}'.format(app, key), default)


def set_session_data(request, app, key, value):
    """Associate data with current user session

    :param request: the request from which session is extracted
    :param str app: application name
    :param str key: session data key for given application
    :param object value: any object that can be pickled can be stored into user session

    .. code-block:: python

        APPLICATION_KEY = 'MyApp'
        SESSION_KEY = 'MyFunction'

        def my_function(request):
            value = {'key1': 'value1', 'key2': 'value2'}
            set_session_data(request, APPLICATION_KEY, SESSION_KEY, value)
    """
    session = request.session
    session['{0}::{1}'.format(app, key)] = value


_MARKER = object()

def session_property(app, key=None, prefix=None):
    """Define a method decorator used to store result into request's session

    If no request is currently running, a new one is created.

    :param str app: application identifier used to prefix session keys
    :param str key: session's value key; if *None*, the key will be the method's object; if *key*
        is a callable object, il will be called to get the actual session key
    :param prefix: str; prefix to use for session key; if *None*, the prefix will be the property
        name
    """

    def session_decorator(func):

        def wrapper(obj, app, key, *args, **kwargs):
            request = check_request()
            if callable(key):
                key = key(obj, *args, **kwargs)
            if not key:
                key = '{1}::{0!r}'.format(obj, prefix or func.__name__)
            data = get_session_data(request, app, key, _MARKER)
            if data is _MARKER:
                data = func
                if callable(data):
                    data = data(obj, *args, **kwargs)
                set_session_data(request, app, key, data)
            return data

        return lambda *args, x, **args: wrapper(x, app, key, *args, **kwargs)

    return session_decorator