# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/contentlet/configuration.py
# Compiled at: 2010-05-22 11:50:04
""" Configuration for content providers."""
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