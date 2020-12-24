# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramusus/workspace/manufacture/env/src/django-twitter-relations-history/twitter_relations_history/models.py
# Compiled at: 2013-05-14 12:34:59
from django.db import models
from django.db.models.query import QuerySet
from django.core.exceptions import MultipleObjectsReturned
from twitter_api import fields
from twitter_api.utils import api
from twitter_api.models import User
from datetime import datetime
import logging
log = logging.getLogger('twitter_relations_history')

class NoDeltaForFirstHistory(ValueError):
    pass


def ModelQuerySetManager(ManagerBase=models.Manager):
    """
    Function that return Manager for using QuerySet class inside the model definition
    @param ManagerBase - parent class Manager
    """
    if not issubclass(ManagerBase, models.Manager):
        raise ValueError("Parent class for ModelQuerySetManager must be models.Manager or it's child")

    class Manager(ManagerBase):
        """
        Manager based on QuerySet class inside the model definition
        """

        def get_query_set(self):
            return self.model.QuerySet(self.model)

    return Manager()


class RelationsHistoryQueryset(object):

    @property
    def visible(self):
        return self.exclude(hidden=True).exclude(time__isnull=True)

    @property
    def light(self):
        return self.defer('followers_ids')


class RelationsHistoryManager(models.Manager, RelationsHistoryQueryset):

    def update_for_user(self, user, offset=0):
        """
        Fetch all users for this user, save them as IDs and after make m2m relations
        """
        try:
            stat, created = self.get_or_create(user=user, time=None)
        except MultipleObjectsReturned:
            self.filter(user=user, time=None).delete()
            stat = self.create(user=user, time=None, offset=0)
            created = True

        if created:
            stat.set_defaults()
        stat.time = datetime.now()
        stat.followers_ids = user.fetch_followers_ids(all=True)
        stat.update()
        stat.save()
        return


class RelationsHistory(models.Model):

    class Meta:
        verbose_name = 'Relations history of twitter users'
        verbose_name_plural = 'Relations histories of twitter users'
        unique_together = ('user', 'time')
        ordering = ('user', 'time', '-id')

    class QuerySet(QuerySet, RelationsHistoryQueryset):
        pass

    user = models.ForeignKey(User, verbose_name='User', related_name='relations_history')
    time = models.DateTimeField('Datetime', null=True)
    hidden = models.BooleanField('Скрыть')
    offset = models.PositiveIntegerField(default=0)
    followers_ids = fields.PickledObjectField(default=[])
    followers_count = models.PositiveIntegerField(default=0)
    objects = ModelQuerySetManager(RelationsHistoryManager)

    def set_defaults(self):
        """
        It's neccesary to call after creating of every instance,
        because `default` attribute of fields.PickledObjectField doesn't work properly
        """
        self.followers_ids = []

    _next = None
    _prev = None

    @property
    def next(self):
        try:
            assert self._next
        except AssertionError:
            try:
                self._next = self.user.relations_history.visible.filter(time__gt=self.time).order_by('time')[0]
            except IndexError:
                return

        return self._next

    @property
    def prev(self):
        try:
            assert self._prev
        except AssertionError:
            try:
                self._prev = self.user.relations_history.visible.filter(time__lt=self.time).order_by('-time')[0]
            except IndexError:
                return

        return self._prev

    def get_delta(self, name, prev=None):
        if name in [ field.name for field in RelationsHistoryDelta._meta.fields if 'followers' in field.name ]:
            if not prev:
                prev = self.prev
            if prev:
                delta = RelationsHistoryDelta.objects.get_or_create(history_from=prev, history_to=self)[0]
                return getattr(delta, name)
            raise NoDeltaForFirstHistory("This history doesn't have previous history")
        else:
            raise AttributeError("type object '%s' has no attribute '%s'" % (self.__class__, name))

    def __getattr__(self, name):
        return self.get_delta(name)

    def delete(self, *args, **kwargs):
        """
        Recalculate next stat members instance
        """
        self.hide()
        super(RelationsHistory, self).delete(*args, **kwargs)

    def hide(self):
        """
        Hide curent migration, and recalculate fields of next migrations
        """
        self.hidden = True
        self.save()

    def update_next(self):
        next_stat = self.next
        if next_stat:
            next_stat.update()
            next_stat.save()

    def save(self, *args, **kwargs):
        update_next = False
        if self.id and self.hidden != self.__class__.objects.light.get(id=self.id).hidden:
            update_next = True
        super(RelationsHistory, self).save(*args, **kwargs)
        if update_next:
            self.update_next()

    def update(self):
        self.update_migration()
        self.update_counters()

    def update_migration(self):
        return
        prev_stat = self.prev
        if prev_stat and self.user:
            self.members_left_ids = list(set(prev_stat.followers_ids).difference(set(self.followers_ids)))
            self.members_entered_ids = list(set(self.followers_ids).difference(set(prev_stat.followers_ids)))

    def update_counters(self):
        for field_name in ['followers']:
            setattr(self, field_name + '_count', len(getattr(self, field_name + '_ids')))


class RelationsHistoryDelta(models.Model):

    class Meta:
        unique_together = ('history_from', 'history_to')

    history_from = models.ForeignKey(RelationsHistory, related_name='deltas_from')
    history_to = models.ForeignKey(RelationsHistory, related_name='deltas_to')
    followers_left_ids = fields.PickledObjectField(default=[])
    followers_entered_ids = fields.PickledObjectField(default=[])
    followers_left_count = models.PositiveIntegerField(default=0)
    followers_entered_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.followers_left_ids = list(set(self.history_from.followers_ids).difference(set(self.history_to.followers_ids)))
        self.followers_entered_ids = list(set(self.history_to.followers_ids).difference(set(self.history_from.followers_ids)))
        self.followers_left_count = len(self.followers_left_ids)
        self.followers_entered_count = len(self.followers_entered_ids)
        super(RelationsHistoryDelta, self).save(*args, **kwargs)


import signals