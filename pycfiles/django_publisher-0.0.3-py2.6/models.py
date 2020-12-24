# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/publisher/models.py
# Compiled at: 2012-05-07 04:22:11
from django.db import models
from django.contrib.contenttypes.models import ContentType

class Publisher(models.Model):
    title = models.CharField(max_length=64)
    content_type = models.ForeignKey(ContentType, editable=False, null=True)
    class_name = models.CharField(max_length=32, editable=False, null=True)

    def __unicode__(self):
        return '%s - %s' % (self._meta.verbose_name, self.title)

    def as_leaf_class(self):
        """
        Returns the leaf class no matter where the calling instance is in the
        inheritance hierarchy.
        Inspired by http://www.djangosnippets.org/snippets/1031/
        """
        try:
            return self.__getattribute__(self.class_name.lower())
        except AttributeError:
            content_type = self.content_type
            model = content_type.model_class()
            if model == ModelBase:
                return self
            return model.objects.get(id=self.id)

    def publish(self, instance):
        self.as_leaf_class().publish(instance)

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        if not self.class_name:
            self.class_name = self.__class__.__name__
        super(Publisher, self).save(*args, **kwargs)


class Buzz(Publisher):

    class Meta:
        ordering = ('title', )
        verbose_name = 'Buzz'
        verbose_name_plural = 'Buzz'


class Facebook(Publisher):

    class Meta:
        ordering = ('title', )
        verbose_name = 'Facebook'
        verbose_name_plural = 'Facebook'


class Mobile(Publisher):

    class Meta:
        ordering = ('title', )
        verbose_name = 'Mobile'
        verbose_name_plural = 'Mobile'


class Twitter(Publisher):

    class Meta:
        ordering = ('title', )
        verbose_name = 'Twitter'
        verbose_name_plural = 'Twitter'


class SocialBookmark(Publisher):
    pass


class Web(Publisher):

    class Meta:
        ordering = ('title', )
        verbose_name = 'Web'
        verbose_name_plural = 'Web'