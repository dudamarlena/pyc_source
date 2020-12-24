# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/contentlet/configuration.py
# Compiled at: 2010-05-22 11:50:04
__doc__ = ' Configuration for content providers.'
from zope.interface import Interface
from zope.interface import implementedBy
from zope.interface.interfaces import IInterface
from repoze.bfg.registry import Registry
from contentlet.interfaces import IContentProvider
__all__ = [
 'Configurator',
 'ContentletConfiguratorMixin']

class ContentletConfiguratorMixin(object):
    """ Mixin for using with repoze.bfg.configuration.Configurator."""

    def add_content_provider(self, provider, name, context=None):
        """ Add content provider."""
        if context is None:
            context = Interface
        if not IInterface.providedBy(context):
            context = implementedBy(context)
        self.registry.registerAdapter(provider, (context,), IContentProvider, name=name)
        return


class Configurator(ContentletConfiguratorMixin):
    """ Configurator for contentlet."""

    def __init__(self, registry=None):
        if registry is None:
            registry = Registry()
        self.registry = registry
        return