# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/uri.py
# Compiled at: 2018-04-15 04:46:41
# Size of source mod 2**32: 10960 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from enum import Enum
from urllib.parse import urlsplit, urlunsplit
from abc import ABCMeta, abstractmethod
from wasp_general.verify import verify_type, verify_subclass

class WURI:
    __doc__ = '\n\tClass that represent URI as it is described in RFC 3986\n\t'

    class Component(Enum):
        __doc__ = ' Parts/components names that URI is consists of\n\t\t'
        scheme = 'scheme'
        username = 'username'
        password = 'password'
        hostname = 'hostname'
        port = 'port'
        path = 'path'
        query = 'query'
        fragment = 'fragment'

    def __init__(self, **components):
        """ Create new WURI object. By default empty URI is created

                :param components: components that must be set for this URI. Keys - components names as they
                defined in :class:`.WURI.Component`, values - corresponding values
                """
        self._WURI__components = {x:None for x in WURI.Component}
        for component_name, component_value in components.items():
            self.component(component_name, component_value)

    @verify_type(item=str)
    def __getattr__(self, item):
        """ Return component value by its name

                :param item: component name
                :return: str
                """
        try:
            components_fn = object.__getattribute__(self, WURI.component.__name__)
            item = WURI.Component(item)
            return lambda : components_fn(item)
        except ValueError:
            pass

        return object.__getattribute__(self, item)

    def __str__(self):
        """ Return string that represents this URI

                :return: str
                """
        netloc = ''
        username = self.username()
        if username is not None:
            netloc += username
        password = self.password()
        if password is not None:
            netloc += ':' + password
        if len(netloc) > 0:
            netloc += '@'
        hostname = self.hostname()
        if hostname is not None:
            netloc += hostname
        port = self.port()
        if port is not None:
            netloc += ':' + str(port)
        scheme = self.scheme()
        path = self.path()
        if len(netloc) == 0:
            if scheme is not None and path is not None:
                path = '//' + path
        return urlunsplit((
         scheme if scheme is not None else '',
         netloc,
         path if path is not None else '',
         self.query(),
         self.fragment()))

    @verify_type(component=(str, Component))
    def component(self, component, value=None):
        """ Set and/or get component value.

                :param component: component name to return
                :param value: if value is not None, this value will be set as a component value
                :return: str
                """
        if isinstance(component, str) is True:
            component = WURI.Component(component)
        if value is not None:
            self._WURI__components[component] = value
            return value
        return self._WURI__components[component]

    @classmethod
    @verify_type(uri=str)
    def parse(cls, uri):
        """ Parse URI-string and return WURI object

                :param uri: string to parse
                :return: WURI
                """
        uri_components = urlsplit(uri)
        adapter_fn = --- This code section failed: ---

 L. 143         0  LOAD_FAST                'x'
                3  LOAD_CONST               None
                6  COMPARE_OP               is-not
                9  POP_JUMP_IF_FALSE    55  'to 55'
               12  LOAD_GLOBAL              isinstance
               15  LOAD_FAST                'x'
               18  LOAD_GLOBAL              str
               21  CALL_FUNCTION_2       2  '2 positional, 0 named'
               24  LOAD_CONST               False
               27  COMPARE_OP               is
               30  JUMP_IF_TRUE_OR_POP    42  'to 42'
               33  LOAD_GLOBAL              len
               36  LOAD_FAST                'x'
               39  CALL_FUNCTION_1       1  '1 positional, 0 named'
             42_0  COME_FROM            30  '30'
               42  LOAD_CONST               0
               45  COMPARE_OP               >
             48_0  COME_FROM             9  '9'
               48  POP_JUMP_IF_FALSE    55  'to 55'
               51  LOAD_FAST                'x'
               54  RETURN_END_IF_LAMBDA
             55_0  COME_FROM            48  '48'
               55  LOAD_CONST               None
               58  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
        return cls(scheme=adapter_fn(uri_components.scheme), username=adapter_fn(uri_components.username), password=adapter_fn(uri_components.password), hostname=adapter_fn(uri_components.hostname), port=adapter_fn(uri_components.port), path=adapter_fn(uri_components.path), query=adapter_fn(uri_components.query), fragment=adapter_fn(uri_components.fragment))

    def __iter__(self):
        """ Iterate over URI components. This method yields tuple of component name and its value

                :return: generator
                """
        for component in WURI.Component:
            component_name = component.value
            component_value_fn = getattr(self, component_name)
            yield (component, component_value_fn())


