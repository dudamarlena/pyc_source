# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/inviteme/templatetags/inviteme_tags.py
# Compiled at: 2012-04-10 18:35:00
from django import template
from django.template.loader import render_to_string
from inviteme.forms import ContactMailForm
register = template.Library()

class MailFormNode(template.Node):

    def render(self, context):
        context.push()
        form_str = render_to_string('inviteme/form.html', {'form': ContactMailForm()}, context)
        context.pop()
        return form_str


def render_mail_form(parser, token):
    """
    Render the contact form (as returned by ``{% render_mail_form %}``) 
    through the ``inviteme/form.html`` template.

    Syntax::

        {% render_mail_form %}
    """
    return MailFormNode()


register.tag(render_mail_form)