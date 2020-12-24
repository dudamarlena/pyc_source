# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_i18n/attr.py
# Compiled at: 2020-02-20 11:01:05
# Size of source mod 2**32: 2950 bytes
"""PyAMS_i18n.attr module

This module provides the main II18n adapter, which is used to get value of translated properties.
"""
from pyramid.exceptions import NotFound
from zope.interface import Interface
from zope.traversing.interfaces import ITraversable
from pyams_i18n.interfaces import II18n, INegotiator
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.registry import query_utility
from pyams_utils.request import check_request
__docformat__ = 'restructuredtext'

@adapter_config(name='i18n', context=Interface, provides=ITraversable)
class I18nAttributeTraverser(ContextAdapter):
    __doc__ = '++i18n++attr:lang namespace traverser\n\n    This traverser is used, for example, by I18n file fields (see :py:mod:pyams_file).\n    '

    def traverse(self, name, furtherpath=None):
        """Traverse to selected attribute"""
        try:
            attr, lang = name.split(':')
            return getattr(self.context, attr, {}).get(lang)
        except AttributeError:
            raise NotFound


@adapter_config(context=Interface, provides=II18n)
class I18nAttributeAdapter(ContextAdapter):
    __doc__ = 'I18n attribute adapter'

    def get_attribute(self, attribute, lang=None, request=None, default=None):
        """Extract attribute value for given language or request"""
        result = getattr(self.context, attribute)
        if not isinstance(result, dict):
            return default
        if lang is None:
            if request is None:
                request = check_request()
            lang = request.params.get('lang') or request.locale_name
        return result.get(lang, default)

    def query_attribute(self, attribute, lang=None, request=None):
        """Extract attribute value for given language or request

        If value is empty or None, value associated to server language is returned.
        """
        result = getattr(self.context, attribute)
        if not isinstance(result, dict):
            return result
        if lang is None:
            if request is None:
                request = check_request()
            lang = request.params.get('lang') or request.locale_name
        value = result.get(lang)
        if not value:
            negotiator = query_utility(INegotiator)
            if negotiator is not None and negotiator.server_language != lang:
                value = result.get(negotiator.server_language)
        return value