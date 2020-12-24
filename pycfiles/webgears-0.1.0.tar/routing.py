# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romanmogilatov/ets-labs/webgears/webgears/routing.py
# Compiled at: 2016-02-05 11:27:08
"""Routing module."""
from werkzeug import routing
from webgears import errors

class Router(routing.Map):
    """General router."""

    def bind_rules_map(self, rules_map):
        """Bind rules map."""
        for rule in rules_map.rules:
            self.add(rule)


class RulesMap(object):
    """View providers catalog rules map."""
    views_catalog = None

    def __init__(self, rules, prefix=None):
        """Initializer."""
        self.rules = rules
        for rule in self.rules:
            rule.bind_to_catalog(self.__class__.views_catalog)
            if prefix:
                rule.rule = ('').join((prefix, rule.rule))

        super(RulesMap, self).__init__()


class Rule(routing.Rule):
    """View routing rule."""

    def __init__(self, string, view_provider, **kwargs):
        """Initializer."""
        self.view_provider = view_provider
        self.views_catalog = None
        super(Rule, self).__init__(string, **kwargs)
        return

    def bind_to_catalog(self, views_catalog):
        """Bind rule with views catalog."""
        if self.views_catalog:
            raise errors.Error(('{0} is already boud to {1}').format(self, self.views_catalog))
        self.views_catalog = views_catalog
        self.endpoint = ('.').join((
         self.views_catalog.__name__,
         views_catalog.get_provider_bind_name(self.view_provider)))


__all__ = ('Router', 'RulesMap', 'Rule')