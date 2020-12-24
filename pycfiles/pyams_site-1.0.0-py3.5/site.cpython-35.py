# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_site/site.py
# Compiled at: 2019-12-16 03:44:54
# Size of source mod 2**32: 4351 bytes
"""PyAMS_site.site module

This module provides all site-related features, like Pyramid's site factory and BaseSiteRoot
which is the base implementation of any website or application.
"""
from pyramid.exceptions import NotFound
from pyramid.path import DottedNameResolver
from pyramid.security import ALL_PERMISSIONS, Allow, Everyone
from pyramid_zodbconn import get_connection
from zope.component import hooks
from zope.component.interfaces import IPossibleSite
from zope.interface import implementer
from zope.site import LocalSiteManager
from zope.site.folder import Folder
from zope.traversing.interfaces import ITraversable
from pyams_site.interfaces import IConfigurationManager, ISiteRoot, ISiteRootFactory, NewLocalSiteCreatedEvent, PYAMS_APPLICATION_DEFAULT_NAME, PYAMS_APPLICATION_FACTORY_KEY, PYAMS_APPLICATION_SETTINGS_KEY
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.registry import get_current_registry
__docformat__ = 'restructuredtext'

@implementer(ISiteRoot, IConfigurationManager)
class BaseSiteRoot(Folder):
    __doc__ = "Default site root\n\n    A site root can be used as base application root in your ZODB.\n    It's also site root responsibility to manage your local site manager.\n\n    BaseSiteRoot defines a basic ACL which gives all permissions to system administrator,\n    and 'public' permission to everyone. But this ACL is generally overriden in subclasses\n    which also inherit from :py:class:`ProtectedObjectMixin\n    <pyams_security.security.ProtectedObjectMixin>`.\n    "
    __acl__ = [
     (
      Allow, 'system:admin', ALL_PERMISSIONS),
     (
      Allow, Everyone, {'public'})]
    config_klass = None


@adapter_config(name='etc', context=ISiteRoot, provides=ITraversable)
class SiteRootEtcTraverser(ContextAdapter):
    __doc__ = 'Site root ++etc++ namespace traverser\n\n    Gives access to local site manager from */++etc++site* URL\n    '

    def traverse(self, name, furtherpath=None):
        """Traverse to site manager;
        see :py:class:`ITraversable <zope.traversing.interfaces.ITraversable>`"""
        if name == 'site':
            return self.context.getSiteManager()
        raise NotFound


def site_factory(request):
    """Application site factory

    On application startup, this factory checks configuration to get application name and
    load it from the ZODB; if the application can't be found, configuration is scanned to
    get application factory, create a new one and create a local site manager.
    """
    conn = get_connection(request)
    root = conn.root()
    application_key = request.registry.settings.get(PYAMS_APPLICATION_SETTINGS_KEY, PYAMS_APPLICATION_DEFAULT_NAME)
    application = root.get(application_key)
    if application is None:
        factory = request.registry.settings.get(PYAMS_APPLICATION_FACTORY_KEY)
        if factory:
            resolver = DottedNameResolver()
            factory = resolver.maybe_resolve(factory)
        else:
            factory = request.registry.queryUtility(ISiteRootFactory, default=BaseSiteRoot)
        application = root[application_key] = factory()
        if IPossibleSite.providedBy(application):
            lsm = LocalSiteManager(application, default_folder=False)
            application.setSiteManager(lsm)
        try:
            hooks.setSite(application)
            get_current_registry().notify(NewLocalSiteCreatedEvent(application))
        finally:
            hooks.setSite(None)

        import transaction
        transaction.commit()
    return application