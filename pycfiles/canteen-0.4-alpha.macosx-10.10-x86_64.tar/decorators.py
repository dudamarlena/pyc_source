# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/util/decorators.py
# Compiled at: 2014-09-26 04:50:19
"""

  decorator utils
  ~~~~~~~~~~~~~~~

  useful (and sometimes critical) decorators, for use inside and
  outside :py:mod:`canteen`.

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
            A copy of this license is included as ``LICENSE.md`` in
            the root of the project.

"""
from __future__ import print_function

class classproperty(property):
    """ Custom decorator for class-level property getters.
      Usable like ``@property`` and chainable with
      ``@memoize``, as long as ``@memoize`` is used as
      the inner decorator. """

    def __get__(self, instance, owner):
        """ Return the property value at the class level.

        :param instance: Current encapsulating object
        dispatching via the descriptor protocol,
        ``None`` if we are being dispatched from the
        class level.

        :param owner: Corresponding owner type, available
        whether we're dispatching at the class or instance
        level.

        :returns: Result of a ``classmethod``-wrapped,
        ``property``-decorated method. """
        return classmethod(self.fget).__get__(None, owner)()


def singleton(target):
    """ Mark a ``target`` class as a singleton, for use with the dependency
      injection system. Classes so-marked will be factoried on first-access and
      subsequently returned for all matching dependency requests.

      :param target: Target class to treat as a singleton.

      :raises RuntimeError: If something other than a class is marked for
        singleton mode.

      :returns: Decorated ``target`` class, after it has been marked. """
    if isinstance(target, type):
        setattr(target, '__singleton__', True)
        return target
    raise RuntimeError('Only classes may be marked/decorated as singletons. Got: "%s".' % target)


class bind(object):
    """ Encapsulated binding config for an injectable meta-implementor of
      ``meta.Proxy.Component``. Allows specification of simple string names to
      be matched during dependency injection. """
    __alias__ = None
    __target__ = None
    __config__ = None
    __namespace__ = True

    def __init__(self, alias=None, namespace=True, *args, **kwargs):
        """ Initialize this binding.

        :param alias: String alias for the target object to be bound. Defaults
          to ``None``, in which case the target function or class' ``__name__``
          will be used.

        :param namespace: ``bool`` flag to activate namespacing. Used on methods
          to explicitly bind them, but namespace them under the class binding
          they are mounted from.

        :param *args:  """
        self.__alias__, self.__config__, self.__namespace__ = alias, (args, kwargs) if args or kwargs else None, namespace
        return

    def __repr__(self):
        """ Generate a pleasant string representation for this binding.

        :returns: String representation for this binding, in the format
          ``<binding 'name'>``. """
        return "<binding '%s'>" % self.__alias__ or self.__target__.__name__

    def __call__(self, target):
        """ Dispatch this binding (the second half of a closured decorator flow) by
        scanning the target for subbindings (if applicable) and preparing (and
        subsequently attaching) an object to describe configuration.

        :param target: Target object (usually a ``function`` or ``class``) to
          *decorate* by scanning for sub-bindings and attaching a object
          describing any injectable resources.

        :raises TypeError: If a ``target`` is passed that is not a valid
          meta-implementor of ``Proxy.Registry`` or ``Proxy.Component``.

        :returns: Decorated ``target``, after scanning for bindings and
          attaching any appropriate configuration objects. """
        from ..core import meta
        self.__alias__ = self.__alias__ or target.__name__
        target.__binding__, target.__target__, self.__target__ = self, self.__alias__, target
        if isinstance(target, type):
            if issubclass(target.__class__, meta.Proxy.Registry):
                _bindings, _aliases, _hooks = set(), {}, []
                if hasattr(target, '__singleton__') and target.__singleton__:
                    target.__class__.prepare(target)
                for mapping in (target.__dict__, target.__class__.__dict__):
                    for k, v in mapping.iteritems():
                        if k.startswith('__'):
                            continue
                        if isinstance(v, (staticmethod, classmethod)):
                            v = v.__func__
                        if hasattr(v, '__binding__') and v.__binding__:
                            _bindings.add(k)
                            if v.__binding__.__alias__:
                                _aliases[v.__binding__.__alias__] = k
                        if hasattr(v, '__hooks__') and v.__hooks__:
                            v.__register__(target)

                target.__aliases__, target.__bindings__ = _aliases, frozenset(_bindings) if _bindings else None
                return target
            raise TypeError('Only meta-implementors of `meta.Proxy.Registry` (anything meta-deriving from `Registry` or `Component` can be bound to injection names.')
        from ..core import hooks
        if self.__config__ and self.__config__[1] and isinstance(self.__config__[1]['wrap'], hooks.HookResponder):
            self.__config__[1]['wrap'].__binding__ = self
        if self.__config__ and 'wrap' in self.__config__[1]:
            return self.__config__[1]['wrap'](target)
        else:
            return target