class WSchemeSpecification:
    __doc__ = ' Specification for URI, that is described by scheme-component\n\t'

    class ComponentDescriptor(Enum):
        __doc__ = ' Value that describes component relation to a scheme specification\n\t\t'
        required = 0
        optional = 1
        unsupported = None

    @verify_type(scheme_name=str)
    def __init__(self, scheme_name, **descriptors):
        """ Create new scheme specification. Every component that was not described by this method is treated
                as unsupported

                :param scheme_name: URI scheme value
                :param descriptors: component names and its descriptors
                (:class:`.WSchemeSpecification.ComponentDescriptor`)
                """
        self._WSchemeSpecification__scheme_name = scheme_name
        self._WSchemeSpecification__descriptors = {x:WSchemeSpecification.ComponentDescriptor.unsupported for x in WURI.Component}
        self._WSchemeSpecification__descriptors[WURI.Component.scheme] = WSchemeSpecification.ComponentDescriptor.required
        for descriptor_name in descriptors.keys():
            component = WURI.Component(descriptor_name)
            if component == WURI.Component.scheme:
                raise TypeError('Scheme name can not be specified twice')
            descriptor = descriptors[descriptor_name]
            if isinstance(descriptor, WSchemeSpecification.ComponentDescriptor) is False:
                raise TypeError('Invalid "%s" descriptor type' % descriptor_name)
            self._WSchemeSpecification__descriptors[component] = descriptor

    def scheme_name(self):
        """ Return scheme name that this specification is describing

                :return: str
                """
        return self._WSchemeSpecification__scheme_name

    @verify_type(component=WURI.Component)
    def descriptor(self, component):
        """ Return descriptor for the specified component

                :param component: component name which descriptor should be returned
                :return: WSchemeSpecification.ComponentDescriptor
                """
        return self._WSchemeSpecification__descriptors[component]

    def __iter__(self):
        """ Iterate over URI components. This method yields tuple of component (:class:`.WURI.Component`) and
                its descriptor

                :return: generator
                """
        for component in WURI.Component:
            yield (
             component, self._WSchemeSpecification__descriptors[component])

    @verify_type(uri=WURI)
    def is_compatible(self, uri):
        """ Check if URI is compatible with this specification. Compatible URI has scheme name that matches
                specification scheme name, has all of the required components, does not have unsupported components
                and may have optional components

                :param uri: URI to check
                :return: bool
                """
        for component, component_value in uri:
            descriptor = self.descriptor(component)
            if component_value is None:
                if descriptor == WSchemeSpecification.ComponentDescriptor.required:
                    return False
            elif descriptor == WSchemeSpecification.ComponentDescriptor.unsupported:
                return False

        return True


class WSchemeHandler(metaclass=ABCMeta):
    __doc__ = ' Handler that do some work for compatible URI\n\t'

    @classmethod
    @abstractmethod
    def scheme_specification(cls):
        """ Return scheme specification

                :return: WSchemeSpecification
                """
        raise NotImplementedError('This method is abstract')

    @classmethod
    @abstractmethod
    @verify_type(uri=WURI)
    def create_handler(cls, uri, **kwargs):
        """ Return handler instance

                :param uri: original URI, that a handler is created for
                :param kwargs: additional arguments that may be used by a handler specialization

                :return: WSchemeHandler
                """
        raise NotImplementedError('This method is abstract')


class WSchemeCollection:
    __doc__ = ' Collection of URI scheme handlers, that is capable to process different WURI. Only one handler per scheme\n\tis supported. Suitable handler will be searched by a scheme name.\n\t'

    class NoHandlerFound(Exception):
        __doc__ = ' Exception that is raised when no handler is found for a URI\n\t\t'

        def __init__(self, uri):
            """ Create new exception object

                        :param uri: URI which scheme does not have a corresponding handler
                        """
            Exception.__init__(self, 'No handler was found for the specified URI: %s' % str(uri))

    class SchemeIncompatible(Exception):
        __doc__ = ' Exception that is raised when URI does not match a specification (:class:`.WSchemeSpecification`).\n\t\tThis happens if URI has unsupported components or does not have a required components.\n\t\t'

        def __init__(self, uri):
            """ Create new exception object

                        :param uri: URI that does not comply a handler specification (:class:`.WSchemeSpecification`)
                        """
            Exception.__init__(self, 'Handler was found for the specified scheme. But URI has not required components or has unsupported components: %s' % str(uri))

    def __init__(self, *scheme_handlers_cls, default_handler_cls=None):
        """ Create new collection

                :param scheme_handlers_cls: handlers to add to this collection
                :param default_handler: handler that must be called for a URI that does not have scheme component
                """
        self._WSchemeCollection__handlers_cls = []
        self._WSchemeCollection__default_handler_cls = default_handler_cls
        for handler_cls in scheme_handlers_cls:
            self.add(handler_cls)

    @verify_subclass(scheme_handler_cls=WSchemeHandler)
    def add(self, scheme_handler_cls):
        """ Append the specified handler to this collection

                :param scheme_handler_cls: handler that should be added
                :return: None
                """
        self._WSchemeCollection__handlers_cls.append(scheme_handler_cls)

    def handler(self, scheme_name=None):
        """ Return handler which scheme name matches the specified one

                :param scheme_name: scheme name to search for
                :return: WSchemeHandler class or None (if matching handler was not found)
                """
        if scheme_name is None:
            return self._WSchemeCollection__default_handler_cls
        for handler in self._WSchemeCollection__handlers_cls:
            if handler.scheme_specification().scheme_name() == scheme_name:
                return handler

    @verify_type(uri=WURI)
    def open(self, uri, **kwargs):
        """ Return handler instance that matches the specified URI. WSchemeCollection.NoHandlerFound and
                WSchemeCollection.SchemeIncompatible may be raised.

                :param uri: URI to search handler for
                :param kwargs: additional arguments that may be used by a handler specialization
                :return: WSchemeHandler
                """
        handler = self.handler(uri.scheme())
        if handler is None:
            raise WSchemeCollection.NoHandlerFound(uri)
        if uri.scheme() is None:
            uri.component('scheme', handler.scheme_specification().scheme_name())
        if handler.scheme_specification().is_compatible(uri) is False:
            raise WSchemeCollection.SchemeIncompatible(uri)
        return handler.create_handler(uri, **kwargs)