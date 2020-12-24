# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/site/conditions.py
# Compiled at: 2020-02-11 04:03:56
"""Condition support for Local Sites."""
from __future__ import unicode_literals

class LocalSiteModelChoiceMixin(object):
    """Mixin to restrict model choices to those on a Local Site.

    This will ensure that any queries are bound to a
    :py:class:`~reviewboard.site.models.LocalSite`, if provided to the
    condition field widget through
    :py:attr:`~djblets.forms.widgets.ConditionsWidget.choice_kwargs`.
    """
    local_site_attr = b'local_site'

    def get_queryset(self):
        """Return a queryset for the choice.

        The queryset will take into account a LocalSite, if one is provided
        for the conditions.

        Returns:
            django.db.models.query.QuerySet:
            The queryset for the choice.
        """
        queryset = super(LocalSiteModelChoiceMixin, self).get_queryset()
        local_site = self.extra_state.get(b'local_site')
        if local_site:
            queryset = queryset.filter(**{self.local_site_attr: local_site})
        return queryset