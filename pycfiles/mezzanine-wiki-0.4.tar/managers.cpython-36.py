# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\landon\dropbox\documents\pycharmprojects\mezzanine-wiki\mezzanine_wiki\managers.py
# Compiled at: 2018-01-31 09:14:33
# Size of source mod 2**32: 1694 bytes
from django.db.models import Manager, Q, CharField, TextField
from django.apps import apps
from mezzanine.conf import settings
from mezzanine.core.managers import CurrentSiteManager, SearchableManager
from django.utils.timezone import now
get_models = apps.get_models

class PublishedManager(Manager):
    __doc__ = '\n    Provides filter for restricting items returned by status and\n    publish date when the given user is not a staff member.\n    '

    def published(self, for_user=None):
        """
        For non-staff users, return items with a published status and
        whose publish and expiry dates fall before and after the
        current date when specified.
        """
        from mezzanine.core.models import CONTENT_STATUS_PUBLISHED, CONTENT_STATUS_DRAFT
        if for_user is not None:
            if for_user.is_staff:
                return self.all()
        elif for_user is not None and for_user.has_perm('mezzanine_wiki.view_wikipage'):
            status_filter = Q(status=CONTENT_STATUS_PUBLISHED) | Q(status=CONTENT_STATUS_DRAFT)
        else:
            status_filter = Q(status=CONTENT_STATUS_PUBLISHED)
        return self.filter(Q(publish_date__lte=(now())) | Q(publish_date__isnull=True), Q(expiry_date__gte=(now())) | Q(expiry_date__isnull=True), status_filter)

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class DisplayableManager(CurrentSiteManager, PublishedManager, SearchableManager):
    __doc__ = '\n    Manually combines ``CurrentSiteManager``, ``PublishedManager``\n    and ``SearchableManager`` for the ``Displayable`` model.\n\n    '