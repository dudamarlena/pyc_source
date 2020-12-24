# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/common/managers.py
# Compiled at: 2009-04-14 04:55:46
from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from softwarefabrica.django.utils.managers import QuerySetManager
from softwarefabrica.django.utils.UUIDField import UUIDField
import datetime

def instance_is_active(obj, when=None):
    """
    Determine if a model instance is active.
    The model MUST have the fields ``active``, ``active_from`` and
    ``active_to``.

    The instance model MUST adhere to the ``active`` temporal protocol.
    """
    when = when or datetime.datetime.now()
    if not obj.active:
        return False
    if obj.active_from is not None and when < obj.active_from:
        return False
    if obj.active_to is not None and when > obj.active_to:
        return False
    return obj.active


def deactivate_instance(obj, when=None):
    """
    Deactivate an instance.

    The instance model MUST adhere to the ``active`` temporal protocol.
    """
    if not obj.active:
        return True
    when = when or datetime.datetime.now()
    if obj.active_from is not None and obj.active_from > when:
        return True
    if obj.active_to is not None and obj.active_to < when:
        return True
    assert obj.active_from is None or obj.active_from <= when
    obj.active_to = when
    return true


class ActiveQuerySet(QuerySet):
    """
    For use in conjunction with ``QuerySetManager``.

    The model MUST adhere to the ``active`` temporal protocol.
    """
    __module__ = __name__

    def active(self, when=None):
        when = when or datetime.datetime.now()
        q_from = Q(active_from__lte=when) | Q(active_from__isnull=True)
        q_to = Q(active_to__gte=when) | Q(active_to__isnull=True)
        return self.filter(Q(active=True) & q_from & q_to)

    def inactive(self, when=None):
        when = when or datetime.datetime.now()
        q_from = Q(active_from__gt=when) | Q(active_from__isnull=True)
        q_to = Q(active_to__lt=when) | Q(active_to__isnull=True)
        q_fromto_notnull = Q(active_from__isnull=False) | Q(active_to__isnull=False)
        q = q_from & q_to & q_fromto_notnull
        return self.filter(Q(active=False) | q)


class OwnedQuerySet(QuerySet):
    """
    For use in conjunction with ``QuerySetManager``.

    The model MUST adhere to the ``owner`` protocol.
    """
    __module__ = __name__

    def owned(self, user=None, group=None, add_public=False):
        import operator
        if user is None and group is None:
            return self.all()
        o_set = self
        or_queries = []
        if user is not None:
            or_queries += [ Q(owner_group=group) for group in user.groups.all() ]
            or_queries.append(Q(owner_user=user))
        if group is not None:
            or_queries.append(Q(owner_group=group))
        if add_public:
            or_queries.append(Q(owner_user__isnull=True) & Q(owner_group__isnull=True))
        o_set = o_set.filter(reduce(operator.or_, or_queries))
        return o_set

    def not_owned(self, user=None, group=None, exclude_public=False):
        if user is None and group is None:
            return self.none()
        o_set = self
        or_queries = []
        if user is not None:
            or_queries += [ Q(owner_group=group) for group in user.groups.all() ]
            or_queries.append(Q(owner_user=user))
        if group is not None:
            or_queries.append(Q(owner_group=group))
        if exclude_public:
            or_queries.append(Q(owner_user__isnull=True) & Q(owner_group__isnull=True))
        o_set = o_set.exclude(reduce(operator.or_, or_queries))
        return o_set

    def owned_or_public(self, user=None, group=None):
        return self.owned(user=user, group=group, add_public=True)

    def public(self):
        return self.filter(Q(owner_user__isnull=True) & Q(owner_group__isnull=True))

    def private(self):
        return self.filter(Q(owner_user__isnull=False) | Q(owner_group__isnull=False))


class OwnedActiveQuerySet(ActiveQuerySet, OwnedQuerySet):
    """
    For use in conjunction with ``QuerySetManager``.

    The instance model MUST adhere to the ``active`` temporal protocol.
    The model MUST adhere to the ``owner`` protocol.
    """
    __module__ = __name__