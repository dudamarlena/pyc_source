# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange_django/templatetags/linkexchange_tags.py
# Compiled at: 2011-05-12 16:15:21
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from linkexchange_django import support
register = template.Library()

def linkexchange_filter(value, request, autoescape=None):
    """
    Django template filter to support linkexchange content filtering.  The
    argument is request object, to access this object add
    'django.core.context_processors.request' to the TEMPLATE_CONTEXT_PROCESSORS
    in your settings.py.

    Usage example:

        {% load linkexchange_tags %}
        {{ page.html|safe|linkexchange_filter:request }}
    """
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    value = esc(force_unicode(value))
    if support.platform is not None:
        value = support.platform.content_filter(support.convert_request(request), value)
    return mark_safe(value)


linkexchange_filter.needs_autoescape = True
register.filter('linkexchange_filter', linkexchange_filter)

class LinkExchangeFilterNode(template.Node):

    def __init__(self, request, nodelist):
        self.request = request
        self.nodelist = nodelist

    def render(self, context):
        request = self.request.resolve(context)
        content = self.nodelist.render(context)
        if support.platform is not None:
            content = support.platform.content_filter(support.convert_request(request), content)
        return content


def linkexchange_filter_tag(parser, token):
    """
    Django template tag to support linkexchange content filtering.  The
    argument is request object, to access this object add
    'django.core.context_processors.request' to the TEMPLATE_CONTEXT_PROCESSORS
    in your settings.py.

    Usage example:

        {% load linkexchange_tags %}
        <html>
        <body>
            {% linkexchange_filter request %}
            Page content.
            {% endlinkexchange_filter %}
        </body>
        </html>
    """
    try:
        tag_name, request = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r tag requires a single argument' % token.contents.split()[0]

    request = parser.compile_filter(request)
    nodelist = parser.parse(('endlinkexchange_filter', ))
    parser.delete_first_token()
    return LinkExchangeFilterNode(request, nodelist)


register.tag('linkexchange_filter', linkexchange_filter_tag)