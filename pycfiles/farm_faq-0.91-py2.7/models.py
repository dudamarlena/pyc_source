# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/faq/models.py
# Compiled at: 2014-03-27 06:14:42
from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    name_field = 'title'

    class Meta:
        ordering = [
         'order', 'title']
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.title

    @property
    def questions(self):
        if not hasattr(self, '_questions'):
            self._questions = self.question_set.filter(active=True)
        return self._questions


class Question(models.Model):
    category = models.ForeignKey(Category)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        ordering = [
         'order', 'question']

    def __unicode__(self):
        return self.question