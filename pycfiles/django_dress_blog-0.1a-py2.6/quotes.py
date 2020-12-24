# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dress_blog/templatetags/quotes.py
# Compiled at: 2012-07-20 05:27:44
from django import template
from django.conf import settings
from django.db import models
import re
Quote = models.get_model('dress_blog', 'quote')
register = template.Library()

class LatestQuotes(template.Node):

    def __init__(self, limit, var_name):
        try:
            self.limit = int(limit)
        except:
            self.limit = template.Variable(limit)

        self.var_name = var_name

    def render(self, context):
        if not isinstance(self.limit, int):
            self.limit = int(self.limit.resolve(context))
        quotes = Quote.objects.published()[:self.limit]
        if quotes:
            context[self.var_name] = quotes
        return ''


@register.tag
def get_latest_quotes(parser, token):
    """
    Gets any number of latest quotes and stores them in a variable.

    Syntax::

        {% get_latest_quotes [limit] as [var_name] %}

    Example usage::

        {% get_latest_quotes 10 as latest_quote_list %}
    """
    try:
        (tag_name, arg) = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, '%s tag requires arguments' % token.contents.split()[0]

    m = re.search('(.*?) as (\\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, '%s tag had invalid arguments' % tag_name
    (format_string, var_name) = m.groups()
    return LatestQuotes(format_string, var_name)


class DraftQuotes(template.Node):

    def __init__(self, limit, var_name):
        try:
            self.limit = int(limit)
        except:
            self.limit = template.Variable(limit)

        self.var_name = var_name

    def render(self, context):
        if not isinstance(self.limit, int):
            self.limit = int(self.limit.resolve(context))
        user = template.Variable('user').resolve(context)
        quotes = Quote.objects.draft(user)[:self.limit]
        if quotes:
            context[self.var_name] = quotes
        return ''


@register.tag
def get_draft_quotes(parser, token):
    """
    Gets any number of draft quotes and stores them in a variable.

    Syntax::

        {% get_draft_quotes [limit] as [var_name] %}

    Example usage::

        {% get_draft_quotes 10 as draft_quote_list %}
    """
    try:
        (tag_name, arg) = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, '%s tag requires arguments' % token.contents.split()[0]

    m = re.search('(.*?) as (\\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, '%s tag had invalid arguments' % tag_name
    (format_string, var_name) = m.groups()
    return DraftQuotes(format_string, var_name)