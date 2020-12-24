# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/callbacks.py
# Compiled at: 2016-07-03 23:28:12
__doc__ = ' Generic signal/slot callback system. '
import inspect, logging, weakref
logger = logging.getLogger(__name__)

class Callback(object):

    def __init__(self, slot):
        self._callback_func_ref = None
        self._callback_self_ref = None
        if inspect.ismethod(slot):
            self._callback_func_ref = weakref.ref(slot.im_func)
            self._callback_self_ref = weakref.ref(slot.im_self)
        else:
            self._callback_func_ref = weakref.ref(slot)
        return

    def __eq__(self, other):
        if isinstance(other, Callback):
            ref_cmp = (
             other._callback_func_ref, other._callback_self_ref)
        elif inspect.ismethod(other):
            ref_cmp = (
             weakref.ref(other.im_func), weakref.ref(other.im_self))
        else:
            ref_cmp = (
             weakref.ref(other), -1)
        return (
         self._callback_func_ref, self._callback_self_ref) == ref_cmp

    def __call__(self, *args):
        """
        Calls this callback with the inputted arguments by accessing its stored
        callback function and self arguments.
        
        :param      *args | <variant>
        """
        if self._callback_func_ref is None:
            return
        else:
            callback_func = self._callback_func_ref()
            if self._callback_self_ref is not None:
                callback_self = self._callback_self_ref()
                if callback_self is None:
                    return
                return callback_func(callback_self, *args)
            return callback_func(*args)
            return

    def isValid(self):
        """
        Checks to see if the callback pointers are still valid or not.
        
        :return     <bool>
        """
        if self._callback_func_ref is not None and self._callback_func_ref():
            if self._callback_self_ref is None or self._callback_self_ref():
                return True
        return False


class CallbackSet(object):

    def __init__(self):
        self._callbacks = {}

    def callbacks(self, signal):
        """
        Returns a list of the callbacks associated with a given key.
        
        :param      signal | <variant>
        
        :return     [<Callback>, ..]
        """
        return self._callbacks.get(signal, [])

    def clear(self, signal=None):
        """
        Clears either all the callbacks or the callbacks for a particular
        signal.
        
        :param      signal | <variant> || None
        """
        if signal is not None:
            self._callbacks.pop(signal, None)
        else:
            self._callbacks.clear()
        return

    def connect(self, signal, slot):
        """
        Creates a new connection between the inputted signal and slot.
        
        :param      signal | <variant>
                    slot   | <callable>
        
        :return     <bool> | new connection created
        """
        if self.isConnected(signal, slot):
            return False
        callback = Callback(slot)
        self._callbacks.setdefault(signal, [])
        self._callbacks[signal].append(callback)
        return True

    def disconnect(self, signal, slot):
        """
        Breaks the connection between the inputted signal and the given slot.
        
        :param      signal | <variant>
                    slot   | <callable>
        
        :return     <bool> | connection broken
        """
        sig_calls = self._callbacks.get(signal, [])
        for callback in sig_calls:
            if callback == slot:
                sig_calls.remove(callback)
                return True

        return False

    def isConnected(self, signal, slot):
        """
        Returns if the given signal is connected to the inputted slot.
        
        :param      signal | <variant>
                    slot   | <callable>
        
        :return     <bool> | is connected
        """
        sig_calls = self._callbacks.get(signal, [])
        for callback in sig_calls:
            if callback == slot:
                return True

        return False

    def emit(self, signal, *args):
        """
        Emits the given signal with the inputted args.  This will go through
        its list of connected callback slots and call them.
        
        :param      signal | <variant>
                    *args  | variables
        """
        callbacks = self._callbacks.get(signal, [])
        new_callbacks = []
        for callback in callbacks:
            if not callback.isValid():
                continue
            new_callbacks.append(callback)
            try:
                callback(*args)
            except StandardError:
                logger.exception('Error occurred during callback.')

        self._callbacks[signal] = new_callbacks