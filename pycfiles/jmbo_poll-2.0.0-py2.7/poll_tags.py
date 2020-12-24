# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/jmbo-foundry/ve/src/jmbo-poll/poll/templatetags/poll_tags.py
# Compiled at: 2015-04-21 15:32:20
from django import template
from django.core.urlresolvers import reverse
from poll.forms import PollVoteForm
register = template.Library()

@register.inclusion_tag('poll/inclusion_tags/poll_detail.html', takes_context=True)
def poll_detail(context, obj):
    can_vote_on_poll, reason = obj.can_vote_on_poll(context['request'])
    context.update({'object': obj, 
       'can_vote_on_poll': can_vote_on_poll, 
       'reason': reason})
    if can_vote_on_poll and not context.has_key('form'):
        context['form'] = PollVoteForm(request=context['request'], poll=obj)
    return context


@register.inclusion_tag('poll/inclusion_tags/poll_widget.html', takes_context=True)
def poll_widget(context, obj):
    return poll_detail(context, obj)