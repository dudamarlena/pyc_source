# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/flatpages/templatetags/flatpages.py
# Compiled at: 2019-02-14 00:35:16
from django import template
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.shortcuts import get_current_site
register = template.Library()

class FlatpageNode(template.Node):

    def __init__(self, context_name, starts_with=None, user=None):
        self.context_name = context_name
        if starts_with:
            self.starts_with = template.Variable(starts_with)
        else:
            self.starts_with = None
        if user:
            self.user = template.Variable(user)
        else:
            self.user = None
        return

    def render(self, context):
        if 'request' in context:
            site_pk = get_current_site(context['request']).pk
        else:
            site_pk = settings.SITE_ID
        flatpages = FlatPage.objects.filter(sites__id=site_pk)
        if self.starts_with:
            flatpages = flatpages.filter(url__startswith=self.starts_with.resolve(context))
        if self.user:
            user = self.user.resolve(context)
            if not user.is_authenticated:
                flatpages = flatpages.filter(registration_required=False)
        else:
            flatpages = flatpages.filter(registration_required=False)
        context[self.context_name] = flatpages
        return ''


@register.tag
def get_flatpages(parser, token):
    """
    Retrieves all flatpage objects available for the current site and
    visible to the specific user (or visible to all users if no user is
    specified). Populates the template context with them in a variable
    whose name is defined by the ``as`` clause.

    An optional ``for`` clause can be used to control the user whose
    permissions are to be used in determining which flatpages are visible.

    An optional argument, ``starts_with``, can be applied to limit the
    returned flatpages to those beginning with a particular base URL.
    This argument can be passed as a variable or a string, as it resolves
    from the template context.

    Syntax::

        {% get_flatpages ['url_starts_with'] [for user] as context_name %}

    Example usage::

        {% get_flatpages as flatpages %}
        {% get_flatpages for someuser as flatpages %}
        {% get_flatpages '/about/' as about_pages %}
        {% get_flatpages prefix as about_pages %}
        {% get_flatpages '/about/' for someuser as about_pages %}
    """
    bits = token.split_contents()
    syntax_message = "%(tag_name)s expects a syntax of %(tag_name)s ['url_starts_with'] [for user] as context_name" % dict(tag_name=bits[0])
    if len(bits) >= 3 and len(bits) <= 6:
        if len(bits) % 2 == 0:
            prefix = bits[1]
        else:
            prefix = None
        if bits[(-2)] != 'as':
            raise template.TemplateSyntaxError(syntax_message)
        context_name = bits[(-1)]
        if len(bits) >= 5:
            if bits[(-4)] != 'for':
                raise template.TemplateSyntaxError(syntax_message)
            user = bits[(-3)]
        else:
            user = None
        return FlatpageNode(context_name, starts_with=prefix, user=user)
    else:
        raise template.TemplateSyntaxError(syntax_message)
        return