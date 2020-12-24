# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_site/site.py
# Compiled at: 2019-12-16 03:44:54
# Size of source mod 2**32: 4351 bytes
__doc__ = "PyAMS_site.site module\n\nThis module provides all site-related features, like Pyramid's site factory and BaseSiteRoot\nwhich is the base implementation of any website or application.\n"
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
    """BaseSiteRoot"""
    __acl__ = [
     (
      Allow, 'system:admin', ALL_PERMISSIONS),
     (
      Allow, Everyone, {'public'})]
    config_klass = None


@adapter_config(name='etc', context=ISiteRoot, provides=ITraversable)
class SiteRootEtcTraverser(ContextAdapter):
    """SiteRootEtcTraverser"""

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