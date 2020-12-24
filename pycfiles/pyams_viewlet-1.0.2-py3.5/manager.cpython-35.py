# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_viewlet/manager.py
# Compiled at: 2020-02-18 20:07:12
# Size of source mod 2**32: 12168 bytes
"""PyAMS_viewlet.manager module

This module defines the viewlet manager, as weel as a "viewletmanager_config" decorator
which can be used instead of ZCML to declare a viewlets manager.
"""
import logging, venusian
from pyramid.exceptions import ConfigurationError
from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.interfaces import IRequest, IView
from pyramid.threadlocal import get_current_registry
from zope.contentprovider.interfaces import BeforeUpdateEvent
from zope.interface import Interface, classImplements, implementer
from zope.interface.interfaces import ComponentLookupError
from zope.location.interfaces import ILocation
from pyams_template.template import get_view_template
from pyams_utils.request import check_request
from pyams_viewlet.interfaces import IViewlet, IViewletManager
__docformat__ = 'restructuredtext'
LOGGER = logging.getLogger('PyAMS (viewlet)')

@implementer(IViewletManager)
class ViewletManager:
    __doc__ = "The Viewlet Manager base\n\n    A generic manager class which can be instantiated.\n\n    A viewlet manager can be used as mapping and can get to a given viewlet by it's name.\n    "
    permission = None
    template = None
    viewlets = None

    def __init__(self, context, request, view):
        self._ViewletManager__updated = False
        self.__parent__ = view
        self.context = context
        self.request = request

    def __getitem__(self, name):
        """See zope.interface.common.mapping.IReadMapping"""
        registry = get_current_registry()
        viewlet = registry.queryMultiAdapter((self.context, self.request, self.__parent__, self), IViewlet, name=name)
        if viewlet is None:
            raise ComponentLookupError('No provider with name `%s` found.' % name)
        if viewlet.permission and not self.request.has_permission(viewlet.permission, context=self.context):
            raise HTTPUnauthorized('You are not authorized to access the provider called `%s`.' % name)
        return viewlet

    def get(self, name, default=None):
        """See zope.interface.common.mapping.IReadMapping"""
        try:
            return self[name]
        except (ComponentLookupError, HTTPUnauthorized):
            return default

    def __contains__(self, name):
        """See zope.interface.common.mapping.IReadMapping"""
        return bool(self.get(name, False))

    def filter(self, viewlets):
        """Filter out all content providers

        :param viewlets: list of viewlets, each element being a tuple of (name, viewlet) form

        Default implementation is filtering out viewlets for which a permission which is not
        granted to the current principal is defined.
        """
        request = self.request

        def _filter(viewlet):
            """Filter viewlet based on permission"""
            _, viewlet = viewlet
            return not viewlet.permission or request.has_permission(viewlet.permission, context=self.context)

        return filter(_filter, viewlets)

    def sort(self, viewlets):
        """Sort the viewlets.

        :param viewlets: list of viewlets, each element being a tuple of (name, viewlet) form

        Default implementation is sorting viewlets by name
        """
        return sorted(viewlets, key=lambda x: x[0])

    def _get_viewlets(self):
        """Find all content providers for the region"""
        registry = self.request.registry
        viewlets = registry.getAdapters((self.context, self.request, self.__parent__, self), IViewlet)
        viewlets = self.filter(viewlets)
        viewlets = self.sort(viewlets)
        return viewlets

    def _update_viewlets(self):
        """Calls update on all viewlets and fires events"""
        registry = self.request.registry
        for viewlet in self.viewlets:
            registry.notify(BeforeUpdateEvent(viewlet, self.request))
            viewlet.update()

    def update(self):
        """See :py:class:`zope.contentprovider.interfaces.IContentProvider`"""
        if self.permission and not self.request.has_permission(self.permission, context=self.context):
            return
        self.viewlets = []
        append = self.viewlets.append
        for name, viewlet in self._get_viewlets():
            if ILocation.providedBy(viewlet):
                viewlet.__name__ = name
            append(viewlet)

        self._update_viewlets()
        self._ViewletManager__updated = True

    def render(self):
        """See :py:class:`zope.contentprovider.interfaces.IContentProvider`"""
        if not (self._ViewletManager__updated and self.viewlets):
            return ''
        if self.template:
            return self.template(viewlets=self.viewlets)
        return '\n'.join([viewlet.render() for viewlet in self.viewlets])

    def reset(self):
        """Reset viewlet manager status"""
        self.viewlets = None
        self._ViewletManager__updated = False


