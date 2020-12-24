# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./ami.py
# Compiled at: 2018-07-20 10:03:27
# Size of source mod 2**32: 3310 bytes
import omniORB
Messaging = omniORB.openModule('Messaging')
CORBA = omniORB.openModule('CORBA')
try:
    property
except NameError:

    def property(*args):
        pass


class PollerImpl(Messaging.Poller):

    def __init__(self, poller):
        self._poller = poller

    def is_ready(self, timeout):
        return self._poller.is_ready(timeout)

    def create_pollable_set(self):
        return PollableSetImpl(self._poller.create_pollable_set(self))

    def _get_operation_target(self):
        return self._poller.operation_target()

    operation_target = property(_get_operation_target)

    def _get_operation_name(self):
        return self._poller.operation_name()

    operation_name = property(_get_operation_name)

    def _get_associated_handler(self):
        return self._poller.get_handler()

    def _set_associated_handler(self, handler):
        self._poller.set_handler(handler)

    associated_handler = property(_get_associated_handler, _set_associated_handler)

    def _get_is_from_poller(self):
        return self._poller.is_from_poller()

    is_from_poller = property(_get_is_from_poller)


class ExceptionHolderImpl(Messaging.ExceptionHolder):

    def __init__(self, poller):
        self._poller = poller

    def raise_exception(self):
        self._poller.raise_exception()


class PollableSetImpl(CORBA.PollableSet):

    def __init__(self, pset):
        self._pset = pset

    def create_dii_pollable(self):
        raise CORBA.NO_IMPLEMENT(omniORB.NO_IMPLEMENT_Unsupported, CORBA.COMPLETED_NO)

    def add_pollable(self, potential):
        if potential is not None:
            self._pset.add_pollable(potential)
        else:
            raise CORBA.BAD_PARAM(omniORB.BAD_PARAM_InvalidPollerType, CORBA.COMPLETED_NO)

    def get_ready_pollable(self, timeout):
        return self._pset.get_ready_pollable(timeout)

    def remove(self, potential):
        if potential is not None:
            self._pset.remove(potential)
        else:
            raise CORBA.BAD_PARAM(omniORB.BAD_PARAM_InvalidPollerType, CORBA.COMPLETED_NO)

    def number_left(self):
        return self._pset.number_left()