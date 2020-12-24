# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johnsanchezc/Projects/django-luhublog/luhublog/templatetags/blog_twittercard_tags.py
# Compiled at: 2015-10-19 12:25:39
from django import template
from django.contrib.contenttypes.models import ContentType
from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import InclusionTag
from luhublog.models import TwitterCard
register = template.Library()

class TwitterCardTag(InclusionTag):
    name = 'twitter_card'
    template = 'luhublog/__twitter_card.html'

    def get_context(self, context):
        object = context.get('object', None)
        if object:
            try:
                content_type = ContentType.objects.get_for_model(object)
            except Exception as e:
                return ''

            try:
                twitter_card = TwitterCard.objects.get(content_type=content_type, object_id=object.id)
            except Exception as e:
                return ''

            return {'twitter': twitter_card}
        return ''


register.tag(TwitterCardTag)