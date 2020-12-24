# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_site/interfaces.py
# Compiled at: 2019-12-06 19:40:43
# Size of source mod 2**32: 2056 bytes
"""PyAMS_site.interfaces module

"""
from zope.annotation import IAttributeAnnotatable
from zope.interface import Attribute, Interface, implementer
from zope.interface.interfaces import IObjectEvent, ObjectEvent
PYAMS_APPLICATION_SETTINGS_KEY = 'pyams.application_name'
PYAMS_APPLICATION_DEFAULT_NAME = 'application'
PYAMS_APPLICATION_FACTORY_KEY = 'pyams.application_factory'

class ISiteRoot(IAttributeAnnotatable):
    __doc__ = 'Marker interface for site root'


class ISiteRootFactory(Interface):
    __doc__ = 'Site root utility factory interface'


class INewLocalSiteCreatedEvent(IObjectEvent):
    __doc__ = 'Event interface when a new site root has been created'


@implementer(INewLocalSiteCreatedEvent)
class NewLocalSiteCreatedEvent(ObjectEvent):
    __doc__ = 'New local site creation event'


class IConfigurationManager(Interface):
    __doc__ = 'Configuration manager marker interface'


class ISiteUpgradeEvent(IObjectEvent):
    __doc__ = 'Event interface when a site upgrade is requested'


@implementer(ISiteUpgradeEvent)
class SiteUpgradeEvent(ObjectEvent):
    __doc__ = 'Site upgrade request event'


SITE_GENERATIONS_KEY = 'pyams.generations'

class ISiteGenerations(Interface):
    __doc__ = 'Site generations interface'
    order = Attribute('Order in which generations should be upgraded')
    generation = Attribute('Current schema generation')

    def evolve(self, site, current=None):
        """Evolve database from current generation to last one"""
        pass