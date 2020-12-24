# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/registry.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 9222 bytes
__doc__ = 'PyAMS_utils.registry module\n\nThis package is used to manage a *local registry*. A local registry is a *site management* component\ncreated automatically on application startup by PyAMS_utils package. It can be used to store and\nregister components, mainly persistent utilities which are created and configured dynamically by a\nsite administrator; this can include SQLAlchemy engines, ZEO connections, and several PyAMS\nutilities like security manager, medias converter, tasks scheduler and many other ones.\n\nSee :ref:`zca` to get a brief introduction about using a local registry with PyAMS packages.\n'
import logging, threading, venusian
from ZODB.POSException import POSError
from pyramid.events import subscriber
from pyramid.interfaces import INewRequest
from pyramid.threadlocal import get_current_registry as get_request_registry, manager
from zope.component.globalregistry import getGlobalSiteManager
from zope.component.interfaces import ISite
from zope.interface import implementedBy, providedBy
from zope.interface.interfaces import ComponentLookupError
from zope.traversing.interfaces import IBeforeTraverseEvent
__docformat__ = 'restructuredtext'
LOGGER = logging.getLogger('PyAMS (utils)')

class LocalRegistry(threading.local):
    """LocalRegistry"""
    _registry = None

    def get_registry(self):
        """Return local registry"""
        return self._registry

    def set_registry(self, registry):
        """Define local registry"""
        self._registry = registry


local_registry = LocalRegistry()

def get_local_registry():
    """Get local registry

    Local registry is automatically defined while traversing a site manager.
    """
    return local_registry.get_registry()


def set_local_registry(registry):
    """Define local registry"""
    local_registry.set_registry(registry)


@subscriber(INewRequest)
def handle_new_request(event):
    """New request event subscriber

    Is used to initialize local registry to None for any new request
    """
    set_local_registry(None)


@subscriber(IBeforeTraverseEvent, context_selector=ISite)
def handle_site_before_traverse(event):
    """Before traverse event subscriber

    Define site's local registry when an object implementing ISite is traversed
    """
    set_local_registry(event.object.getSiteManager())


def get_registries():
    """Iterator on components registries

    Returns an iterator on current local registry (if any) and registries associated
    in current thread stack.
    """
    seen = []
    append = seen.append
    registry = local_registry.get_registry()
    if registry is not None:
        yield registry
        append(registry)
    for entry in reversed(manager.stack):
        stack_registry = entry.get('registry')
        if stack_registry is not None and stack_registry not in seen:
            yield stack_registry
            append(stack_registry)


def get_global_registry():
    """Get global registry"""
    return getGlobalSiteManager()


def get_current_registry(context=None):
    """Get current or global registry

    The function is looking for given request registry.
    If registry is None, returns the global registry.
    """
    registry = get_request_registry(context)
    if registry is None:
        registry = get_global_registry()
    return registry


def registered_utilities():
    """Get utilities registrations as generator

    Iterates over utilities defined in all registries, starting with local ones.
    """
    for registry in get_registries():
        for utility in registry.registeredUtilities():
            yield utility


def query_utility(provided, name='', default=None):
    """Query utility registered with given interface

    Do a registry lookup for given utility into local registry first, then on each registry
    associated with current thread stack.

    :param Interface provided: the requested interface
    :param str name: name of the requested utility
    :param object default: the default object returned if the requested utility can't be found
    :return: object; the requested object, or *default* if it can't be found
    """
    try:
        for registry in get_registries():
            utility = registry.queryUtility(provided, name, default)
            if utility is not None:
                return utility

    except POSError:
        pass

    return default


def get_utility(provided, name=''):
    """Get utility registered with given interface

    Do a registry lookup for given utility into local registry first, then on each registry
    associated with current thread stack.

    :param Interface provided: the requested interface
    :param str name: name of the requested utility
    :return: object; the requested object. A *ComponentLookupError* is raised if the utility
        can't be found.
    """
    for registry in get_registries():
        utility = registry.queryUtility(provided, name)
        if utility is not None:
            return utility

    raise ComponentLookupError(provided, name)


def get_utilities_for(interface):
    """Get utilities registered with given interface as (name, util) tuples iterator

    Do a registry lookup for matching utilities into local registry first, then on each registry
    associated with current thread stack.
    """
    for registry in get_registries():
        for utility in registry.getUtilitiesFor(interface):
            yield utility


def get_all_utilities_registered_for(interface):
    """Get list of registered utilities for given interface

    Do a registry lookup for matching utilities into local registry first, then on each registry
    associated with current thread stack.
    """
    result = []
    for registry in get_registries():
        for utilities in registry.getAllUtilitiesRegisteredFor(interface):
            result.append(utilities)

    return result


class utility_config:
    """utility_config"""
    venusian = venusian

    def __init__(self, **settings):
        self.__dict__.update(settings)

    def __call__(self, wrapped):
        settings = self.__dict__.copy()
        depth = settings.pop('_depth', 0)

        def callback(context, name, obj):
            if isinstance(obj, type):
                factory = obj
                component = None
            else:
                factory = None
                component = obj
            provides = settings.get('provides')
            if provides is None:
                if factory:
                    provides = list(implementedBy(factory))
                else:
                    provides = list(providedBy(component))
                if len(provides) == 1:
                    provides = provides[0]
            else:
                raise TypeError("Missing 'provides' argument")
            LOGGER.debug("Registering utility {0} named '{1}' providing {2}".format(str(component) if component else str(factory), settings.get('name', ''), str(provides)))
            registry = settings.get('registry')
            if registry is None:
                config = context.config.with_package(info.module)
                registry = config.registry
            registry.registerUtility(component=component, factory=factory, provided=provides, name=settings.get('name', ''))

        info = self.venusian.attach(wrapped, callback, category='pyams_utility', depth=depth + 1)
        if info.scope == 'class' and settings.get('attr') is None:
            settings['attr'] = wrapped.__name__
        settings['_info'] = info.codeinfo
        return wrapped