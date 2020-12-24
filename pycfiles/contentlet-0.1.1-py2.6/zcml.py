# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/contentlet/zcml.py
# Compiled at: 2010-05-22 11:50:36
""" ZCML directives."""
from zope.interface import Interface
from zope.configuration.fields import GlobalObject
from zope.schema import TextLine
from repoze.bfg.threadlocal import get_current_registry
from contentlet.configuration import Configurator
__all__ = [
 'IContentProviderDirective',
 'contentprovider']

class IContentProviderDirective(Interface):
    provider = GlobalObject(title='Content provider to be registered.', required=True)
    name = TextLine(title='The name of the content provider.', required=True)
    context = GlobalObject(title='Context type or interface for which content provider register.', required=False)


def contentprovider(_context, provider=None, name=None, context=None):
    registry = get_current_registry()

    def register():
        config = Configurator(registry)
        config.add_content_provider(provider, name, context=context)

    _context.action(discriminator=(
     name,), callable=register)