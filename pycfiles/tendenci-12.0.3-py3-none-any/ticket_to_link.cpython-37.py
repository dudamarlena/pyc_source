# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/helpdesk/templatetags/ticket_to_link.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 1787 bytes
"""
django-helpdesk - A Django powered ticket tracker for small enterprise.

(c) Copyright 2008 Jutda. All Rights Reserved. See LICENSE for details.

templatetags/ticket_to_link.py - Used in ticket comments to allow wiki-style
                                 linking to other tickets. Including text such
                                 as '#3180' in a comment automatically links
                                 that text to ticket number 3180, with styling
                                 to show the status of that ticket (eg a closed
                                 ticket would have a strikethrough).
"""
import re
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from tendenci.apps.helpdesk.models import Ticket

class ReverseProxy:

    def __init__(self, sequence):
        self.sequence = sequence

    def __iter__(self):
        length = len(self.sequence)
        i = length
        while i > 0:
            i = i - 1
            yield self.sequence[i]


def num_to_link(text):
    if text == '':
        return text
    matches = []
    for match in re.finditer('(?:[^&]|\\b|^)#(\\d+)\\b', text):
        matches.append(match)

    for match in ReverseProxy(matches):
        number = match.groups()[0]
        url = reverse('helpdesk_view', args=[number])
        try:
            ticket = Ticket.objects.get(id=number)
        except Ticket.DoesNotExist:
            ticket = None

        if ticket:
            style = ticket.get_status_display()
            text = "%s <a href='%s' class='ticket_link_status ticket_link_status_%s'>#%s</a>%s" % (text[:match.start()], url, style, match.groups()[0], text[match.end():])

    return mark_safe(text)


register = template.Library()
register.filter(num_to_link)