# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/adapter.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 7493 bytes
"""Adapters management package

This package provides a small set of standard base adapters for *context*, *context* and *request*,
and *context* and *request* and *view*.

See :ref:`zca` to see how PyAMS can help components management.
"""
import logging
from inspect import isclass
import venusian
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides, classImplements, implementedBy
from zope.lifecycleevent import ObjectCreatedEvent
from zope.location import locate as zope_locate
from pyams_utils.factory import get_object_factory, is_interface
from pyams_utils.registry import get_current_registry
__docformat__ = 'restructuredtext'
LOGGER = logging.getLogger('PyAMS (utils)')

class ContextAdapter:
    __doc__ = 'Context adapter'

    def __init__(self, context):
        self.context = context


class ContextRequestAdapter:
    __doc__ = 'Context + request multi-adapter'

    def __init__(self, context, request):
        self.context = context
        self.request = request


class ContextRequestViewAdapter:
    __doc__ = 'Context + request + view multi-adapter'

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view


class NullAdapter:
    __doc__ = 'An adapter which always return None!\n\n    Can be useful to override a default adapter...\n    '

    def __new__(cls, *args, **kwargs):
        pass


class adapter_config:
    __doc__ = "Function or class decorator to declare an adapter\n\n    Annotation parameters can be:\n\n    :param str='' name: name of the adapter\n    :param [Interface...] required: an interface, or a tuple of interfaces, that the component\n        adapts; 'adapts' and 'context' are synonyms for 'required' argument name\n    :param Interface provided: the interface that the adapter provides; 'provides' is a synonym\n        for 'provided' argument name\n    :param registry: the registry into which adapter registration should be made\n    "
    venusian = venusian

    def __init__(self, **settings):
        if 'for_' in settings and settings.get('required') is None:
            settings['required'] = settings.pop('for_')
        self.__dict__.update(settings)

    def __call__(self, wrapped):
        settings = self.__dict__.copy()
        depth = settings.pop('_depth', 0)

        def callback(context, name, obj):
            required = settings.get('required') or settings.get('adapts') or settings.get('context')
            if required is None:
                required = getattr(obj, '__component_adapts__', None)
                if required is None:
                    raise TypeError("No for argument was provided for %r and can't determine what the factory adapts." % obj)
            if not isinstance(required, tuple):
                required = (
                 required,)
            provided = settings.get('provided') or settings.get('provides')
            if provided is None:
                intfs = list(implementedBy(obj))
                if len(intfs) == 1:
                    provided = intfs[0]
                if provided is None:
                    raise TypeError("Missing 'provided' argument")
                if isclass(obj) and not provided.implementedBy(obj):
                    classImplements(obj, provided)
            LOGGER.debug('Registering adapter %s for %s providing %s', str(obj), str(required), str(provided))
            registry = settings.get('registry')
            if registry is None:
                config = context.config.with_package(info.module)
                registry = config.registry
            registry.registerAdapter(obj, required, provided, settings.get('name', ''))

        info = self.venusian.attach(wrapped, callback, category='pyams_utils', depth=depth + 1)
        if info.scope == 'class' and settings.get('attr') is None:
            settings['attr'] = wrapped.__name__
        settings['_info'] = info.codeinfo
        return wrapped


def get_annotation_adapter(context, key, factory=None, markers=None, notify=True, locate=True, parent=None, name=None, callback=None, **kwargs):
    """Get an adapter via object's annotations, creating it if not existent

    :param object context: context object which should be adapted
    :param str key: annotations key to look for
    :param factory: if annotations key is not found, this is the factory which will be used to
        create a new object; factory can be a class or callable object, or an interface for which
        a factory has been registered; if factory is None and is requested object can't be found,
        None is returned
    :param markers: if not None, list of marker interfaces which created adapter should provide
    :param bool=True notify: if 'False', no notification event will be sent on object creation
    :param bool=True locate: if 'False', the new object is not attached to any parent
    :param object=None parent: parent to which new object is attached; if None, object is
        attached to context
    :param str=None name: if locate is not False, this is the name with which the new object is
        attached to it's parent
    :param callback: if not None, callback function which will be called after object creation
    """
    annotations = IAnnotations(context, None)
    if annotations is None:
        return
    adapter = annotations.get(key)
    if adapter is None:
        if 'default' in kwargs:
            return kwargs['default']
        if factory is None:
            return
        if is_interface(factory):
            factory = get_object_factory(factory, registry=kwargs.get('registry'))
            assert factory is not None, 'Missing object factory'
        adapter = annotations[key] = factory()
        if markers:
            if not isinstance(markers, (list, tuple, set)):
                markers = {
                 markers}
            for marker in markers:
                alsoProvides(adapter, marker)

        if notify:
            get_current_registry().notify(ObjectCreatedEvent(adapter))
        if locate:
            zope_locate(adapter, context if parent is None else parent, name)
        if callback:
            callback(adapter)
    return adapter


def get_adapter_weight(item):
    """Get adapters weight sort key"""
    name, adapter = item
    try:
        return (
         int(adapter.weight), name)
    except (TypeError, AttributeError):
        return (
         0, name)