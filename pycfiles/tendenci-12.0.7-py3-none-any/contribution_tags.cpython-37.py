# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/contributions/templatetags/contribution_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 2163 bytes
from django.template import Library, Node, TemplateSyntaxError, Variable
import django.utils.translation as _
from tendenci.apps.contributions.models import Contribution
register = Library()

@register.inclusion_tag('contributions/options.html', takes_context=True)
def contribution_options(context, user, contribution):
    context.update({'contribution':contribution, 
     'user':user})
    return context


@register.inclusion_tag('contributions/nav.html', takes_context=True)
def contribution_nav(context, user):
    context.update({'user': user})
    return context


@register.inclusion_tag('contributions/search-form.html', takes_context=True)
def contribution_search(context):
    return context


@register.inclusion_tag('contributions/top_nav_items.html', takes_context=True)
def contribution_current_app(context, user, contribution=None):
    context.update({'app_object':contribution, 
     'user':user})
    return context


class LatestContributionsNode(Node):

    def __init__(self, **kwargs):
        self.user = Variable(kwargs.get('user', None))
        self.limit = Variable(kwargs.get('limit', '40'))
        self.context_var = kwargs.get('context_var', None)

    def render(self, context):
        limit = self.limit.resolve(context)
        contributions = Contribution.objects.filter(owner=(self.user.resolve(context))).order_by('-create_dt')[:limit]
        context[self.context_var] = contributions
        return ''


@register.tag
def latest_contributions(parser, token):
    """
    Retrieves a list of the users newest contributions.

    Usage::

        {% latest_contributions [user] as [contributions] %}
        {% latest_contributions [user] [limit] as [contributions] %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        if len(bits) != 5:
            raise TemplateSyntaxError(_('%(b)s tag requires 4 or 5 arguments') % {'b': bits[0]})
    if len(bits) == 4:
        return LatestContributionsNode(user=(bits[1]), context_var=(bits[3]))
    if len(bits) == 5:
        return LatestContributionsNode(user=(bits[1]), limit=(bits[2]), context_var=(bits[4]))