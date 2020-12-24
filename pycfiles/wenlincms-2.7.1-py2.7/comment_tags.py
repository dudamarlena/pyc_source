# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/generic/templatetags/comment_tags.py
# Compiled at: 2016-05-20 23:42:06
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.template.defaultfilters import linebreaksbr, urlize
from future.builtins import int
from wenlincms import template
from wenlincms.conf import settings
from wenlincms.generic.forms import ThreadedCommentForm
from wenlincms.generic.models import ThreadedComment
from wenlincms.utils.importing import import_dotted_path
from wenlincms.utils.views import paginate
from wlapps.utils.common import get_theme
register = template.Library()

@register.inclusion_tag(get_theme() + b'/generic/includes/comments.html', takes_context=True)
def wlcomments_for(context, obj):
    u"""
    主评论模块，和页面同步加载
    """
    form = ThreadedCommentForm(context[b'request'], obj)
    try:
        context[b'posted_comment_form']
    except KeyError:
        context[b'posted_comment_form'] = form

    context[b'unposted_comment_form'] = form
    context[b'comment_url'] = reverse(b'comment')
    context[b'object_for_comments'] = obj
    return context


@register.inclusion_tag(get_theme() + b'/generic/includes/comment.html', takes_context=True)
def wlcomment_thread(context, obj):
    u"""
    评论嵌入，非池，2015-08-31
    """
    if b'all_comments' not in context:
        if b'request' in context:
            comments_queryset = obj.comments.all().order_by(b'-submit_date')
        else:
            comments_queryset = obj.comments.visible().order_by(b'-submit_date')
        comments_queryset = paginate(comments_queryset, context[b'request'].GET.get(b'page', 1), settings.LIST_PER_PAGE, settings.MAX_PAGING_LINKS)
        context[b'all_comments'] = comments_queryset
    try:
        replied_to = int(context[b'request'].POST[b'replied_to'])
    except KeyError:
        replied_to = 0

    context.update({b'wlcomments_for_thread': context[b'all_comments'], 
       b'no_comments': not context[b'all_comments'], 
       b'replied_to': replied_to, 
       b'wlajaxid': b'#comment_thread', 
       b'commenturl': obj.get_absolute_url() + b'comment/'})
    return context


@register.filter(name=b'show_parent_comment')
def show_parent_comment(pid):
    objs = ThreadedComment.objects.filter(pk=pid)
    if len(objs):
        result = objs[0].comment
        if objs[0].user.u_profile:
            result = objs[0].user.u_profile.title + b': ' + result
        else:
            result = objs[0].user.username + b': ' + result
        return result
    return pid


@register.inclusion_tag(b'admin/includes/recent_comments.html', takes_context=True)
def recent_comments(context):
    """
    Dashboard widget for displaying recent comments.
    """
    latest = context[b'settings'].COMMENTS_NUM_LATEST
    comments = ThreadedComment.objects.all().select_related(b'user')
    context[b'comments'] = comments.order_by(b'-id')[:latest]
    return context


@register.filter
def wlcomment_filter(comment_text):
    """
    Passed comment text to be rendered through the function defined
    by the ``COMMENT_FILTER`` setting. If no function is defined
    (the default), Django's ``linebreaksbr`` and ``urlize`` filters
    are used.
    """
    filter_func = settings.COMMENT_FILTER
    if not filter_func:

        def filter_func(s):
            return linebreaksbr(urlize(s, autoescape=True), autoescape=True)

    elif not callable(filter_func):
        filter_func = import_dotted_path(filter_func)
    return filter_func(comment_text)