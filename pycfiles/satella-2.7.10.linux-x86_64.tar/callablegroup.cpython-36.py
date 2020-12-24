# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/coding/concurrent/callablegroup.py
# Compiled at: 2020-04-14 13:42:23
# Size of source mod 2**32: 2483 bytes
import collections, copy, typing as tp
__all__ = [
 'CallableGroup']
T = tp.TypeVar('T')

class CallableGroup(tp.Generic[T]):
    __doc__ = '\n    This behaves like a function, but allows to add other functions to call\n    when invoked, eg.\n\n        c1 = Callable()\n\n        c1.add(foo)\n        c1.add(bar)\n\n        c1(2, 3)\n\n    Now both foo and bar will be called with arguments (2, 3). Their exceptions\n    will be propagated.\n\n    '
    __slots__ = ('callables', 'gather', 'swallow_exceptions')

    def __init__(self, gather: bool=True, swallow_exceptions: bool=False):
        """
        :param gather: if True, results from all callables will be gathered
                       into a list and returned from __call__
        :param swallow_exceptions: if True, exceptions from callables will be
                                   silently ignored. If gather is set,
                                   result will be the exception instance
        """
        self.callables = collections.OrderedDict()
        self.gather = gather
        self.swallow_exceptions = swallow_exceptions

    def add(self, callable_: tp.Callable[([], T)], one_shot: bool=False):
        """
        :param callable_: callable
        :param one_shot: if True, callable will be unregistered after single call
        """
        from ..structures.hashable_objects import HashableWrapper
        callable_ = HashableWrapper(callable_)
        if callable_ in self.callables:
            return
        self.callables[callable_] = one_shot

    def __call__(self, *args, **kwargs) -> tp.Optional[tp.List[T]]:
        """
        Run the callable. All registered callables will be called with
        passed arguments, so they should have the same arity.

        If callables raise, it will be passed through.

        :return: list of results if gather was set, else None
        """
        callables = copy.copy(self.callables)
        results = []
        for call, one_shot in callables.items():
            try:
                q = call(*args, **kwargs)
            except Exception as e:
                if not self.swallow_exceptions:
                    raise
                q = e

            if self.gather:
                results.append(q)
            if not one_shot:
                self.add(call, one_shot)

        if self.gather:
            return results