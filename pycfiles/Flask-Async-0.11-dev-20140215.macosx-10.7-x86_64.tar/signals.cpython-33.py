# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/flask/signals.py
# Compiled at: 2014-01-20 12:41:11
# Size of source mod 2**32: 2140 bytes
"""
    flask.signals
    ~~~~~~~~~~~~~

    Implements signals based on blinker if available, otherwise
    falls silently back to a noop

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
signals_available = False
try:
    from blinker import Namespace
    signals_available = True
except ImportError:

    class Namespace(object):

        def signal(self, name, doc=None):
            return _FakeSignal(name, doc)


    class _FakeSignal(object):
        __doc__ = 'If blinker is unavailable, create a fake class with the same\n        interface that allows sending of signals but will fail with an\n        error on anything else.  Instead of doing anything on send, it\n        will just ignore the arguments and do nothing instead.\n        '

        def __init__(self, name, doc=None):
            self.name = name
            self.__doc__ = doc

        def _fail(self, *args, **kwargs):
            raise RuntimeError('signalling support is unavailable because the blinker library is not installed.')

        send = lambda *a**a: None
        connect = disconnect = has_receivers_for = receivers_for = temporarily_connected_to = connected_to = _fail
        del _fail


_signals = Namespace()
template_rendered = _signals.signal('template-rendered')
request_started = _signals.signal('request-started')
request_finished = _signals.signal('request-finished')
request_tearing_down = _signals.signal('request-tearing-down')
got_request_exception = _signals.signal('got-request-exception')
appcontext_tearing_down = _signals.signal('appcontext-tearing-down')
appcontext_pushed = _signals.signal('appcontext-pushed')
appcontext_popped = _signals.signal('appcontext-popped')
message_flashed = _signals.signal('message-flashed')