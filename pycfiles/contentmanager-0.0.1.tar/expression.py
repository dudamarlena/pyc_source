# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/contentlet/expression.py
# Compiled at: 2010-05-23 04:54:46
__doc__ = ' TALES expression.'
from zope.interface import providedBy
from chameleon.core import types
from chameleon.zpt import expressions
from repoze.bfg.threadlocal import get_current_request
from contentlet.provider import query_provider
__all__ = [
 'ProviderExpression']

def render_contentprovider(name):
    request = get_current_request()
    attrs = request.__dict__
    context = attrs.get('context')
    registry = attrs.get('registry')
    provider = query_provider(name, context=context, registry=registry)
    if provider is None:
        return ''
    else:
        return provider(context, request)


class ProviderExpression(expressions.ExpressionTranslator):
    """ TALES translator for executing content providers."""
    symbol = '_render_contentprovider'

    def translate(self, string, escape=None):
        value = types.value("%s('%s')" % (self.symbol, string))
        value.symbol_mapping[self.symbol] = render_contentprovider
        return value