def ViewletManagerFactory(name, interface, bases=(), cdict=None):
    """Viewlet manager factory"""
    attr_dict = {'__name__': name}
    attr_dict.update(cdict or {})
    if ViewletManager not in bases:
        if not (len(bases) == 1 and IViewletManager.implementedBy(bases[0])):
            bases = bases + (ViewletManager,)
    viewlet_manager_class = type('<ViewletManager providing %s>' % interface.getName(), bases, attr_dict)
    classImplements(viewlet_manager_class, interface)
    return viewlet_manager_class


def get_weight(item):
    """Get sort weight of a given viewlet"""
    _, viewlet = item
    try:
        return int(viewlet.weight)
    except (TypeError, AttributeError):
        return 0


def get_label(item, request=None):
    """Get sort label of a given viewlet"""
    _, viewlet = item
    try:
        if request is None:
            request = check_request()
        return request.localizer.translate(viewlet.label)
    except AttributeError:
        return '--'


def get_weight_and_label(item, request=None):
    """Get sort weight and label of a given viewlet"""
    return (
     get_weight(item), get_label(item, request))


class WeightOrderedViewletManager(ViewletManager):
    __doc__ = 'Weight ordered viewlet managers.\n\n    Viewlets with the same weight are sorted by label\n    '

    def sort(self, viewlets):
        return sorted(viewlets, key=lambda x: get_weight_and_label(x, request=self.request))


class ConditionalViewletManager(WeightOrderedViewletManager):
    __doc__ = 'Conditional weight ordered viewlet managers'

    def filter(self, viewlets):
        """Sort out all viewlets which are explicitly not available

        Viewlets shoud have a boolean "available" attribute to specify if they are available
        or not.
        """

        def is_available(viewlet):
            _, viewlet = viewlet
            try:
                return (not viewlet.permission or viewlet.request.has_permission(viewlet.permission, context=viewlet.context)) and viewlet.available
            except AttributeError:
                return True

        return filter(is_available, viewlets)


class TemplateBasedViewletManager:
    __doc__ = 'Template based viewlet manager mixin class'
    template = get_view_template()


class viewletmanager_config:
    __doc__ = "Class or interface decorator used to declare a viewlet manager\n\n    You can provide same arguments as in 'viewletManager' ZCML directive:\n    :param name: name of the viewlet; may be unique for a given viewlet manager\n    :param view: the view class or interface for which viewlet is displayed\n    :param for_: the context class or interface for which viewlet is displayed\n    :param permission: name of a permission required to display the viewlet\n    :param layer: request interface required to display the viewlet\n    :param class_: the class handling the viewlet manager; if the decorator is applied\n        on an interface and if this argument is not provided, the viewlet manager\n        will be handled by a default ViewletManager class\n    :param provides: an interface the viewlet manager provides; if the decorator is\n        applied on an Interface, this will be the decorated interface; if the\n        decorated is applied on a class and if this argument is not specified,\n        the manager will provide IViewletManager interface.\n    "
    venusian = venusian

    def __init__(self, **settings):
        if not settings.get('name'):
            raise ConfigurationError('You must provide a name for a ViewletManager')
        if 'for_' in settings and settings.get('context') is None:
            settings['context'] = settings['for_']
        self.__dict__.update(settings)

    def __call__(self, wrapped):
        settings = self.__dict__.copy()

        def callback(context, name, obj):
            cdict = {'__name__': settings.get('name')}
            if 'permission' in settings:
                cdict['permission'] = settings.get('permission')
            if issubclass(obj, Interface):
                class_ = settings.get('class_', ViewletManager)
                provides = obj
            else:
                class_ = obj
                provides = settings.get('provides', IViewletManager)
            new_class = ViewletManagerFactory(settings.get('name'), provides, (class_,), cdict)
            LOGGER.debug('Registering viewlet manager {0} ({1})'.format(settings.get('name'), str(new_class)))
            registry = settings.get('registry')
            if registry is None:
                config = context.config.with_package(info.module)
                registry = config.registry
            registry.registerAdapter(new_class, (
             settings.get('context', Interface),
             settings.get('layer', IRequest),
             settings.get('view', IView)), provides, settings.get('name'))

        info = self.venusian.attach(wrapped, callback, category='pyams_viewlet')
        if info.scope == 'class' and settings.get('attr') is None:
            settings['attr'] = wrapped.__name__
        settings['_info'] = info.codeinfo
        return wrapped