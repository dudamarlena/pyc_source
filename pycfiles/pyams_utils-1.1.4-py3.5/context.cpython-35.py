# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/context.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 2800 bytes
"""PyAMS_utils.context module

This module provides a "context" selector which can be used as Pyramid's subscriber
predicate. Matching argument can be a class or an interface: for subscriber to be actually called,
subscriber's argument should inherit from it (if it's a class) or implement it (if it's an
interface).
"""
import sys
from contextlib import contextmanager
from io import StringIO
__docformat__ = 'restructuredtext'

@contextmanager
def capture(func, *args, **kwargs):
    """Context manager used to capture standard output"""
    out, sys.stdout = sys.stdout, StringIO()
    try:
        func(*args, **kwargs)
        sys.stdout.seek(0)
        yield sys.stdout.read()
    finally:
        sys.stdout = out


@contextmanager
def capture_stderr(func, *args, **kwargs):
    """Context manager used to capture error output"""
    err, sys.stderr = sys.stderr, StringIO()
    try:
        func(*args, **kwargs)
        sys.stderr.seek(0)
        yield sys.stderr.read()
    finally:
        sys.stderr = err


class ContextSelector:
    __doc__ = "Interface based context selector\n\n    This selector can be used as a predicate to define a class or an interface that the context\n    must inherit from or implement for the subscriber to be called:\n\n    .. code-block:: python\n\n        from zope.lifecycleevent.interfaces import IObjectModifiedEvent\n        from pyams_site.interfaces import ISiteRoot\n\n        @subscriber(IObjectModifiedEvent, context_selector=ISiteRoot)\n        def siteroot_modified_event_handler(event):\n            '''This is an event handler for an ISiteRoot object modification event'''\n    "

    def __init__(self, ifaces, config):
        if not isinstance(ifaces, (list, tuple, set)):
            ifaces = (
             ifaces,)
        self.interfaces = ifaces

    def text(self):
        """Return selector """
        return 'context_selector = %s' % str(self.interfaces)

    phash = text

    def __call__(self, event):
        for intf in self.interfaces:
            try:
                if intf.providedBy(event.object):
                    return True
            except (AttributeError, TypeError):
                if isinstance(event.object, intf):
                    return True

        return False