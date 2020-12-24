# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yakonfig/factory.py
# Compiled at: 2015-07-07 22:00:14
"""Discover object configuration from parameter lists.

.. This software is released under an MIT/X11 open source license.
   Copyright 2014-2015 Diffeo, Inc.

.. autoclass:: AutoFactory

"""
from __future__ import absolute_import, division, print_function
import abc, inspect
from six import iteritems, string_types
from yakonfig.configurable import Configurable
from yakonfig.exceptions import ConfigurationError, ProgrammerError

class AutoFactory(Configurable):
    """A configurable that discovers the its childrens' configuration.

    Clients that subclass :class:`AutoFactory` must implement the
    :attr:`auto_config` property, which should be an iterable of
    things to automatically a configuration from. Notably, subclasses
    should *not* implement :attr:`~yakonfig.Configurable.sub_modules`,
    as this class provides its own implementation of it using
    :attr:`auto_config`.

    Items in :attr:`auto_config` may be functions, methods, or
    classes.  If a class, its `__new__` or `__init__` function will be
    inspected.  Any parameters beyond :keyword:`self` are extracted
    from this function.  Keyword parameters with default values become
    the default configuration of the object.  Parameters without
    default values must be provided by the :class:`AutoFactory`
    instance as properties of the derived class.  The configurable
    callables may not take variable argument lists (``*args,
    **kwargs``).  If they are classes, they may have a
    :attr:`~yakonfig.Configurable.config_name` but no other
    :class:`~yakonfig.Configurable` metadata.

    As a special case, if a configurable callable contains a parameter
    named `config`, that parameter will receive the child's config
    dictionary (as distinct from the parent's saved config dictionary
    :attr:`config`), and the configuration check will allow unexpected
    configuration values.  This supports older modules that explicitly
    passed configuration dictionaries to their children.  If the
    configurable callable is a class with a
    :attr:`~yakonfig.Configurable.config_name` then it is used
    directly during the configuration cycle.

    This class hooks into the :mod:`yakonfig` configuration sequence
    to capture its part of the configuration at startup time.  Child
    callables' configuration may not contain settings that are not any
    of the defaulted parameters.  If this class is used outside the
    standard sequence, then you must set :attr:`config` before calling
    :meth:`create`.

    Currently, this class does **not** support a hierarchical
    configuration: items in :attr:`auto_config` may not be
    :class:`~yakonfig.Configurable`, and :class:`AutoFactory` objects
    may not be nested.  This is likely to change in the future.

    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, config=None):
        """Create a new object factory.

        If `config` is :const:`None` (the default), then the
        :attr:`config` property must be set before calling
        :meth:`create`.  Passing this factory object to
        :func:`yakonfig.parse_args` or a similar high-level
        :mod:`yakonfig` setup method will also accomplish this.

        :param dict config: local configuration dictionary (if available)

        """
        super(AutoFactory, self).__init__()
        self._config = config

    @property
    def sub_modules(self):
        return [ AutoConfigured.from_obj(obj, any_configurable=True) for obj in self.auto_config
               ]

    @abc.abstractproperty
    def auto_config(self):
        """Must return a list of objects to automatically configure.

        This list is interpreted shallowly. That is, all configuration
        from each object is discovered through its name and parameter
        list only. Everything else is ignored.

        """
        pass

    def check_config(self, config, prefix=''):
        for child in self.sub_modules:
            if hasattr(child, 'check_config'):
                child.check_config(config)

    def normalize_config(self, config):
        """Rewrite (and capture) the configuration of this object."""
        self.config = config

    @property
    def config(self):
        """Saved configuration for the factory and its sub-objects."""
        if self._config is None:
            raise ProgrammerError('Tried to access saved factory configuration before yakonfig configuration was run.')
        return self._config

    @config.setter
    def config(self, c):
        self._config = c
        self.new_config()

    def new_config(self):
        """Hook called when the configuration changes.

        If factory implementations keep properties that are created
        from the configuration, this is a place to create or reset them.
        The base class implementation does nothing.

        """
        pass

    def create(self, configurable, config=None, **kwargs):
        """Create a sub-object of this factory.

        Instantiates the `configurable` object with the current saved
        :attr:`config`.  This essentially translates to
        ``configurable(**config)``, except services defined in the
        parent and requested by `configurable` (by setting the
        ``services`` attribute) are injected. If a service is not
        defined on this factory object, then a
        :exc:`yakonfig.ProgrammerError` is raised.

        If `config` is provided, it is a local configuration for
        `configurable`, and it overrides the saved local configuration
        (if any).  If not provided, then :attr:`config` must already be
        set, possibly by passing this object into the :mod:`yakonfig`
        top-level setup sequence.

        :param callable configurable: object to create
        :param dict config: local configuration for `configurable`
        :param kwargs: additional keyword parameters
        :return: ``configurable(**config)``

        """
        if isinstance(configurable, string_types):
            candidates = [ ac for ac in self.sub_modules if ac.config_name == configurable ]
            if len(candidates) == 0:
                raise KeyError(configurable)
            configurable = candidates[0]
        if not isinstance(configurable, AutoConfigured):
            configurable = AutoConfigured.from_obj(configurable)
        if config is None:
            config = self.config.get(configurable.config_name, {})
        params = {}
        for other, default in iteritems(configurable.default_config):
            params[other] = kwargs.get(other, config.get(other, default))

        for other in getattr(configurable, 'services', []):
            if other == 'config':
                params[other] = dict(config, **kwargs)
            elif other in kwargs:
                params[other] = kwargs[other]
            elif other in config:
                params[other] = config[other]
            else:
                params[other] = getattr(self, other)

        return configurable(**params)


class AutoConfigured(Configurable):
    """Configurable proxy object for callable children.

    This is an wrapper class that provides an implementation that
    satisfies :class:`yakonfig.Configurable` for objects that can have
    their configuration automatically discovered.

    This class is for internal library use only and is not part
    of the yakonfig factory API.

    """

    def __init__(self, obj, config_name, services, default_config):
        self.obj = obj
        self._config_name = config_name
        self._services = services
        self._default_config = default_config

    @classmethod
    def from_obj(cls, obj, any_configurable=False):
        """Create a proxy object from a callable.

        If `any_configurable` is true, `obj` takes a parameter named
        ``config``, and `obj` smells like it implements
        :class:`yakonfig.Configurable` (it has a
        :attr:`~yakonfig.Configurable.config_name`), then return it
        directly.

        """
        discovered = cls.inspect_obj(obj)
        if any_configurable and 'config' in discovered['required'] and hasattr(obj, 'config_name'):
            return obj
        return cls(obj, discovered['name'], discovered['required'], discovered['defaults'])

    def __call__(self, *args, **kwargs):
        return self.obj(*args, **kwargs)

    @property
    def config_name(self):
        """Name of this object as it appears in configuration."""
        return self._config_name

    @property
    def services(self):
        """List of externally provided parameter names."""
        return self._services

    @property
    def default_config(self):
        """Derived default configuration for this object."""
        return self._default_config

    def check_config(self, config, name=''):
        """Check that the configuration for this object is valid.

        This is a more restrictive check than for most :mod:`yakonfig`
        objects.  It will raise :exc:`yakonfig.ConfigurationError` if
        `config` contains any keys that are not in the underlying
        callable's parameter list (that is, extra unused configuration
        options).  This will also raise an exception if `config`
        contains keys that duplicate parameters that should be
        provided by the factory.

        .. note:: This last behavior is subject to change; future
                  versions of the library may allow configuration to
                  provide local configuration for a factory-provided
                  object.

        :param dict config: the parent configuration dictionary,
          probably contains :attr:`config_name` as a key
        :param str name: qualified name of this object in the configuration
        :raise: :exc:`yakonfig.ConfigurationError` if excess parameters exist

        """
        config = config.get(self.config_name, {})
        extras = set(config.keys()).difference(self.default_config)
        if 'config' not in self.services and extras:
            raise ConfigurationError('Unsupported config options for "%s": %s' % (
             self.config_name, (', ').join(extras)))
        missing = set(self.default_config).difference(config)
        if missing:
            raise ConfigurationError('Missing config options for "%s": %s' % (
             self.config_name, (', ').join(missing)))
        duplicates = set(config.keys()).intersection(set(self.services))
        if duplicates:
            raise ConfigurationError('Disallowed config options for "%s": %s' % (
             self.config_name, (', ').join(duplicates)))

    @staticmethod
    def inspect_obj(obj):
        """Learn what there is to be learned from our target.

        Given an object at `obj`, which must be a function, method or
        class, return a configuration *discovered* from the name of
        the object and its parameter list. This function is
        responsible for doing runtime reflection and providing
        understandable failure modes.

        The return value is a dictionary with three keys: ``name``,
        ``required`` and ``defaults``. ``name`` is the name of the
        function/method/class. ``required`` is a list of parameters
        *without* default values. ``defaults`` is a dictionary mapping
        parameter names to default values. The sets of parameter names in
        ``required`` and ``defaults`` are disjoint.

        When given a class, the parameters are taken from its ``__init__``
        method.

        Note that this function is purposefully conservative in the things
        that is will auto-configure. All of the following things will result
        in a :exc:`yakonfig.ProgrammerError` exception being raised:

        1. A parameter list that contains tuple unpacking. (This is invalid
           syntax in Python 3.)
        2. A parameter list that contains variable arguments (``*args``) or
           variable keyword words (``**kwargs``). This restriction forces
           an auto-configurable to explicitly state all configuration.

        Similarly, if given an object that isn't a function/method/class, a
        :exc:`yakonfig.ProgrammerError` will be raised.

        If reflection cannot be performed on ``obj``, then a ``TypeError``
        is raised.

        """
        skip_params = 0
        if inspect.isfunction(obj):
            name = obj.__name__
            inspect_obj = obj
            skip_params = 0
        elif inspect.ismethod(obj):
            name = obj.im_func.__name__
            inspect_obj = obj
            skip_params = 1
        elif inspect.isclass(obj):
            inspect_obj = None
            if hasattr(obj, '__dict__') and '__new__' in obj.__dict__:
                inspect_obj = obj.__new__
            elif hasattr(obj, '__init__'):
                inspect_obj = obj.__init__
            else:
                raise ProgrammerError('Class "%s" does not have a "__new__" or "__init__" method, so it cannot be auto configured.' % str(obj))
            name = obj.__name__
            if hasattr(obj, 'config_name'):
                name = obj.config_name
            if not inspect.ismethod(inspect_obj) and not inspect.isfunction(inspect_obj):
                raise ProgrammerError('"%s.%s" is not a method/function (it is a "%s").' % (
                 str(obj), inspect_obj.__name__, type(inspect_obj)))
            skip_params = 1
        else:
            raise ProgrammerError('Expected a function, method or class to automatically configure, but got a "%s" (type: "%s").' % (
             repr(obj), type(obj)))
        argspec = inspect.getargspec(inspect_obj)
        if argspec.varargs is not None or argspec.keywords is not None:
            raise ProgrammerError('The auto-configurable "%s" cannot contain "*args" or "**kwargs" in its list of parameters.' % repr(obj))
        if not all(isinstance(arg, string_types) for arg in argspec.args):
            raise ProgrammerError('Expected an auto-configurable with no nested parameters, but "%s" seems to contain some tuple unpacking: "%s"' % (
             repr(obj), argspec.args))
        defaults = argspec.defaults or []
        i_defaults = len(argspec.args) - len(defaults)
        return {'name': name, 
           'required': argspec.args[skip_params:i_defaults], 
           'defaults': dict([ (k, defaults[i]) for i, k in enumerate(argspec.args[i_defaults:])
                     ])}