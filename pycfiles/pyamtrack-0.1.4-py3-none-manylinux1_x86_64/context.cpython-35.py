# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/context.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 2800 bytes
__doc__ = 'PyAMS_utils.context module\n\nThis module provides a "context" selector which can be used as Pyramid\'s subscriber\npredicate. Matching argument can be a class or an interface: for subscriber to be actually called,\nsubscriber\'s argument should inherit from it (if it\'s a class) or implement it (if it\'s an\ninterface).\n'
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
    """ContextSelector"""

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