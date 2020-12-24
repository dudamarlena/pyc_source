# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/news/templatetags/news_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 2786 bytes
from datetime import datetime
from django.template import Library, TemplateSyntaxError
import django.utils.translation as _
from tendenci.apps.base.template_tags import ListNode, parse_tag_kwargs
from tendenci.apps.news.models import News
register = Library()

@register.inclusion_tag('news/options.html', takes_context=True)
def news_options(context, user, news):
    context.update({'opt_object':news, 
     'user':user})
    return context


@register.inclusion_tag('news/nav.html', takes_context=True)
def news_nav(context, user, news=None):
    context.update({'nav_object':news, 
     'user':user})
    return context


@register.inclusion_tag('news/search-form.html', takes_context=True)
def news_search(context):
    return context


@register.inclusion_tag('news/top_nav_items.html', takes_context=True)
def news_current_app(context, user, news=None):
    context.update({'app_object':news, 
     'user':user})
    return context


class ListNewsNode(ListNode):
    model = News
    perms = 'news.view_news'

    def custom_model_filter(self, qset, user):
        return qset.filter(release_dt_local__lte=(datetime.now()))


@register.tag
def list_news(parser, token):
    """
    Used to pull a list of :model:`news.News` items.

    Usage::

        {% list_news as [varname] [options] %}

    Be sure the [varname] has a specific name like ``news_sidebar`` or
    ``news_list``. Options can be used as [option]=[value]. Wrap text values
    in quotes like ``tags="cool"``. Options include:

        ``limit``
           The number of items that are shown. **Default: 3**
        ``order``
           The order of the items. **Default: Latest Release Date**
        ``user``
           Specify a user to only show public items to all. **Default: Viewing user**
        ``query``
           The text to search for items. Will not affect order.
        ``tags``
           The tags required on items to be included.
        ``random``
           Use this with a value of true to randomize the items included.

    Example::

        {% list_news as news_list limit=5 tags="cool" %}
        {% for news_item in news_list %}
            {{ news_item.headline }}
        {% endfor %}
    """
    args, kwargs = [], {}
    bits = token.split_contents()
    context_var = bits[2]
    if len(bits) < 3:
        message = "'%s' tag requires more than 3" % bits[0]
        raise TemplateSyntaxError(_(message))
    if bits[1] != 'as':
        message = "'%s' second argument must be 'as" % bits[0]
        raise TemplateSyntaxError(_(message))
    kwargs = parse_tag_kwargs(bits)
    if 'order' not in kwargs:
        kwargs['order'] = '-release_dt'
    return ListNewsNode(context_var, *args, **kwargs)