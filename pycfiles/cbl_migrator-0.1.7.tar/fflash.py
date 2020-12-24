# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cblog/fflash.py
# Compiled at: 2006-12-13 20:03:41
__doc__ = 'Functions for displaying status messages on the next page.\n\nIntended as drop-in replacement and building on turbogears.flash() but\nallow for much nicer styling of the messages, since you can pass a "status"\nparameter, which will be used for the CSS class of the DIV element that\nencloses the status message.\n'
__all__ = [
 'error', 'info', 'set_default_message_timeout', 'statusmessage', 'success', 'warning']
import turbogears
from simplejson import dumps
_default_timeout = 0

def set_default_message_timeout(timeout):
    """Set the default timeout after which the message box disappears."""
    global _default_timeout
    _default_timeout = timeout


def statusmessage(msg, status='info', timeout=0, allow_html=False):
    assert isinstance(status, basestring)
    tg_flash = dict(msg=msg, status=status)
    if timeout:
        tg_flash['timeout'] = timeout
    elif _default_timeout:
        tg_flash['timeout'] = _default_timeout
    if allow_html:
        tg_flash['allow_html'] = True
    turbogears.flash(dumps(tg_flash))


def info(msg, timeout=0, allow_html=False):
    statusmessage(msg, 'info', timeout)


def error(msg, timeout=0, allow_html=False):
    statusmessage(msg, 'error', timeout)


def warning(msg, timeout=0, allow_html=False):
    statusmessage(msg, 'warning', timeout)


def success(msg, timeout=0, allow_html=False):
    statusmessage(msg, 'success', timeout)