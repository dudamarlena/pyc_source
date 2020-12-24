# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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