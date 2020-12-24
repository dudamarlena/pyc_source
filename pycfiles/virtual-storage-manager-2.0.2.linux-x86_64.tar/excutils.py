# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/excutils.py
# Compiled at: 2016-06-13 14:11:03
"""
Exception related utilities.
"""
import contextlib, logging, sys, traceback
from vsm.openstack.common.gettextutils import _

@contextlib.contextmanager
def save_and_reraise_exception():
    """Save current exception, run some code and then re-raise.

    In some cases the exception context can be cleared, resulting in None
    being attempted to be re-raised after an exception handler is run. This
    can happen when eventlet switches greenthreads or when running an
    exception handler, code raises and catches an exception. In both
    cases the exception context will be cleared.

    To work around this, we save the exception state, run handler code, and
    then re-raise the original exception. If another exception occurs, the
    saved exception is logged and the new exception is re-raised.
    """
    type_, value, tb = sys.exc_info()
    try:
        yield
    except Exception:
        logging.error(_('Original exception being dropped: %s'), traceback.format_exception(type_, value, tb))
        raise

    raise type_, value, tb