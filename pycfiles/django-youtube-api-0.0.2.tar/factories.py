# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/movister/env/src/django-youtube-api/youtube_api/factories.py
# Compiled at: 2015-09-09 15:42:22
import random, string, factory
from django.utils import timezone
from . import models

class VideoFactory(factory.DjangoModelFactory):
    video_id = factory.Sequence(lambda n: ('').join([ random.choice(string.letters) for i in xrange(11) ]))
    published_at = factory.LazyAttribute(lambda o: timezone.now())

    class Meta:
        model = models.Video