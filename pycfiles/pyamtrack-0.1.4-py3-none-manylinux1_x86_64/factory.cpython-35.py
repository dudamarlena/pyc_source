# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/factory.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 6110 bytes
__doc__ = 'PyAMS_utils.factory module\n\nThis module provides a decorator and a small set of functions to handle object factories.\n\nInstead of directly using a class as an object factory, the object of this module is to\nlet you create an object based on an interface. The first step is to create an object\nimplementing this interface, and then to register it as a factory:\n\n.. code-block:: python\n\n    @implementer(IMyInterface)\n    class MyClass(object):\n        \'\'\'Class implementing my interface\'\'\'\n\n    register_factory(IMyInterface, MyClass)\n\nFactory registry can also be handle by a decorator called "factory_config":\n\n.. code-block:: python\n\n    @factory_config(IMyInterface)\n    class MyClass(object):\n        \'\'\'Class implementing my interface\'\'\'\n\nA class declared as factory for a specific interface automatically implements the given interface.\nYou can also provide a tuple or set of interfaces in "factory_config()" decorator.\n\nWhen a factory is registered, you can look for a factory:\n\n.. code-block:: python\n\n    factory = get_object_factory(IMyInterface)\n    if factory is not None:\n        myobject = factory()\n    else:\n        myobject = MyDefaultImplementation()\n\nBy registering their own objects factories, extension packages can easily provide their\nown implementation of any PyAMS interface handled by factories.\n'
import logging, venusian
from zope.component import adapter
from zope.interface import Interface, classImplements, implementer
from zope.interface.interface import InterfaceClass
from pyams_utils.interfaces import IObjectFactory
from pyams_utils.registry import get_global_registry
__docformat__ = 'restructuredtext'
LOGGER = logging.getLogger('PyAMS (utils)')

def is_interface(obj):
    """Check if given object is an interface"""
    return issubclass(obj.__class__, InterfaceClass)


def get_interface_name(iface):
    """Get interface full name"""
    return iface.__module__ + '.' + iface.__name__


@adapter(Interface)
@implementer(IObjectFactory)
class ObjectFactoryAdapter:
    """ObjectFactoryAdapter"""
    factory = None

    def __init__(self, context):
        self.context = context

    def __call__(self, *args, **kwargs):
        return self.factory(*args, **kwargs)


def register_factory(interface, klass, registry=None, name=''):
    """Register factory for a given interface

    :param interface: the interface for which the factory is registered
    :param klass: the object factory
    :param registry: the registry into which factory adapter should be registered; if None, the
        global registry is used
    :param name: custom name given to registered factory
    """

    class Temp(ObjectFactoryAdapter):
        """register_factory.<locals>.Temp"""
        classImplements(klass, interface)
        factory = klass

    if_name = get_interface_name(interface)
    if name:
        if_name = '{0}::{1}'.format(if_name, name)
    if registry is None:
        registry = get_global_registry()
    registry.registerAdapter(Temp, name=if_name)


class factory_config:
    """factory_config"""
    venusian = venusian

    def __init__(self, provided, **settings):
        settings['provided'] = provided
        self.__dict__.update(settings)

    def __call__(self, wrapped):
        settings = self.__dict__.copy()
        depth = settings.pop('_depth', 0)

        def callback(context, name, obj):
            factory_name = settings.get('name', '')
            provided = settings.get('provided')
            if not provided:
                raise TypeError('No provided interface(s) was given for registered factory %r' % obj)
            if not isinstance(provided, tuple):
                provided = (
                 provided,)
            config = context.config.with_package(info.module)
            for interface in provided:
                if name:
                    LOGGER.debug('Registering factory %s for interface %s with name %s', str(obj), str(interface), factory_name)
                else:
                    LOGGER.debug('Registering default factory %s for interface %s', str(obj), str(interface))
                register_factory(interface, obj, config.registry, factory_name)

        info = self.venusian.attach(wrapped, callback, category='pyams_factory', depth=depth + 1)
        if info.scope == 'class' and settings.get('attr') is None:
            settings['attr'] = wrapped.__name__
        settings['_info'] = info.codeinfo
        return wrapped


def get_object_factory(interface, registry=None, name=''):
    """Get registered factory for given interface

    :param interface: the interface for which a factory is requested
    :param registry: the registry into which registered factory should be looked for
    :param name: name of requested factory
    :return: the requested object factory, or None if it can't be found
    """
    if_name = get_interface_name(interface)
    if name:
        if_name = '{0}::{1}'.format(if_name, name)
    if registry is None:
        registry = get_global_registry()
    return registry.queryAdapter(interface, IObjectFactory, name=if_name)