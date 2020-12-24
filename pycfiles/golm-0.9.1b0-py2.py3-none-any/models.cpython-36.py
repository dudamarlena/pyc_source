# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/golm_webgui/models.py
# Compiled at: 2018-04-15 14:00:29
# Size of source mod 2**32: 1351 bytes
import datetime, pytz
from django.db import models

class Message(models.Model):
    text = models.CharField(max_length=255)
    uid = models.CharField(max_length=255)
    timestamp = models.BigIntegerField()
    is_response = models.BooleanField(default=False)

    def get_time(self) -> str:
        return datetime.datetime.fromtimestamp((self.timestamp), tz=(pytz.timezone('Europe/Prague'))).strftime('%Y-%m-%d %H:%M')

    def get_buttons(self) -> list:
        return list(Button.objects.all().filter(message_id__exact=(self.id)))

    def get_elements(self) -> list:
        return list(Element.objects.all().filter(message_id__exact=(self.id)))


class Button(models.Model):
    message = models.ForeignKey(Message, on_delete=(models.CASCADE))
    text = models.CharField(max_length=255, null=True, blank=True)
    action = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=1024, null=True, blank=True)


class Element(models.Model):
    message = models.ForeignKey(Message, on_delete=(models.CASCADE))
    title = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)