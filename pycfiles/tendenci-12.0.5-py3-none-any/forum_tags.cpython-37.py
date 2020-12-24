# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/forums/templatetags/forum_tags.py
# Compiled at: 2020-02-26 15:11:55
# Size of source mod 2**32: 2460 bytes
import django.utils.translation as _
from django.template import Library, TemplateSyntaxError
from tendenci.apps.base.template_tags import ListNode, parse_tag_kwargs
from tendenci.apps.forums.models import Category
register = Library()

class ListForumCategoriesNode(ListNode):
    model = Category
    perms = 'forums.view_category'

    def custom_model_filter(self, items, user):
        if not user.is_staff:
            return items.filter(hidden=False)
        return items


@register.tag
def list_forum_categories(parser, token):
    """
    Used to pull a list of :model:`forums.Category` items.

    Usage::

        {% list_forum_categories as [varname] [options] %}

    Be sure the [varname] has a specific name like ``forums_sidebar`` or
    ``forum_categories_list``. Options can be used as [option]=[value]. Wrap text values
    in quotes like ``tags="cool"``. Options include:

        ``limit``
           The number of items that are shown. **Default: 3**
        ``order``
           The order of the items. **Default: name**
        ``user``
           Specify a user to only show public items to all. **Default: Viewing user**
        ``query``
           The text to search for items. Will not affect order.
        ``random``
           Use this with a value of true to randomize the items included.

    Example::

        {% list_forum_categories as forum_categories_list limit=5 %}
        <ul>
        {% for cat in forum_categories_list %}
            {% with cat.forums.count as c %}
            <li><a href="{% url 'pybb:category' cat.slug %}">{{ cat.name }}</a> - {{ c }} forum{{ c|pluralize }}</li>
            {% endwith %}
        {% endfor %}
        </ul>
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
        kwargs['order'] = 'name'
    return ListForumCategoriesNode(context_var, *args, **kwargs)


@register.inclusion_tag('pybb/top_nav_items.html', takes_context=True)
def forums_current_app(context, user, forum=None):
    context.update({'app_object':forum, 
     'user':user})
    return context