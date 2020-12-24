# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/base/protocol.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = "\n\n  protocol base\n  ~~~~~~~~~~~~~\n\n  ``Protocol`` classes help the framework understand different serialization\n  dialects for use in RPC. For example, the JSON format used for most browser\n  is specified as a ``Protocol``.\n\n  As is customary with :py:mod:`protorpc` (where the equivalent class used to\n  be called a ``Mapper`` and is now just a sloppy collection of ``object``s),\n  ``Protocol``s register ``Content-Type``s to respond to. When an RPC message\n  matching that content type is submitted, the proper ``Protocol`` is used to\n  decode it.\n\n  On the client side, ``Protocol`` objects can be used by handing in a custom\n  object when creating a ``Transport``.\n\n  Example:\n\n    # -*- coding: utf-8 -*-\n    import json\n    from canteen import Protocol\n\n    @Protocol.register('jsonrpc', ('application/json', 'text/json'))\n    class JSONRPC(Protocol):\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n"
import abc
from ..core import runtime
from ..util import decorators
with runtime.Library('protorpc') as (library, protorpc):
    messages, protojson, remote = library.load(*('messages', 'protojson', 'remote'))

    class Protocol(object):
        """ Base ``Protocol`` class for adding serialization dialects to the RPC
        engine. Implementing subclasses is easy - just specify an encoder and
        decoder function at ``encode_message`` and ``decode_message``.

        Once a ``Protocol`` class is written, it can be registered with the RPC
        subsystem by decorating it with ``Protocol.register``, along with a
        short string name (for instance, ``jsonrpc``) and a set of content types
        to respond to. """
        __label__ = None
        __config__ = None
        __protocols__ = {}
        __metaclass__ = abc.ABCMeta
        __content_types__ = ('', )

        @decorators.classproperty
        def all(cls):
            """ Class-level generator accessor to iterate through all registered
          ``Protocol`` implementations. Used at construction time to find
          protocol classes to bundle into a :py:mod:`protorpc` ``Protocols``
          object.

          :param cls: Current ``cls``, as this is a class-level property.

          :returns: Yields ``Protocol`` implementations one at a time. """
            for protocol in cls.__protocols__.itervalues():
                yield protocol

        @decorators.classproperty
        def mapping(cls):
            """ Class-level accessor for creating a :py:mod:`protorpc` ``Protocols``
          container, which resolves the proper ``Protocol`` object to dispatch
          an RPC with, based on the HTTP ``Content-Type`` header.

          :param cls: Current ``cls``, as this is a class-level property.

          :returns: :py:class:`protorpc.remote.Protocols` object containing all
            registered :py:class:`Protocol` objects. """
            container = remote.Protocols()
            for protocol in cls.all:
                singleton = protocol()
                container.add_protocol(*(
                 singleton,
                 singleton.name,
                 singleton.content_type,
                 singleton.alternative_content_types))

            return container

        @classmethod
        def register(cls, name, types, **config):
            """ Register a ``Protocol`` implementation by name and a set of content
          types. Usually used as a decorator.

          ``kwargs`` are taken as configuration to add to the protocol target.

          :param name: Name to register this protocol under. ``str`` or
            ``unicode``.

          :param types: Content types to use this mapper for. Iterable of
            ``str`` or ``unicode`` ``Content-Type`` values to match on.

          :param config: Keyword arguments are accepted as extra config to be
            passed to the underlying ``Protocol`` subclass.

          :returns: Closured wrapper to register the protocol and return it. """
            assert isinstance(name, basestring), 'protocol name must be a string'
            assert isinstance(types, (list, tuple)), 'types must be an iterable'

            def _register_protocol(klass):
                """ Closure to register a class as an available protocol right before
            class construction. Mounts a ``Protocol``'s label, content types,
            and configuration.

            :param klass: Target class to register and return. Subclass of
              :py:class:`canteen.base.protocol.Protocol`.

            :returns: Target ``klass``, after registration. """
                klass.__label__, klass.__content_types__, klass.__config__ = name, types, config
                if name not in Protocol.__protocols__:
                    Protocol.__protocols__[name] = klass
                return klass

            return _register_protocol

        @decorators.classproperty
        def name(cls):
            """ Class-level accessor for the 'short name' of this ``Protocol`` class.
          For example, ``jsonrpc``.

          :param cls: Current ``cls``, as this is a class-level property.

          :returns: ``str`` short name for this :py:class:`Protocol`. """
            return cls.__label__

        @decorators.classproperty
        def content_type(cls):
            """ Class-level accessor for the primary ``Content-Type`` this
          :py:class:`Protocol` should respond to. The first entry in the
          available options is used as the primary ``Content-Type``.

          :param cls: Current ``cls``, as this is a class-level property.

          :returns: Primary ``str`` ``Content-Type`` value. """
            return cls.__content_types__[0]

        @decorators.classproperty
        def alternative_content_types(cls):
            """ Class-level accessor for 'alternative' ``Content-Type``s that this
          :py:class:`Protocol` should respond to. Alternative content types
          will be responded to, but not used for responses (the 'primary'
          ``Content-Type`` is used as the response's type).

          :param cls: Current ``cls``, as this is a class-level property.

          :returns: ``list`` of ``str`` ``Content-Type``s. """
            return [ i for i in filter(lambda x: x != cls.content_type, cls.__content_types__)
                   ]

        @abc.abstractmethod
        def encode_message(self, message):
            """ Encode a message according to this :py:class:`Protocol`. Must be
          implemented by child classes, and so is marked as an abstract method.

          Failure to specify this method will prevent an implementing class
          from being constructed.

          :param message: Object to encode with ``Protocol``. Passed-in from
            ProtoRPC as ``message.Message``.

          :raises NotImplementedError: Always, as this method is abstract.

          :returns: ``None``, but child class implementations are expected to
            return an encoded ``str``/``unicode`` representation of
            ``message``. """
            raise NotImplementedError('Method `Protocol.encode_message` is abstract.')

        @abc.abstractmethod
        def decode_message(self, message_type, encoded_message):
            """ Decode a message according to this :py:class:`Protocol`. Must be
          implemented by child classes, and so is marked as an abstract method.

          Failure to specify this method will prevent an implementing class from
          being constructed.

          :param message_type: Type to expand from ``encoded_message``. Subclass
            of :py:class:`messages.Message`.

          :param encoded_message: Encoded message to be decoded. ``str``,
            ``unicode`` or iterable string buffer.

          :raises NotImplementedError: Always, as this method is abstract.

          :returns: ``None``, but child class implementations are expected to
            return an inflated ``message_type`` based on the provided
            ``encoded_message``. """
            raise NotImplementedError('Method `Protocol.decode_message` is abstract.')

        CONTENT_TYPE = content_type
        ALTERNATIVE_CONTENT_TYPES = alternative_content_types