# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_seatbelt/seatbelt.py
# Compiled at: 2011-07-05 10:31:21
import contextlib, sys

@contextlib.contextmanager
def fasten(allow_callbacks=None):
    """
    Fasten seatbelts for production.

    With this context manager sys.path will not contain any unwanted junk that
    users happily stick into /usr/local/ and other similar places just a moment
    before calling you to report your application is broken.
    """
    orig_sys_path = sys.path
    sys.path = _filtered_sys_path(allow_callbacks)
    try:
        yield
    finally:
        sys.path = orig_sys_path


def solder(allow_callbacks=None):
    """
    Solder seatbelts for production.

    Like fasten() but without the context manager. That is, the original
    sys.path is never restored. This is perfect for your .wsgi files.
    """
    sys.path = _filtered_sys_path(allow_callbacks)


def _filtered_sys_path(allow_callbacks=None):
    """
    Calculate how sys.path should look like as filtered by the provided
    white-list callbacks.

    :param allow_callbacks:
        List of white-list call-backs that check if a particular path entry is
        permitted or not. If left empty then default of
        :ref:`django_seatbelt.allow_callbacks:DEFAULT_ALLOW_CALLBACKS` is used

    :return:
        The new sys.path (the actual sys.path is not modified)
    """
    if allow_callbacks is None:
        from django_seatbelt.allow_callbacks import DEFAULT_ALLOW_CALLBACKS
        allow_callbacks = DEFAULT_ALLOW_CALLBACKS
    filtered_sys_path = []
    for path in sys.path:
        if any(is_allowed(path) for is_allowed in allow_callbacks):
            filtered_sys_path.append(path)

    return filtered_sys_path