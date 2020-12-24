# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/core/hooks.py
# Compiled at: 2014-09-26 04:50:19
"""

  core hooks
  ~~~~~~~~~~

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
            A copy of this license is included as ``LICENSE.md`` in
            the root of the project.

"""
import inspect
from . import runtime

class HookResponder(object):
    """ Provides an object that can hook into named points in runtime execution
      flow. Context is provided as keyword arguments and may be subscribed to by
      item name.

      A full list of hook points or context items is not yet available. """
    __slots__ = ('__func__', '__wrap__', '__hooks__', '__argspec__', '__binding__')

    def __init__(self, *events, **kwargs):
        """ Initialize this ``HookResponder``.

        :param *events: Iterable of event names to subscribe to.
        :param **kwargs: Configuration, notably ``wrap`` (which can be used to
          re-wrap the target callable). """
        self.__hooks__, self.__argspec__, self.__wrap__ = frozenset(events), Context(kwargs.get('context'), kwargs.get('rollup', False), kwargs.get('notify', False)) if kwargs else None, kwargs.get('wrap')
        return

    def __register__(self, context):
        """ Register this ``HookResponder`` with the currently-active runtime, which
        will make it available when hooks are due to be executed.

        :param context: Requested context to register alongside this
          ``HookResponder``.

        :returns: Nothing. """
        for i in self.__hooks__:
            runtime.Runtime.add_hook(i, (context, self))

    def __call__(self, *args, **kwargs):
        """ Execute this local ``HookResponder``, which will dispatch the underlying
        hook target, passing along any arguments and keyword arguments.

        :param **args: Positional arguments to pass to the target callable.
        :param **kwargs: Keyword arguments to pass to the target callable.

        :returns: Whatever the target callable returns. """
        from ..util import decorators
        if not hasattr(self, '__func__') or not getattr(self, '__func__'):
            hook = args[0]
            if not self.__argspec__:
                _hook_i = inspect.getargspec(hook)
                self.__argspec__ = Context([ i for i in _hook_i.args if i not in ('self',
                                                                                  'cls')
                                           ], _hook_i.keywords is not None)
            self.__binding__ = hook.__binding__ if isinstance(self.__wrap__, decorators.bind) else None

            def run_hook(*args, **kwargs):
                """ Execute the local hook according to the configuration held by the
            encapsulating ``HookResponder``.

            :param *args: Positional arguments to pass to the hook.
            :param **kwargs: Keyword arguments to pass to the hook.

            :returns: Whatever the hook returns. """
                return self.__argspec__(self.__wrap__(hook) if self.__wrap__ else hook)(*args, **kwargs)

            return setattr(self, '__func__', run_hook) or self
        else:
            return self.__func__(*args, **kwargs)


class Context(object):
    """ Object that contains context for a given ``HookResponder`` instance. Holds
      hook kwargs and args for target execution. """
    __slots__ = ('__requested__', '__rollup__', '__notify__')

    def __init__(self, requested, rollup=True, notify=False):
        """ Initialize this ``HookResponder`` ``Context`` object.

        :param requested: Context items that are explicitly requested to be
          provided at runtime.

        :param rollup: ``Bool``, indicating support in the target callable for
          accepting a ``**kwargs``-style rolled-up set of context items,
          including extra (unrequested) context items.

        :param notify: ``Bool``, indicating that the target expects the event
          name for which it is being called to be inserted as the first
          positional argument. """
        self.__requested__, self.__rollup__, self.__notify__ = requested, rollup, notify

    def __call__(self, func):
        """ Pair this ``Context`` with the target ``func`` and execute using the
        locally-attached ``requested`` args, potentially using ``rollup``.

        :param func: Target function to wrap with a closure to properly call it
          with the provided context.

        :raises RuntimeError: In the inner hook closure, if a case arises where
          a target requests a context item that is not available.

        :returns: ``with_context`` inner closure, that applies stored context to
          the target ``func`` when dispatched. """

        def with_context(*args, **context):
            """ Closure returned to execute args and context items with a provided
          target ``func``, usually the backing to a ``HookResponder``. Arguments
          are passed through to the target callable.

          Accepts positional and keyword arguments on behalf of the wrapped
          ``func``.

          :param args: Positional arguments to pass to target hook responder.

          :param context: Keyword arguments (considered as "context" in this,
            well, context) to pass to the target hook responder.

          :raises RuntimeError: If a case is encountered where a hook function
            requests a context item that is not yet available in the runtime
            execution flow.

          :returns: Result of calling the target ``func`` with applied ``args``
            and ``context``. """
            hookname, args = args[0], args[1:]
            _args, _kwargs = [], {}
            if self.__requested__:
                for prop in self.__requested__:
                    if prop not in context:
                        raise RuntimeError('Cannot satisfy request for context entry `%s` in hook `%s` for event point `%s`.' % (
                         prop,
                         func if not isinstance(func, (classmethod, staticmethod)) else func.__func__.__name__, hookname))
                    _args.append(context[prop])

            if self.__rollup__:
                _kwargs = context
            dispatch = func if not isinstance(func, (classmethod, staticmethod)) else func.__func__
            if self.__notify__:
                _args.insert(0, hookname)
            return dispatch(*tuple(list(args) + _args), **_kwargs)

        return with_context