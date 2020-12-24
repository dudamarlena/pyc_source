# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/link/models.py
# Compiled at: 2018-05-10 08:40:57
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
try:
    from django.urls import reverse, NoReverseMatch
except ImportError:
    from django.core.urlresolvers import reverse, NoReverseMatch

class ViewParam(models.Model):
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=256)

    class Meta:
        ordering = [
         'key']

    def __unicode__(self):
        return '%s:%s' % (self.key, self.value)

    __str__ = __unicode__


class Link(models.Model):
    title = models.CharField(max_length=256, help_text='A short descriptive title.')
    slug = models.SlugField(max_length=256, db_index=True)
    view_name = models.CharField(max_length=256, blank=True, null=True, help_text='View name to which this link will redirect.')
    view_params = models.ManyToManyField(ViewParam, blank=True, null=True)
    target_content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='link_target_content_type', on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField(blank=True, null=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    url = models.CharField(max_length=256, blank=True, null=True, help_text='URL to which this link will redirect.')

    class Meta:
        ordering = [
         'title']

    def __unicode__(self):
        return self.title

    __str__ = __unicode__

    @property
    def absolute_url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        """
        Returns URL to which link should redirect based on a reversed view
        name, category, target or explicitly provided URL.
        """
        if self.view_name:
            kwargs = dict((param.key, param.value) for param in self.view_params.all())
            try:
                return reverse(self.view_name, kwargs=kwargs)
            except NoReverseMatch:
                pass

        elif self.target:
            try:
                return self.target.get_absolute_url()
            except AttributeError:
                pass

        else:
            if '://' in self.url:
                return self.url
            if not self.url.startswith('/'):
                return self.url
            try:
                root = reverse('home')
            except NoReverseMatch:
                return self.url

            if not self.url.startswith(root):
                return root.rstrip('/') + '/' + self.url.lstrip('/')
        return self.url