# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/steve/dev/django-socketio/django_socketio/example_project/chat/models.py
# Compiled at: 2013-11-04 16:45:11
from django.db import models
from django.template.defaultfilters import slugify

class ChatRoom(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(blank=True)

    class Meta:
        ordering = ('name', )

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('room', (self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(ChatRoom, self).save(*args, **kwargs)


class ChatUser(models.Model):
    name = models.CharField(max_length=20)
    session = models.CharField(max_length=20)
    room = models.ForeignKey('chat.ChatRoom', related_name='users')

    class Meta:
        ordering = ('name', )

    def __unicode__(self):
        return self.name