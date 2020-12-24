# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/projectownership.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import operator
from django.db import models
from django.db.models import Q
from django.utils import timezone
from sentry.db.models import Model, sane_repr
from sentry.db.models.fields import FlexibleForeignKey, JSONField
from sentry.ownership.grammar import load_schema
from functools import reduce

class ProjectOwnership(Model):
    __core__ = True
    project = FlexibleForeignKey('sentry.Project', unique=True)
    raw = models.TextField(null=True)
    schema = JSONField(null=True)
    fallthrough = models.BooleanField(default=True)
    auto_assignment = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    Everyone = object()

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_projectownership'

    __repr__ = sane_repr('project_id', 'is_active')

    @classmethod
    def get_owners(cls, project_id, data):
        """
        For a given project_id, and event data blob.

        If Everyone is returned, this means we implicitly are
        falling through our rules and everyone is responsible.

        If an empty list is returned, this means there are explicitly
        no owners.
        """
        try:
            ownership = cls.objects.get(project_id=project_id)
        except cls.DoesNotExist:
            ownership = cls(project_id=project_id)

        rules = cls._matching_ownership_rules(ownership, project_id, data)
        if not rules:
            return (cls.Everyone if ownership.fallthrough else [], None)
        else:
            owners = {o for rule in rules for o in rule.owners}
            return (
             filter(None, resolve_actors(owners, project_id).values()), rules)

    @classmethod
    def get_autoassign_owner(cls, project_id, data):
        """
        Get the auto-assign owner for a project if there are any.

        Will return None if there are no owners, or a list of owners.
        """
        try:
            ownership = cls.objects.get(project_id=project_id)
        except cls.DoesNotExist:
            return

        if not ownership.auto_assignment:
            return
        else:
            rules = cls._matching_ownership_rules(ownership, project_id, data)
            if not rules:
                return
            score = 0
            owners = None
            for rule in rules:
                candidate = len(rule.matcher.pattern)
                if candidate > score:
                    score = candidate
                    owners = rule.owners

            actors = filter(None, resolve_actors(owners, project_id).values())
            if not actors:
                return
            return actors[0].resolve()

    @classmethod
    def _matching_ownership_rules(cls, ownership, project_id, data):
        rules = []
        if ownership.schema is not None:
            for rule in load_schema(ownership.schema):
                if rule.test(data):
                    rules.append(rule)

        return rules


def resolve_actors(owners, project_id):
    """ Convert a list of Owner objects into a dictionary
    of {Owner: Actor} pairs. Actors not identified are returned
    as None. """
    from sentry.api.fields.actor import Actor
    from sentry.models import User, Team
    if not owners:
        return {}
    users, teams = [], []
    owners_lookup = {}
    for owner in owners:
        owners_lookup[(owner.type, owner.identifier.lower())] = owner
        if owner.type == 'user':
            users.append(owner)
        elif owner.type == 'team':
            teams.append(owner)

    actors = {}
    if users:
        actors.update({('user', email.lower()):Actor(u_id, User) for u_id, email in User.objects.filter(reduce(operator.or_, [ Q(emails__email__iexact=o.identifier) for o in users ]), is_active=True, sentry_orgmember_set__organizationmemberteam__team__projectteam__project_id=project_id).distinct().values_list('id', 'emails__email')})
    if teams:
        actors.update({('team', slug):Actor(t_id, Team) for t_id, slug in Team.objects.filter(slug__in=[ o.identifier for o in teams ], projectteam__project_id=project_id).values_list('id', 'slug')})
    return {o:actors.get((o.type, o.identifier.lower())) for o in owners}