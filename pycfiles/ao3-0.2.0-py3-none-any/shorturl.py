# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ao/shorturl/templatetags/shorturl.py
# Compiled at: 2010-03-20 21:26:52
import ao.shorturl
from django import template
register = template.Library()

def shorturl(parser, token):
    """Return the short URL for the context."""
    context = token.split_contents()[1]
    return URL(context)


register.tag(shorturl)

class URL(template.Node):
    """The URL node."""

    def __init__(self, context):
        """Save the context variable to self.context."""
        self.context = template.Variable(context)
        self.handler = ao.shorturl.getHandler()

    def render(self, context):
        """Render the link for self.context."""
        return self.handler.construct_url(self.context.resolve(context))