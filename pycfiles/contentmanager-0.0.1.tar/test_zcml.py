# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/contentlet/tests/test_zcml.py
# Compiled at: 2010-05-22 12:33:11
__doc__ = ' Tests for contentlet.zcml.'
import unittest
from zope.interface import implements
from repoze.bfg import testing
from repoze.bfg.registry import Registry
from contentlet.interfaces import IContentProvider
__all__ = [
 'TestContentProviderDirective']

class TestContentProviderDirective(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()
        self.request = testing.DummyRequest()
        testing.setUp(registry=self.registry, request=self.request)

    def tearDown(self):
        testing.tearDown()

    def _callContentProvider(self, *args, **kwargs):
        from contentlet.zcml import contentprovider
        return contentprovider(*args, **kwargs)

    def _getProvider(self, name, context_iface=None):
        if context_iface is None:
            from zope.interface import Interface
            context_iface = Interface
        return self.registry.adapters.lookup((
         context_iface,), IContentProvider, name=name, default=None)

    def test_contentprovider_no_context(self):
        context = DummyContext()
        self._callContentProvider(context, DummyProvider('content'), 'name')
        self.assertEqual(len(context.actions), 1)
        action = context.actions[0]
        self.assertEqual(action['discriminator'], ('name', ))
        register = action['callable']
        register()
        provider = self._getProvider('name')
        self.assertNotEqual(provider, None)
        self.assertTrue(IContentProvider.providedBy(provider))
        self.assertEqual(provider(None, None), 'content')
        return

    def test_contentprovider_no_context(self):
        context = DummyContext()
        self._callContentProvider(context, DummyProvider('content'), 'name', context=DummyContext)
        self.assertEqual(len(context.actions), 1)
        action = context.actions[0]
        self.assertEqual(action['discriminator'], ('name', ))
        register = action['callable']
        register()
        provider = self._getProvider('name')
        self.assertEqual(provider, None)
        from zope.interface import implementedBy
        provider = self._getProvider('name', context_iface=implementedBy(DummyContext))
        self.assertNotEqual(provider, None)
        self.assertTrue(IContentProvider.providedBy(provider))
        self.assertEqual(provider(None, None), 'content')
        return


class DummyProvider(object):
    implements(IContentProvider)

    def __init__(self, content):
        self.content = content

    def __call__(self, context, request):
        return self.content


class DummyContext(object):
    pass


class DummyContext(object):

    def __init__(self):
        self.actions = []

    def action(self, discriminator, callable=None, args=(), kw={}, order=0):
        self.actions.append({'discriminator': discriminator, 'callable': callable, 
           'args': args, 
           'kw': kw})