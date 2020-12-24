# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/contentlet/tests/test_expression.py
# Compiled at: 2010-05-23 04:43:23
__doc__ = ' Tests for contentlet.expressions.'
import unittest
from repoze.bfg.registry import Registry
from repoze.bfg import testing
__all__ = [
 'TestProviderExpression']

class DummyProvider(object):

    def __init__(self, content):
        self.content = content

    def __call__(self, context, request):
        return self.content


class TestProviderExpression(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()
        request = testing.DummyRequest()
        request.registry = self.registry
        request.context = None
        testing.setUp(registry=self.registry, request=request)
        return

    def _registerTranslator(self, translator):
        from chameleon.zpt.interfaces import IExpressionTranslator
        self.registry.registerUtility(translator, IExpressionTranslator, name='contentprovider')

    def _registerProvider(self, provider, name, context_iface=None):
        from zope.interface import Interface
        from contentlet.interfaces import IContentProvider
        if context_iface is None:
            context_iface = Interface
        self.registry.registerAdapter(provider, (context_iface,), IContentProvider, name=name)
        return

    def tearDown(self):
        testing.tearDown()

    def test_it(self):
        from contentlet.expression import ProviderExpression
        self._registerTranslator(ProviderExpression())
        self._registerProvider(DummyProvider('content'), 'name')
        from chameleon.zpt.template import PageTemplate
        template = PageTemplate('        <div tal:replace="contentprovider:name">\n          Hello World!\n        </div>', None)
        rendered = template()
        self.assertEqual(rendered, 'content')
        return

    def test_no_provider(self):
        from contentlet.expression import ProviderExpression
        self._registerTranslator(ProviderExpression())
        from chameleon.zpt.template import PageTemplate
        template = PageTemplate('        <div tal:replace="contentprovider:name">\n          Hello World!\n        </div>', None)
        rendered = template()
        self.assertEqual(rendered, '')
        return