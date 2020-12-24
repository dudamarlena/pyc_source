# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/contentlet/zcml.py
# Compiled at: 2010-05-22 11:50:36
__doc__ = ' ZCML directives.'
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