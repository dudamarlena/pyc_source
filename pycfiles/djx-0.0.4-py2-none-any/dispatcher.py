# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/dispatch/dispatcher.py
# Compiled at: 2019-02-14 00:35:17
import sys, threading, warnings, weakref
from django.utils import six
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.inspect import func_accepts_kwargs
from django.utils.six.moves import range
if six.PY2:
    from .weakref_backports import WeakMethod
else:
    from weakref import WeakMethod

def _make_id(target):
    if hasattr(target, '__func__'):
        return (id(target.__self__), id(target.__func__))
    return id(target)


NONE_ID = _make_id(None)
NO_RECEIVERS = object()

class Signal(object):
    """
    Base class for all signals

    Internal attributes:

        receivers
            { receiverkey (id) : weakref(receiver) }
    """

    def __init__(self, providing_args=None, use_caching=False):
        """
        Create a new signal.

        providing_args
            A list of the arguments this signal can pass along in a send() call.
        """
        self.receivers = []
        if providing_args is None:
            providing_args = []
        self.providing_args = set(providing_args)
        self.lock = threading.Lock()
        self.use_caching = use_caching
        self.sender_receivers_cache = weakref.WeakKeyDictionary() if use_caching else {}
        self._dead_receivers = False
        return

    def connect(self, receiver, sender=None, weak=True, dispatch_uid=None):
        """
        Connect receiver to sender for signal.

        Arguments:

            receiver
                A function or an instance method which is to receive signals.
                Receivers must be hashable objects.

                If weak is True, then receiver must be weak referenceable.

                Receivers must be able to accept keyword arguments.

                If a receiver is connected with a dispatch_uid argument, it
                will not be added if another receiver was already connected
                with that dispatch_uid.

            sender
                The sender to which the receiver should respond. Must either be
                a Python object, or None to receive events from any sender.

            weak
                Whether to use weak references to the receiver. By default, the
                module will attempt to use weak references to the receiver
                objects. If this parameter is false, then strong references will
                be used.

            dispatch_uid
                An identifier used to uniquely identify a particular instance of
                a receiver. This will usually be a string, though it may be
                anything hashable.
        """
        from django.conf import settings
        if settings.configured and settings.DEBUG:
            if not callable(receiver):
                raise AssertionError('Signal receivers must be callable.')
                raise (func_accepts_kwargs(receiver) or ValueError)('Signal receivers must accept keyword arguments (**kwargs).')
        if dispatch_uid:
            lookup_key = (
             dispatch_uid, _make_id(sender))
        else:
            lookup_key = (
             _make_id(receiver), _make_id(sender))
        if weak:
            ref = weakref.ref
            receiver_object = receiver
            if hasattr(receiver, '__self__') and hasattr(receiver, '__func__'):
                ref = WeakMethod
                receiver_object = receiver.__self__
            if six.PY3:
                receiver = ref(receiver)
                weakref.finalize(receiver_object, self._remove_receiver)
            else:
                receiver = ref(receiver, self._remove_receiver)
        with self.lock:
            self._clear_dead_receivers()
            for r_key, _ in self.receivers:
                if r_key == lookup_key:
                    break
            else:
                self.receivers.append((lookup_key, receiver))

            self.sender_receivers_cache.clear()

    def disconnect(self, receiver=None, sender=None, weak=None, dispatch_uid=None):
        """
        Disconnect receiver from sender for signal.

        If weak references are used, disconnect need not be called. The receiver
        will be remove from dispatch automatically.

        Arguments:

            receiver
                The registered receiver to disconnect. May be none if
                dispatch_uid is specified.

            sender
                The registered sender to disconnect

            dispatch_uid
                the unique identifier of the receiver to disconnect
        """
        if weak is not None:
            warnings.warn('Passing `weak` to disconnect has no effect.', RemovedInDjango20Warning, stacklevel=2)
        if dispatch_uid:
            lookup_key = (
             dispatch_uid, _make_id(sender))
        else:
            lookup_key = (
             _make_id(receiver), _make_id(sender))
        disconnected = False
        with self.lock:
            self._clear_dead_receivers()
            for index in range(len(self.receivers)):
                r_key, _ = self.receivers[index]
                if r_key == lookup_key:
                    disconnected = True
                    del self.receivers[index]
                    break

            self.sender_receivers_cache.clear()
        return disconnected

    def has_listeners(self, sender=None):
        return bool(self._live_receivers(sender))

    def send(self, sender, **named):
        """
        Send signal from sender to all connected receivers.

        If any receiver raises an error, the error propagates back through send,
        terminating the dispatch loop. So it's possible that all receivers
        won't be called if an error is raised.

        Arguments:

            sender
                The sender of the signal. Either a specific object or None.

            named
                Named arguments which will be passed to receivers.

        Returns a list of tuple pairs [(receiver, response), ... ].
        """
        if not self.receivers or self.sender_receivers_cache.get(sender) is NO_RECEIVERS:
            return []
        return [ (receiver, receiver(signal=self, sender=sender, **named)) for receiver in self._live_receivers(sender)
               ]

    def send_robust(self, sender, **named):
        """
        Send signal from sender to all connected receivers catching errors.

        Arguments:

            sender
                The sender of the signal. Can be any python object (normally one
                registered with a connect if you actually want something to
                occur).

            named
                Named arguments which will be passed to receivers. These
                arguments must be a subset of the argument names defined in
                providing_args.

        Return a list of tuple pairs [(receiver, response), ... ]. May raise
        DispatcherKeyError.

        If any receiver raises an error (specifically any subclass of
        Exception), the error instance is returned as the result for that
        receiver. The traceback is always attached to the error at
        ``__traceback__``.
        """
        if not self.receivers or self.sender_receivers_cache.get(sender) is NO_RECEIVERS:
            return []
        responses = []
        for receiver in self._live_receivers(sender):
            try:
                response = receiver(signal=self, sender=sender, **named)
            except Exception as err:
                if not hasattr(err, '__traceback__'):
                    err.__traceback__ = sys.exc_info()[2]
                responses.append((receiver, err))
            else:
                responses.append((receiver, response))

        return responses

    def _clear_dead_receivers(self):
        if self._dead_receivers:
            self._dead_receivers = False
            new_receivers = []
            for r in self.receivers:
                if isinstance(r[1], weakref.ReferenceType) and r[1]() is None:
                    continue
                new_receivers.append(r)

            self.receivers = new_receivers
        return

    def _live_receivers(self, sender):
        """
        Filter sequence of receivers to get resolved, live receivers.

        This checks for weak references and resolves them, then returning only
        live receivers.
        """
        receivers = None
        if self.use_caching and not self._dead_receivers:
            receivers = self.sender_receivers_cache.get(sender)
            if receivers is NO_RECEIVERS:
                return []
        if receivers is None:
            with self.lock:
                self._clear_dead_receivers()
                senderkey = _make_id(sender)
                receivers = []
                for (receiverkey, r_senderkey), receiver in self.receivers:
                    if r_senderkey == NONE_ID or r_senderkey == senderkey:
                        receivers.append(receiver)

                if self.use_caching:
                    if not receivers:
                        self.sender_receivers_cache[sender] = NO_RECEIVERS
                    else:
                        self.sender_receivers_cache[sender] = receivers
        non_weak_receivers = []
        for receiver in receivers:
            if isinstance(receiver, weakref.ReferenceType):
                receiver = receiver()
                if receiver is not None:
                    non_weak_receivers.append(receiver)
            else:
                non_weak_receivers.append(receiver)

        return non_weak_receivers

    def _remove_receiver(self, receiver=None):
        self._dead_receivers = True


def receiver(signal, **kwargs):
    """
    A decorator for connecting receivers to signals. Used by passing in the
    signal (or list of signals) and keyword arguments to connect::

        @receiver(post_save, sender=MyModel)
        def signal_receiver(sender, **kwargs):
            ...

        @receiver([post_save, post_delete], sender=MyModel)
        def signals_receiver(sender, **kwargs):
            ...
    """

    def _decorator(func):
        if isinstance(signal, (list, tuple)):
            for s in signal:
                s.connect(func, **kwargs)

        else:
            signal.connect(func, **kwargs)
        return func

    return _decorator