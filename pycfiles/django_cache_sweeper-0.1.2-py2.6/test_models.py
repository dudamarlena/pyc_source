# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/cachesweeper/test_models.py
# Compiled at: 2011-01-26 07:33:18
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.cache import cache
from cachesweeper.utils import invalidate_cache_handler, invalidate_cache_for, ModelSweeper

class Article(models.Model):
    """An article"""
    title = models.CharField(blank=True, max_length=100)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created_at'

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    """A comment for an article"""
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def likes(self):
        return self.vote_set.filter(direction='+')

    def like_it(self):
        return self.vote_set.create(direction='+')

    def dislikes(self):
        return self.vote_set.filter(direction='-')

    def dislike_it(self):
        return self.vote_set.create(direction='-')

    class Meta:
        get_latest_by = 'created_at'
        ordering = ['created_at']

    def __unicode__(self):
        return 'Comment: %s' % (' - ').join(map(str, [self.article, self.user, self.content]))


class Vote(models.Model):
    """A like or a dislike"""
    comment = models.ForeignKey(Comment)
    direction = models.CharField(choices=(('+', 'Like'), ('-', 'Dislike')), max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Vote %s1 for %s' % (self.direction, self.comment)


class TestMixinModel(ModelSweeper, models.Model):
    text = models.TextField(blank=True)


class TestAttributeModel(models.Model):
    text = models.TextField(blank=True)
    cachesweeper = ModelSweeper()


def invalidate_vote_cache(sender, **kwargs):
    instance = kwargs.get('instance')
    invalidate_cache_for(instance.comment)


post_save.connect(invalidate_vote_cache, sender=Vote)