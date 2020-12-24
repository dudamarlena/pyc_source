# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/syn/dev/test/mogo62/mogo/mgof/templatetags/mgof.py
# Compiled at: 2016-09-04 06:17:49
from django import template
from ..models import Topic
register = template.Library()

class LastPosts(template.Node):

    def __init__(self, num_posts=10):
        topics = Topic.objects.filter().select_related('forum').order_by('-last_post_date')[:num_posts]
        topics_ok = []
        for topic in topics:
            if topic.forum.is_public is True:
                topics_ok.append(topic)

        self.topics = topics_ok

    def render(self, context):
        context['topics'] = self.topics
        return ''


def forums_last_posts(parser, token):
    return LastPosts()


register.tag('forums_last_posts', forums_last_posts)